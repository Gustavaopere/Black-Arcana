# Apothic Compat 2.0.2

Status: `EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION PIN / APOTHEOSIS LOOT-CATEGORY DATA-MAP + AFFIX-BLACKLIST COMPAT PROVIDER / 0 SPELLS / 0 MIXINS / 13 DATA-MAP OVERRIDES / 1 CONFIG KEY / HOST-PRIVATE-FIELD + FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `apothic_compat-2.0.2.jar`
- mod id: `apothic_compat`
- display name: `Apothic Compat`
- runtime version: `2.0.2`
- physical SHA-1: `868506b8367be2c155acde0ef186b5a3e6ba8db9`
- CurseForge project/file: `1516278 / 8219980`
- exact publisher release: NeoForge 1.21.1, 2026-06-09
- official source repository at the release line: `Nightwielder23/apothic-category-compat`
- exact source revision: `cebf69a37f8c6573fc0c0295e627f4636e7bd026`
- exact source revision message: `ported to neoforge 1.21.1 with apotheosis 8.x data map architecture`

The exact source `gradle.properties` declares:

- Minecraft `1.21.1`;
- NeoForge `21.1.230`;
- `mod_id=apothic_compat`;
- `mod_version=2.0.2`;
- Apotheosis baseline `8.5.4`;
- Placebo baseline `9.9.1`;
- Apothic Attributes baseline `2.9.1`.

The physical pack uses NeoForge `21.1.248`, Apotheosis `8.8.0`, Placebo `9.9.2` and Apothic Attributes `2.10.1`. The runtime metadata requires Apotheosis `[8.5,9)`, so the physical version satisfies the declared range; private-reflection parity against 8.8.0 remains a separate QA boundary.

## Exact role on 1.21.1

Apotheosis 8.x owns loot-category semantics and the `apotheosis` data-map type. Apothic Compat supplies missing item-to-category entries in:

`data/apotheosis/data_maps/item/loot_category_overrides.json`

The exact source states that Apotheosis itself consumes this data map; Apothic Compat does not run a second category-assignment code path.

The provider also owns one auxiliary policy surface: a config-driven blacklist that rebuilds Apotheosis's affix-by-type selection pool without selected affix IDs.

## Exact source surface

The exact source tree contains **4 Java classes**:

1. `ApothicCompat`
2. `ReloadCommand`
3. `AffixBlacklist`
4. `ApothicCompatConfig`

There is no mixin manifest or mixin package in the exact tree. Exact provider mixin count is therefore **0**.

The exact data map contains **13 item overrides**, all targeting `apotheosis:bow`:

- Alex's Caves: 2;
- Alex's Mobs: 2;
- Born in Chaos: 1;
- L_Ender's Cataclysm: 5;
- The Undergarden: 1;
- Twilight Forest: 2.

See [DATA-MAP-AND-AFFIX-BLACKLIST.md](DATA-MAP-AND-AFFIX-BLACKLIST.md) for the exact IDs.

## Runtime hooks

`ApothicCompat` registers on the NeoForge event bus and handles only:

- `RegisterCommandsEvent` -> register provider reload commands;
- `ServerStartedEvent` -> load/apply affix blacklist;
- full `OnDatapackSyncEvent` (`event.getPlayer() == null`) -> reapply affix blacklist after Apotheosis rebuilds its affix pool.

Reload aliases require permission level 2:

- `/apothiccompat reload`
- `/ac reload`

The data map follows normal datapack reload; the provider command is for the affix-blacklist file.

## Semantic inventory result

For exact 2.0.2:

- standalone spells: **0**;
- glyphs: **0**;
- rituals: **0**;
- provider mana/casting resource: **0**;
- provider mixins: **0**;
- provider Java classes: **4**;
- loot-category data-map overrides: **13**;
- distinct target category IDs: **1** (`apotheosis:bow`);
- config keys: **1** (`affix_blacklist`);
- provider command roots/aliases: **2**;
- provider event hooks: **3**.

These are compatibility/data objects, not Black Arcana spell identities.

## Authority

- **Apotheosis** owns loot categories, affix registry/pools, affix rolling and category synchronization.
- **Apothic Compat** owns only its contributed data-map values, config parsing, blacklist policy/reapplication and command UX.
- **Black Arcana** retains casting, costs, targeting, cooldowns/charges, spell/hazard effects, Corruption, Strain, Arcane Danger, Backlash and `WorldEffectPolicy`.
- **RPG Skill Tree** remains progression/Mastery/perk authority only through real contracts.

Black Arcana must not duplicate this item's category-override layer, mutate Apotheosis private affix pools to implement BA magic rules, or infer BA casting/proc causality from an affix-category assignment.

## Static QA boundary

`AffixBlacklist` reflectively accesses the private field name `AffixRegistry.byType`. Reflection failure is caught and logged, so the blacklist fails without crashing through that path, but exact compatibility with physical Apotheosis 8.8.0 is not inferred from the declared version range alone.

A second exact source discrepancy is preserved: if `/ac reload` changes a previously non-empty blacklist to empty, `AffixBlacklist.apply()` returns immediately and does not restore the already-filtered `byType` pool itself. A normal Apotheosis pool rebuild (such as datapack reload/server lifecycle) restores the unfiltered pool before the empty blacklist is reapplied. Runtime regression should cover this before any reliance on live blacklist removal semantics.

## Evidence files

- [DATA-MAP-AND-AFFIX-BLACKLIST.md](DATA-MAP-AND-AFFIX-BLACKLIST.md)
- [RUNTIME-AND-AUTHORITY.md](RUNTIME-AND-AUTHORITY.md)
- [EVIDENCE-AND-PROVENANCE.md](EVIDENCE-AND-PROVENANCE.md)
