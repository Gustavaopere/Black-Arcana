# Ars Zero 2.0.2 — Evidence and Provenance Ledger

## Installed artifact authority

Latest physical modlist supplied 2026-09-08:

- filename: `ars_zero-1.21.1-2.0.2.jar`;
- mod id: `ars_zero`;
- mod name: `Ars Zero`;
- runtime version: `2.0.2`;
- SHA-1: `ac9b6e6f7a2bd403ee7cdc16023509fde7c4e1d0`;
- CurseForge hash field in the modlist: `3531379200`;
- environment modloader: NeoForge `21.1.248`.

This physical identity supersedes older project-guide snapshots for presence/version.

## Exact release evidence

Official CurseForge 1.21.1 release:

- project ID: `1377482`;
- file ID: `8703997`;
- filename: `ars_zero-1.21.1-2.0.2.jar`;
- release channel: Release;
- loader: NeoForge;
- game: 1.21.1;
- upload date: 2026-08-22;
- project license shown by CurseForge: GPLv3.

Links:

- https://www.curseforge.com/minecraft/mc-mods/ars-zero
- https://www.curseforge.com/minecraft/mc-mods/ars-zero/files/8703997

The current project page is used for the public item/glyph/voxel semantics. The exact 2.0.2 file changelog is used for release-specific behavior, production staff promotion, world-safety/security changes and regression-test claims.

## Public source boundary

Public repository:

- https://github.com/zeroregard/Ars-Zero
- default branch: `1.21.1`
- observed branch head during this audit: `9478291a9f331ee2b4a391c4581a342d342ac7dc`

The repository metadata reports its last upstream push before the August 2026 2.0.2 release. The visible `1.21.1` source documentation identifies an older 1.x project state, and the visible `1.20.1-Forge` branch likewise exposes an older beta version string in `gradle.properties`.

Therefore **neither branch is treated as exact 2.0.2 source authority**. Historical source may explain architecture lineage but cannot prove current class names, APIs, registry IDs, signatures or constants.

## Clean-room rule

This catalog paraphrases public behavior and records interoperability/safety boundaries. It does not copy provider source, assets, text, models or sounds into Black Arcana.

GPLv3 project licensing does not automatically authorize mixing provider implementation into Black Arcana without a deliberate compatible-license/provenance decision. For this Phase 2 catalog, source is evidence only.

## Evidence confidence

| Field | Confidence | Reason |
|---|---|---|
| installed filename/mod id/version/SHA-1 | HIGH | current physical modlist |
| CurseForge file identity | HIGH | exact official file page |
| current public glyph/item/voxel semantics | HIGH at documented semantic level | official current project description |
| 2.0.2 release changes/security/test claim | HIGH | exact official 2.0.2 changelog |
| exact registry IDs | NOT VERIFIED | exact binary/source not inspected |
| exact mana costs/tier/config defaults except explicitly release-documented values | NOT VERIFIED | not proven by exact 2.0.2 authority available here |
| exact API/classes/method signatures | NOT VERIFIED | public source is stale relative to release |
| full-modpack runtime compatibility | NOT VERIFIED | no real-client/full-pack run performed in this phase |

## Pending evidence

If the exact installed JAR becomes available to the audit environment, a future binary inspection may close registry/config/API identity without changing provider authority. Until then, these fields remain fail-closed.
