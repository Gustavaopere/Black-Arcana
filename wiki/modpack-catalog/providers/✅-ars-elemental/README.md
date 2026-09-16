# Ars Elemental

Status: `SOURCE CATALOG COMPLETE / INSTALLED CONFIG + RUNTIME QA PENDING`

- Current JAR: `ars_elemental-1.21.1-0.7.10.1.jar`
- Physical SHA-1: `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`
- Mod id: `ars_elemental`
- Runtime version: `0.7.10.1`
- Source checkpoint: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
- Ars Nouveau 5.13.1 API checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Provider class: `ARS NOUVEAU ADDON / GLYPH + RITUAL + FAMILIAR + PERK + GEAR + WORLD SYSTEM PROVIDER`
- Primary casting authority: Ars Nouveau.

The exact source checkpoint is used as a semantic source pin for 0.7.10.1. It is not cryptographic proof that the installed JAR was built from that exact commit.

## Source-pinned surface

The production/source audit closes:

- 39/39 production spell parts: 23 effects, 2 cast methods, 2 propagators and 12 creature-category filters;
- exact source-default tier/mana plus compatible augments and provider-specific config/limit knobs for all 39 spell parts;
- 39/39 generated glyph learning recipes;
- 8/8 rituals, including inherited Ars 5.13.1 semantics for both Archwood rituals;
- 3/3 familiars;
- 3/3 Ars perks/threads and their event/attribute paths;
- 12 elemental armor sets, 48 armor pieces total, all registered as Ars perk providers;
- 8 SpellCaster providers;
- 32 EntityTypes;
- 16/16 mixins: 14 common and 2 client;
- 2/2 registered network payloads;
- Ars Source-capable advanced relays plus elemental machines, foci, bangles, caster tomes and spell infrastructure;
- provider worldgen and Ars-core mutation boundaries.

`MethodCarianPhalanx` exists in source but is only registered under `!isProduction()`. It is not part of the production JAR glyph surface.

See:

- [GLYPHS.md](GLYPHS.md)
- [ACQUISITION.md](ACQUISITION.md)
- [RITUALS.md](RITUALS.md)
- [FAMILIARS.md](FAMILIARS.md)
- [PERKS.md](PERKS.md)
- [SYSTEMS.md](SYSTEMS.md)
- [MIXIN-BOUNDARIES.md](MIXIN-BOUNDARIES.md)
- [REGISTRIES.md](REGISTRIES.md)

## Authority and deduplication

Ars Nouveau and Ars Elemental remain authority for their own mana, Source, glyph resolution, spell-cost calculation, spell modifiers, familiars, rituals, perk threads, elemental gear, entities and provider world effects.

Black Arcana must not:

- settle a second mana/Source cost for a provider cast;
- treat child projectiles, propagators or familiar event callbacks as new root casts;
- replay provider block mutation, biome conversion, lightning, summons or ritual effects;
- duplicate perk/focus/familiar damage or cost modifiers;
- derive gameplay authority from client VFX or rendering state.

Independent Black Arcana destructive effects still pass through `WorldEffectPolicy`.

## High-impact overlaps

### Arcana Vincular

`ars_elemental:glyph_life_link` directly occupies generic damage/healing life-link semantics. Black Arcana's Vincular identity therefore requires a larger typed-link infrastructure: explicit ownership/consent rules, persistence/lifecycle, transactional cost sources, failure behavior and loop prevention.

### Chaos

Charm, Rage, state detonations, homing/propagation and Randomize-compatible effects mean that generic mind control, explosions or visually erratic projectiles are not a sufficient Chaos delta.

### Order

Bubble Shield, Nullify Defense and the twelve targeting filters already provide protection/filter/constraint primitives. Order requires canonical law/seal/contract semantics rather than renamed filters or barriers.

### Witchcraft / toxin

Envenom, Poison Spores, Charm, Rage and Phantom Grasp overlap toxin, curse, domination and occult-support fantasies.

## Verified source divergences

### Familiar cost descriptions

The Flarecannon and Flashjack book descriptions say their relevant spell costs are reduced by 20%. Their source handlers instead subtract `spell.getCost() * 0.5` from `event.currentCost`. This remains `DESCRIPTION-PATH DIVERGENCE / RUNTIME QA REQUIRED`; the catalog does not choose one behavior by inference.

### Summoning Thread sickness description

The provider description says Summoning Sickness is reduced by 10% per tier. The exact event handler multiplies duration by `1 - countForPerk(...) / 10`. Ars 5.13.1 `countForPerk` returns the maximum worn slot value; for ordinary values 1–3, Java integer division makes the divisor term 0 and leaves the source-path multiplier at 1. This remains `DESCRIPTION-PATH DIVERGENCE / RUNTIME QA REQUIRED`.

### License metadata

The exact README and `neoforge.mods.toml` say LGPL v3, while the root `LICENSE` contains GPL v3 text. Phase 2U records the discrepancy and remains clean-room; it does not resolve the license by assumption.

## QA state

The source catalog is complete for the pinned surface and dependencies used by this phase. Still pending are comparison against the real installed/generated Ars Elemental config/datapack and runtime/client/dedicated/full-modpack interoperability checks. Those pending observations do not convert source defaults into installed-runtime claims.

This provider catalog does not promote any Black Arcana runtime Stage.
