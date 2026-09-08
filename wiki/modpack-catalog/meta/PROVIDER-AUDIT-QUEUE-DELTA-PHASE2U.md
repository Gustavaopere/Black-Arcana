# Provider Audit Queue Delta — Phase 2U Ars Elemental 0.7.10.1

Status: `SOURCE CATALOG CLOSED / INSTALLED CONFIG + RUNTIME QA OPEN`

## Closed — source catalog

- installed identity/version/file SHA-1;
- semantic provider source pin plus exact Ars Nouveau 5.13.1 API pin used for inheritance;
- bootstrap reachability;
- 39 production spell-part registry inventory;
- 39 generated glyph acquisition paths;
- exact source-default tier and mana for all 39 production glyphs;
- compatible augments, explicit augment limits/cost overrides and provider-specific config defaults for the 39-glyph surface;
- inherited Tier I/filter defaults from exact Ars 5.13.1 where the addon does not override them;
- eight rituals;
- exact inherited radius/Source/progress semantics for both Archwood rituals;
- three familiars;
- three local perks;
- exact Summoning Thread sickness event path and its integer-division divergence;
- 48 armor perk providers;
- eight SpellCaster providers;
- 32 EntityTypes;
- 16 mixins;
- two network payloads;
- Source/mana/foci/armor authority seams;
- Ars core school/augment modifications;
- worldgen/world-effect boundary;
- license metadata discrepancy.

## Source divergences carried into runtime QA

1. Flarecannon description says 20% projectile-spell cost reduction; executable source subtracts 50% of base spell cost from `currentCost`.
2. Flashjack description says 20% movement-spell cost reduction; executable source subtracts 50% of base spell cost from `currentCost`.
3. Summoning Thread description says 10% Summoning Sickness reduction per tier; exact handler uses `1 - countForPerk(...) / 10`. With Ars 5.13.1 maximum slot values 1–3, integer division leaves the source-path multiplier at 1.
4. Cavitate's pre-config duration fallbacks are 15/5, but its built source config calls Ars `addDefaultPotionConfig`, producing configured defaults 30/8. The catalog records configured source defaults as 30/8.
5. Oxidize reads a Randomize buff count in its block path although Randomize is not in its compatible-augment set at the pin.
6. Summon Slime reads amplification for slime size although Amplify is not in its compatible-augment set at the pin.

These are factual source observations, not automatic bug fixes or runtime conclusions.

## Open — installed runtime/config

1. Compare real generated/installed Ars Elemental config values against the source-default catalog.
2. Validate 39 glyph registrations and conditional Nullify acquisition in the installed JAR/datapack.
3. Validate familiar event ordering with Ars Nouveau 5.13.1 and other Ars addons in the current pack.
4. Measure Flarecannon/Flashjack effective cost reduction in runtime.
5. Measure Summoning Thread sickness reduction in runtime.
6. Validate armor perk-provider layout and modifier stacking.
7. Validate worldgen, Flashing-biome lightning and Archwood rituals in a dedicated-server/full-pack context.
8. Validate network payload registration and server-side Curio Bag revalidation.
9. Run client/full-pack interoperability QA.

## Open — provenance

Resolve the LGPL-vs-GPL metadata discrepancy before any future source copying, derivative implementation or asset reuse. Phase 2U itself remains clean-room and copies no upstream implementation/assets.

## Merge gate

Before merge: fetch current `main`, reconcile any relevant advancement semantically, inspect the final PR diff, run CI on the reconciled HEAD and only merge with fresh green evidence. Runtime/config observations above may remain explicitly deferred because this PR is a source catalog; they must not be reported as validated runtime behavior.
