# Provider Audit Queue Delta — Phase 2U Ars Elemental 0.7.10.1

Status: `SOURCE SURFACE INVENTORY CLOSED / DEEP DEFAULTS + RUNTIME QA OPEN`

## Closed

- installed identity/version/file SHA-1;
- semantic source pin;
- bootstrap reachability;
- 39 production spell-part registry inventory;
- 39 generated glyph acquisition paths;
- eight rituals;
- three familiars;
- three local perks;
- 48 armor perk providers;
- eight SpellCaster providers;
- 32 EntityTypes;
- 16 mixins;
- two network payloads;
- Source/mana/foci/armor authority seams;
- Ars core school/augment modifications;
- worldgen/world-effect boundary;
- license metadata discrepancy.

## Open — source normalization

1. Source-audit every production glyph's exact default tier and mana cost.
2. Source-audit compatible augments, limits and glyph-specific config defaults not already pinned.
3. Confirm exact inherited Source/radius/progress semantics for the two Archwood rituals against the matching Ars Nouveau base implementation.
4. Locate and verify the implementation path behind Summoning Thread's documented 10% Summon Sickness reduction; fail closed if no path is found.
5. Confirm whether Flarecannon/Flashjack effective runtime discounts follow the executable 50%-base-cost calculation or differ due to event ordering/other provider logic.

## Open — installed runtime/config

1. Compare real generated/installed config values against source defaults.
2. Validate 39 glyph registrations and conditional Nullify acquisition in the installed JAR/datapack.
3. Validate familiar event ordering with Ars Nouveau 5.13.1 and other Ars addons in the current pack.
4. Validate armor perk-provider layout and modifier stacking.
5. Validate worldgen, Flashing biome lightning and Archwood rituals in a dedicated-server context.
6. Validate network payload registration and server-side Curio Bag revalidation.
7. Run client/full-pack interoperability QA.

## Open — provenance

Resolve the LGPL-vs-GPL metadata discrepancy before any future source copying, derivative implementation or asset reuse. Phase 2U itself remains clean-room and copies no upstream implementation/assets.

## Merge gate

Before merge: fetch current `main`, reconcile any relevant advancement semantically, inspect the final diff, run CI on the reconciled HEAD and only merge with fresh green evidence.