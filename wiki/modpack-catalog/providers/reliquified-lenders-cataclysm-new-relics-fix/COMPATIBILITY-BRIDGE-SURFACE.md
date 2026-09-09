# New Relics Fix 1.0.2 — compatibility bridge surface

This document records only behavior explicitly supported by the physical inventory and the exact publisher 1.0.2 release surface. No private JAR internals are inferred.

## Problem boundary

Reliquified L_Ender's Cataclysm `0.1.1` was authored against Relics `0.10` APIs. The publisher states that classes/methods removed or changed in Relics `0.12` can otherwise cause startup/linkage failures or broken relic behavior.

The fix translates that old-addon expectation into the current Relics line without modifying the original addon JAR.

## 1.0.2 narrowing

The exact 1.0.2 file changelog states:

> Limited the compatibility bridge to the add-on’s base class, preventing global `RelicItem` modifications.

Catalog consequence: the bridge is addon-scoped. Black Arcana must not interpret it as a general override of every Relics item in the pack.

## Published compatibility families

| Surface | Published 1.0.2 purpose | Authority | Black Arcana disposition |
|---|---|---|---|
| Removed `IRelicItem` API | prevent startup/linkage errors | Relics API + fix translation | do not bind BA to removed API |
| `RelicTemplate` conversion | adapt old relic definitions | Relics current framework | no duplicate template conversion |
| Curios integration | restore equip integration | Curios + addon/fix | do not duplicate equip settlement |
| Attribute modifiers | restore addon modifiers | addon intent via current framework | no second modifier application |
| Stats / levels / ranks | adapt progression semantics | Relics/addon | no parallel progression ledger |
| Cooldowns | adapt legacy cooldown handling | Relics/addon | no second cooldown owner |
| Experience | adapt relic XP behavior | Relics/addon | no double XP award |
| Active abilities | restore legacy active behavior | addon identity + fix translation | do not re-trigger ability |
| Player motion networking | replace removed packet path | provider runtime | exact protocol remains unverified |
| Ability order | preserve ordering | addon/fix | do not reorder from BA |
| Progression values | preserve existing values | addon | do not reinterpret as BA/RPG values |
| Descriptions/tooltips | restore presentation compatibility | provider/client presentation | no gameplay authority inferred |

## Fixed relic identities

Publisher scope is limited to:

- Void Cloak;
- Scouring Eye;
- Void Vortex in Bottle;
- Vacuum Glove;
- Void Bubble.

The bridge does not publish five new relics. These names describe existing addon content that receives compatibility repair.

## Causality and double-processing

A future observer must preserve one causal path:

1. original relic/addon action occurs;
2. bridge translates obsolete API expectations where required;
3. current Relics/Curios runtime settles state;
4. clients receive only the synchronization/presentation appropriate to the provider contract.

Black Arcana must not insert an additional XP/rank/cooldown/modifier/ability mutation for the same event.

## Network boundary

The publisher says the fix replaces a removed player-motion network packet. It does **not** publish the exact packet class, payload fields, direction, registration API, validation or replay behavior.

Therefore all of those details are `NÃO VERIFICADO` and cannot be used as a Black Arcana adapter contract.

The only safe catalog conclusion is that a real networking compatibility seam exists and multiplayer motion behavior requires regression testing.

## Persistence boundary

The publisher states that stats, levels, ranks, cooldowns and experience are adapted, but does not publish exact NBT/attachment/component keys or migration code.

Consequently:

- do not invent save keys;
- do not assume migration is idempotent;
- do not assume death/relog/restart semantics beyond the framework's verified behavior;
- runtime QA must detect resets, duplicates and stale modifiers.

## Runtime QA matrix

Semantic closure does not mark these tests as passed:

- dedicated-server boot without old-API linkage errors;
- instantiate/equip each of the five relics;
- Curios equip/unequip/relog without duplicate/stale modifiers;
- XP/level/rank progresses once and persists;
- cooldown starts/ends once and persists correctly;
- active abilities work in singleplayer and remote multiplayer;
- player-motion behavior has no desync/rubber-banding/double execution;
- tooltips remain consistent with functional state;
- removal of the fix reproduces the expected compatibility failure in an isolated QA environment;
- reinstallation restores the stack without migration duplication.

## Black Arcana boundary

This provider is not a spell host and does not create a Black Arcana magic boundary. Its relevance is deduplication and cross-domain safety: relic state/progression/network translation already has an owner.

Any later Black Arcana interaction with these relics must consume stable provider-visible state or events, never duplicate the bridge's translation path and never transfer BA's own runtime authority out of the canonical casting/effect pipeline.
