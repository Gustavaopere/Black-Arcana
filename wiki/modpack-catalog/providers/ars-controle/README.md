# Ars Controle — Ars Nouveau control/automation provider

Status: `PHASE 2R / SOURCE-PINNED 1.6.15 CATALOG IN PROGRESS / RUNTIME+PACK QA PENDING`

## Exact installed identity

- JAR: `ars_controle-1.21.1-1.6.15.jar`
- Mod id: `ars_controle`
- Runtime version: `1.21.1-1.6.15`
- Physical SHA-1: `fdf381d5733698abe336354c7541299ab495ecae`
- Loader/game: NeoForge 1.21.1

## Exact source checkpoint

Read-only factual cataloging is pinned to `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.

At that revision `gradle.properties` declares:

- `mc_version=1.21.1`;
- `neo_version=21.1.217`;
- `mod_id=ars_controle`;
- `mod_version=1.6.15`;
- `mod_license=LGPLv3`;
- Ars Nouveau build baseline `5.10.6.1245`;
- Curios baseline `9.0.12`;
- CC:Tweaked baseline `1.112.0`.

The physical pack is newer in important providers, including NeoForge `21.1.248`, Ars Nouveau `5.13.1` and Curios `9.5.1+1.21.1`; effective runtime compatibility is therefore a separate QA gate.

## Provider authority

Ars Nouveau remains authority for mana, Source, spell grammar, resolver/cast lifecycle and the base Ars ritual/warp infrastructure. Ars Controle owns only its added filters/effect, control blocks/items, persisted endpoint/reference state and provider-specific routing behavior.

Black Arcana must not turn a routed provider spell into a second cast, charge mana/cooldown/Mastery twice, infer loaded remote endpoints from stale state, or treat Ars Controle infrastructure as permission to weaken Black Arcana targeting/world-safety rules.

## Exact registry correction

The source-pinned release registers:

- 4 blocks;
- 6 items: 4 block items + Remote + Portable Brazier Relay;
- 3 BlockEntityTypes;
- 2 persistent/network-synchronized data components;
- 4 attachment types;
- 1 creative tab;
- 9 Ars spell parts: 1 effect + 8 filters.

The Temporal Stability Sensor is a registered block but has no BlockEntityType in `ACRegistry.Tiles`.

A prior Notion dossier described "4 block entities" and "31 Ars/logic components". Those values are retained as historical/editorial context only. They do not match the exact 1.6.15 registry: the current release source registers 3 block-entity types and 9 glyph/spell parts. Internal concepts/classes must not be promoted to player glyphs without registry evidence.

## Current Phase 2R progress

- provider identity/provenance: source-pinned;
- exact registries: source-pinned;
- glyphs/spell parts: 9/9 identities and acquisition source-pinned;
- detailed block/item/remote/relay behavior: pending granular audit;
- networking/config/optional compatibility: pending granular audit;
- final runtime/config/client/full-pack QA: pending.
