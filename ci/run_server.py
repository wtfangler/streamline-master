"""Builds a server from a pack with server/build_server.py and checks that it starts.

    python ci/run_server.py <pack.mrpack> --work <dir> --out <results dir>

Uses the builder exactly as a player would, then accepts the EULA in this
throw-away CI copy only, runs start.sh, waits for "Done (", records the start-up
time and stops the server cleanly. Writes <out>/server.md and <out>/server.log.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOISE = re.compile(r"(\bERROR\b|Exception|Mixin apply failed|Incompatible mod)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()
    work, out = os.path.abspath(args.work), os.path.abspath(args.out)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(out, exist_ok=True)

    subprocess.run([sys.executable, os.path.join(ROOT, "server", "build_server.py"), args.pack, work, "--ram", "3G"], check=True)
    with open(os.path.join(work, "eula.txt"), "w") as f:
        f.write("eula=true\n")  # CI-only copy, deleted with the runner

    log_path = os.path.join(out, "server.log")
    start = time.time()
    done_at, lines = None, []
    proc = subprocess.Popen(["bash", "start.sh"], cwd=work, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        lines.append(line)
        if done_at is None and "Done (" in line:
            done_at = time.time() - start
            proc.stdin.write("stop\n")
            proc.stdin.flush()
        if time.time() - start > args.timeout:
            proc.kill()
            break
    code = proc.wait(timeout=120)
    with open(log_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    text = "".join(lines)
    loaded = next((l.strip() for l in lines if "Loading " in l and " mods" in l), "")
    noise = [l.rstrip() for l in lines if NOISE.search(l)]
    passed = done_at is not None and code == 0
    report = [
        "# Server built from the pack",
        "",
        "**%s** — %s, exit %s" % ("PASS" if passed else "FAIL",
                                  "ready in %.1f s" % done_at if done_at else "never reached \"Done\"", code),
        "",
        "```", loaded, "```", "",
        "## Errors and warnings worth reading (%d)" % len(noise), "", "```",
    ] + noise[:100] + ["```", ""]
    with open(os.path.join(out, "server.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print("\n".join(report[:3]))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
