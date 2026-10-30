"""Frame-time statistics from PresentMon or CapFrameX captures.

docs/benchmark.md says what to measure; this computes it the same way every
time, so a claim against Fabulously Optimized is a number with a threshold
rather than an impression.

    python bench.py run2.csv run3.csv
    python bench.py slm-2.csv slm-3.csv --vs fo-2.csv fo-3.csv

Each side is the median of its runs, per metric. Definitions:

* avg FPS   - frames divided by captured time (time-weighted, not a mean of
              per-frame FPS, which overstates fast frames)
* 1% low    - 1000 / mean of the slowest 1% of frame times
* 0.1% low  - the same over the slowest 0.1%
* stutters  - frames longer than 2.5x the median frame time, per minute

Different tools define "1% low" differently; compare only captures made with
the same tool.
"""
import argparse
import csv
import statistics
import sys

FRAME_TIME_COLUMNS = ("msbetweenpresents", "frametime", "msbetweendisplaychange")
JAVA_APPS = ("javaw.exe", "java.exe", "java")
# docs/benchmark.md: below these, the difference is measurement noise on a 15 W laptop.
AVG_THRESHOLD = 10.0
LOW_THRESHOLD = 15.0
STUTTER_FACTOR = 2.5


def read_frame_times(path, app=None):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].startswith("//")]
    if not rows:
        raise ValueError("%s: empty" % path)
    header = [h.strip().lower() for h in rows[0]]
    col = next((header.index(c) for c in FRAME_TIME_COLUMNS if c in header), None)
    if col is None:
        raise ValueError("%s: no frame-time column (looked for %s)" % (path, ", ".join(FRAME_TIME_COLUMNS)))
    app_col = header.index("application") if "application" in header else None

    data = rows[1:]
    if app_col is not None:
        apps = {r[app_col].strip().lower() for r in data if len(r) > app_col}
        want = app.lower() if app else next((a for a in JAVA_APPS if a in apps), None)
        if want:
            data = [r for r in data if len(r) > app_col and r[app_col].strip().lower() == want]
        elif len(apps) > 1:
            raise ValueError("%s: several applications captured (%s), pick one with --app"
                             % (path, ", ".join(sorted(apps))))

    times = []
    for r in data:
        try:
            t = float(r[col])
        except (IndexError, ValueError):
            continue
        if t > 0:
            times.append(t)
    if len(times) < 100:
        raise ValueError("%s: only %d frames, capture at least 60 s" % (path, len(times)))
    return times


def slowest_mean(times, fraction):
    worst = sorted(times, reverse=True)
    n = max(1, int(len(worst) * fraction))
    return statistics.fmean(worst[:n])


def metrics(times):
    total_ms = sum(times)
    med = statistics.median(times)
    stutters = sum(1 for t in times if t > STUTTER_FACTOR * med)
    return {
        "frames": len(times),
        "seconds": total_ms / 1000.0,
        "avg": 1000.0 * len(times) / total_ms,
        "low1": 1000.0 / slowest_mean(times, 0.01),
        "low01": 1000.0 / slowest_mean(times, 0.001),
        "stutter_min": stutters / (total_ms / 60000.0),
    }


def combine(runs):
    return {k: statistics.median(r[k] for r in runs) for k in runs[0]}


def load(paths, app):
    runs = []
    for p in paths:
        m = metrics(read_frame_times(p, app))
        runs.append(m)
        print("  %-34s %6d frames %6.1f s   avg %6.1f   1%% low %6.1f   0.1%% low %6.1f   stutter/min %5.1f"
              % (p[-34:], m["frames"], m["seconds"], m["avg"], m["low1"], m["low01"], m["stutter_min"]))
    return combine(runs)


def pct(new, base):
    return 100.0 * (new - base) / base if base else 0.0


def main():
    ap = argparse.ArgumentParser(description="avg FPS, 1%/0.1% lows and stutter from PresentMon/CapFrameX CSV")
    ap.add_argument("runs", nargs="+", help="captures of the build under test")
    ap.add_argument("--vs", nargs="+", default=[], help="captures of the baseline (e.g. Fabulously Optimized)")
    ap.add_argument("--app", help="process name to keep when a capture holds several (default: java/javaw)")
    args = ap.parse_args()

    try:
        print("test runs")
        a = load(args.runs, args.app)
        if not args.vs:
            return 0
        print("baseline runs")
        b = load(args.vs, args.app)
    except (OSError, ValueError) as e:
        print("error: %s" % e)
        return 2

    print("")
    print("median of runs        test   baseline    diff")
    rows = (("avg FPS", "avg", AVG_THRESHOLD),
            ("1% low", "low1", LOW_THRESHOLD),
            ("0.1% low", "low01", None),
            ("stutter/min", "stutter_min", None))
    for label, key, _ in rows:
        print("  %-14s %9.1f %9.1f %+7.1f%%" % (label, a[key], b[key], pct(a[key], b[key])))

    print("")
    wins = [label for label, key, limit in rows if limit and pct(a[key], b[key]) >= limit]
    losses = [label for label, key, limit in rows if limit and pct(a[key], b[key]) <= -limit]
    if wins and not losses:
        print("verdict: test build is ahead on %s (above the noise threshold)" % ", ".join(wins))
    elif losses and not wins:
        print("verdict: baseline is ahead on %s (above the noise threshold)" % ", ".join(losses))
    elif wins and losses:
        print("verdict: mixed - ahead on %s, behind on %s" % (", ".join(wins), ", ".join(losses)))
    else:
        print("verdict: tie - differences are within noise (avg < %.0f%%, 1%% low < %.0f%%)"
              % (AVG_THRESHOLD, LOW_THRESHOLD))
    return 0


if __name__ == "__main__":
    sys.exit(main())
