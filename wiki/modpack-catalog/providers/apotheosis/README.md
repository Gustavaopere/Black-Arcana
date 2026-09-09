# Apotheosis 8.8.0 provider record

## Catalog disposition

Phase 2AV treats installed `apotheosis` 8.8.0 as one Adventure/RPG provider component, candidate **#50**.

Branch base `main@f3a3f95a10cf830b6bf973612d519e53d9168adc` already contains Phase 2AU / PR #158, so canonical catalog coverage is **49/100 = 49%**. This record represents **50/100 = 50% only as a candidate** until final reconciliation, exact-HEAD CI GREEN, merge and post-merge main confirmation.

`apothic_attributes`, `apothic_enchanting` and `apothic_spawners` remain separate provider components and are not counted again here.

## Exact identity

- physical JAR: `Apotheosis-1.21.1-8.8.0.jar`;
- mod id: `apotheosis`;
- physical SHA-1: `1e4837fcaf24fe73dba1082656736d872690b303`;
- physical runtime: Minecraft 1.21.1 / NeoForge 21.1.248;
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- CurseForge project/file: `313970 / 8826922`;
- exact official source: `Shadows-of-Fire/Apotheosis@e825cd9dcb9a6fff5e163659812ff32390e343a6`;
- source root tree: `98ffba7432210ac6b5d807a83fc8e49e74db31fd`;
- exact Apotheosis Java package tree: `a517a5e6ecf47bc1eae07c28206868a4317ffb8b`.

Upstream build metadata targets Java 21 / Minecraft 1.21.1 and declares NeoForge 21.1.235+, Placebo 9.9.2+ and Apothic Attributes 2.10.0+ as mandatory version floors. The physical pack satisfies those floors.

## Provider authority

The exact 8.8.0 bootstrap owns dynamic/data-backed registries for rarity, affix, gem, affix loot, invaders, rogue spawners, elites, purity weights, augments, tiered augments and rarity overrides.

Provider state also covers player world tier/unlocks, invader/spawn state, bonus loot/damage-reduction metadata and affixed/gem/rarity/UI item data. Reforging, salvaging, augmenting and gem-cutting workflows are provider-owned.

Seven provider payload types are registered. Relevant client-originated paths are validated by provider server state/context. They are provider UI/interaction/world-tier messages, not Black Arcana cast packets.

No standalone spell/mana/ritual/casting registry or payload surface was observed in the exact source-tree/bootstrap/network audit. The `Spellbreaker` changelog item is an affix and does not establish a spell-runtime bridge.

## Black Arcana boundary

Black Arcana remains authority for:

- canonical server-authoritative casting;
- targeting validation;
- transactional costs/replay protection;
- BA cooldowns/charges;
- hazards and destructive world-effect policy;
- rituals;
- Corruption and Strain;
- Arcane Danger;
- Backlash;
- world safety.

Do not create a second mana/resource or cast pipeline from Apotheosis state. Do not mirror its dynamic registries as a competing authority.

Any future integration must be provider-native first, live behind a dedicated adapter/boundary, preserve reload/server-validation semantics, avoid double processing, and fail closed when no exact safe seam is proven.

## Clean-room / evidence ceiling

The exact source is inspected read-only for factual provider ownership and compatibility analysis. Implementation classes are not automatically stable public APIs.

License layers remain separate: exact source code is MIT; exact source assets are All Rights Reserved; the current CurseForge project surface is All Rights Reserved. No upstream code/assets/text are copied or adapted.

Still unproven: source↔physical-JAR byte reproducibility, direct publisher-file hash equality, full-pack reload/mixin/runtime behavior, optional compatibility paths and non-API binary stability.

See [`EVIDENCE-AND-PROVENANCE.md`](./EVIDENCE-AND-PROVENANCE.md) for the detailed evidence record and `../../meta/PHASE2AV-APOTHEOSIS-CHECKPOINT.md` for the phase gate.
