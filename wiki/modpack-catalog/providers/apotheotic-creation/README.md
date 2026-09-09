# Apotheotic Creation 2.0.0

## Catalog status

Phase 2AW catalogs installed `apotheoticcreation` 2.0.0 as candidate component **#51**.

- canonical base: `main@517b3e9c6da648c1470c227a11f571d951fbee47`;
- canonical coverage at base: **50/100 = 50%**;
- candidate coverage represented by this tranche: **51/100 = 51%**;
- canonicalization requires latest-main reconciliation, CI GREEN on the exact reconciled HEAD, merge and post-merge main confirmation.

## What this addon owns

Apotheotic Creation is a narrow compatibility adapter between Apotheosis item metadata and Create's Attribute Filter system.

At the exact 2.0.0 source pin it registers two Create item-attribute types:

- `apotheoticcreation:rarity`;
- `apotheoticcreation:affix`.

The implementation reads Apotheosis rarity/affix state and exposes it through Create's item-attribute contracts. It does not create a second rarity/affix system.

## Provider boundaries

Apotheosis remains authority for:

- rarity identities/state;
- affix identities/state;
- affixed item metadata.

Create remains authority for:

- `ItemAttributeType` registration semantics;
- Attribute Filter configuration/matching framework;
- downstream logistics that consume filters.

Apotheotic Creation owns only the translation/registration bridge.

Black Arcana remains authority for canonical casting, targeting, transactional costs, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety. No addon filter packet/state is routed into BA's cast pipeline because no addon-owned packet/state surface is observed at this exact pin.

## Exact behavior caveat

Affix enumeration via `AffixAttribute.Type.getAllAttributes` excludes provider affix paths `socket` and `durable`. Do not describe the UI/enumeration contract as exposing every affix.

The addon itself does not establish special Smart Observer, Brass Tunnel, funnel or other logistics hooks. Those are downstream Create consumers of normal Attribute Filter behavior and require Create/runtime evidence for consumer-specific claims.

## Identity / evidence

- physical JAR: `apotheoticcreation-2.0.0.jar`;
- physical SHA-1: `6bbb91aea834941b47a6af3318b091f64e4375ab`;
- current pack: Create 6.0.10 + Apotheosis 8.8.0;
- CurseForge project/file: `956637 / 8391265`;
- exact source: `maxpowa/ApotheoticCreation@ed56ccf54e1be132c983c524597300e852098840`;
- exact tree: `5c5d51ef69b5f0f50d398d7f0479b8ca83894f7d`;
- complete recursive tree contains one Java source file;
- required source metadata ranges: Create `[6,)`, Apotheosis `[8,)`;
- license evidence: MIT.

See [`EVIDENCE-AND-PROVENANCE.md`](./EVIDENCE-AND-PROVENANCE.md) for the exact source/publisher/runtime boundary and fail-closed QA items.

## Black Arcana integration disposition

No new Black Arcana runtime integration is justified by installation alone. The existing addon already owns the narrow bridge. If a future BA mechanic needs equivalent classification, use a proven provider-native exact-version seam behind a BA-owned adapter rather than mirroring registries or duplicating matching logic.

Phase 3 remains blocked until the full provider catalog/deduplication pass establishes real Black Arcana gaps.