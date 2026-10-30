"""Builds the Streamline Bench mod (not shipped in any pack).

    python bench/build.py --dev-dir <dir from ci/fetch_dev.py> [--install]

--install copies the jar to bench/jar/, where bench_setup.py picks it up.
"""
import argparse
import glob
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "ci"))
import javamod  # noqa: E402

VERSION = "1.0.0"
MC = "26.3"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-dir", required=True)
    ap.add_argument("--install", action="store_true")
    args = ap.parse_args()
    name = "slm_bench-%s+mc%s.jar" % (VERSION, MC)
    jar = javamod.build(HERE, os.path.abspath(args.dev_dir), MC, VERSION, name)
    if args.install:
        target = os.path.join(HERE, "jar")
        os.makedirs(target, exist_ok=True)
        for old in glob.glob(os.path.join(target, "slm_bench-*.jar")):
            os.remove(old)
        shutil.copyfile(jar, os.path.join(target, name))
        print("installed into bench/jar")


if __name__ == "__main__":
    main()
