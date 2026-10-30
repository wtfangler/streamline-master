"""Publishes one built pack to Modrinth, following the project's existing naming.

    python release.py 26.3 --channel beta            # dry run: shows what would be sent
    MODRINTH_TOKEN=... python release.py 26.3 --channel beta --publish

Before anything is sent the pack must match its line in SHA256SUMS (so what is
published is what the repository reproduces), pass validate.py, and have a
CHANGELOG.md section for its pack version; and Modrinth must not already have
that version number. Names follow the published history: "Streamline Master
1.5.2" / file "Streamline Master 1.5.2.mrpack", and for betas "Streamline Master
1.6.2 Beta" / "Streamline Master 1.6.2-beta-mc26.3.mrpack".
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://api.modrinth.com/v2"
PROJECT = "VTmQPM8k"
UA = "wtfangler/streamline-master (release.py)"


def pack_version(mc):
    with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    for t in manifest["targets"]:
        if t["minecraft"] == mc:
            return manifest["name"], t["packVersion"]
    raise SystemExit("no target %s in manifest.json" % mc)


def expected_sha256(filename):
    with open(os.path.join(ROOT, "SHA256SUMS"), encoding="utf-8") as f:
        for line in f:
            h, _, name = line.strip().partition(" ")
            if name.lstrip("*") == filename:
                return h
    raise SystemExit("%s has no line in SHA256SUMS" % filename)


def changelog_for(version):
    """The CHANGELOG.md section whose heading names this pack version, without the heading."""
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        text = f.read()
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    for s in sections:
        heading, _, body = s.partition("\n")
        if re.search(r"(?<![\d.])%s(?![\d.])" % re.escape(version), heading):
            if "unreleased" in heading.lower():
                raise SystemExit("CHANGELOG.md still marks %s as unreleased; date it first" % version)
            return body.split("\n---")[0].strip()
    raise SystemExit("CHANGELOG.md has no section for %s" % version)


def http(method, url, token=None, body=None, content_type=None):
    req = urllib.request.Request(url, data=body, method=method, headers={"User-Agent": UA})
    if token:
        req.add_header("Authorization", token)
    if content_type:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"null")


def multipart(data, filename, payload):
    boundary = uuid.uuid4().hex
    parts = [
        b"--" + boundary.encode(),
        b'Content-Disposition: form-data; name="data"',
        b"Content-Type: application/json",
        b"",
        json.dumps(data).encode(),
        b"--" + boundary.encode(),
        ('Content-Disposition: form-data; name="file"; filename="%s"' % filename).encode(),
        b"Content-Type: application/x-modrinth-modpack+zip",
        b"",
        payload,
        b"--" + boundary.encode() + b"--",
        b"",
    ]
    return b"\r\n".join(parts), "multipart/form-data; boundary=" + boundary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("minecraft")
    ap.add_argument("--channel", choices=("release", "beta", "alpha"), default="release")
    ap.add_argument("--dist", default=os.path.join(ROOT, "dist"))
    ap.add_argument("--publish", action="store_true", help="actually upload (needs MODRINTH_TOKEN)")
    args = ap.parse_args()

    name, pv = pack_version(args.minecraft)
    built = os.path.join(args.dist, "%s %s.mrpack" % (name, args.minecraft))
    if not os.path.isfile(built):
        raise SystemExit("%s not found; run: python build.py --offline" % built)
    with open(built, "rb") as f:
        payload = f.read()

    sha = hashlib.sha256(payload).hexdigest()
    if sha != expected_sha256(os.path.basename(built)):
        raise SystemExit("the built pack does not match SHA256SUMS; rebuild from the committed lockfiles")
    if subprocess.run([sys.executable, os.path.join(ROOT, "validate.py"), built]).returncode:
        raise SystemExit("validate.py refused the pack")
    changelog = changelog_for(pv)

    beta = args.channel != "release"
    title = "%s %s%s" % (name, pv, " " + args.channel.capitalize() if beta else "")
    filename = "%s %s%s.mrpack" % (name, pv, "-%s-mc%s" % (args.channel, args.minecraft) if beta else "")
    data = {
        "name": title,
        "version_number": pv,
        "changelog": changelog,
        "dependencies": [],
        "game_versions": [args.minecraft],
        "version_type": args.channel,
        "loaders": ["fabric"],
        "featured": False,
        "project_id": PROJECT,
        "file_parts": ["file"],
        "primary_file": "file",
    }
    print("title    %s" % title)
    print("file     %s (%d bytes, sha256 %s)" % (filename, len(payload), sha))
    print("channel  %s, Minecraft %s" % (args.channel, args.minecraft))
    print("changelog:\n" + "\n".join("  " + l for l in changelog.splitlines()[:12]) + ("\n  ..." if changelog.count("\n") > 12 else ""))

    try:
        existing = http("GET", "%s/project/%s/version" % (API, PROJECT))
    except urllib.error.URLError as e:
        raise SystemExit("cannot reach Modrinth: %s" % e)
    for v in existing:
        if v["version_number"] == pv and args.minecraft in v["game_versions"]:
            raise SystemExit("Modrinth already has %s for %s: %s" % (pv, args.minecraft, v["id"]))

    if not args.publish:
        print("\ndry run: nothing sent (add --publish and MODRINTH_TOKEN to upload)")
        return 0
    token = os.environ.get("MODRINTH_TOKEN")
    if not token:
        raise SystemExit("MODRINTH_TOKEN is not set")
    body, ctype = multipart(data, filename, payload)
    try:
        v = http("POST", API + "/version", token, body, ctype)
    except urllib.error.HTTPError as e:
        raise SystemExit("Modrinth refused: %s %s" % (e.code, e.read().decode("utf-8", "replace")[:500]))
    url = v["files"][0]["url"] if v.get("files") else ""
    print("\npublished %s: https://modrinth.com/modpack/slm/version/%s" % (v["id"], v["id"]))
    if url:
        print("download  %s" % url)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("Published **%s**: https://modrinth.com/modpack/slm/version/%s\n\nDownload: %s\n" % (title, v["id"], url))
    return 0


if __name__ == "__main__":
    sys.exit(main())
