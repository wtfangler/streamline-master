"""Builds Streamline Loader and optionally installs it into the 26.3 pack.

    python loader/build.py --dev-dir <dir from ci/fetch_dev.py> [--install]

--install puts the jar in overrides-<mc>/mods/, replacing an older build, so the
next `python build.py` ships it inside the pack.
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
    name = "streamline_loader-%s+mc%s.jar" % (VERSION, MC)
    jar = javamod.build(HERE, os.path.abspath(args.dev_dir), MC, VERSION, name)
    if args.install:
        mods = os.path.join(ROOT, "overrides-%s" % MC, "mods")
        os.makedirs(mods, exist_ok=True)
        for old in glob.glob(os.path.join(mods, "streamline_loader-*.jar")):
            os.remove(old)
        shutil.copyfile(jar, os.path.join(mods, name))
        print("installed into %s" % os.path.relpath(mods, ROOT))


if __name__ == "__main__":
    main()
