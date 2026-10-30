# Streamline Master

A performance-first Fabric modpack. No new blocks, no new mobs, no quests — every mod in
this pack exists to give back frames, memory or load time.

Built for low-end laptops and integrated graphics, and tuned on one: a 4-core 15 W CPU
with Intel UHD 620 graphics.

## What makes it different

- **Every pack is started before it ships.** An automated job installs each pack exactly
  as a launcher does, starts the real game, generates a world, joins it and quits — for
  all four game versions — and starts a server built from the same pack.
- **Reproducible and auditable.** Each release is rebuilt byte for byte from lockfiles
  that pin the version and hash of every file. The source and the checksums are on
  [GitHub](https://github.com/wtfangler/streamline-master).
- **Measured, not claimed.** On Minecraft 26.3, started side by side with Fabulously
  Optimized on the same machine, the pack reaches the main menu 24% sooner, a playable
  world 18% sooner and keeps 15% less memory (loading and memory only; frame rate needs
  your hardware). Changes that cost frames have been taken out again: 1.6.2 removed five
  mods that made 26.3 about 10% slower on a UHD 620 laptop. The repository
  ships a benchmark you can run in this pack and in any other, on your own hardware.
- **Its own loading screen on 26.3**, drawn only while the game loads, so it costs
  nothing in play.

## Core rendering

Sodium · Sodium Extra · Reese's Sodium Options · Iris (26.x) · ImmediatelyFast ·
Better Block Entities · Sodium Shadowy Path Blocks · Continuity · Chloride (26.2 and older) ·
Exordium (26.1.2, 1.21.11)

## Culling

Entity Culling · More Culling · Particle Core · Entity View Distance (26.3)

## Engine, memory and world

Lithium · FerriteCore · ModernFix · BadOptimizations · Let Me Despawn ·
Alternate Current · Fast Noise · Clumps · Ksyxis (all four 26.3) · ThreadTweak (1.21.11)

## Network

Krypton · Packet Fixer · Fast IP Ping

## Client behaviour

Dynamic FPS · Ixeris · FastQuit · Remove Reloading Screen (26.2, 26.1.2) · Debugify ·
Language Reload · Zoomify · Mod Menu · Main Menu Credits · AudioThrottle ·
Raise Sound Limit Simplified · Async Logger · Force Close World Loading Screen ·
Quick Pack (the last five on 26.3)

Smooth Gui, Smooth Scrolling and Smooth Swapping animate menus only and cost nothing
in the world.

## Requirements

- Fabric Loader (the launcher installs it)
- **Java 25** for Minecraft 26.x, **Java 21** for 1.21.11 — the Modrinth App and Prism
  pick the right one by themselves
- 3 GB of allocated RAM is enough; 4 GB is the sensible maximum on a laptop

Install as a **new instance**. Most launchers skip existing config files when updating
in place, which silently discards the pack's tuning.

Iris is included on the 26.x builds, but no shader pack ships with the pack. Drop one
into `shaderpacks` if you want shaders — and expect integrated graphics to struggle with
any of them. The 1.21.11 build has no Iris: the current Sodium there is incompatible with
the newest Iris for that version.

## Settings

The pack ships an `options.txt` with graphics settings chosen for this hardware:
render distance 8, simulation distance 5, fast clouds, fewer particles. Installing an
update overwrites it — back it up first if you have tuned your own.

The JVM arguments and the GPU choice cannot ship inside a modpack. The repository's
`tune.py` sets them in a Prism instance (heap sized to your RAM, G1 garbage-collector
settings, and on Windows the high-performance GPU for the game). For hardware weaker
than a UHD 620, `tune.py --preset potato` lowers the graphics settings further.

On 26.2 and older, two Chloride options are worth turning on by hand in Video Settings:
**Entity Distance Culling** and **Text Shadows**. Leave Chloride's own Fast Models and
Leaves Culling off — Better Block Entities and More Culling already cover those.

## Versions

Separate builds for Minecraft 26.3, 26.2, 26.1.2 and 1.21.11. Each build resolves its own
mod versions, so nothing is shimmed across game versions. Where a mod cannot be
reconciled with a game version it is left out of that build only:

- **26.3:** no Chloride (no build for 26.3 yet) and no Remove Reloading Screen (it would
  hide the pack's own start-up screen, and its 26.3 build is an alpha).
- **1.21.11:** no Iris (Sodium/Iris version clash) and no Remove Reloading Screen (its
  only 1.21.11 build hard-requires Forge Config API Port).

Running a server for friends? The repository's server builder turns any of these packs
into a Fabric server folder with only the server-side mods.
