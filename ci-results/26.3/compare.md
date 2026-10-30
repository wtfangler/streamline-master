# Streamline Master vs Fabulously Optimized

Streamline Master: `1.6.3+26.3`, 3 passing run(s)
Fabulously Optimized: `15.0.0-beta.2`, 3 passing run(s)

Same runner, same world, same JVM arguments, runs alternated. Software rendering:
these are CPU-side costs (loading, world join, memory), not frame rate.

| metric | Streamline Master | Fabulously Optimized | diff | verdict |
| --- | --- | --- | --- | --- |
| start to playable world (s) | 27.59 | 32.00 | -13.8% | tie (within run-to-run spread 5.35) |
| heap after GC in world (MB) | 320.26 | 372.91 | -14.1% | Streamline Master lower |

Fabulously Optimized build used: fabulously-optimized 15.0.0-beta.2 (beta, 2026-10-20), 48 files
