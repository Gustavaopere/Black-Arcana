# Provider Audit Queue Delta — Phase 2Q

Status: `SOURCE-PINNED CATALOG COMPLETE / RUNTIME+PACK QA PENDING`

This delta supersedes the stale granular state for `ars_additions` in `PROVIDER-AUDIT-QUEUE.md` until the shared queue is regenerated safely.

## Ars Additions

| Field | Phase 2Q value |
|---|---|
| Mod id | `ars_additions` |
| Installed JAR | `ars_additions-1.21.1-21.3.0.jar` |
| Installed/runtime version | `1.21.1-21.3.0` |
| Physical SHA-1 | `ce2440b606acb20b79a42bf7c6c24d163c93241f` |
| Source checkpoint | `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` |
| Granular state | `SOURCE-PINNED 21.3.0 / MATERIAL MAGIC SURFACE CATALOG COMPLETE / RUNTIME+CONFIG+CLIENT+PACK QA PENDING` |

## Closed material surface

- 3/3 glyphs;
- 2/2 rituals;
- 1/1 perk;
- 1/1 mob effect;
- 12/12 charms;
- 35 blocks + 35 block items;
- 26 direct items / 61 total registered items including block items;
- 5 block entities / 0 custom EntityTypes;
- 11 data components / 4 attachments;
- 5 recipe serializers / 5 recipe types;
- 15 built-in structure-locator recipes;
- provider state/resource/warp/storage/spawner/automation systems;
- Spellweave and Enchanting Wixie Ars-base extensions;
- Arcane Library, Nexus Tower and Ruined Warp Portal worldgen/loot/config;
- dormant weather infrastructure explicitly separated from active magic.

## Fail-closed remainder

- runtime compatibility of the installed Ars Additions 21.3.0 JAR with installed Ars Nouveau 5.13.1;
- effective modpack configs/datapacks versus source defaults;
- Retaliate five-second description versus executable last-attacker path;
- Memory Crystal default acquisition path;
- event/mixin ordering with other installed Ars addons;
- real-client presentation and full-pack dedicated-server QA.

Phase 2Q does not mark sibling Ars addons complete. `ars_controle`, `ars_creo`, `ars_elemancy`, `ars_elemental`, `ars_hex`, `ars_morph`, `ars_zero`, `ars_technica` and other Ars-related providers remain separate queue entries and require their own exact-version audits.
