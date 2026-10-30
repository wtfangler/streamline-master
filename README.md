# Streamline Master

A performance-first Fabric modpack for Minecraft, built from a single manifest
for four game versions. No new blocks, no new mobs, no quests — every mod in
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
| 26.3      | 1.6.3 | 51 |
| 26.2      | 1.5.2 | 41 |
| 26.1.2    | 1.4.3 | 42 |
| 1.21.11   | 1.3.2 | 41 |

The project goes back further than that. Twenty-four versions are published, reaching
back to Minecraft 1.18.2 in April 2024 — see [`CHANGELOG.md`](CHANGELOG.md) for the full
list. Releases up to 1.2 predate this build system and cannot be rebuilt from
here; they stay on Modrinth as they were published.

Requires **Java 25** for Minecraft 26.x and **Java 21** for 1.21.11; the Modrinth
App and Prism pick the right one themselves. 3–4 GB of allocated RAM is plenty; the pack is tuned to need less, not more. Install as a **new instance** —
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

**Started, not just built.** The [`client`](.github/workflows/client.yml) workflow
installs each pack the way a launcher does (every mod downloaded from Modrinth
and checked against its SHA-512), generates a world with the vanilla server,
starts the real game under Xvfb, joins the world and quits — for all four game
versions. It then builds a server from the same pack and starts that too. Logs,
crash reports and screenshots land in [`ci-results/`](ci-results). A pack that
does not start fails the build, which is how 1.6.0 should have been caught.

**Measured against Fabulously Optimized.** The same workflow runs the newest
Fabulously Optimized for 26.3 next to this pack — three alternating runs each,
one world, identical JVM arguments — and compares time to the main menu, time to
a playable world and the heap kept after a full GC
([`ci-results/26.3/compare.md`](ci-results/26.3/compare.md)). It reports a
difference only when it is larger than the spread between runs. Latest result,
1.6.3 against Fabulously Optimized 15.0.0-beta.2: main menu 22.6 s vs 29.9 s,
playable world 36.8 s vs 44.7 s, 309 MB vs 364 MB kept after a full GC. The runner has
no GPU, so this covers loading and memory, never frame rate; frame rate needs
your hardware and [`bench.py`](bench.py).

## Own loading screen

On Minecraft 26.3 the pack ships one mod of its own, Streamline Loader
([`loader/`](loader)): the start-up and resource-reload screen, the world loading
screen and the "Saving world" screen get the pack's dark violet, its wordmark and
a thin progress line instead of the Mojang logo. It draws only while the game is
loading, so it costs nothing in play, and if anything about it fails the vanilla
screen stays. It is built with plain `javac` against the unobfuscated client
(no Gradle) into a reproducible jar, and needs no Fabric API.

## Build it yourself

Python 3.9+, no third-party dependencies.

```bash
python build.py            # resolve against Modrinth, write lock/ and dist/
python build.py --offline  # rebuild from lockfiles, no network, reproducible
python build.py --survey   # table of which mod resolves to what on each version
python validate.py "dist/*.mrpack" --online
python whatsnew.py         # newer Minecraft versions, and how ready the mods are
python tune.py <instance> --gpu      # JVM args, heap and GPU for a Prism instance
python tune.py <instance> --preset potato   # lower options.txt for weaker hardware
python bench.py a.csv --vs b.csv     # avg / 1% low / stutter from PresentMon captures
python server/build_server.py "dist/Streamline Master 26.3.mrpack" my_server --ram 4G
python bench_setup.py list                  # instances the benchmark can go into (or: bench.cmd)
python release.py 26.3 --channel beta       # dry run of a Modrinth release
```

`server/build_server.py` turns any of the packs into a Fabric server folder:
only the server-side mods (Lithium, FerriteCore, Krypton, Clumps, Alternate
Current, …), each checked against the pack's hash, the official Fabric server
launcher, and start scripts with the same G1 arguments as `tune.py`. It never
writes into a world. Accept the EULA in `eula.txt`, then run `start.bat` or
`start.sh`.

Releases go out through the [`release`](.github/workflows/release.yml) workflow
(Actions → release → Run workflow). It is a dry run unless "publish" is ticked,
needs the `MODRINTH_TOKEN` secret, and refuses a pack that does not match
`SHA256SUMS`, fails validation, has an undated CHANGELOG section, or is already
on Modrinth.

On Windows, double-clicking `build.cmd` does the build and validation in one
step. `doctor.cmd` compares an installed instance against a pack and reports
which files the launcher failed to write. `tune.cmd` applies the launcher-side
tuning a `.mrpack` cannot carry: heap size, G1 arguments and, on Windows, the
high-performance GPU for the instance's Java.

## Layout

```
manifest.json          mod list, targets, pack metadata — the single source of truth
build.py               Modrinth version resolver + .mrpack generator
validate.py            structural and online validation of built packs
doctor.py              compares an installed instance against a pack
tune.py                JVM arguments, heap, GPU preference and the potato preset
bench.py               frame-time statistics from PresentMon / CapFrameX captures
release.py             publishes one pack to Modrinth (used by the release workflow)
loader/                Streamline Loader, the pack's own loading-screen mod (26.3)
server/                server builder and its templates
ci/                    the client/server start test, harness mod and FO comparison
ci-results/<mc>/       what the last CI run saw: summary, logs, screenshots
overrides/             configs shared by every game version
overrides-<mc>/        version-specific configs, layered over the above
lock/<mc>.json         resolved versions and hashes (committed on purpose)
site/                  the landing page
docs/                  audit, comparison, benchmark protocol, tuning notes
```

## Adding a new Minecraft version

A Minecraft release is not the signal to act — the mod ecosystem catching up is.
Without Sodium there is no performance pack, and Fabric API gates most of the
rest. `whatsnew.py` measures that instead of guessing:

```
minecraft          type      released    fabric  mods      verdict
26.3-snapshot-10   snapshot  2026-08-25  yes     4/46 9%   wait - no sodium, lithium
```

It takes three HTTP requests: Mojang for what exists, Fabric for whether the
loader runs on it, Modrinth for how many of the manifest's mods have builds.
A scheduled workflow runs it weekly and opens an issue once a version reaches
90% coverage with Sodium, Lithium and Fabric API present — snapshots essentially
never do, which is the point.

When one does, confirm with `python build.py --survey` (the weekly figure is an
estimate; a project's advertised game versions aggregate every loader), then add
the target to `manifest.json` with its own `packVersion` and an
`overrides-<mc>/options.txt.tmpl`.

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
- **Remove Reloading Screen** — its only Fabric builds for 1.21.11 hard-require
  Forge Config API Port.

Both ship normally on 26.2 and 26.1.2. On Minecraft 26.3, **Chloride** is excluded:
it has no 26.3 build yet. **Remove Reloading Screen** is left out there too: its 26.3
build is an alpha, its settings cannot be changed without Forge Config API Port, and
it hides the start-up screen the pack's own loader draws on (Particle Core, excluded for the same reason in 1.6.1
and 1.6.2, is back in 1.6.3). The 26.3 pack also carries twelve mods the older
packs do not (HUD, particle, sound, redstone, world-generation and loading-time
optimisations plus their two libraries); they are `skipTargets`-ed everywhere
else, so adding them never changes an older pack.

C2ME, Very Many Players and ScalableLux are in the manifest but skipped on every
target since 1.6.2 / 1.5.2 / 1.4.2 / 1.3.2 (see the changelog for the
measurement); Gnetum and Smart Particles likewise. They stay listed so that
bringing one back is a one-line, reviewable change.

`build.py` resolves each target independently and does no cross-mod
compatibility checking, so conflicts like these are found by launching the game
— which the `client` workflow now does for every pack on every change.

## Documentation

[`CHANGELOG.md`](CHANGELOG.md) covers the full release history: what each release
fixed, what it measured, and which mods are excluded where.

The notes in [`docs/`](docs) are written in Polish:

- [`tuning.md`](docs/tuning.md) — why each default is what it is, JVM arguments, the potato preset
- [`benchmark.md`](docs/benchmark.md) — the measurement protocol and the benchmark mod
- [`audit.md`](docs/audit.md) — audit of the 1.3 / 1.4 / 1.5 generation (historical)
- [`comparison.md`](docs/comparison.md) — that generation against Fabulously Optimized (historical)
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

This repository ships no third-party mod binaries. A built `.mrpack` contains
references to files hosted on Modrinth's CDN, and every mod remains the property
of its own author under its own licence. The only jars in the repository are the
project's own: Streamline Loader (`overrides-26.3/mods/`, inside the 26.3 pack)
and the benchmark mod (`bench/jar/`, never inside a pack), both MIT and built by
CI from the sources next to them. The loader's wordmark uses Pixelify Sans under
the SIL Open Font License ([`loader/art/OFL.txt`](loader/art/OFL.txt)). Not
affiliated with Mojang or Microsoft.
