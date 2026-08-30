# Release history

Every release is on [Modrinth](https://modrinth.com/modpack/slm/versions). Each one
targets a single Minecraft version; the pack number and the game version move
independently, which is why 1.3.1, 1.4.1 and 1.5.1 are the *same* generation of the
pack for three different games.

**What this repository can rebuild.** The manifest and lockfiles here cover
Minecraft **26.2, 26.1.2 and 1.21.11** only. Releases up to and including 1.2 were
assembled before this build system existed and cannot be reproduced from this
repository — they remain downloadable on Modrinth, unchanged.

---

## 1.5.1 · 1.4.1 · 1.3.1 — 2026-08-29

Current. Minecraft 26.2, 26.1.2 and 1.21.11.

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
