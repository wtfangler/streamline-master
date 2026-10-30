"""Shared builder for the repository's own client mods (loader/, bench/).

No Gradle/Loom: Minecraft 26.x ships unobfuscated, so plain javac and Mixin
annotations are enough (mixins are applied by Fabric Loader at run time; there is
no refmap because nothing is remapped). The jar is written with fixed entry
metadata, like the packs, so a rebuild from the same sources is byte-identical.
"""
import glob
import io
import os
import shutil
import subprocess
import zipfile

ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


def classpath(dev, mc):
    cp = [os.path.join(dev, mc, "client.jar")]
    cp += sorted(glob.glob(os.path.join(dev, mc, "libs", "*.jar")))
    cp += sorted(glob.glob(os.path.join(dev, "fabric", "*.jar")))
    if not os.path.isfile(cp[0]):
        raise SystemExit("no client jar at %s; run ci/fetch_dev.py first" % cp[0])
    return cp


def _entry(z, name, data):
    info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    z.writestr(info, data)


def _walk(base):
    for dirpath, dirs, names in os.walk(base):
        dirs.sort()
        for n in sorted(names):
            full = os.path.join(dirpath, n)
            yield os.path.relpath(full, base).replace(os.sep, "/"), full


def build(module, dev, mc, version, jar_name):
    """Compiles <module>/src against the client and packs it with <module>/resources into <module>/dist/<jar_name>."""
    out = os.path.join(module, "build")
    classes = os.path.join(out, "classes")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(classes)
    sources = sorted(glob.glob(os.path.join(module, "src", "**", "*.java"), recursive=True))
    cmd = [os.environ.get("JAVAC", "javac"), "--release", "25", "-encoding", "UTF-8", "-proc:none",
           "-Xlint:-options", "-d", classes, "-cp", os.pathsep.join(classpath(dev, mc))] + sources
    print("javac %d files in %s for %s" % (len(sources), os.path.basename(module), mc))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        print(res.stderr[:6000])
        raise SystemExit("compile failed")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, full in _walk(classes):
            with open(full, "rb") as f:
                _entry(z, rel, f.read())
        for rel, full in _walk(os.path.join(module, "resources")):
            with open(full, "rb") as f:
                data = f.read()
            if rel == "fabric.mod.json":
                data = data.decode("utf-8").replace("${version}", "%s+mc%s" % (version, mc)) \
                    .replace("${minecraft}", "~" + mc).encode("utf-8")
            _entry(z, rel, data)
    jar = os.path.join(module, "dist", jar_name)
    os.makedirs(os.path.dirname(jar), exist_ok=True)
    with open(jar, "wb") as f:
        f.write(buf.getvalue())
    print("built %s (%d bytes)" % (jar, len(buf.getvalue())))
    return jar
