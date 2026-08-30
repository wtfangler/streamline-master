# Streamline Master

A performance-first Fabric modpack for Minecraft, built from a single manifest
for three game versions. No new blocks, no new mobs, no quests — every mod in
the pack exists to give back frames, memory or load time.

[![build](https://github.com/wtfangler/streamline-master/actions/workflows/build.yml/badge.svg)](https://github.com/wtfangler/streamline-master/actions/workflows/build.yml)
[![licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)
[![Modrinth](https://img.shields.io/badge/Modrinth-slm-1bd96a.svg)](https://modrinth.com/modpack/slm)

Tuned on a low-end machine on purpose: an HP EliteBook x360 with an i5-8350U and
integrated graphics. It runs well above that, but the defaults are chosen for
hardware that has no headroom to waste.

## Download

Install through the [Modrinth App](https://modrinth.com/app) or Prism Launcher
and you get update notifications and a clean instance. Direct `.mrpack` files
live on the [project page](https://modrinth.com/modpack/slm).

These are the targets this repository builds:

| Minecraft | Pack | Files |
| --------- | ---- | ----- |
| 26.2      | 1.5.1 | 44 |
| 26.1.2    | 1.4.1 | 45 |
| 1.21.11   | 1.3.1 | 43 |

The project goes back further than that. Twenty versions are published, reaching
Minecraft 1.18.2 in April 2024 — see [`CHANGELOG.md`](CHANGELOG.md) for the full
list. Releases up to 1.2 predate this build system and cannot be rebuilt from
here; they stay on Modrinth as they were published.

Requires **Java 21 or newer** (Minecraft 1.20.5+). 3–4 GB of allocated RAM is
plenty; the pack is tuned to need less, not more. Install as a **new instance** —
most launchers skip existing config files when updating in place, which silently
discards the pack's tuning.

## What makes this different

Most modpacks are a folder of jars someone assembled by hand. This one is a
build system, and that has consequences you can check rather than take on trust.

**Reproducible.** `python build.py --offline` rebuilds every pack from the
committed lockfiles with no network access and produces **byte-identical**
files — on any operating system. [`SHA256SUMS`](SHA256SUMS) holds the hash of
each pack as this repository builds it, and CI verifies the Linux build against
those hashes (committed from Windows) on every push, so the claim has a guard
that can actually fail rather than being asserted in a readme.

```bash
python build.py --offline --out dist
cd dist && sha256sum --check ../SHA256SUMS
```

These hashes describe what the build system produces. A release published from
this repository can be checked against them; a `.mrpack` exported by hand from a
launcher cannot, because it carries whatever else was sitting in that instance's
config folder.

**Auditable.** [`lock/`](lock) pins the exact version, file size and SHA-512 of
every single file in a release. You can see precisely what a pack contains, and
verify a downloaded `.mrpack` against it, without installing anything.

**Validated.** [`validate.py`](validate.py) checks index structure, hash format,
duplicate paths, paths escaping their allowed roots, download hosts, `env`
flags, collisions between `overrides/` and indexed files, machine-specific files
that must never ship (`sodium-fingerprint.json`), and config files shipped
without the mod they belong to. With `--online` it also asks Modrinth whether
every pinned file still exists and still supports its target game version.

## Build it yourself

Python 3.9+, no third-party dependencies.

```bash
python build.py            # resolve against Modrinth, write lock/ and dist/
python build.py --offline  # rebuild from lockfiles, no network, reproducible
python build.py --survey   # table of which mod resolves to what on each version
python validate.py "dist/*.mrpack" --online
```

On Windows, double-clicking `build.cmd` does the build and validation in one
step. `doctor.cmd` compares an installed instance against a pack and reports
which files the launcher failed to write.

## Layout

```
manifest.json          mod list, targets, pack metadata — the single source of truth
build.py               Modrinth version resolver + .mrpack generator
validate.py            structural and online validation of built packs
doctor.py              compares an installed instance against a pack
overrides/             configs shared by every game version
overrides-<mc>/        version-specific configs, layered over the above
lock/<mc>.json         resolved versions and hashes (committed on purpose)
site/                  the landing page
docs/                  audit, comparison, benchmark protocol, tuning notes
```

## How versions work

Each target in `manifest.json` carries its own `packVersion`, which becomes both
the `.mrpack` version id and the label shown in the corner of the main menu, so
the number is never written out by hand.

Some mods are excluded on specific versions via `skipTargets`, because the only
build available there cannot be reconciled with the rest of the set. Currently,
on Minecraft 1.21.11:

- **Iris** — Sodium 0.8.13+ declares `breaks: iris <=1.10.7`, and 1.10.7 is the
  newest Iris for that game version. Holding Sodium back was not an option:
  Sodium Extra and Chloride both require 0.8.13+.
- **C2ME** — its `c2me-opts-natives-math` module requires Java 22+, but the
  runtime for 1.21.11 is Java 21.
- **Remove Reloading Screen** — its only Fabric builds for 1.21.11 hard-require
  Forge Config API Port.

All three ship normally on 26.x. `build.py` resolves each target independently
and does no cross-mod compatibility checking, so conflicts like these are found
by launching the game, not by the build.

## Documentation

[`CHANGELOG.md`](CHANGELOG.md) covers the release history, including what the
1.5.1 / 1.4.1 / 1.3.1 generation fixed and which mods are excluded where.

The notes in [`docs/`](docs) are written in Polish:

- [`audit.md`](docs/audit.md) — audit of the 1.3 / 1.4 / 1.5 releases
- [`comparison.md`](docs/comparison.md) — what changed, and how it compares to Fabulously Optimized
- [`benchmark.md`](docs/benchmark.md) — the measurement protocol
- [`tuning.md`](docs/tuning.md) — why each default is what it is
- [`modrinth-description.md`](docs/modrinth-description.md) — the project page copy (English)

## Contributing

Issues and pull requests are welcome. Useful bug reports include the game
version, the pack version from the corner of the main menu, and the launcher
log. If a mod is misbehaving, `doctor.py` output helps rule out a launcher that
failed to apply the pack's config.

Adding a mod is one entry in `manifest.json` with a `slug`, `group` and `env`.
Please make the case for it in terms of what it gives back — this pack does not
add features.

## Licence

[MIT](LICENSE), covering the build tooling, the manifest, the configs and the
website.

This repository ships no mod binaries. A built `.mrpack` contains only
references to files hosted on Modrinth's CDN, and every mod remains the property
of its own author under its own licence. Not affiliated with Mojang or
Microsoft.
