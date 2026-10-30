# Release history

Every release is on [Modrinth](https://modrinth.com/modpack/slm/versions). Each one
targets a single Minecraft version; the pack number and the game version move
independently, which is why 1.3.1, 1.4.1 and 1.5.1 are the *same* generation of the
pack for three different games.

**What this repository can rebuild.** The manifest and lockfiles here cover
Minecraft **26.3, 26.2, 26.1.2 and 1.21.11** only. Releases up to and including 1.2 were
assembled before this build system existed and cannot be reproduced from this
repository — they remain downloadable on Modrinth, unchanged.

---

## 1.6.3 — unreleased

Minecraft 26.3. Picks up the upstream fixes released since 1.6.2 that matter for frame
rate and memory, and brings Particle Core back. Every other file is the same as in 1.6.2,
and the other targets are unchanged.

- **Particle Core is back on 26.3** (0.3.3+fix1). It was left out of 1.6.1 and 1.6.2
  only because there was no 26.3 build; the one published on 2026-10-10 lists 26.3 and
  its requirements (Fabric Loader ≥0.19.2, Fabric Language Kotlin ≥1.13.9, Fzzy Config
  ≥0.7.6) are all met by the pack. It is the same mod the 26.2 pack ships, and it covers
  the particle side that Smart Particles covered in 1.6.1.
- **Entity Culling 1.11.2 → 1.11.3.** Fixes frustum culling ignoring its whitelist and
  using the uninflated hitbox, which caused entities to pop in and out when turning
  the camera, and fixes a leak where leaving a world could keep the whole level in
  memory (upstream traced it to Fabric API together with tr7zw's TRansition library).
- **Lithium 0.26.2 → 0.26.3.** Fixes a player memory leak through maps in item frames
  (and stops sending map data packets that are not needed), plus two correctness fixes.
  Same Fabric Loader requirement (≥0.19.5).
- **Smooth Scrolling 3.0.0 → 3.0.2.** Bug fixes only: chat position at non-100% chat
  scale, and bundle scrolling moving the creative screen.
- **New tools: `tune.py` / `tune.cmd` and `bench.py`.** The pack cannot carry JVM
  arguments, heap size or the GPU choice, and on a weak laptop those matter more than
  any mod. `tune` writes them into a Prism instance (heap from the machine's RAM, the
  G1 arguments from `docs/tuning.md`, and on Windows the high-performance GPU for the
  instance's Java; a backup of `instance.cfg` first). `bench` turns PresentMon or
  CapFrameX captures into avg FPS, 1% / 0.1% lows and stutters per minute, and says
  whether a difference against another pack clears the noise thresholds in
  `docs/benchmark.md`. Neither changes the `.mrpack`.
- **Held back on purpose:**
  - Sodium 0.9.3-beta.1 and everything that follows it (Better Block Entities 1.4.0
    requires that exact build, and Reese's Sodium Options 2.2.5 requires exactly
    0.9.2). This is the chain that kept 1.6.0 from starting.
  - Sodium Extra 0.9.5 requires Fabric Loader 0.20.1; the pack is on 0.19.5, and
    the release has no changelog to weigh against a loader bump.
  - Zoomify 2.17.0 adds a new required library, Almanac/Let Me Despawn 1.26.10.2
    move to a new config system, and Fabric API, Fabric Language Kotlin, Ixeris, Ksyxis,
    Async Logger, Fast Noise and Smooth Gui had updates with nothing for performance.
- **Not yet launched or measured.** The versions were checked against the
  requirements in each mod's source, not by starting the game. Before release:
  import into Prism, load a world, check the log, and repeat the 1.6.2 measurement
  (same scene, 40 samples after 100 s). Only a difference above ~10% counts.

---

## 1.6.2 — 2026-10-06

Minecraft 26.3. Fixes a startup crash and removes the mods that made the pack slower
than it should be.

- **Fixed: "Resource reload failed" crash on start.** ModernFix's
  `dynamic_entity_renderers` option (the pack turned it on) replaces the entity renderer
  map, and Entity View Distance's own mixin on `EntityRenderDispatcher` then hit a
  `ClassCastException`, leaving every entity without a renderer. The option is back at
  its default (off). 1.6.1 starts on some machines and not on others, so do not rely on
  it.
- **Removed on 26.3: C2ME, Very Many Players, ScalableLux, Gnetum and Smart Particles.**
  Measured on an Intel UHD 620 laptop (i5-8350U, 16 GB), same world and spot, 40
  frame-counter samples after a 100 s warm-up. The 1.6.2 build averaged about 135 FPS
  (lowest sample 116), the same as a plain Fabulously-Optimized-style control with default
  configs. 1.6.1 with the crash fixed, i.e. with all five still in, averaged about 121
  and dipped to 92, in two separate runs. The remaining 1.6.1 additions (Entity View
  Distance, Ksyxis, Alternate Current, Fast Noise, Clumps, AudioThrottle, Raise Sound
  Limit Simplified, Async Logger, Force Close World Loading Screen, Quick Pack) cost
  nothing measurable and stay. Other targets are unchanged.
- **Lithium experimental mixins are off on 26.3** (they were on for every target). They did
  not change the measured frame rate; they are simply not worth the risk.
- **`options.txt` on 26.3:** `maxAnisotropyBit` is 1 (the old 0 is outside the game's 1–4
  range and logged a parse error on every start) and `exclusiveFullscreen` is off, which
  is the game's default and the setting every measurement above ran with. Exclusive
  fullscreen was not measured.
- **Honest limit of the measurements.** They are a stationary scene on one machine;
  frame rate varied by roughly ±10% between identical runs, so only differences larger
  than that mean anything. Stutter while exploring was not measured reliably.

**1.6.1 (26.3, beta) is superseded.** Use 1.6.2.

---

## 1.5.2 · 1.4.2 · 1.3.2 — 2026-10-06

Minecraft 26.2, 26.1.2 and 1.21.11. The same tuning as 1.6.2, carried back.

- **Removed: C2ME, Very Many Players and ScalableLux** (on 1.21.11 only the last two were
  present). On 26.3 the build without them was measurably smoother on a weak laptop. On 26.2 a
  controlled A/B (two pairs, order swapped) gave opposite results, so there is no frame-rate
  claim for the older games. They go for consistency and because C2ME and VMP are still
  prerelease upstream.
- **One performance counter, not two.** These builds showed Sodium Extra's
  "FPS (avg / 1% low / 0.1% low)" and Chloride's "FPS | MIN | AVG" on top of each other.
  Chloride's overlay is now off; Sodium Extra's stays.
- **ModernFix `dynamic_entity_renderers` is back at its default (off)**, and Lithium's
  experimental mixins are off.
- **`options.txt`:** `maxAnisotropyBit` is 1 (the old 0 is outside the game's 1–4 range and
  logged an error on every start); on 26.2 and 26.1.2 `exclusiveFullscreen` is off.
- Each pack was imported into Prism and started, a world was loaded, and the log showed no
  errors.

---

## 1.6.1 — 2026-10-05

Minecraft 26.3. First working release for that game version.

- **Excluded: Chloride and Particle Core.** Neither has a 26.3 build; they return
  when one is published. Smart Particles covers the particle side in the meantime.
- **New on 26.3:** Gnetum, Smart Particles, Entity View Distance, Ksyxis, Alternate
  Current, Fast Noise, Clumps, AudioThrottle, Raise Sound Limit Simplified, Async
  Logger, Force Close World Loading Screen and Quick Pack, plus the libraries Text
  Placeholder API (required by Mod Menu 21) and ZConfig (required by Fast Noise).
- **Sodium is 0.9.2, not 0.9.3-alpha.** Reese's Sodium Options 2.2.5 requires exactly
  0.9.2+mc26.3, so the alpha makes Fabric Loader stop with "Incompatible mods found".
- **Cull Fewer Leaves is not included.** It was evaluated and rejected: More Culling
  declares it as a hard conflict (`breaks`), which the Modrinth API does not expose
  and which only shows up when the game starts.
- Still prerelease upstream, so the least settled part of the pack: C2ME, VMP,
  ScalableLux, Remove Reloading Screen and Smooth Swapping.

**1.6.0 (26.3, alpha) is superseded and should not be used.** It shipped Sodium
0.9.3-alpha.1 against Reese's Sodium Options 2.2.5 and omitted Text Placeholder API,
so it did not start. Both are fixed in 1.6.1.

---

## 1.5.1 · 1.4.1 · 1.3.1 — 2026-08-29

Latest for Minecraft 26.2, 26.1.2 and 1.21.11.

- **1.3.1 fixes a launch failure on 1.21.11.** Fabric Loader refused to start with
  "Incompatible mods found". Three mods had to go on that game version, and only
  that one:
  - **Iris** — Sodium 0.8.13+ declares `breaks: iris <=1.10.7`, and 1.10.7 is the
    newest Iris built for 1.21.11. Pinning Sodium back was not viable: Sodium Extra
    0.9.3 and Chloride 1.8.1 both require 0.8.13+.
  - **C2ME** — the `c2me-opts-natives-math` module requires Java 22 or newer, and
    1.21.11 runs on Java 21.
  - **Remove Reloading Screen** — its only Fabric builds for 1.21.11 hard-require
    Forge Config API Port, which the pack does not ship.
- All three still ship on 26.2 and 26.1.2, where the conflicts do not arise.
- The pack version now shows per game version in the corner of the main menu
  (1.5.1 / 1.4.1 / 1.3.1) instead of a single shared number.

## 1.5 · 1.4 · 1.3 — 2026-08-28

Superseded by the releases above, and marked beta on Modrinth. This generation was
the rewrite that introduced the manifest-driven build:

- `options.txt` became pack defaults rather than a personal configuration dump.
  Earlier releases shipped keybindings, volumes, mouse sensitivity and language,
  which overwrote the player's own settings on every update.
- Graphics defaults rebalanced for integrated graphics: leaves render as cutout
  again, render distance and mipmaps moved to where they pay for themselves.
- Sodium's entity culling switched on. It had been off in every 1.x build.
- Thirteen mods added, mostly culling and rendering; two removed for doing nothing
  measurable.
- Pack name and version shown in the main menu and pause screen.

Notes on this generation are in [`docs/comparison.md`](docs/comparison.md) and
[`docs/audit.md`](docs/audit.md) (Polish).

## 1.2 and earlier

Predate this repository. Listed for completeness; still available on Modrinth.

| Pack | Minecraft | Released | Type |
| ---- | --------- | -------- | ---- |
| 1.2 | 1.21.8 | 2025-09-07 | release |
| 1.1 | 1.21.7 | 2025-09-07 | release |
| 1.0.9 | 1.21.6 | 2025-09-07 | release |
| 1.0.8 | 1.21.4 | 2025-09-07 | release |
| 1.0.7 | 1.21.1 | 2025-09-07 | release |
| 1.0.6 | 1.21 | 2025-09-07 | release |
| 1.0.5 | 1.20.6 | 2024-05-15 | release |
| 1.0.4 | 1.20.5 | 2024-05-15 | release |
| 1.0.3.2 | 1.20.4 | 2024-04-23 | release |
| 1.0.3.1 | 1.20.4 | 2024-04-03 | release |
| 1.0.3 | 1.20.4 | 2024-04-02 | beta |
| 1.0.2 | 1.20.2 | 2024-04-02 | beta |
| 1.0.1 | 1.19.4 | 2024-04-02 | beta |
| 1.0.0 | 1.18.2 | 2024-04-02 | beta |

First release 2024-04-02, on Minecraft 1.18.2.
