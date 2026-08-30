import argparse
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://api.modrinth.com/v2"
FABRIC_META = "https://meta.fabricmc.net/v2/versions/loader"
UA = "streamline-master/2.0 (modrinth pack builder)"
RANK = {"release": 3, "beta": 2, "alpha": 1}
SHA1 = re.compile(r"^[0-9a-f]{40}$")
SHA512 = re.compile(r"^[0-9a-f]{128}$")

ENV_MAP = {
    "client": {"client": "required", "server": "unsupported"},
    "server": {"client": "unsupported", "server": "required"},
    "both": {"client": "required", "server": "required"},
}
TEMPLATE_SUFFIX = ".tmpl"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


class BuildError(Exception):
    pass


def http_json(url, attempts=5):
    delay = 1.0
    last = None
    for _ in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                return None
            if e.code not in (429, 500, 502, 503, 504):
                raise
        except urllib.error.URLError as e:
            last = e
        time.sleep(delay)
        delay *= 2
    raise BuildError("request failed: %s (%s)" % (url, last))


def load_manifest():
    with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def pack_version(manifest, mc):
    for t in manifest["targets"]:
        if t["minecraft"] == mc:
            return t.get("packVersion") or manifest["packVersion"]
    return manifest["packVersion"]


def loader_version(pinned):
    if pinned:
        return pinned
    data = http_json(FABRIC_META)
    for entry in data:
        if entry.get("stable"):
            return entry["version"]
    return data[0]["version"]


def fetch_versions(slug, url):
    data = http_json(url)
    if data is None:
        raise BuildError("unknown project: %s" % slug)
    return data


def query_versions(slug, mc, loader, any_loader=False):
    q = urllib.parse.urlencode({"game_versions": json.dumps([mc])})
    urls = [
        "%s/project/%s/version?%s" % (API, slug, q),
        "%s/project/%s/version" % (API, slug),
    ]
    for url in urls:
        out = []
        for v in fetch_versions(slug, url):
            if mc not in v.get("game_versions", []):
                continue
            if not any_loader and loader not in v.get("loaders", []):
                continue
            out.append(v)
        if out:
            return out
    return []


def supported_versions(slug, loader):
    try:
        data = http_json("%s/project/%s/version" % (API, slug))
    except BuildError:
        return []
    seen = []
    for v in data or []:
        if loader not in v.get("loaders", []):
            continue
        for g in v.get("game_versions", []):
            if g not in seen:
                seen.append(g)
    return seen


def pick(versions, allow_prerelease):
    if not versions:
        return None
    pool = [v for v in versions if v.get("version_type") == "release"]
    if not pool and allow_prerelease:
        pool = versions
    if not pool:
        return None
    pool.sort(key=lambda v: (RANK.get(v.get("version_type"), 0), v.get("date_published", "")), reverse=True)
    return pool[0]


def primary_file(version):
    files = version.get("files") or []
    for f in files:
        if f.get("primary"):
            return f
    if files:
        return files[0]
    raise BuildError("version %s has no files" % version.get("id"))


def check_file(slug, f):
    h = f.get("hashes") or {}
    sha1 = h.get("sha1", "")
    sha512 = h.get("sha512", "")
    if not SHA1.match(sha1):
        raise BuildError("%s: bad sha1 %r" % (slug, sha1))
    if not SHA512.match(sha512):
        raise BuildError("%s: bad sha512 %r" % (slug, sha512))
    if not isinstance(f.get("size"), int) or f["size"] <= 0:
        raise BuildError("%s: bad size" % slug)
    if not str(f.get("url", "")).startswith("https://cdn.modrinth.com/"):
        raise BuildError("%s: unexpected download host" % slug)


def resolve(manifest, target):
    mc = target["minecraft"]
    loader = manifest["loader"]
    allow = target.get("allowPrerelease", False)
    entries = []
    missing = []
    for mod in manifest["mods"]:
        slug = mod["slug"]
        if mc in mod.get("skipTargets", []):
            continue
        folder = mod.get("path", "mods")
        chosen = pick(query_versions(slug, mc, loader, folder != "mods"), allow)
        if chosen is None:
            if mod.get("optional"):
                missing.append(slug)
                continue
            known = supported_versions(slug, loader)
            hint = ("this project has %s builds for: %s" % (loader, ", ".join(known[:10]))
                    if known else "this project has no %s builds at all" % loader)
            raise BuildError(
                "no %s build of %s for %s\n       %s\n       "
                "fix the slug in manifest.json, or add \"optional\": true to skip it"
                % (loader, slug, mc, hint)
            )
        f = primary_file(chosen)
        check_file(slug, f)
        entries.append(
            {
                "slug": slug,
                "group": mod["group"],
                "env": mod["env"],
                "path": folder,
                "projectId": chosen["project_id"],
                "versionId": chosen["id"],
                "versionNumber": chosen["version_number"],
                "versionType": chosen["version_type"],
                "filename": f["filename"],
                "size": f["size"],
                "sha1": f["hashes"]["sha1"],
                "sha512": f["hashes"]["sha512"],
                "url": f["url"],
            }
        )
    entries.sort(key=lambda e: e["filename"].lower())
    return entries, missing


def lock_path(mc):
    return os.path.join(ROOT, "lock", "%s.json" % mc)


def write_lock(mc, loader_ver, entries, missing):
    payload = {
        "minecraft": mc,
        "fabricLoader": loader_ver,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "missingOptional": missing,
        "mods": entries,
    }
    os.makedirs(os.path.dirname(lock_path(mc)), exist_ok=True)
    # newline="\n" so a build on Windows does not rewrite every lockfile with
    # CRLF and show the whole of lock/ as modified in git.
    with open(lock_path(mc), "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    return payload


def read_lock(mc):
    p = lock_path(mc)
    if not os.path.exists(p):
        raise BuildError("no lock for %s, run without --offline first" % mc)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def collect_overrides(mc):
    roots = [os.path.join(ROOT, "overrides")]
    special = os.path.join(ROOT, "overrides-%s" % mc)
    if os.path.isdir(special):
        roots.append(special)
    files = {}
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _, names in os.walk(root):
            for n in names:
                full = os.path.join(dirpath, n)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                if rel.endswith(TEMPLATE_SUFFIX):
                    rel = rel[: -len(TEMPLATE_SUFFIX)]
                files[rel] = full
    return files


def render_override(path, subs, packs):
    with open(path, encoding="utf-8") as f:
        body = f.read()
    if not path.endswith(TEMPLATE_SUFFIX):
        return body.encode("utf-8")
    for k, v in subs.items():
        body = body.replace("{{%s}}" % k, str(v))

    def resourcepack(m):
        slug = m.group(1)
        if slug not in packs:
            raise BuildError("%s: no resourcepack %s in this build" % (path, slug))
        return packs[slug]

    body = re.sub(r"\{\{resourcepack:([A-Za-z0-9_-]+)\}\}", resourcepack, body)
    left = re.search(r"\{\{[^}]+\}\}", body)
    if left:
        raise BuildError("%s: unresolved placeholder %s" % (path, left.group(0)))
    return body.encode("utf-8")


def index_json(manifest, lock):
    files = []
    for e in lock["mods"]:
        files.append(
            {
                "path": "%s/%s" % (e.get("path", "mods"), e["filename"]),
                "hashes": {"sha1": e["sha1"], "sha512": e["sha512"]},
                "env": ENV_MAP[e["env"]],
                "downloads": [e["url"]],
                "fileSize": e["size"],
            }
        )
    return {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": "%s+%s" % (pack_version(manifest, lock["minecraft"]), lock["minecraft"]),
        "name": manifest["name"],
        "summary": manifest["summary"],
        "files": files,
        "dependencies": {
            "minecraft": lock["minecraft"],
            "fabric-loader": lock["fabricLoader"],
        },
    }


def add_entry(z, name, data):
    """Write one zip entry with a fixed timestamp and fixed permissions.

    zipfile stamps entries with the current local time by default, which makes
    every build produce a different file even when the contents are identical.
    Pinning the timestamp is what lets `--offline` actually reproduce a release
    byte for byte, so a published .mrpack can be checked against a rebuild.
    ZIP_EPOCH is the earliest date the zip format can store.
    """
    info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    if isinstance(data, str):
        data = data.encode("utf-8")
    z.writestr(info, data)


def write_pack(manifest, lock, outdir):
    mc = lock["minecraft"]
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "%s %s.mrpack" % (manifest["name"], mc))
    idx = index_json(manifest, lock)
    overrides = collect_overrides(mc)
    subs = {
        "name": manifest["name"],
        "packVersion": pack_version(manifest, mc),
        "minecraft": mc,
        "loaderVersion": lock["fabricLoader"],
    }
    packs = {e["slug"]: e["filename"] for e in lock["mods"] if e.get("path") == "resourcepacks"}
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        add_entry(z, "modrinth.index.json", json.dumps(idx, indent=2) + "\n")
        for rel in sorted(overrides):
            add_entry(z, "overrides/%s" % rel, render_override(overrides[rel], subs, packs))
    return out, len(idx["files"]), len(overrides)


def survey(manifest):
    loader = manifest["loader"]
    rows = []
    for mod in manifest["mods"]:
        row = {"slug": mod["slug"]}
        for target in manifest["targets"]:
            mc = target["minecraft"]
            if mc in mod.get("skipTargets", []):
                row[mc] = "skip"
                continue
            any_loader = mod.get("path", "mods") != "mods"
            chosen = pick(query_versions(mod["slug"], mc, loader, any_loader), target.get("allowPrerelease", False))
            row[mc] = "%s (%s)" % (chosen["version_number"], chosen["version_type"]) if chosen else "-"
        rows.append(row)
    width = max(len(r["slug"]) for r in rows) + 2
    header = "mod".ljust(width) + "".join(t["minecraft"].ljust(34) for t in manifest["targets"])
    print(header)
    print("-" * len(header))
    for r in rows:
        print(r["slug"].ljust(width) + "".join(str(r[t["minecraft"]]).ljust(34) for t in manifest["targets"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--survey", action="store_true")
    ap.add_argument("--loader-version", default="")
    ap.add_argument("--clean", action="store_true")
    args = ap.parse_args()

    manifest = load_manifest()

    if args.survey:
        survey(manifest)
        return 0

    if args.clean and os.path.isdir(args.out):
        shutil.rmtree(args.out)

    targets = manifest["targets"]
    if args.only:
        wanted = set(args.only)
        targets = [t for t in targets if t["minecraft"] in wanted]
        if not targets:
            raise BuildError("no target matches %s" % sorted(wanted))

    loader_ver = None if args.offline else loader_version(args.loader_version)

    for target in targets:
        mc = target["minecraft"]
        if args.offline:
            lock = read_lock(mc)
        else:
            entries, missing = resolve(manifest, target)
            lock = write_lock(mc, loader_ver, entries, missing)
            if missing:
                print("%s: skipped optional %s" % (mc, ", ".join(missing)))
        path, nmods, nover = write_pack(manifest, lock, args.out)
        prerelease = [e["slug"] for e in lock["mods"] if e["versionType"] != "release"]
        print("%s -> %s" % (mc, os.path.relpath(path, ROOT)))
        print("   loader %s | %d mods | %d override files" % (lock["fabricLoader"], nmods, nover))
        if prerelease:
            print("   prerelease: %s" % ", ".join(sorted(prerelease)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as e:
        print("error: %s" % e, file=sys.stderr)
        sys.exit(1)
