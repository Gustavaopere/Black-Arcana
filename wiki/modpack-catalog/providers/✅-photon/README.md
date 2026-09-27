# Photon — 2.2.6.a

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_VFX_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical authority

- JAR: `photon-neoforge-1.21.1-2.2.6.a-all.jar`;
- mod id: `photon`;
- runtime: `2.2.6.a`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `5b725c08494375b4ae8917fca3f357a85a0fa6d2`;
- CurseForge project/file: `871522 / 8824095`.

Exact NON-MERGE audit branch `audit/photon-runiclib-zero-semantic-2026-09-27` materialized File `8824095` and hard-verified the same SHA-1. Physical↔publisher identity is closed.

## Semantic role

Photon is VFX/editor infrastructure. It owns effect graphs, particles, trails, emitters, timelines, materials/rendering support and effect execution plumbing. A consumer mod or datapack owns the gameplay event that causes a Photon effect to play.

The official project description likewise presents Photon as a VFX editor inspired by Unity with particle/trailing systems for modders and players.

## Exact artifact boundary

The hash-matched artifact closes:

- provider namespace resources: **124**;
- provider assets: **124**;
- provider data files: **0**;
- spell/ritual/rite/ability-like archive paths: **0**;
- spell/ritual/rite/ability-like class names: **0**;
- VFX-surface class-name matches: **509**;
- gameplay data paths under recipe/loot/advancement/tags/damage/worldgen families: **0**.

See [`EXACT-2.2.6A-ZERO-SEMANTIC-AUDIT.md`](EXACT-2.2.6A-ZERO-SEMANTIC-AUDIT.md).

## Semantic disposition

Photon does not mint an independent spell, glyph, ritual, rite or equivalent discrete supernatural player-action catalog in the exact installed artifact.

Commands/editor actions that preview or execute VFX are authoring/debug/infrastructure surfaces, not provider-owned gameplay magic identities.

**Semantic contribution: +0 (`ZERO_SEMANTIC_VFX_INFRA`).**

## Authority boundary

Photon owns VFX representation/execution infrastructure. Consumer providers remain authority for damage, targeting, cooldown, mana/resource settlement, progression, persistence and the semantic identity of the spell/action being visualized.

Black Arcana may consume Photon only through an explicit supported integration if one is later adopted; it must not infer a gameplay event solely from VFX.

## Runtime QA remains separate

Still fail-closed:

- exact consumers of Photon in the assembled pack;
- dedicated-server/client classloading;
- glTF/resource reload behavior;
- shaders/PartiCull/culling/transform-space interaction;
- performance and cleanup of emitters/trails;
- any future Black Arcana adapter.

## Result

**✅ Cataloged — exact zero-semantic VFX infrastructure.**
