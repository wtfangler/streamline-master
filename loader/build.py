"""Compiles Streamline Loader against the Minecraft client jar and packs a reproducible jar.

    python loader/build.py --dev-dir <dir> [--install]

<dir> holds what ci/fetch_dev.py downloads: <mc>/client.jar, <mc>/libs/*.jar and
fabric/*.jar (Fabric Loader and Mixin). No Gradle/Loom: Minecraft 26.x ships
unobfuscated, so plain javac and Mixin annotations are enough (mixins are applied
by Fabric Loader at run time; there is no refmap because nothing is remapped).

--install puts the jar in overrides-<mc>/mods/, replacing an older build, so the
next `python build.py` ships it inside the pack.
"""
import argparse
import glob
import io
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VERSION = "1.0.0"
MC = "26.3"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


def write_entry(z, name, data):
    # Same fixed metadata as the pack builder, so the jar is byte-identical between builds.
    info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    z.writestr(info, data)


def files_under(base):
    for dirpath, dirs, names in os.walk(base):
        dirs.sort()
        for n in sorted(names):
            full = os.path.join(dirpath, n)
            yield os.path.relpath(full, base).replace(os.sep, "/"), full


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-dir", required=True)
    ap.add_argument("--install", action="store_true")
    args = ap.parse_args()

    dev = os.path.abspath(args.dev_dir)
    cp = [os.path.join(dev, MC, "client.jar")]
    cp += sorted(glob.glob(os.path.join(dev, MC, "libs", "*.jar")))
    cp += sorted(glob.glob(os.path.join(dev, "fabric", "*.jar")))
    if not os.path.isfile(cp[0]):
        sys.exit("no client jar at %s; run ci/fetch_dev.py first" % cp[0])

    out = os.path.join(HERE, "build")
    classes = os.path.join(out, "classes")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(classes)
    sources = sorted(glob.glob(os.path.join(HERE, "src", "**", "*.java"), recursive=True))
    cmd = [os.environ.get("JAVAC", "javac"), "--release", "25", "-encoding", "UTF-8", "-proc:none",
           "-Xlint:-options", "-d", classes, "-cp", os.pathsep.join(cp)] + sources
    print("javac %d files for %s" % (len(sources), MC))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        print(res.stderr[:4000])
        sys.exit("compile failed")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, full in files_under(classes):
            with open(full, "rb") as f:
                write_entry(z, rel, f.read())
        for rel, full in files_under(os.path.join(HERE, "resources")):
            with open(full, "rb") as f:
                data = f.read()
            if rel == "fabric.mod.json":
                data = data.decode("utf-8").replace("${version}", "%s+mc%s" % (VERSION, MC)).replace("${minecraft}", "~" + MC).encode("utf-8")
            write_entry(z, rel, data)

    name = "streamline_loader-%s+mc%s.jar" % (VERSION, MC)
    jar = os.path.join(HERE, "dist", name)
    os.makedirs(os.path.dirname(jar), exist_ok=True)
    with open(jar, "wb") as f:
        f.write(buf.getvalue())
    print("built %s (%d bytes)" % (jar, len(buf.getvalue())))

    if args.install:
        mods = os.path.join(ROOT, "overrides-%s" % MC, "mods")
        os.makedirs(mods, exist_ok=True)
        for old in glob.glob(os.path.join(mods, "streamline_loader-*.jar")):
            os.remove(old)
        shutil.copyfile(jar, os.path.join(mods, name))
        print("installed into %s" % os.path.relpath(mods, ROOT))


if __name__ == "__main__":
    main()
