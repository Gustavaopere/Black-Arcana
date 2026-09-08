# Phase 2Y — Ars Nouveau's Flavors & Delight 2.2.2 checkpoint

Status: `SOURCE CATALOG COMPLETE / PRE-CI MAIN SYNC COMPLETE / CI PENDING / INSTALLED JAR + CURRENT-HOST RUNTIME QA DEFERRED`

Execution branch: `docs/magic-catalog-phase2y-ars-delight`
Base `main` at phase start: `4ce5699cc76b511804956f903559ae8f7e44ba12`
Pre-CI `main` confirmed: `4ce5699cc76b511804956f903559ae8f7e44ba12`
Pre-CI branch relation: `0 behind / catalog-only delta under wiki/modpack-catalog/**`
Provider source checkpoint: `Minecraft-LightLand/Ars-Nouveau-Flavors-Delight@1443c80842575f7d775c522d2b2cd32441592e26` (`VERSION-ALIGNED 2.2.2`, not claimed byte-identical)
Physical JAR: `arsdelight-2.2.2.jar`
Physical mod id/version: `arsdelight` / `2.2.2`
Physical SHA-1: `98e98fc1f03192bb7680ef9a3ba9a99c2df625bb`
Physical CurseForge hash: `1990459316`

## Current physical host snapshot

- NeoForge project baseline: `21.1.248`;
- Ars Nouveau: `5.13.1` (`ars_nouveau`);
- Farmer's Delight: `1.3.4` (`farmersdelight`);
- Ars Elemental: `0.7.10.1` (`ars_elemental`) — present;
- Cuisine Delight: `1.2.10` (`cuisinedelight`) — present;
- Thirst Was Reclaimed: `1.21.1-3.0.4`, mod id `thirst` — present, compatibility with the source's legacy Thirst API not inferred;
- Archwood Good: no top-level physical JAR found in this checkpoint;
- Diet: no top-level physical JAR found in this checkpoint.

## Closed source catalog

- exact physical JAR/mod id/version/SHA-1/hash;
- exact public source branch/head declaring `mod_version=2.2.2`;
- LGPL-2.1 source license signal and root license agreement;
- required Ars Nouveau `[5.8.1,)` and Farmer's Delight `[1.3,)` metadata boundaries;
- source NeoForge build pin `21.1.205` vs current project `21.1.248`;
- 42/42 base `ADFood` entries from the verified inventory;
- 8/8 base non-food items;
- 8/8 base crate/cabinet/feast blocks;
- 5/5 base jelly blocks + 1 jelly block-entity type;
- 4/4 base pies + 4 slice items;
- 5/5 base provider effects;
- exact heal/spell-damage/max-mana/mana-regen event formulas;
- Enchanter's Knife Ars caster-tool boundary and acquisition recipe;
- Cutting Board `EffectResolveEvent.Pre` processing/cancellation seam;
- Jelly `IPrismaticBlock` + `IContextAttachment` + `EffectInfuse` seam;
- Drygmy `ANFakePlayer` tool-lending mixin lifecycle;
- 3/3 declared mixins classified;
- three provider global-loot modifier intents classified;
- conditional Ars Elemental / Archwood Good / Thirst compatibility paths;
- Cuisine Delight generated-config integration path;
- no Ars Delight-owned production spell-part/glyph registration identified in the exact source content tree;
- no Ars Delight-owned custom payload class/registration surface identified in the exact source tree despite an L2 `PacketHandler` field;
- provider authority/deduplication consequences;
- clean-room provenance.

## High-value factual consequences

1. Ars Delight is a content/crossover provider, not a replacement casting or progression authority.
2. Flourishing writes directly to Ars mana after healing; Black Arcana must not create a second mana credit for that heal.
3. Wilden modifies Ars damage/max-mana/regen calculations; those provider calculations settle once.
4. Freezing Spell and optional Lightning Curse are descendants of Ars spell-damage events, not independent casts.
5. Cutting Board integration deliberately cancels the handled Ars effect; any observer must honor the cancellation outcome.
6. Enchanter's Knife turns a melee hit into an Ars-native spell resolution through the provider item; it is not a Black Arcana cast surface by default.
7. Jelly infusion mutates Ars spell context/potion data through provider-owned attachment logic; BA must not serialize or replay that state.
8. Drygmy integration targets concrete Ars internals with mixins and is not a safe BA bridge contract.
9. Source-required versions admit the current Ars/FD versions by range, but exact current-host behavior remains a runtime gate.
10. Current pack uses `thirst` from Thirst Was Reclaimed, while source was compiled against a Thirst Was Taken artifact/API; identical mod id does not prove class/API compatibility.

## Deferred installed-runtime/JAR validation

- extract/inventory the physical 2.2.2 JAR and compare packaged registry/data/mixin surfaces to the version-aligned source checkpoint;
- client and dedicated-server boot on the current host set;
- all five base effect event paths, including multiplayer caster ownership and event ordering;
- Enchanter's Knife scribing, mana cost/discount, melee→spell exactly-once resolution and death/logout lifecycle;
- Cutting Board Cut/Crush/Fell/Break handling, cancellation and AOE exclusion;
- Jelly projectile hit, context attachment, Infuse replacement and food-effect probability/duration semantics;
- Drygmy adjacent-pedestal selection, tool copy/enchant behavior, durability and cleanup;
- feast/pie/jelly serving/drop conservation under break/explosion/save-reload;
- three global-loot modifier paths and no duplicate reward under other loot addons;
- Ars Elemental present path under 0.7.10.1;
- Archwood Good absent classloading path;
- Diet absent path;
- current `thirst` provider API/classloading compatibility;
- Cuisine Delight 1.2.10 generated-config compatibility;
- full-pack food/nutrition/heal/spell-event interop.

These are runtime/package gates, not missing factual source-catalog entries.

## Pre-CI / merge gate

Pre-CI synchronization and diff review are complete against `main@4ce5699cc76b511804956f903559ae8f7e44ba12`; the branch was 0 commits behind and its delta was confined to ten new files under `wiki/modpack-catalog/**` before this checkpoint update.

Remaining gate:

1. open/refresh the Phase 2Y PR;
2. require fresh CI on the exact final execution HEAD;
3. keep review threads clear;
4. immediately before merge, fetch/reconcile `main` again and revalidate if needed;
5. merge only after those gates pass;
6. confirm final `main` SHA.

Phase 2Y is documentation/catalog state only and does not promote any Black Arcana runtime Stage.
