# Phase 2U — Ars Elemental 0.7.10.1 checkpoint

Status: `SOURCE SURFACE + ACQUISITION INVENTORY COMPLETE / PER-GLYPH DEFAULT NORMALIZATION + RUNTIME QA PENDING`

Execution branch: `docs/magic-catalog-phase2u-ars-elemental`
Base main at phase start: `019eb1723b7a70b9fd888ce44d1eb9b85dfa7b13`
Provider source pin: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
Physical JAR: `ars_elemental-1.21.1-0.7.10.1.jar`
Physical SHA-1: `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`

## Closed source surface

- exact mod id `ars_elemental` and runtime version 0.7.10.1 confirmed;
- production bootstrap and post-init path confirmed;
- 39/39 production glyph registrations identified;
- 39/39 generated glyph acquisition recipes identified;
- `MethodCarianPhalanx` excluded from production glyph count because registration is gated by `!isProduction()`;
- 8/8 ritual registrations identified and source behavior classified;
- 3/3 familiar holders identified and behavior classified;
- 3/3 local perks identified;
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
3. Exact README and `neoforge.mods.toml` declare LGPL v3, while root `LICENSE` contains GPL v3 text.

No divergence is resolved by inference. Runtime/license questions remain fail-closed where applicable.

## Remaining Phase 2U work

- normalize exact source-default tier, mana, augment limits and per-glyph config for production glyphs not yet individually source-audited;
- verify inherited ritual defaults where behavior comes from Ars Nouveau base ritual classes;
- locate the provider implementation path, if any, for Summoning Thread's documented Summon Sickness reduction;
- compare installed config with source defaults;
- client, dedicated-server and full-modpack QA;
- final main synchronization, CI and merge.

This checkpoint is documentation/catalog state only. It does not promote a Black Arcana runtime Stage.