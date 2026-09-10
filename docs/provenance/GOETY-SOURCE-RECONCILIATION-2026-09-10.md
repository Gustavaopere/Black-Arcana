# Goety 3.1.4 source/provenance reconciliation — 2026-09-10

## Scope

This checkpoint records the evidence used to correct Black Arcana's base-Goety catalog. It is a factual/provenance record only. It does not create a source-derived implementation contract, does not transfer provider authority to Black Arcana and does not change the strict semantic-magic total.

## Installed authority

Current physical modpack evidence identifies:

- JAR: `goety-3.1.4.jar`;
- mod id: `goety`;
- runtime version: `3.1.4`;
- SHA-1: `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`;
- Minecraft: `1.21.1`;
- NeoForge: `21.1.248`.

This physical identity remains authoritative for the installed provider.

## Public source line

Repository: `https://github.com/Vivideru/Goety-3`

Audited checkpoints:

| Commit | Declared version evidence | Use |
|---|---|---|
| `4230e3bce2842779a6667ae6e5bfef8f53a27541` | Minecraft `1.21.1`, Goety `3.1.0` in `gradle.properties` | lower audited endpoint |
| `6c41a04f2d712097c4461f969a6bb8ee277149ef` | Goety `3.1.1` in `gradle.properties` | latest audited public endpoint |

No public source/tag corresponding to distributed Goety `3.1.2` or installed `3.1.4` was established during this audit. Therefore the public tree is current-line factual evidence, not exact 3.1.4 source authority.

## Focus registry evidence

Audited file:

`src/main/java/com/Polarice3/Goety/common/items/ModItems.java`

The file has identical blob SHA at both audited checkpoints:

`db3c63b366803e2d46aa4a996b5bb0f358437a7f`

Read-only factual enumeration establishes **123 active Focus item registrations** in the audited public 3.1.0/3.1.1 source interval:

| Category | Count |
|---|---:|
| Magic | 26 |
| Necromancy | 11 |
| Geomancy | 11 |
| Frost | 9 |
| Wild | 12 |
| Wind | 9 |
| Storm | 11 |
| Abyss | 9 |
| Nether | 11 |
| Void | 14 |
| **Total** | **123** |

The previous official-Wiki-derived catalog contained 110 names. The public source registry contains 13 additional IDs:

- `illuminate_focus`
- `earth_punch_focus`
- `smack_stone_focus`
- `ministrous_focus`
- `carrion_focus`
- `razor_wind_focus`
- `surging_focus`
- `sprightly_focus`
- `thunderstorm_focus`
- `water_whip_focus`
- `hogging_focus`
- `stellar_focus`
- `void_flash_focus`

The 110-name Wiki list is therefore retained only as a documentary subset; it is not treated as a complete current 1.21.1 source-line registry.

## License boundary

Upstream `LICENSE.txt` is mixed-license:

- original code under `src/main/java/com/Polarice3/` is stated as MIT;
- additions under `src/main/java/com/Vivideru/` are All Rights Reserved unless specifically stated otherwise.

The audited `ModItems.java` path is under `com/Polarice3`. Black Arcana uses that file only for factual identifiers, counts, blob identity and version/provenance reconciliation. This record does not characterize the whole upstream repository as MIT and does not authorize copying/adapting implementation, assets, text, models or sounds.

## Semantic and runtime limits

This audit does not prove:

- that installed Goety `3.1.4` contains exactly the same 123 Focus registrations;
- that every registered Focus item is reachable/player-facing as a distinct semantic action;
- that 123 registry entries equal 123 semantic magic objects under Black Arcana's metric;
- exact 3.1.4 Focus costs, cooldowns, damage, duration, range, targeting or settlement behavior;
- exact discrete ritual identity count;
- a stable/supported 3.1.4 integration API/event boundary.

Accordingly:

- canonical Goety state: `OPEN CURRENT REGISTRY / EXACT 3.1.4 JAR-SOURCE RECONCILIATION PENDING`;
- Goety semantic delta at this checkpoint: `+0`;
- strict reconstructible semantic minimum remains **796**;
- provider-native Soul Energy, Focus casting, ritual and servant authority remains unchanged;
- integration that depends on unverified 3.1.4 internals remains fail-closed.

## Canonical files reconciled by this checkpoint

- `wiki/modpack-catalog/providers/goety/README.md`
- `wiki/modpack-catalog/providers/goety/FOCUS-CATALOG.md`
- `wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md`
- `wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2J.md`
- `wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md`
- `SOURCES.md`
- `THIRD_PARTY_NOTICES.md`

`docs/provenance/REFERENCE_LEDGER.md` is intentionally not rewritten in this branch because the available connector requires whole-file replacement and the file is a large shared ledger. This scoped checkpoint preserves the provenance evidence without risking destructive replacement of unrelated concurrent entries. A future integral provenance-ledger regeneration may index this checkpoint.
