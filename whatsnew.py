"""Report which Minecraft versions are newer than the pack's targets, and how
close the mod set is to being buildable on each.

A new Minecraft version is not the signal to act. The signal is the mod
ecosystem catching up: without Sodium there is no performance pack, and
without Fabric API most of the rest will not load. This asks Mojang what
exists, Fabric whether the loader runs on it, and Modrinth how many of the
mods in manifest.json have builds for it.

    python whatsnew.py               releases and snapshots newer than the targets
    python whatsnew.py --releases    skip snapshots
    python whatsnew.py --json        machine-readable, for CI

Three HTTP requests total, regardless of how many mods are in the manifest.

Caveat: readiness is an estimate. A Modrinth project's game_versions list
aggregates every file it has, including other loaders, so a mod can be
counted here and still not resolve for Fabric. Before committing to a new
target, confirm with `python build.py --survey`, which resolves per loader
and per version properly.
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

MOJANG = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
FABRIC_GAME = "https://meta.fabricmc.net/v2/versions/game"
MODRINTH = "https://api.modrinth.com/v2/projects"
UA = "streamline-master/2.0 (version watch)"

# Without these the pack has no reason to exist, so they are reported
# separately rather than being lost in a percentage.
KEYSTONES = ("sodium", "fabric-api", "lithium")


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def load_manifest():
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def candidates(manifest, mojang, include_snapshots):
    """Versions released after the newest one the pack already targets."""
    times = {v["id"]: v["releaseTime"] for v in mojang["versions"]}
    targets = [t["minecraft"] for t in manifest["targets"]]
    known = [times[t] for t in targets if t in times]
    if not known:
        return []
    newest = max(known)

    out = []
    for v in mojang["versions"]:
        if v["releaseTime"] <= newest or v["id"] in targets:
            continue
        if v["type"] != "release" and not include_snapshots:
            continue
        out.append(v)
    out.sort(key=lambda v: v["releaseTime"], reverse=True)
    return out


def mod_support(manifest):
    """slug -> set of game versions, in one bulk request."""
    slugs = [m["slug"] for m in manifest["mods"]]
    q = urllib.parse.urlencode({"ids": json.dumps(slugs)})
    data = http_json("%s?%s" % (MODRINTH, q))
    return {p["slug"]: set(p.get("game_versions") or []) for p in data}


def assess(manifest, mc, support):
    total = ready = 0
    missing_key = []
    for mod in manifest["mods"]:
        if mc in mod.get("skipTargets", []):
            continue
        total += 1
        if mc in support.get(mod["slug"], ()):
            ready += 1
        elif mod["slug"] in KEYSTONES:
            missing_key.append(mod["slug"])
    pct = round(100 * ready / total) if total else 0
    return {"ready": ready, "total": total, "percent": pct, "missingKeystones": missing_key}


def verdict(row):
    if row["missingKeystones"]:
        return "wait - no " + ", ".join(row["missingKeystones"])
    if row["percent"] >= 90:
        return "READY - add a target"
    if row["percent"] >= 60:
        return "close - check --survey"
    return "wait - ecosystem behind"


def issue_body(row):
    return """Minecraft **{mc}** ({type}, released {released}) looks buildable.

- Fabric Loader support: {fabric}
- Mods resolving: **{ready}/{total} ({percent}%)**

Readiness above is estimated from each project's advertised game versions, which
aggregate every loader. Confirm properly before committing to it:

```
python build.py --survey
```

Then add the target to `manifest.json` with its own `packVersion`, add
`overrides-{mc}/options.txt.tmpl` carrying the `version:` number from a clean
instance of that game version, build, and launch it once. `build.py` resolves
each mod independently and does not check mods against each other, so version
conflicts only show up at startup.

Opened automatically by `.github/workflows/watch.yml`.
""".format(
        mc=row["minecraft"],
        type=row["type"],
        released=row["released"],
        fabric="yes" if row["fabricLoader"] else "no",
        ready=row["ready"],
        total=row["total"],
        percent=row["percent"],
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--releases", action="store_true", help="ignore snapshots")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--limit", type=int, default=12, help="how many versions to report (default 12)")
    ap.add_argument(
        "--ready-only",
        action="store_true",
        help="print just the version ids worth acting on, one per line",
    )
    ap.add_argument("--issue-body", metavar="MC", help="print the issue text for one version")
    args = ap.parse_args()

    manifest = load_manifest()
    mojang = http_json(MOJANG)
    fabric = {f["version"] for f in http_json(FABRIC_GAME)}

    found = candidates(manifest, mojang, include_snapshots=not args.releases)[: args.limit]

    if not found:
        if args.json:
            print(json.dumps({"newer": []}))
        elif not (args.ready_only or args.issue_body):
            print(
                "Nothing newer than the current targets: %s"
                % ", ".join(t["minecraft"] for t in manifest["targets"])
            )
        return 0

    support = mod_support(manifest)

    rows = []
    for v in found:
        row = assess(manifest, v["id"], support)
        row.update(
            {
                "minecraft": v["id"],
                "type": v["type"],
                "released": v["releaseTime"][:10],
                "fabricLoader": v["id"] in fabric,
            }
        )
        row["verdict"] = "wait - no Fabric Loader" if not row["fabricLoader"] else verdict(row)
        rows.append(row)

    if args.issue_body:
        match = [r for r in rows if r["minecraft"] == args.issue_body]
        if not match:
            print("unknown version: %s" % args.issue_body, file=sys.stderr)
            return 1
        print(issue_body(match[0]), end="")
        return 0

    if args.ready_only:
        for r in rows:
            if r["verdict"].startswith("READY"):
                print(r["minecraft"])
        return 0

    if args.json:
        print(json.dumps({"targets": [t["minecraft"] for t in manifest["targets"]], "newer": rows}, indent=2))
        return 0

    print("Targets in manifest.json: %s" % ", ".join(t["minecraft"] for t in manifest["targets"]))
    print()
    print("%-18s %-9s %-11s %-7s %-9s %s" % ("minecraft", "type", "released", "fabric", "mods", "verdict"))
    print("-" * 92)
    for r in rows:
        print(
            "%-18s %-9s %-11s %-7s %-9s %s"
            % (
                r["minecraft"],
                r["type"],
                r["released"],
                "yes" if r["fabricLoader"] else "no",
                "%d/%d %d%%" % (r["ready"], r["total"], r["percent"]),
                r["verdict"],
            )
        )
    print()
    print("Readiness is an estimate from each project's advertised game versions.")
    print("Confirm a promising version with: python build.py --survey")
    return 0


if __name__ == "__main__":
    sys.exit(main())
