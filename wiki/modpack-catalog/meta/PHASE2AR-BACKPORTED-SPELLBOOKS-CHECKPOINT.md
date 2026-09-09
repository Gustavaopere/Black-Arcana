# Phase 2AR — Backported Spellbooks checkpoint

## Scope

Phase 2AR audits `backportedspellbooks` against the current physical modpack and the strongest publisher/source evidence available. It is a catalog/deduplication phase only; no Black Arcana runtime implementation is added.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: `21.1.248`
- physical modlist: 595 top-level entries
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- physical artifact filename: `backportedspellbooks-0.1.2.jar`
- physical mod ID: `backportedspellbooks`
- physical runtime metadata version: `0.1.0`

## Publisher/source evidence

- CurseForge exact file: project `1283913`, file `8158731`, NeoForge Minecraft 1.21.1, released 2026-05-28, filename `backportedspellbooks-0.1.2.jar`.
- Exact public 0.1.2 changelog adds Miasmic Staff, Quicksilver Spellbook, Slime Boots, Slime Aspect, Sulfur Clouds, Sulfur Bomb, Sulfur Release, plus Corroded Fossils and Quicksilver in Sulfur Caves.
- Official public repository: `RedReaper28/BackportedSpellbooks-1.21.1`.
- Release-day source pin: `07cb65efca0c264762a21c2d6bce0f83e3947226`.
- The release-day source still declares `mod_version=0.1.0`, matching the runtime metadata in the physical inventory while differing from the publisher/file label `0.1.2`.

This phase preserves all three layers instead of silently normalizing the version.

## Semantic closure

The release-day source closes the provider-owned spell registry at exactly six registrations:

- `slime_aspect`
- `sulfur_bomb`
- `sulfur_clouds`
- `sulfur_release`
- `pale_thorn`
- `resin_spray`

The four sulfur/slime spells are exactly the 0.1.2 publisher delta. Pale Thorn and Resin Spray predate that delta.

Additional release-day source surfaces closed for deduplication include:

- Pale Flora school/sub-school registration;
- 19 item registry objects including block-items;
- 4 blocks;
- 5 entity types;
- 4 effects;
- 2 particle types;
- 1 fluid plus 1 fluid type;
- 19 recipe JSONs;
- Corroded Fossil and Quicksilver worldgen in `minecraft:sulfur_caves` at `underground_ores`;
- server-side equipment hooks for Miasma Staff, Garden Rapier and Slime Boots.

No provider custom payload registration, provider SavedData/attachment/data-component persistence subsystem, or mixin configuration was observed in the inspected release-day source tree. These are source observations only, not claims about unverified physical bytecode.

## Authority and deduplication

- Iron's owns host casting, mana, cooldown/container and host spell runtime.
- Backported Spellbooks owns its six spell identities, Pale Flora surface, effects/entities/equipment/worldgen and provider procs.
- Vanilla Backport and Ace's Spell Utils retain authority over their own consumed content/API surfaces.
- Black Arcana retains its single canonical server-authoritative cast pipeline, transactional costs, BA cooldowns/charges, targeting, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- Black Arcana must not clone the six spells, duplicate the equipment procs, add a second mana/cooldown settlement path or treat provider worldgen as BA world-mutation authority.
- RPG Skill Tree receives no provider magic-runtime authority.

## Static QA / unresolved boundaries

- no byte-for-byte equivalence between physical JAR and source pin has been proven;
- physical SHA-1 for the Backported artifact is not available in the current exported modlist text and is therefore not invented;
- source targets NeoForge `21.1.216` and Iron's `1.21.1-3.15.4`, while the pack uses NeoForge `21.1.248` and Iron's `1.21.1-3.16.3`;
- generated metadata observed in source formally declares NeoForge/Minecraft only even though code imports Iron's, Vanilla Backport and Ace's; loader/dependency parity remains runtime QA;
- Slime Boots has cooldown-related presentation/constants but the inspected fall-event hook cancels fall without an observed cooldown gate; live semantics remain QA;
- full-pack event ordering, proc duplication, provider spell configuration, network synchronization and dedicated-server behavior remain QA;
- CurseForge labels MIT while release-day source metadata declares All Rights Reserved; source/data inspection is factual/read-only and no implementation/assets are copied.

## Coverage decision

This provider is eligible to become component **#46** because its semantic provider surface is closed at a defensible evidence ceiling: exact physical presence, exact publisher release identity/changelog, release-day official source, a complete six-spell registry and bounded supporting runtime/content surfaces.

The point is not canonical until this branch is reconciled with the latest `main`, CI is GREEN on the reconciled HEAD, the PR is merged and post-merge `main` is confirmed. Until then canonical coverage remains **45/100**.

Phase 3 remains blocked.
