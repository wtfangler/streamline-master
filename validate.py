import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile

API = "https://api.modrinth.com/v2"
UA = "streamline-master/2.0 (modrinth pack validator)"
SHA1 = re.compile(r"^[0-9a-f]{40}$")
SHA512 = re.compile(r"^[0-9a-f]{128}$")
ALLOWED_ROOTS = ("mods/", "resourcepacks/", "shaderpacks/", "config/")
CONFIG_OWNERS = {
    "config/isxander-main-menu-credits.json": ("mainmenucredits",),
    "config/threadtweak.json": ("threadtweak",),
    "config/exordium.json": ("exordium",),
    "config/moreculling.toml": ("moreculling",),
    "config/sodium-options.json": ("sodium",),
    "config/entityculling.json": ("entityculling",),
    "config/c2me.toml": ("c2me",),
    "config/vmp.properties": ("vmp",),
    "config/lithium.properties": ("lithium",),
    "config/ferritecore.mixin.properties": ("ferritecore",),
    "config/modernfix-mixins.properties": ("modernfix",),
    "config/badoptimizations.txt": ("badoptimizations",),
    "config/immediatelyfast.json": ("immediatelyfast",),
    "config/dynamic_fps.json": ("dynamicfps",),
    "config/languagereload.json": ("languagereload",),
    "config/letmedespawn.json": ("letmedespawn", "lmd"),
    "config/zoomify.json": ("zoomify",),
    "config/modmenu.json": ("modmenu",),
    "config/iris.properties": ("iris",),
    "config/sodium-extra-options.json": ("sodiumextra",),
    "config/smoothgui.json": ("smoothgui",),
    "config/smoothscroll.json": ("smoothscroll",),
    "config/smoothswapping.json": ("smoothswapping",),
}
STRAY_FILES = ("config/sodium-fingerprint.json",)


UNREACHABLE = object()


def http_json(url, attempts=3):
    delay = 1.0
    for _ in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code not in (429, 500, 502, 503, 504):
                return UNREACHABLE
        except urllib.error.URLError:
            pass
        time.sleep(delay)
        delay *= 2
    return UNREACHABLE


def check(path, online):
    problems = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "modrinth.index.json" not in names:
            return ["missing modrinth.index.json"]
        idx = json.loads(z.read("modrinth.index.json").decode("utf-8"))
        overrides = [n for n in names if n.startswith("overrides/") and not n.endswith("/")]

    if idx.get("formatVersion") != 1:
        problems.append("formatVersion is not 1")
    if idx.get("game") != "minecraft":
        problems.append("game is not minecraft")
    deps = idx.get("dependencies") or {}
    if "minecraft" not in deps:
        problems.append("dependencies.minecraft missing")
    if "fabric-loader" not in deps:
        problems.append("dependencies.fabric-loader missing")

    seen_paths = set()
    seen_hashes = set()
    for f in idx.get("files", []):
        p = f.get("path", "")
        if not p.startswith(ALLOWED_ROOTS):
            problems.append("%s: path outside allowed roots" % p)
        if ".." in p or p.startswith("/"):
            problems.append("%s: unsafe path" % p)
        if p in seen_paths:
            problems.append("%s: duplicate path" % p)
        seen_paths.add(p)
        h = f.get("hashes") or {}
        if not SHA1.match(h.get("sha1", "")):
            problems.append("%s: malformed sha1" % p)
        if not SHA512.match(h.get("sha512", "")):
            problems.append("%s: malformed sha512" % p)
        if h.get("sha512") in seen_hashes:
            problems.append("%s: duplicate sha512" % p)
        seen_hashes.add(h.get("sha512"))
        if not isinstance(f.get("fileSize"), int) or f["fileSize"] <= 0:
            problems.append("%s: bad fileSize" % p)
        dl = f.get("downloads") or []
        if not dl or not all(u.startswith("https://cdn.modrinth.com/") for u in dl):
            problems.append("%s: bad downloads" % p)
        env = f.get("env") or {}
        if env.get("client") not in ("required", "optional", "unsupported"):
            problems.append("%s: bad env.client" % p)
        if env.get("server") not in ("required", "optional", "unsupported"):
            problems.append("%s: bad env.server" % p)

    jars = " ".join(p.rsplit("/", 1)[-1].lower() for p in seen_paths).replace("-", "").replace("_", "")
    for name in overrides:
        rel = name[len("overrides/"):]
        if rel in seen_paths:
            problems.append("%s: shipped both as override and as index file" % rel)
        if rel in STRAY_FILES:
            problems.append("%s: machine-specific file, should not ship" % rel)
        owners = CONFIG_OWNERS.get(rel)
        if owners and not any(o in jars for o in owners):
            problems.append("%s: config shipped but %s is not in the index" % (rel, owners[0]))

    if online:
        mc = deps.get("minecraft")
        unreachable = 0
        for f in idx.get("files", []):
            if unreachable >= 3:
                print("   note: online check aborted, Modrinth unreachable")
                break
            sha = (f.get("hashes") or {}).get("sha512", "")
            data = http_json("%s/version_file/%s?algorithm=sha512" % (API, sha))
            if data is UNREACHABLE:
                unreachable += 1
                continue
            if data is None:
                problems.append("%s: sha512 does not resolve on Modrinth" % f.get("path"))
                continue
            if mc not in data.get("game_versions", []):
                problems.append("%s: resolved version does not support %s" % (f.get("path"), mc))
            match = [x for x in (data.get("files") or []) if (x.get("hashes") or {}).get("sha512") == sha]
            if match and match[0].get("size") != f.get("fileSize"):
                problems.append("%s: fileSize mismatch" % f.get("path"))
        if 0 < unreachable < 3:
            print("   note: %d file(s) not verified online" % unreachable)

    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packs", nargs="+")
    ap.add_argument("--online", action="store_true")
    args = ap.parse_args()

    packs = []
    for a in args.packs:
        packs.extend(sorted(glob.glob(a)) if any(c in a for c in "*?[") else [a])

    failed = 0
    for p in packs:
        if not os.path.exists(p):
            print("%s: not found" % p)
            failed += 1
            continue
        problems = check(p, args.online)
        if problems:
            failed += 1
            print("%s: %d problem(s)" % (os.path.basename(p), len(problems)))
            for x in problems:
                print("   %s" % x)
        else:
            print("%s: ok" % os.path.basename(p))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
