# Phase 2U — Ars Elemental 0.7.10.1 checkpoint

Status: `SOURCE CATALOG COMPLETE / FINAL MAIN RECONCILED / INSTALLED CONFIG + RUNTIME QA DEFERRED`

Execution branch: `docs/magic-catalog-phase2u-ars-elemental`
Base main at phase start: `019eb1723b7a70b9fd888ce44d1eb9b85dfa7b13`
Final pre-merge reconciliation: `main@db7f4858b3c5eda3bba957db7de194228b6d4df6` merged into the execution branch through synchronization PR #113; branch reconciliation checkpoint `09ec2220978850b50f070aee9414e2f1ae434033`.
Provider source pin: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
Ars Nouveau 5.13.1 API pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
Physical JAR: `ars_elemental-1.21.1-0.7.10.1.jar`
Physical SHA-1: `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`

## Closed source catalog

- exact mod id `ars_elemental` and runtime version 0.7.10.1 confirmed;
- production bootstrap and post-init path confirmed;
- 39/39 production glyph registrations identified;
- 39/39 generated glyph acquisition recipes identified;
- 39/39 production glyph source defaults normalized for tier, mana, compatible augments and provider-specific config/limit behavior;
- Ars Nouveau inherited Tier I/filter defaults pinned where the addon does not override them;
- `MethodCarianPhalanx` excluded from production glyph count because registration is gated by `!isProduction()`;
- 8/8 ritual registrations identified and source behavior classified;
- exact Ars 5.13.1 inheritance pinned for `ConjureBiomeRitual` and `FeaturePlacementRitual` used by the two Archwood rituals;
- 3/3 familiar holders identified and behavior classified;
- 3/3 local perks identified, including the Summoning Thread sickness event path;
- 48/48 elemental armor perk providers identified across 12 sets;
- 8 SpellCaster providers identified;
- 32 EntityTypes inventoried;
- 16/16 mixins classified;
- 2/2 registered network payloads classified;
- Ars Source capability seam, focus/armor resource behavior, school/augment mutations and worldgen boundaries classified;
- clean-room provenance and license-metadata divergence documented.

## Important divergences

1. Flarecannon book text says 20% projectile-spell cost reduction; executable source subtracts 50% of base spell cost from current cost.
2. Flashjack book text says 20% movement-spell cost reduction; executable source subtracts 50% of base spell cost from current cost.
3. Summoning Thread text says 10% Summoning Sickness reduction per tier; the exact event handler uses integer division `countForPerk(...) / 10`, while Ars 5.13.1 `countForPerk` returns the maximum slot value. Ordinary slot values 1–3 therefore leave the observed source-path multiplier at 1.
4. Exact README and `neoforge.mods.toml` declare LGPL v3, while root `LICENSE` contains GPL v3 text.

No divergence is resolved by inference. Runtime/license questions remain fail-closed where applicable.

## Source-default clarifications closed in this checkpoint

- Spark inherits Ars Tier I and has provider default mana 15.
- All twelve creature filters inherit Ars Tier I / 0 mana / no compatible augments.
- Nullify Defense is Tier III / 1000 mana / Necromancy / no augments; its executable effect resets `LivingEntity.invulnerableTime` to 0. Its normal generated learning recipe remains config-gated with source default disabled.
- Conjure Island: Archwood Forest inherits radius 7, +1 radius per consumed Source Gem, `getSourceCost() = 50`, and a Source request after every five successful block placements.
- Forestation — Archwood inherits radius 7, +1 radius per consumed Source Gem and `getSourceCost() = 0` from `AbstractRitual`.

## Deferred installed-runtime/config validation

- compare real generated/installed Ars Elemental config and datapack values against the source defaults;
- validate the 39 glyph registrations and conditional Nullify acquisition in the installed runtime;
- validate familiar event ordering and the two 20%-text/50%-source cost divergences with Ars Nouveau 5.13.1 and the current addon set;
- validate Summoning Thread sickness duration behavior in runtime;
- validate armor perk-provider layout/modifier stacking;
- validate worldgen, Flashing-biome lightning and Archwood rituals in dedicated-server/full-pack runtime;
- validate network payload registration/server Curio Bag revalidation and client behavior;
- resolve license metadata discrepancy before any future source copying/derivative implementation/asset reuse.

These are runtime/config/provenance gates, not missing source-catalog entries, and they are not reported as PASS by Phase 2U.

## Final merge gate

- current `main` reconciliation: complete through PR #113 against `main@db7f4858b3c5eda3bba957db7de194228b6d4df6`;
- final catalog-only diff review: complete before this checkpoint update; no Java/runtime/Gradle/workflow path is part of Phase 2U;
- exact final execution HEAD CI: must be GREEN after this checkpoint commit;
- review threads: must remain clear;
- merge: only after the exact final HEAD satisfies the gates above.

This checkpoint is documentation/catalog state only and does not promote a Black Arcana runtime Stage.