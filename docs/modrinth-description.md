# Streamline Master

A performance-first Fabric modpack. No new blocks, no new mobs, no quests — every mod in
this pack exists to give back frames, memory or load time.

Built for low-end laptops and integrated graphics, and tuned on one: a 4-core 15 W CPU
with Intel UHD graphics.

## What 2.0 changes

- **Settings are pack defaults now, not someone's personal dump.** Earlier versions shipped
  a full `options.txt` including keybinds, volumes, mouse sensitivity and language, which
  overwrote yours on every update. 2.0 ships graphics and window settings only.
- **Graphics defaults rebalanced.** Leaves render as cutout again, render distance and
  mipmaps sit where they pay for themselves on integrated graphics.
- **Sodium's entity culling is on.** It was switched off in every 1.x build.
- **Thirteen mods added**, mostly culling and rendering; two removed for doing nothing
  measurable.
- Pack name and version now show in the bottom right of the main menu and pause screen.

## Core rendering

Sodium · Sodium Extra · Reese's Sodium Options · Chloride · Iris (26.x) · ImmediatelyFast ·
Better Block Entities · Sodium Shadowy Path Blocks · Continuity · Exordium (1.21.11)

## Culling

Entity Culling · More Culling · Particle Core

## Engine, memory and world

Lithium · FerriteCore · ModernFix · ScalableLux · BadOptimizations · C2ME (26.x) ·
Very Many Players · Let Me Despawn · ThreadTweak (1.21.11)

## Network

Krypton · Packet Fixer · Fast IP Ping

## Client behaviour

Dynamic FPS · Ixeris · FastQuit · Remove Reloading Screen (26.x) · Debugify · Language Reload ·
Zoomify · Mod Menu · Main Menu Credits

## Requirements

- Fabric Loader
- Java 21 or newer
- 3 GB of allocated RAM is enough; 4 GB is the sensible maximum on a laptop

Iris is included on the 26.x builds but no shader pack ships with the pack. Drop one into
`shaderpacks` if you want shaders — and expect integrated graphics to struggle with any of
them. The 1.21.11 build has no Iris: the current Sodium build there is incompatible with
the newest Iris release, and holding Sodium back would drag the rest of the render stack
with it.

## Settings

The pack ships an `options.txt` with graphics settings chosen for this hardware.
Installing an update overwrites it. Back it up first if you have tuned your own.

Two Chloride options are worth turning on by hand in Video Settings: **Entity Distance
Culling** and **Text Shadows**. Leave Chloride's own Fast Models and Leaves Culling off —
Better Block Entities and More Culling already cover those.

## Versions

Separate builds for 26.2, 26.1.2 and 1.21.11. Each build resolves its own mod versions,
so nothing is shimmed across game versions.

The 1.21.11 build drops three mods that cannot be reconciled on that game version:
**Iris** (Sodium/Iris version clash, see above), **C2ME** (its native-math module needs
Java 22+, but 1.21.11 runs on Java 21) and **Remove Reloading Screen** (its only 1.21.11
build hard-requires Forge Config API Port). Everything else is shared.
