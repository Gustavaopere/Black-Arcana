# RunicLib — 5.0.7

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_LIBRARY_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical authority

- JAR: `neoforge-runiclib-1.21.1-5.0.7.jar`;
- mod id: `runiclib`;
- runtime: `5.0.7`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `f0422c70689d5b31b65ef5a84c1d5eb2d7536d4c`;
- CurseForge project/file: `880879 / 8188562`.

Exact NON-MERGE audit branch `audit/photon-runiclib-zero-semantic-2026-09-27` materialized File `8188562` and hard-verified the same SHA-1. Physical↔publisher identity is closed.

## Semantic role

RunicLib is shared library infrastructure for AZURUNE consumers. Its public role is MultiLoader utilities plus reusable attributes/effects and registration helpers; release 5.0.7 adds common villager/wandering-trader registration utilities.

In the current pack Dungeon's Delight is a confirmed consumer. Consumer gameplay remains owned by the consumer rather than transferred to RunicLib.

## Exact artifact boundary

The hash-matched artifact closes:

- provider namespace resources: **54**;
- assets: **50**;
- data files: **4**;
- spell/ritual/rite/ability-like archive paths: **0**;
- spell/ritual/rite/ability-like class names: **0**;
- library/API/effect/attribute/trade-oriented class-name matches: **29**.

The four exact provider data paths are:

- `data/runiclib/damage_type/creative_shock.json`;
- `data/runiclib/damage_type/retaliation.json`;
- `data/runiclib/damage_type/venom.json`;
- `data/runiclib/tags/damage_type/bypasses_dodge.json`.

There are no provider recipe, loot, advancement or action-registry data paths in the exact namespace inventory.

See [`EXACT-5.0.7-ZERO-SEMANTIC-AUDIT.md`](EXACT-5.0.7-ZERO-SEMANTIC-AUDIT.md).

## Semantic disposition

RunicLib owns reusable MobEffects, attributes, damage types, tags and helper/services infrastructure. These are not independently player-invoked spells, glyphs, rituals, rites or equivalent discrete supernatural action identities under the current metric.

**Semantic contribution: +0 (`ZERO_SEMANTIC_LIBRARY_INFRA`).**

## Authority boundary

RunicLib owns its library types/services. Consumers own the gameplay action that uses them. Black Arcana must not count a RunicLib effect/damage type once as a library action and again under the consumer that actually exposes gameplay.

## Runtime QA remains separate

Still fail-closed:

- API/major-line compatibility with all installed consumers;
- mixin/attribute/effect stacking;
- RLTrade usage by consumers;
- dedicated-server lifecycle;
- any Black Arcana integration.

## Result

**✅ Cataloged — exact zero-semantic library infrastructure.**
