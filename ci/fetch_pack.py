"""Downloads the newest .mrpack of a Modrinth modpack for one Minecraft version.

    python ci/fetch_pack.py fabulously-optimized 26.3 <out.mrpack>

Prints the version it took and the Fabric Loader the pack asks for (the last
line is just that version, for the workflow). The file is checked against the
SHA-512 Modrinth publishes. Release builds are preferred over beta and alpha.
"""
import hashlib
import json
import sys
import urllib.parse
import urllib.request
import zipfile

API = "https://api.modrinth.com/v2"
UA = "wtfangler/streamline-master (ci comparison)"
RANK = {"release": 3, "beta": 2, "alpha": 1}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
        return r.read()


def main():
    slug, mc, out = sys.argv[1:4]
    q = urllib.parse.urlencode({"game_versions": json.dumps([mc]), "loaders": json.dumps(["fabric"])})
    versions = json.loads(get("%s/project/%s/version?%s" % (API, slug, q)))
    if not versions:
        sys.exit("%s has no Fabric build for %s" % (slug, mc))
    versions.sort(key=lambda v: (RANK.get(v["version_type"], 0), v["date_published"]), reverse=True)
    v = versions[0]
    f = next((x for x in v["files"] if x["primary"]), v["files"][0])
    data = get(f["url"])
    if hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
        sys.exit("sha512 mismatch for %s" % f["url"])
    with open(out, "wb") as fh:
        fh.write(data)
    with zipfile.ZipFile(out) as z:
        idx = json.loads(z.read("modrinth.index.json"))
    print("%s %s (%s, %s), %d files" % (slug, v["version_number"], v["version_type"], v["date_published"][:10], len(idx["files"])))
    print(idx["dependencies"]["fabric-loader"])


if __name__ == "__main__":
    main()
