# Phase 2AP checkpoint — Create Enchantment Industry Plus 1.1.1

## State

`CATALOG CLOSURE CANDIDATE / EXACT PHYSICAL+OFFICIAL SOURCE VERSION / RECIPE+CONTENT EXTENSION / CREATE METADATA TABLE MIS-KEYED / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical main: `068ca67e786d95255ccecb70433dd66d26a4b3e4`
- predecessor: Phase 2AO / PR #150, component #43
- branch: `docs/magic-catalog-phase2ap-create-enchantment-industry-plus-1.1.1`
- canonical coverage at branch creation: **43/100 = 43%**
- proposed coverage after canonical merge: **44/100 = 44%**

## Physical identity

- `create_enchantment_industry_plus-1.1.1-1.21.1.jar`
- mod id `create_enchantment_industry_plus`
- runtime `1.1.1`
- SHA-1 `c7e87eb00e10cb347f6372e17d38da51ce6f1975`
- current physical pack: 595 top-level entries
- NeoForge: `21.1.248`

Relevant physical host/provider stack:

- Create `6.0.10`;
- Create: Enchantment Industry `2.5.3b`;
- Create: Dragons Plus `1.11.8b`.

## Exact source evidence

- official repository: `TiesToetToet/create_enchantment_industry_plus`;
- exact source revision: `fb97ed35288f7ff2c80d43ef33f051db93d281d5`;
- exact source metadata: version 1.1.1, Minecraft 1.21.1;
- addon-keyed required dependencies: NeoForge `[21.1.0,)`, Minecraft `[1.21.1,1.22)`, Create: Enchantment Industry `[2.0.0,)`;
- source contains Create range `[6.0.4,6.1.0)` under mis-keyed table `[[dependencies.create_enchantment_industry]]`, not the addon's `dependencies.create_enchantment_industry_plus` table;
- physical Create `6.0.10` satisfies the numeric range, but physical-JAR metadata parity / loader interpretation of the source table mismatch is **NÃO VERIFICADO**;
- source package contains two Java files and one registered addon item;
- exact source tree contains six addon recipe JSONs and one explicit host-recipe disable overlay;
- no mixin configuration, standalone spell, glyph, ritual, cast resource, network payload or persistence surface observed.

## Exact content closure

The addon closes with:

- **0 spells**;
- **0 glyphs**;
- **0 rituals**;
- **1 item**: `create_enchantment_industry_plus:sac`;
- **6 addon recipes**;
- **1 host-recipe disable overlay** for CEI `mixing/ink`;
- **0 mixins**.

Four recipe routes depend on Create: Dragons Plus identifiers or recipe type, despite Create: Dragons Plus not being declared in the mod metadata. The current pack contains CDP 1.11.8b, so the data dependency is physically satisfiable in this pack but remains an explicit compatibility risk.

## Discrepancies retained

### Create dependency metadata

The intended Create range is visible in the exact source TOML, but its dependency table key belongs to `create_enchantment_industry`, not `create_enchantment_industry_plus`. This catalog records the source exactly and does not guess NeoForge's treatment of the physical JAR.

### Publisher drain route

Publisher-facing material describes an Ink Sac drain/recovery path, but the exact 1.1.1 source tree contains no `emptying`/drain recipe. The catalog therefore does not assign that route to this addon without runtime/provider evidence.

## Black Arcana disposition

This component is a cross-domain recipe/content provider, not a spell system. It must not:

- increase BA spell count with recipe objects;
- create a second Create/CEI processing pipeline;
- double-charge CEI experience or duplicate fluid/item settlement;
- synthesize CDP black dye/grinding when CDP is missing;
- infer Arcane Danger/Corruption/Strain/Backlash from recipe execution;
- transfer BA runtime authority to RPG Skill Tree.

## License / clean-room

Exact source metadata and Modrinth indicate MIT; CurseForge currently labels LGPLv3; repository `LICENSE.txt` is Forge-origin LGPL boilerplate. The discrepancy is preserved. Source/data inspection is read-only for factual cataloging and interoperability; no code/assets are copied.

## Remaining QA / fail-closed

- source↔physical-JAR byte reproducibility;
- physical-JAR metadata parity and NeoForge loader interpretation of the mis-keyed Create dependency table;
- full-modpack recipe/datapack reload behavior;
- JEI/runtime visibility and resource conservation under repetition;
- actual provider/ID for any drain route seen at runtime;
- compatibility if CDP recipe/fluid identifiers change;
- license metadata reconciliation for reuse.

## Merge gate

Before component #44 is canonical:

1. review branch diff;
2. run Black Arcana CI on the exact branch/PR HEAD;
3. re-fetch latest `main`;
4. if `main` advanced, reconcile semantically and rerun CI on the reconciled HEAD;
5. merge only with the expected exact HEAD;
6. confirm final `main` SHA and merged state;
7. verify `CATALOG-COVERAGE-CURRENT.md` from final main reports **44/100 = 44%**.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.