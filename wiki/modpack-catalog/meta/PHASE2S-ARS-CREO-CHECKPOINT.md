# Phase 2S — Ars Creo 5.4.0 checkpoint

Status: `SOURCE CATALOG COMPLETE / FINAL DIFF+SYNC+CI+MERGE PENDING / RUNTIME+PACK QA PENDING`

Execution branch: `docs/magic-catalog-phase2s-ars-creo`
PR: `#104`
Base main at phase start: `acbea2c897805e0d51476360c27adfd20fabfc64`
Provider source pin: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`
Physical JAR: `ars_creo-1.21.1-5.4.0.jar`
Physical SHA-1: `22a6afd4fbe76354acc9c1ba076c89a94d120d94`

## Closed source surface

- 1/1 provider block;
- 1/1 provider BlockEntityType;
- 1/1 provider item;
- 1/1 creative tab;
- 2/2 Create Display Sources;
- 1/1 provider recipe;
- 7/7 material bridge/system families;
- moving turret cast/source semantics classified;
- moving Source provider classified;
- moving portal and ritual behavior classified;
- Potion Jar fluid capability classified;
- 2 registered S2C payloads classified with active send path not proven;
- common/client mixin surface classified;
- config/default/dependency contract classified;
- authority/deduplication rules written.

## Corrections

1. Notion 8 blocks / 8 BEs is stale: exact source registers 1/1.
2. No Ars Creo glyph registry exists at the checkpoint.
3. Starbuncle Wheel runtime does not require a living Starbuncle; Starbuncle Charm appears in its recipe.
4. Ritual support is explicitly partial/stand-in based; universal ritual compatibility is not claimed.
5. Source metadata says LGPLv3 while root LICENSE is Unlicense text; license identity remains divergent rather than normalized.
6. Two S2C packets are registered, but active production send use is not proven at this checkpoint.

Runtime/config/client/Aeronautics-Sable/full-pack QA remains pending. No Black Arcana runtime Stage is promoted.