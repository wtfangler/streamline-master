"""Puts the benchmark into game instances and compares what it recorded.

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

Works for Prism Launcher (instance folder or its minecraft/.minecraft) and for
the Modrinth App (profile folder). Use the same Minecraft version, the same
options.txt and the same JVM arguments (tune.py) in both, or you measure those.
"""
import argparse
import glob
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import bench  # noqa: E402

SCENES = ("static", "flight")


def game_dir(path):
    path = os.path.abspath(path)
    for sub in ("minecraft", ".minecraft"):
        if os.path.isdir(os.path.join(path, sub)):
            return os.path.join(path, sub)
    return path


def bench_jar():
    jars = sorted(glob.glob(os.path.join(ROOT, "bench", "jar", "slm_bench-*.jar")))
    if not jars:
        raise SystemExit("no bench jar in bench/jar; the CI client job builds it")
    return jars[-1]


def install(args):
    game = game_dir(args.instance)
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
