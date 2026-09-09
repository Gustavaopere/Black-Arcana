# Phase 2AT — Apothic Spawners 1.4.0 checkpoint

## Scope

Phase 2AT audits `apothic_spawners` 1.4.0 against the current physical modpack, publisher release and exact official source release commit. This is catalog/deduplication work only; no Black Arcana runtime implementation is added.

## Canonical base

- base `main`: `063135e690b4c066db582be1be6dd1e1387f1758`
- canonical component count on that base: **47/100 = 47%**
- Phase 2AS / PR #155 is canonical as component #47 and its post-merge CI #2239 is GREEN on the exact merge SHA.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: `21.1.248`
- physical modlist: 595 top-level entries
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- physical artifact: `ApothicSpawners-1.21.1-1.4.0.jar`
- mod id: `apothic_spawners`
- physical version: `1.4.0`
- physical SHA-1: `b3be29751daea738e691db8949cce079e5aae3be`

## Publisher/source evidence

- CurseForge project/file: `986583 / 8469405`, released 2026-07-20 for NeoForge Minecraft 1.21.1.
- Official repository: `Shadows-of-Fire/Apothic-Spawners`.
- Official 1.21 maintenance branch exists and carries exact 1.4.0 source.
- Exact release commit: `d3bc0b40d46bee476fc770f8e4e44a1c35ecddd3`, message `1.4.0`.
- Exact release tree: `7cd127fe22a9810b22bd8203cb2286d53b840e25`.
- Immediate parent `9b144c0ed58a7c0a83635b9a52653b1228844f55` introduces `The Nuclear Spawner` as a 26.1 backport.
- Earlier `af8b7c4f8a5dd7915b18a0cdab7549f12b4f4ea2` backports the float-comparison fix.
- The later branch HEAD is five commits ahead only in translation/schema documentation; exact compare shows no Java/gameplay datapack drift.

## Semantic closure

Exact 1.4.0 source closes:

- 0 standalone spells;
- 0 glyphs;
- 0 rituals;
- 0 provider mana/cast resource;
- no provider C2S cast-intent path;
- 27 Java files;
- exactly 16 spawner-stat registry identities;
- exactly 32 stock modifier recipes, 16 direct + 16 inverse;
- modifier operations `add` and `set`;
- one `spawner_modifier` recipe type/serializer;
- Capturing effect component, modifier advancement trigger, spawn-egg predicate, entity blacklist tag and unstable-spawner loot key;
- exactly 2 common mixins and 0 client mixins;
- replacement of vanilla Spawner block/item implementation and `MOB_SPAWNER` block-entity factory;
- 5 config values;
- one clientbound PLAY config payload, protocol/version `2`;
- explicit tile NBT persistence for stats, player-modified state, instability countdown and captured spawn data;
- Capturing, Echoing loot/XP, No-AI/movable and spawner-only despawn semantics;
- bounded Nuclear Spawner behavior: 60 ticks, explosion radius 8, 12 spawn attempts and provider unstable-spawner loot.

## Authority / deduplication result

Apothic Spawners owns its spawner lifecycle, not magic casting. Black Arcana therefore does not:

- create spell identities for Capturing/Echoing;
- duplicate the 16-stat/modifier runtime;
- mirror provider tile persistence;
- add a second Capturing/Echoing loot/XP pass;
- alter generic mob despawn based only on thematic similarity;
- directly multiply provider spawn loops from RPG perks;
- invoke Nuclear Spawner helpers as a shortcut around `WorldEffectPolicy`.

For BA-caused destruction, BA first applies `WorldEffectPolicy`. If the permitted world effect naturally reaches an Apothic spawner and the provider enters instability, that subsequent transition belongs to Apothic Spawners and must not be processed a second time by BA.

## Exact release dependency/license boundary

Generated 1.4.0 metadata requires Minecraft 1.21.1+, NeoForge 21.1.187+ and Placebo 9.9.0+. Physical NeoForge 21.1.248 and Placebo 9.9.2 satisfy those minimums.

License layers are not flattened: source code/generated metadata indicate MIT; source assets are All Rights Reserved; the current CurseForge project surface labels the project All Rights Reserved. Inspection is factual/read-only and no code/assets are copied.

## Remaining QA

Fail-closed:

- byte-for-byte source↔physical-JAR reproducibility;
- direct physical-vs-publisher-file hash equality;
- complete-modpack reload/event ordering;
- provider explosion interaction with protection/world-policy mods;
- alternate spawner implementation compatibility;
- external machine-spawner/summon integration.

## Coverage decision

The provider is eligible to become component **#48** because its current physical identity and exact 1.4.0 release source close the full provider-owned semantic/runtime surface relevant to Black Arcana deduplication, including the exact result of zero standalone spells.

Until final latest-main reconciliation, exact-head CI GREEN, merge and post-merge `main` confirmation, canonical coverage remains **47/100 = 47%** and Phase 2AT represents **48/100 = 48%** only as a candidate.

Phase 3 remains blocked.