# Brew of Bloodlust

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE VERIFIED / DOCUMENTED LIFESTEAL-STRENGTH PATH NOT LOCATED / RUNTIME QA REQUIRED`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_bloodlust`
- Effect ID: `hexalia:bloodlust`
- Acquisition: Small Cauldron
- Base effect duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `hexalia:mandrake`
2. `hexalia:spirit_powder`
3. `hexalia:tree_resin`
4. `minecraft:rotten_flesh`

Result: `hexalia:brew_of_bloodlust`.

## Efeito diretamente comprovado no source

`BloodlustEffect` ticks continuously and inspects all active MobEffects on the affected entity. It removes every active effect whose registry **path** contains the substring `regeneration`.

Consequences of the exact source path:

- vanilla Regeneration is removed;
- a modded effect whose registry path also contains `regeneration` can be caught by the same predicate;
- the predicate is name/path based, not a generic healing-block contract.

The registered Bloodlust effect also declares an `ATTACK_DAMAGE` attribute modifier with base amount `0.0`, operation `ADD_VALUE`.

## Public-description/source mismatch

The Verdant Grimoire describes Bloodlust as allowing the user to heal from damage dealt while preventing natural regeneration. Other provider localization describes increased strength/restoration behavior.

At the exact 1.3.6 pin:

- the `BloodlustEffect` class proves the regeneration-effect removal described above;
- its constructor receives `3.0D`, but that argument is not stored or used by the class;
- the registered attack-damage modifier has raw amount `0.0`;
- repo-wide search during this audit did **not** locate a Bloodlust-specific damage/lifesteal event path implementing the advertised heal-from-damage behavior.

Therefore the strongest current classification is:

- regeneration-effect suppression: `SOURCE-CONFIRMED 1.3.6`;
- lifesteal/heal-from-damage: `PUBLIC DESCRIPTION / IMPLEMENTATION PATH NOT LOCATED / RUNTIME QA REQUIRED`;
- effective strength/damage increase: `PUBLIC DESCRIPTION + ZERO RAW ATTRIBUTE MODIFIER / EXACT EFFECT NOT PROVEN`.

This discrepancy must not be papered over by assuming the intended design is the actual runtime behavior.

## Blood-domain deduplication

Bloodlust is **blood-themed witchcraft**, not a blood-volume resource authority. It does not establish:

- a stored blood fluid;
- Hematic Reservoir capacity;
- blood-only spell payment;
- persistent blood binding;
- provider-independent life-cost settlement.

It does occupy the semantic space of a prepared offensive/lifesteal-style witch brew. Black Arcana should not clone that consumable identity, while its reservoir/binding architecture remains distinct.

## Authority

Hexalia owns the brew/effect state. Black Arcana does not turn each damage event or effect tick into a cast, does not synthesize missing lifesteal behavior, and does not double-settle healing/progression if a verified provider path is later identified.
