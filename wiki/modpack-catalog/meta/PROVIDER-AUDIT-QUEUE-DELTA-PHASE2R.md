# Provider Audit Queue Delta — Phase 2R

Status: `SOURCE-PINNED CATALOG COMPLETE / RUNTIME+CONFIG+CLIENT+PACK QA PENDING`

This narrow delta supersedes the stale granular state for `ars_controle` in `PROVIDER-AUDIT-QUEUE.md` until the shared queue is regenerated safely.

## Ars Controle

| Field | Phase 2R value |
|---|---|
| Mod id | `ars_controle` |
| Installed JAR | `ars_controle-1.21.1-1.6.15.jar` |
| Installed/runtime version | `1.21.1-1.6.15` |
| Physical SHA-1 | `fdf381d5733698abe336354c7541299ab495ecae` |
| Source checkpoint | `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430` |
| Source license | GNU LGPL v3 |
| Granular state | `SOURCE-PINNED 1.6.15 / MATERIAL MAGIC+CONTROL SURFACE CATALOG COMPLETE / RUNTIME+CONFIG+CLIENT+PACK QA PENDING` |

## Closed material surface

- 4/4 registered blocks;
- 6/6 registered items;
- 3/3 registered BlockEntityTypes;
- 2/2 persistent/network-synchronized data components;
- 4/4 attachment types;
- 1/1 creative tab;
- 9/9 Ars spell parts individually cataloged;
- 9/9 default glyph-learning recipes resolved;
- 6/6 player-facing control systems individually cataloged;
- 6/6 default system acquisition paths resolved;
- 5 provider network payloads classified;
- server/startup config defaults classified;
- Scryer's Linkage generic capability delegation/blacklists classified;
- provider mixins/validators classified;
- optional ComputerCraft peripherals classified and currently absent from the physical pack;
- provider-native authority/deduplication matrix written.

## Exact editorial corrections

- exact release registers 3 BlockEntityTypes, not the older Notion count of 4;
- exact release registers 9 Ars spell parts, not the older editorial "31 components" as a glyph count;
- Temporal Stability Sensor is a block-only implementation without a registered BlockEntityType;
- the older Notion optional-integration inventory is not promoted over exact 1.6.15 source evidence.

## Fail-closed remainder

- installed-JAR behavior against physical Ars Nouveau 5.13.1 / NeoForge 21.1.248 / Curios 9.5.1;
- effective server/startup config and datapack overrides;
- Warping Spell Prism entity-target Source settlement, whose audited path returns before the block-target deduction block;
- effective Scryer's Linkage chunk-loading behavior versus its declared `load_time=600` config;
- Remote multiple-selection practical/server bounds;
- mixin/event ordering with sibling Ars addons;
- real-client presentation and full-pack dedicated-server QA.

Phase 2R does not mark sibling Ars providers complete. `ars_creo`, `ars_elemancy`, `ars_elemental`, `ars_hex`, `ars_morph`, `ars_zero`, `ars_technica`, `ars_two_way_portals` and other queue entries remain independent audits.
