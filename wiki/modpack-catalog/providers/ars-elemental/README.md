# Ars Elemental

Status: `SOURCE SURFACE + ACQUISITION INVENTORY COMPLETE / PER-GLYPH DEFAULTS + RUNTIME QA PENDING`

- Current JAR: `ars_elemental-1.21.1-0.7.10.1.jar`
- Physical SHA-1: `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`
- Mod id: `ars_elemental`
- Runtime version: `0.7.10.1`
- Source checkpoint: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
- Provider class: `ARS NOUVEAU ADDON / GLYPH + RITUAL + FAMILIAR + PERK + GEAR + WORLD SYSTEM PROVIDER`
- Primary casting authority: Ars Nouveau.

The exact source checkpoint is used as a semantic source pin for 0.7.10.1. It is not cryptographic proof that the installed JAR was built from that exact commit.

## Source-pinned surface

The production bootstrap registers:

- 39 production spell parts: 23 effects, 2 cast methods, 2 propagators and 12 creature-category filters;
- 8 rituals;
- 3 familiars;
- 3 Ars perks/threads;
- 12 elemental armor sets, 48 armor pieces total, all registered as Ars perk providers;
- 8 SpellCaster providers;
- 32 EntityTypes;
- 16 mixins: 14 common and 2 client;
- 2 network payloads;
- Ars Source-capable advanced relays plus other elemental machines, foci, bangles, caster tomes and spell infrastructure.

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

## Verified divergences

### Familiar cost descriptions

The Flarecannon and Flashjack book descriptions say their relevant spell costs are reduced by 20%. Their source handlers instead subtract `spell.getCost() * 0.5` from `event.currentCost`. This remains `DESCRIPTION-PATH DIVERGENCE / RUNTIME QA REQUIRED`; the catalog does not choose one behavior by inference.

### License metadata

The exact README and `neoforge.mods.toml` say LGPL v3, while the root `LICENSE` contains GPL v3 text. Phase 2U records the discrepancy and remains clean-room; it does not resolve the license by assumption.

## QA state

Source registry/acquisition/boundary inventory is complete. Individual source-default tier/mana/config behavior still needs normalization where not already audited, and installed-JAR config/client/dedicated/full-pack QA remains pending.

This provider catalog does not promote any Black Arcana runtime Stage.