# Ars Elemental 0.7.10.1 — production glyph surface

Status: `39/39 PRODUCTION REGISTRATIONS SOURCE-PINNED / INDIVIDUAL DEFAULT NORMALIZATION PARTIAL`

Source checkpoint: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`

`ArsNouveauRegistry.registerGlyphs()` is the production registration authority. `GlyphRegistry.registerSpell(...)` is called for every entry below.

## Effects — 23

| Registry id | Role |
|---|---|
| `ars_elemental:glyph_watery_grave` | air depletion, drowning/downward control |
| `ars_elemental:glyph_bubble_shield` | mana-backed defensive coating |
| `ars_elemental:glyph_conjure_terrain` | terrain placement/composition |
| `ars_elemental:glyph_charm` | temporary domination / tame-love interactions |
| `ars_elemental:glyph_phantom_grasp` | undead healing; living magic damage/exhaustion |
| `ars_elemental:glyph_life_link` | life-force damage/healing linkage |
| `ars_elemental:glyph_poison_spores` | poison/hunger spreading damage field |
| `ars_elemental:glyph_envenom` | poison escalation |
| `ars_elemental:glyph_spike` | persistent/falling dripstone geometry |
| `ars_elemental:glyph_discharge` | shocked/static discharge interaction |
| `ars_elemental:glyph_spark` | lightning damage + shocked state |
| `ars_elemental:glyph_conflagrate` | fire-state detonation |
| `ars_elemental:glyph_cauterize` | harmful-effect cleanse with self-harm tradeoff |
| `ars_elemental:glyph_rage` | forced hostility/friendly-fire behavior |
| `ars_elemental:glyph_water_jet` | delayed high-pressure water attack |
| `ars_elemental:glyph_geyser` | temporary geyser / vertical force |
| `ars_elemental:glyph_mist` | vision denial / mob targeting disruption |
| `ars_elemental:glyph_slip_feet` | slippery locomotion state |
| `ars_elemental:glyph_cavitate` | water-pressure area damage |
| `ars_elemental:glyph_oxidize` | armor/block oxidation interaction |
| `ars_elemental:glyph_summon_bee` | temporary bee summon |
| `ars_elemental:glyph_summon_slime` | temporary slime summon |
| `ars_elemental:glyph_nullify_defense` | removes/changes target post-hit defense window |

The semantic role column preserves the already-audited provider-aware Phase 2 descriptions. Registration and acquisition are source-pinned here; source-default tier/mana values are not claimed complete unless separately verified.

## Cast methods — 2

- `ars_elemental:glyph_homing_projectile`
- `ars_elemental:glyph_arc_projectile`

Arc Projectile is source-confirmed T2 with default mana 10 and gravity. Homing remains registered in production and is acquisition-pinned; its complete defaults remain in the per-glyph normalization queue.

## Propagators — 2

- `ars_elemental:glyph_propagator_homing`
- `ars_elemental:glyph_propagator_arc`

These re-emit the remaining provider spell chain through the corresponding projectile semantics. They remain part of one Ars causal cast and must not produce a second Black Arcana settlement.

## Filters — 12

`ElementalAbstractFilter` extends Ars `AbstractFilter`, uses type index `15`, and cancels `SpellContext` resolution when the target fails its condition. Normal/inverted variants are separate registered spell parts.

- `ars_elemental:glyph_aquatic_filter`
- `ars_elemental:glyph_not_aquatic_filter`
- `ars_elemental:glyph_fiery_filter`
- `ars_elemental:glyph_not_fiery_filter`
- `ars_elemental:glyph_aerial_filter`
- `ars_elemental:glyph_not_aerial_filter`
- `ars_elemental:glyph_insect_filter`
- `ars_elemental:glyph_not_insect_filter`
- `ars_elemental:glyph_undead_filter`
- `ars_elemental:glyph_not_undead_filter`
- `ars_elemental:glyph_summon_filter`
- `ars_elemental:glyph_not_summon_filter`

These are targeting primitives, not proof of a Black Arcana Order/law system.

## Production exclusion

`MethodCarianPhalanx.INSTANCE` is registered only when `!isProduction()`. The associated source class/EntityType does not make the glyph production-accessible.

## Direct source-confirmed examples

- Bubble Shield: Water school, T2, default mana 400; applies provider mana bubble only when target has Ars mana capability. Default absorption cost config is 350 mana per mitigation.
- Watery Grave: Water school, T2, default mana 25; drains air or damages by drowning and can start Zombie-to-Drowned conversion.
- Conjure Terrain: Conjuration + Earth, default mana 20; places terrain and composes with Conjure Water, Crush and Smelt.
- Charm: T2, default mana 30; server-side player caster path, blacklist-aware and health-limited by config.
- Phantom Grasp: Necromancy, T2, default mana 50; heals inverted-heal targets and damages/exhausts living targets.

## Remaining normalization

Exact source-default tier, mana, augment limits and config knobs for every remaining production glyph remain a Phase 2U documentation task. No unspecified default is inferred from Ars Nouveau core.