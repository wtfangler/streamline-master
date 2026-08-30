import argparse
import hashlib
import json
import os
import sys
import zipfile

CONFIG_ROOTS = ("config", "options.txt")


def sha1_of(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_pack(pack_path):
    with zipfile.ZipFile(pack_path) as z:
        idx = json.loads(z.read("modrinth.index.json").decode("utf-8"))
        overrides = {}
        for n in z.namelist():
            if n.startswith("overrides/") and not n.endswith("/"):
                overrides[n[len("overrides/"):]] = hashlib.sha1(z.read(n)).hexdigest()
    return idx, overrides


def listdir(path):
    if not os.path.isdir(path):
        return set()
    return {n for n in os.listdir(path) if not n.startswith(".")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("instance")
    args = ap.parse_args()

    if not os.path.exists(args.pack):
        print("pack not found: %s" % args.pack)
        return 2
    root = args.instance
    if os.path.isdir(os.path.join(root, ".minecraft")):
        root = os.path.join(root, ".minecraft")
    if not os.path.isdir(root):
        print("instance folder not found: %s" % args.instance)
        return 2

    idx, overrides = read_pack(args.pack)
    print("pack     %s %s" % (idx.get("name"), idx.get("versionId")))
    print("instance %s" % root)
    print("")

    expected = {}
    for f in idx.get("files", []):
        folder, name = f["path"].split("/", 1)
        expected.setdefault(folder, {})[name] = f["hashes"]["sha1"]

    problems = 0
    for folder in sorted(expected):
        on_disk = listdir(os.path.join(root, folder))
        want = expected[folder]
        missing = sorted(set(want) - on_disk)
        extra = sorted(n for n in on_disk - set(want) if n.lower().endswith((".jar", ".zip")))
        print("%s: %d expected, %d present" % (folder, len(want), len(want) - len(missing)))
        for n in missing:
            print("   MISSING  %s" % n)
            problems += 1
        for n in extra:
            print("   EXTRA    %s" % n)
        print("")

    print("overrides: %d files shipped" % len(overrides))
    stale = []
    absent = []
    for rel, want_sha in sorted(overrides.items()):
        full = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(full):
            absent.append(rel)
            continue
        if sha1_of(full) != want_sha:
            stale.append(rel)
    for rel in absent:
        print("   ABSENT   %s" % rel)
        problems += 1
    for rel in stale:
        print("   DIFFERS  %s" % rel)
    print("   identical: %d" % (len(overrides) - len(absent) - len(stale)))
    print("")

    if absent or stale:
        print("Files marked ABSENT or DIFFERS were not applied by the launcher.")
        print("Most launchers skip existing files when updating a pack in place.")
        print("Delete them in the instance and reinstall, or install into a new instance.")
    if problems == 0 and not stale:
        print("Instance matches the pack.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
