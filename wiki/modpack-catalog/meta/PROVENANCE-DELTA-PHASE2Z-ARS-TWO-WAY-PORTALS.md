# Provenance Delta — Phase 2Z Ars Nouveau: Two-Way Portals 2.0.0

Status: `EXACT RELEASE METADATA + PUBLIC 1.3.4 SOURCE BASELINE / CLEAN-ROOM`

## Installed identity

Physical modlist authority:

- mod id: `ars_two_way_portals`;
- JAR: `ars_two_way_portals-2.0.0.jar`;
- version: `2.0.0`;
- SHA-1: `233846fc30667893c5f36a719da576d5eed43f5c`;
- CurseForge hash: `683033210`.

CurseForge file `8515817` independently identifies `ars_two_way_portals-2.0.0.jar` as a 1.21.1 NeoForge release uploaded 2026-07-26, size 65.8 KB. The project page lists LGPLv3 and Client & Server.

## Public source mismatch

The publisher's Source link resolves to:

`Astrologic-Git/ars-nouveau-two-way-portals`

Its visible release source is currently:

`f4b2e2e1fef99284968cfa99fc405ead7f56efbf` — commit message `Release source for v1.3.4`.

At that checkpoint `gradle.properties` declares Minecraft 1.20.1, Forge 47.4.0 and mod version 1.3.4. `mods.toml` requires Ars Nouveau `[4.12.7,5)` and optional Immersive Portals `[3.0.7,4)`. This cannot serve as an exact 2.0.0 NeoForge 1.21.1 source pin.

Phase 2Z therefore calls it a **public behavioral/source baseline**, never an exact installed-source checkpoint.

## License

The 1.3.4 baseline declares `LGPL-3.0-or-later`, and its root `LICENSE` contains GNU Lesser General Public License Version 3. CurseForge classifies the project LGPLv3. No contradictory audited license signal was found, but Black Arcana remains clean-room regardless.

## Clean-room posture

The baseline source is used read-only to identify factual architecture that helps deduplication and risk analysis:

- pair identity and transaction shape;
- bounded portal scans;
- portal cooldown intent;
- provider/Ars/Immersive authority separation;
- historical mixin targets;
- acquisition shape;
- endpoint lifecycle.

No upstream implementation, texture, model, translation or other asset is copied/adapted into Black Arcana.

## Fail-closed rule

Where the exact 2.0.0 publisher page and 1.3.4 source disagree — notably the 1.21.1 frame-replacement path — the old implementation is not treated as current. Exact 2.0.0 binary/source inspection is required before any code-level interoperability adapter can depend on those internals.
