"""Puts the benchmark into game instances and compares what it recorded.

    python bench_setup.py list                      # your instances and their Minecraft version
    python bench_setup.py install <instance> --label SLM
    python bench_setup.py install <other instance> --label FO
        (start each instance once; the run takes about 2 minutes and the game closes itself)
    python bench_setup.py compare <instance> <other instance>
    python bench_setup.py remove <instance>

install copies bench/jar/slm_bench-*.jar into the instance's mods folder and
writes slm-bench.txt, the switch the mod looks for. The mod then opens (or on
first use creates) the world "SLM Benchmark" from a fixed seed and records two
scenes: "static" (30 s, fixed view) and "flight" (60 s along a fixed line at 10
blocks/s, where chunk building happens). compare takes the newest recording of
each scene from both instances and runs bench.py on them. remove deletes the
jar and the switch; the world and the recordings stay.

<instance> is a folder path or simply the instance's name as `list` shows it
(a unique part of it is enough). Works for Prism Launcher and the Modrinth App. Use the same Minecraft version, the same
options.txt and the same JVM arguments (tune.py) in both, or you measure those.
"""
import argparse
import glob
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import bench  # noqa: E402

SCENES = ("static", "flight")
BENCH_MC = "26.3"  # the bench jar is built against this client


def launcher_dirs():
    """Where Prism Launcher and the Modrinth App keep instances by default, per OS."""
    if sys.platform == "win32":
        base = [os.environ.get("APPDATA", "")]
    elif sys.platform == "darwin":
        base = [os.path.expanduser("~/Library/Application Support")]
    else:
        base = [os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")]
    out = []
    for b in base:
        prism = os.path.join(b, "PrismLauncher")
        inst = os.path.join(prism, "instances")
        cfg = os.path.join(prism, "prismlauncher.cfg")
        if os.path.isfile(cfg):  # a custom instance folder set in Prism's settings
            for line in open(cfg, encoding="utf-8", errors="replace"):
                k, _, v = line.partition("=")
                if k.strip() == "InstanceDir" and v.strip():
                    v = v.strip().strip('"')
                    inst = v if os.path.isabs(v) else os.path.join(prism, v)
        out.append(("Prism", inst))
        out.append(("Modrinth App", os.path.join(b, "ModrinthApp", "profiles")))
    return out


def minecraft_version(folder):
    """Prism records it in mmc-pack.json; the Modrinth App keeps it in its database, so unknown there."""
    try:
        with open(os.path.join(folder, "mmc-pack.json"), encoding="utf-8") as f:
            for c in json.load(f).get("components", []):
                if c.get("uid") == "net.minecraft":
                    return c.get("version")
    except (OSError, ValueError):
        pass
    return None


def instances():
    found = []
    for launcher, base in launcher_dirs():
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base), key=str.lower):
            folder = os.path.join(base, name)
            if os.path.isdir(folder) and not name.startswith((".", "_")):
                found.append((launcher, name, folder))
    return found


def resolve(arg):
    """A path, or an instance name (or a unique part of one) from the launchers' folders."""
    looks_like_path = os.path.isabs(arg) or "/" in arg or "\\" in arg
    if looks_like_path:
        if os.path.isdir(arg):
            return os.path.abspath(arg)
        raise SystemExit('folder not found: %s\nrun: python bench_setup.py list' % arg)
    all_ = instances()
    exact = [f for _, n, f in all_ if n.lower() == arg.lower()]
    partial = [f for _, n, f in all_ if arg.lower() in n.lower()]
    hits = exact or partial
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit('no folder or instance called "%s"; run: python bench_setup.py list' % arg)
    raise SystemExit('"%s" matches several instances (%s); use more of the name'
                     % (arg, ", ".join(os.path.basename(h) for h in hits)))


def game_dir(path):
    path = resolve(path)
    for sub in ("minecraft", ".minecraft"):
        if os.path.isdir(os.path.join(path, sub)):
            return os.path.join(path, sub)
    return path


def list_instances(args):
    rows = instances()
    if not rows:
        print("no Prism or Modrinth App instances found in the default folders;")
        print("pass the instance folder itself (Prism: right-click the instance, Folder)")
        return
    for launcher, name, folder in rows:
        mc = minecraft_version(folder) or "?"
        mark = "" if mc in (BENCH_MC, "?") else "   (benchmark needs %s)" % BENCH_MC
        print("%-13s %-8s %s%s" % (launcher, mc, name, mark))


def bench_jar():
    jars = sorted(glob.glob(os.path.join(ROOT, "bench", "jar", "slm_bench-*.jar")))
    if not jars:
        raise SystemExit("no bench jar in bench/jar; the CI client job builds it")
    return jars[-1]


def install(args):
    folder = resolve(args.instance)
    mc = minecraft_version(folder)
    if mc and mc != BENCH_MC:
        raise SystemExit("%s is Minecraft %s; the benchmark mod is built for %s" % (os.path.basename(folder), mc, BENCH_MC))
    game = game_dir(folder)
    mods = os.path.join(game, "mods")
    if not os.path.isdir(mods):
        raise SystemExit("no mods folder in %s; is this a Minecraft instance?" % game)
    for old in glob.glob(os.path.join(mods, "slm_bench-*.jar")):
        os.remove(old)
    jar = bench_jar()
    shutil.copyfile(jar, os.path.join(mods, os.path.basename(jar)))
    with open(os.path.join(game, "slm-bench.txt"), "w", encoding="utf-8") as f:
        f.write(args.label + "\n")
    print("installed %s into %s, label %s" % (os.path.basename(jar), mods, args.label))
    print("start the instance; the benchmark runs by itself and closes the game (about 2 minutes)")


def remove(args):
    game = game_dir(args.instance)
    gone = glob.glob(os.path.join(game, "mods", "slm_bench-*.jar")) + glob.glob(os.path.join(game, "slm-bench.txt"))
    for f in gone:
        os.remove(f)
    print("removed %d file(s); recordings stay in %s" % (len(gone), os.path.join(game, "slm-bench")))


def newest(game, scene):
    files = sorted(glob.glob(os.path.join(game, "slm-bench", "*-%s.csv" % scene)), key=os.path.getmtime)
    return files[-1] if files else None


def compare(args):
    a, b = game_dir(args.a), game_dir(args.b)
    for scene in SCENES:
        fa, fb = newest(a, scene), newest(b, scene)
        print("\n=== %s" % scene)
        if not fa or not fb:
            print("missing recording: %s" % (a if not fa else b))
            continue
        sys.argv = ["bench.py", fa, "--vs", fb]
        bench.main()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.set_defaults(fn=list_instances)
    p = sub.add_parser("install")
    p.add_argument("instance")
    p.add_argument("--label", required=True, help="name written into the recordings, e.g. SLM or FO")
    p.set_defaults(fn=install)
    p = sub.add_parser("remove")
    p.add_argument("instance")
    p.set_defaults(fn=remove)
    p = sub.add_parser("compare")
    p.add_argument("a", help="instance under test")
    p.add_argument("b", help="baseline instance")
    p.set_defaults(fn=compare)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
