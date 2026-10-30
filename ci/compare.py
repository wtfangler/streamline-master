"""Compares harness metrics of two packs over several alternating runs.

    python ci/compare.py --a "SLM" runs/slm-* --b "FO" runs/fo-* --out compare.md

Each argument after --a/--b is a results folder holding metrics.json from
ci/run_client.py. Per metric it reports the median of each side and the
difference, and calls a difference real only when it is larger than the spread
of either side's runs (max - min): CI runners are shared machines and their
timing noise is the thing to beat. Lower is better for every metric here.
"""
import argparse
import json
import os
import statistics

LABELS = {
    "startup_s": "start to main menu (s)",
    "world_ready_s": "start to playable world (s)",
    "heap_after_gc_mb": "heap after GC in world (MB)",
}


def load(dirs):
    runs = []
    for d in dirs:
        p = os.path.join(d, "metrics.json")
        if os.path.isfile(p):
            m = json.load(open(p))
            if m.get("passed"):
                runs.append(m)
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", nargs="+", required=True, help="label then result folders")
    ap.add_argument("--b", nargs="+", required=True, help="label then result folders")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    (la, *da), (lb, *db) = args.a, args.b
    ra, rb = load(da), load(db)
    lines = ["# %s vs %s" % (la, lb), ""]
    if ra:
        lines.append("%s: `%s`, %d passing run(s)" % (la, ra[0]["pack"], len(ra)))
    if rb:
        lines.append("%s: `%s`, %d passing run(s)" % (lb, rb[0]["pack"], len(rb)))
    lines += [
        "",
        "Same runner, same world, same JVM arguments, runs alternated. Software rendering:",
        "these are CPU-side costs (loading, world join, memory), not frame rate.",
        "",
        "| metric | %s | %s | diff | verdict |" % (la, lb),
        "| --- | --- | --- | --- | --- |",
    ]
    if not ra or not rb:
        lines.append("| — | %d runs | %d runs | | not enough passing runs to compare |" % (len(ra), len(rb)))
    else:
        for key, label in LABELS.items():
            va = [r["metrics"][key] for r in ra if key in r["metrics"]]
            vb = [r["metrics"][key] for r in rb if key in r["metrics"]]
            if not va or not vb:
                # Say so rather than drop the row: a missing metric is a finding too (for
                # start-up it means the harness never saw the loading overlay in that pack).
                lines.append("| %s | %s | %s | | not measured |" % (
                    label, "%d/%d runs" % (len(va), len(ra)), "%d/%d runs" % (len(vb), len(rb))))
                continue
            ma, mb = statistics.median(va), statistics.median(vb)
            diff = 100.0 * (ma - mb) / mb if mb else 0.0
            noise = max(max(va) - min(va), max(vb) - min(vb))
            if abs(ma - mb) <= noise:
                verdict = "tie (within run-to-run spread %.2f)" % noise
            else:
                verdict = "%s lower" % (la if ma < mb else lb)
            lines.append("| %s | %.2f | %.2f | %+.1f%% | %s |" % (label, ma, mb, diff, verdict))
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
