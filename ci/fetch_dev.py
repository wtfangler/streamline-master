"""Downloads what compiling and launching the 26.3 client needs, outside the pack.

    python ci/fetch_dev.py <dir> [--mc 26.3] [--loader 0.19.5]

<dir>/<mc>/client.jar, server.jar, version.json, libs/ (Linux libraries),
assets/ (index and objects without sounds), <dir>/fabric/ (Fabric Loader and its
libraries) and <dir>/fabric/profile.json. Every file is checked against the hash
Mojang publishes; Fabric's Maven publishes none, so those are trusted over HTTPS.
Runs in CI, where Mojang and Fabric are reachable.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import sys
import urllib.request

MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
FABRIC = "https://meta.fabricmc.net/v2/versions/loader/%s/%s/profile/json"
ASSETS = "https://resources.download.minecraft.net/%s/%s"
UA = "streamline-master-ci"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def fetch(url, path, sha1=None):
    if os.path.isfile(path) and (sha1 is None or hashlib.sha1(open(path, "rb").read()).hexdigest() == sha1):
        return path
    data = get(url)
    if sha1 and hashlib.sha1(data).hexdigest() != sha1:
        raise RuntimeError("sha1 mismatch: %s" % url)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return path


def allowed(rules):
    if not rules:
        return True
    ok = False
    for rule in rules:
        if "features" in rule:
            continue
        osr = rule.get("os")
        if not osr or osr.get("name") == "linux":
            ok = rule["action"] == "allow"
    return ok


def maven_path(name):
    parts = name.split(":")
    group, artifact, version = parts[:3]
    classifier = "-" + parts[3] if len(parts) > 3 else ""
    return "%s/%s/%s/%s-%s%s.jar" % (group.replace(".", "/"), artifact, version, artifact, version, classifier)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--mc", default="26.3")
    ap.add_argument("--loader", default="0.19.5")
    args = ap.parse_args()
    root = os.path.abspath(args.dir)
    base = os.path.join(root, args.mc)

    manifest = json.loads(get(MANIFEST))
    entry = next((v for v in manifest["versions"] if v["id"] == args.mc), None)
    if entry is None:
        sys.exit("Mojang has no version %s" % args.mc)
    with open(fetch(entry["url"], os.path.join(base, "version.json"), entry["sha1"]), "rb") as f:
        vj = json.loads(f.read())
    print("java %s required" % vj.get("javaVersion", {}).get("majorVersion"))
    d = vj["downloads"]
    fetch(d["client"]["url"], os.path.join(base, "client.jar"), d["client"]["sha1"])
    fetch(d["server"]["url"], os.path.join(base, "server.jar"), d["server"]["sha1"])

    jobs = []
    for lib in vj["libraries"]:
        if not allowed(lib.get("rules")):
            continue
        art = (lib.get("downloads") or {}).get("artifact")
        if art:
            jobs.append((art["url"], os.path.join(base, "libs", os.path.basename(art["path"])), art["sha1"]))

    index_info = vj["assetIndex"]
    index_path = os.path.join(base, "assets", "indexes", index_info["id"] + ".json")
    fetch(index_info["url"], index_path, index_info["sha1"])
    objects = json.load(open(index_path))["objects"]
    skipped = 0
    for name, obj in objects.items():
        # Sounds are most of the download and the test never plays them.
        if name.startswith(("minecraft/sounds/", "minecraft/resourcepacks/")) or name.endswith(".ogg"):
            skipped += 1
            continue
        h = obj["hash"]
        jobs.append((ASSETS % (h[:2], h), os.path.join(base, "assets", "objects", h[:2], h), h))

    profile = json.loads(get(FABRIC % (args.mc, args.loader)))
    os.makedirs(os.path.join(root, "fabric"), exist_ok=True)
    with open(os.path.join(root, "fabric", "profile.json"), "w") as f:
        json.dump(profile, f, indent=1)
    for lib in profile["libraries"]:
        url = lib.get("url", "https://maven.fabricmc.net/").rstrip("/") + "/" + maven_path(lib["name"])
        jobs.append((url, os.path.join(root, "fabric", os.path.basename(maven_path(lib["name"]))), lib.get("sha1")))

    with concurrent.futures.ThreadPoolExecutor(16) as pool:
        for fut in [pool.submit(fetch, *j) for j in jobs]:
            fut.result()
    print("%d files, %d sound assets skipped, loader %s" % (len(jobs) + 3, skipped, args.loader))


if __name__ == "__main__":
    main()
