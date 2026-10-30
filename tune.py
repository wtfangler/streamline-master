"""Apply the launcher-side tuning that a .mrpack cannot carry.

A modpack ships mods and config files. It cannot set the JVM arguments, the
heap size or which GPU Windows hands the game, and on a 15 W laptop those
decide more than any mod does (see docs/tuning.md). This script writes them:

* Prism Launcher instance (instance.cfg): heap size from the machine's RAM,
  and the G1 arguments from docs/tuning.md. A backup of instance.cfg is
  written next to it first.
* Windows, with --gpu: marks the instance's java.exe / javaw.exe as
  "High performance" in Settings > Display > Graphics, the same registry value
  that page writes. On a laptop with a second GPU this is the difference
  between running on the integrated and the dedicated one; on a machine with
  only one GPU it changes nothing.

The Modrinth App keeps its settings in a database this script does not
touch; for it, the values are printed to paste by hand.

Close Prism before running: it rewrites instance.cfg on exit.
"""
import argparse
import ctypes
import os
import shutil
import subprocess
import sys

# docs/tuning.md, minus -Xms/-Xmx: Prism passes those from MinMemAlloc /
# MaxMemAlloc, and giving them twice leaves it to argument order which wins.
G1_ARGS = (
    "-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:MaxGCPauseMillis=50 "
    "-XX:+ParallelRefProcEnabled -XX:G1NewSizePercent=20 -XX:G1MaxNewSizePercent=40 "
    "-XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 "
    "-XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=20 "
    "-XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 "
    "-XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:+PerfDisableSharedMem "
    "-XX:-OmitStackTraceInFastThrow"
)
MIN_HEAP_MB = 1024
GPU_KEY = r"Software\Microsoft\DirectX\UserGpuPreferences"
GPU_HIGH = "GpuPreference=2;"


def total_ram_mb():
    if sys.platform == "win32":
        class MemStatus(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        st = MemStatus()
        st.dwLength = ctypes.sizeof(MemStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st)):
            return st.ullTotalPhys // (1 << 20)
        return None
    if sys.platform == "darwin":
        try:
            out = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=True)
            return int(out.stdout.strip()) // (1 << 20)
        except (OSError, ValueError, subprocess.CalledProcessError):
            return None
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) // 1024
    except OSError:
        pass
    return None


def heap_for(ram_mb):
    """Max heap per docs/tuning.md: 4 GB on 16 GB machines, 3 GB on 8 GB.

    Thresholds sit below the nominal sizes because the OS reports less than
    the marketing figure (an 8 GB laptop shows about 7.8 GB, minus iGPU memory).
    """
    if ram_mb is None:
        return 3072
    if ram_mb >= 14 * 1024:
        return 4096
    if ram_mb >= 7 * 1024:
        return 3072
    return 2048


def find_instance_cfg(path):
    path = os.path.abspath(path)
    for candidate in (path, os.path.dirname(path)):
        cfg = os.path.join(candidate, "instance.cfg")
        if os.path.isfile(cfg):
            return cfg
    return None


def read_ini(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def get_key(lines, key):
    for line in lines:
        k, sep, v = line.partition("=")
        if sep and k.strip() == key:
            return v.strip()
    return None


def set_keys(lines, values):
    """Set keys in the [General] section (or the section-less top of a legacy
    MultiMC file), keeping every other line and its order intact."""
    out = list(lines)
    pending = dict(values)
    section = None
    insert_at = None
    for i, line in enumerate(out):
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            if section in (None, "General") and insert_at is None and i > 0:
                insert_at = i
            section = s[1:-1]
            continue
        if section not in (None, "General"):
            continue
        k, sep, _ = line.partition("=")
        if sep and k.strip() in pending:
            out[i] = "%s=%s" % (k.strip(), pending.pop(k.strip()))
    if pending:
        add = ["%s=%s" % kv for kv in pending.items()]
        if insert_at is None:
            insert_at = len(out)
        while insert_at > 0 and not out[insert_at - 1].strip():
            insert_at -= 1
        out[insert_at:insert_at] = add
    return out


def prism_java_path(cfg_path, lines):
    # instances/<name>/instance.cfg -> <data dir>/prismlauncher.cfg. A Java that
    # Prism downloaded itself is stored relative to that data dir.
    data_dir = os.path.dirname(os.path.dirname(os.path.dirname(cfg_path)))
    found = None
    if get_key(lines, "OverrideJavaLocation") == "true":
        found = get_key(lines, "JavaPath")
    for name in ("prismlauncher.cfg", "multimc.cfg"):
        g = os.path.join(data_dir, name)
        if not found and os.path.isfile(g):
            found = get_key(read_ini(g), "JavaPath")
    if not found:
        return None
    found = found.strip('"')
    return found if os.path.isabs(found) else os.path.join(data_dir, found)


def java_executables(java_path):
    folder = os.path.dirname(java_path)
    found = []
    for exe in ("java.exe", "javaw.exe"):
        full = os.path.normpath(os.path.join(folder, exe))
        if os.path.isfile(full):
            found.append(full)
    return found


def set_gpu_preference(exes):
    import winreg

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, GPU_KEY) as k:
        for exe in exes:
            winreg.SetValueEx(k, exe, 0, winreg.REG_SZ, GPU_HIGH)


def print_manual(heap):
    print("Modrinth App: no instance.cfg here, so nothing is written.")
    print("Set it by hand in the profile: Settings > Java and memory.")
    print("")
    print("  Memory:          %d MB" % heap)
    print("  Java arguments:  %s" % G1_ARGS)


def main():
    ap = argparse.ArgumentParser(description="Apply JVM, heap and GPU tuning to a Prism instance.")
    ap.add_argument("instance", help="Prism instance folder (the one holding instance.cfg) or its .minecraft")
    ap.add_argument("--heap", type=int, help="max heap in MB instead of the RAM-based default")
    ap.add_argument("--gpu", action="store_true", help="Windows: run this instance's Java on the high-performance GPU")
    ap.add_argument("--yes", action="store_true", help="apply without asking")
    ap.add_argument("--dry-run", action="store_true", help="show what would change and stop")
    args = ap.parse_args()

    if not os.path.isdir(args.instance):
        print("instance folder not found: %s" % args.instance)
        return 2

    ram = total_ram_mb()
    heap = args.heap or heap_for(ram)
    print("RAM      %s" % ("%d MB" % ram if ram else "unknown"))
    print("heap     %d MB (min %d MB)" % (heap, MIN_HEAP_MB))
    if heap > 6144:
        print("         above 6 GB: on four cores a larger heap means longer GC pauses, not fewer")
    print("")

    cfg = find_instance_cfg(args.instance)
    if cfg is None:
        print_manual(heap)
        return 0

    lines = read_ini(cfg)
    values = {
        "OverrideMemory": "true",
        "MinMemAlloc": str(MIN_HEAP_MB),
        "MaxMemAlloc": str(heap),
        "OverrideJavaArgs": "true",
        "JvmArgs": G1_ARGS,
    }
    changes = [(k, get_key(lines, k), v) for k, v in values.items() if get_key(lines, k) != v]

    exes = []
    if args.gpu:
        if sys.platform != "win32":
            print("--gpu only applies on Windows, skipped")
        else:
            java = prism_java_path(cfg, lines)
            exes = java_executables(java) if java else []
            if not exes:
                print("--gpu: no Java path in instance.cfg or prismlauncher.cfg; launch the")
                print("       instance once so Prism picks one, then run this again")

    print("instance %s" % cfg)
    if not changes and not exes:
        print("already tuned, nothing to change")
        return 0
    for k, old, new in changes:
        print("  %-17s %s" % (k, new))
        if old is not None:
            print("  %-17s (was %s)" % ("", old))
    for exe in exes:
        print("  GPU high perf.    %s" % exe)
    print("")

    if args.dry_run:
        return 0
    if not args.yes:
        try:
            answer = input("Apply? [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes", "t", "tak"):
            print("nothing written")
            return 1

    if changes:
        backup = cfg + ".bak"
        shutil.copy2(cfg, backup)
        with open(cfg, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(set_keys(lines, values)) + "\n")
        print("written, backup at %s" % backup)
    if exes:
        set_gpu_preference(exes)
        print("GPU preference set; it applies from the next launch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
