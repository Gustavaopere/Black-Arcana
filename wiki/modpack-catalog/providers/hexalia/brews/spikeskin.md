# Brew of Spikeskin

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE VERIFIED / ATTRIBUTE EFFECTIVE VALUES + REFLECTION PATH REQUIRE QA`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_spikeskin`
- Effect ID: `hexalia:spikeskin`
- Acquisition: Small Cauldron
- Base duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `hexalia:celestial_crystal`
2. `minecraft:iron_nugget`
3. `minecraft:sweet_berries`
4. `hexalia:tree_resin`

Result: `hexalia:brew_of_spikeskin`.

## Registered attribute surface

At the exact 1.3.6 pin, `ModMobEffects` registers Spikeskin with two attribute templates:

- `ARMOR`, raw amount `0.0`, operation `ADD_VALUE`;
- `MOVEMENT_SPEED`, raw amount `-0.10`, operation `ADD_MULTIPLIED_TOTAL`.

The custom `SpikeskinEffect` is constructed with `modifier=3.0D` and overrides `adjustModifierAmount(int amplifier, AttributeModifier modifier)` to return:

`3.0 × (amplifier + 1)`

without branching on which `AttributeModifier` was supplied.

### Effective-value caveat

Because the same override is defined for the whole effect while two different attribute templates are registered, the source is not safely summarized as simply “+3 armor and -10% speed” without confirming the exact mapped/API application semantics used by this 1.3.6 build.

The catalog therefore records the raw registrations and override separately rather than inventing the final effective attribute pair.

Status:

`EFFECTIVE ARMOR/MOVEMENT MODIFIERS = SOURCE STRUCTURE KNOWN / EXACT APPLIED VALUES REQUIRE BUILD-RUNTIME QA`.

## Reflected-damage claim

The provider localization and Verdant Grimoire describe Spikeskin as:

- increasing armor;
- reflecting a portion of incoming damage;
- reducing movement speed.

A repo-wide audit at the exact 1.3.6 pin located Spikeskin in effect registration, item/recipe/data/localization and `SpikeskinEffect`. The effect class itself contains only the modifier-adjustment logic, and no Spikeskin-specific incoming-damage/reflection handler was located during this audit.

Therefore:

`DAMAGE REFLECTION = PUBLIC DESCRIPTION / IMPLEMENTATION PATH NOT LOCATED / RUNTIME QA REQUIRED`.

Black Arcana must not synthesize the advertised reflection behavior on Hexalia's behalf.

## Deduplication

At semantic level, Hexalia owns the prepared witch-brew concept of defensive armor/retaliation with a mobility tradeoff. Black Arcana should not create a generic copy based solely on those three presentation traits.

A distinct Black Arcana ward/barrier remains possible only when its authority, resource settlement, geometry, hazard and lifecycle contracts differ materially.

## Authority

Hexalia owns the MobEffect and attribute mutation. Black Arcana does not reapply armor/speed, reflect damage a second time, or convert incoming hits into repeated casts/mastery merely because Spikeskin is active.
