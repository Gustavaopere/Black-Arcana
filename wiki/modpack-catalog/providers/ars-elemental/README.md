# Ars Elemental

Status: `HIGH-IMPACT CURRENT GLYPHS VERIFIED; COMPLETE ADDON PRIMITIVE PASS STILL OPEN`

- Current JAR: `ars_elemental-1.21.1-0.7.10.1.jar`
- Mod id: `ars_elemental`
- Runtime version: `0.7.10.1`
- Provider class: `ARS GLYPH / SYSTEM PROVIDER`
- Primary casting authority: Ars Nouveau.

## Current verified capability surface

The provider-aware current Ars 1.21.1 guide exposes many `ars_elemental:` primitives. High-impact entries already verified for Phase 2 include:

| Glyph | Registry id | Type / tier | Semantic role |
|---|---|---|---|
| Arc Projectile | `ars_elemental:glyph_arc_projectile` | Form / T2 | gravity-affected projectile / bounce via Pierce |
| Bubble Shield | `ars_elemental:glyph_bubble_shield` | Effect / T2 | mana-backed damage reduction and some debuff protection |
| Charm | `ars_elemental:glyph_charm` | Effect / T2 | temporary hostile domination / tame-love interactions |
| Cauterize | `ars_elemental:glyph_cauterize` | Effect / T3 | self-harming cleanse of milk-curable harmful effects |
| Cavitate | `ars_elemental:glyph_cavitate` | Effect / T3 | water-pressure area damage / soaked interaction |
| Conflagrate | `ars_elemental:glyph_conflagrate` | Effect / T3 | fire-state detonation / secondary explosive behavior |
| Conjure Terrain | `ars_elemental:glyph_conjure_terrain` | Effect / T1 | terrain creation/composition |
| Create Geyser | `ars_elemental:glyph_geyser` | Effect / T2 | temporary geyser / vertical force / soaked interaction |
| Discharge | `ars_elemental:glyph_discharge` | Effect / T2 | consumes shocked/static state into damage / nearby shock |
| Envenom | `ars_elemental:glyph_envenom` | Effect / T2 | poison escalation into stronger venom |
| Homing Projectile | `ars_elemental:glyph_homing_projectile` | Form / T3 | target-seeking projectile |
| Life Link | `ars_elemental:glyph_life_link` | Effect / T3 | bidirectional/reversible damage-healing relationship |
| Mist Cloud | `ars_elemental:glyph_mist` | Effect / T2 | vision denial + mob target loss |
| Nullify Defense | `ars_elemental:glyph_nullify_defense` | Effect / T3 | removes target's post-hit innate immunity window |
| Oxidize | `ars_elemental:glyph_oxidize` | Effect / T3 | temporary armor reduction / block oxidation interaction |
| Phantom Grasp | `ars_elemental:glyph_phantom_grasp` | Effect / T2 | heals undead; harms/exhausts living targets |
| Poison Spores | `ars_elemental:glyph_poison_spores` | Effect / T2 | conditional poison/hunger spreading damage field |
| Propagate Arc | `ars_elemental:glyph_propagator_arc` | Effect / T2 | re-emits remaining chain as Arc Projectile |
| Propagate Homing | `ars_elemental:glyph_propagator_homing` | Effect / T3 | re-emits remaining chain as Homing Projectile |
| Rage | `ars_elemental:glyph_rage` | Effect / T3 | forced hostility/friendly-fire behavior + damage increase |
| Sliding | `ars_elemental:glyph_slip_feet` | Effect / T2 | slippery-foot locomotion state |
| Spark | `ars_elemental:glyph_spark` | Effect / T1 | lightning damage + shocked state, stronger on wet targets |
| Spike | `ars_elemental:glyph_spike` | Effect / T2 | persistent/falling dripstone damage geometry |
| Summon Bee | `ars_elemental:glyph_summon_bee` | Effect / T2 | temporary combat summons + Summoning Sickness |
| Summon Slime | `ars_elemental:glyph_summon_slime` | Effect / T2 | temporary combat summons + Summoning Sickness |
| Water Jet | `ars_elemental:glyph_water_jet` | Effect / T3 | delayed high-pressure armor-ignoring water attack |
| Watery Grave | `ars_elemental:glyph_watery_grave` | Effect / T2 | air-supply depletion / drowning / downward control |

The current guide additionally exposes creature-category filters (`Aerial`, `Aquatic`, `Fiery`, `Insect`, `Summon`, `Undead` and inverse forms). Those are targeting primitives and will be normalized in the full addon pass rather than counted as distinct combat spells.

## Life Link — direct Arcana Vincular overlap

The current public guide describes `Life Link` as follows at the semantic level:

- creates a life-force link between caster and target;
- damage dealt to the caster is shared with the target;
- healing received by the target is shared with the caster;
- `Sensitive` reverses the direction;
- `Cut` can sever the link.

This is direct mechanical overlap with any proposed Black Arcana spell whose sole identity is “link two beings and share damage/healing”.

Black Arcana's prospective **Arcana Vincular** delta must therefore be broader and infrastructural:

- persistent typed links rather than one generic health-sharing effect;
- explicit ownership and consent/protection gates;
- sources such as blood reservoir, spirit inventory, familiar/servant, ritual artifact or living donor;
- transactional reserve/commit/refund for cast costs;
- fail-closed behavior when the linked source is unavailable;
- no recursive damage/heal loops across providers;
- canonical link lifecycle, persistence and cleanup.

## Chaos overlap

`Charm`, `Rage`, homing/propagation, pressure/fire detonations and state-driven combos occupy many effects that could visually resemble chaos magic. They do not prove entropy/reality manipulation, but they eliminate generic mind-control, random-looking projectile and explosive-state mechanics as sufficient deltas.

## Order overlap

`Bubble Shield`, `Nullify Defense`, creature filters and state-aware control already supply protection/filter/constraint primitives. Order requires a server-authoritative law/seal layer, not a renamed Ars filter or barrier.

## Witchcraft / toxin overlap

`Envenom`, `Poison Spores`, `Charm`, `Rage` and `Phantom Grasp` directly intersect poison, curse, domination and occult-support fantasies. Hexalia/Toxony must be cataloged alongside this provider before integrated Witchcraft is finalized.

## Provenance / confidence

- Presence/version: current modlist — HIGH.
- Registry IDs and semantics above: current provider-aware Ars 1.21.1 guide — HIGH.
- Complete Ars Elemental inventory: still `IN PROGRESS`; the table is a high-impact subset, not a false claim of completeness.
- No Java bytecode was decompiled.
