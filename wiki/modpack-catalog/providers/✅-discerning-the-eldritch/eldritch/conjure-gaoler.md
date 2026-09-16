# Conjure: Gaoler

- **ID:** `discerning_the_eldritch:conjure_gaoler`
- **School:** Eldritch
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 100 ticks / 5 s
- **Mana:** 500
- **Spell power neutral:** 25
- **Cooldown:** 600 s
- **Summon lifetime:** 60 s
- **Neutral Gaoler damage:** 112.5
- **Neutral Gaoler HP:** 512.5

## Acquisition/cast gates

- `canBeCraftedBy=false`;
- `allowCrafting=false`;
- `allowLooting=false`;
- `requiresLearning=false`;
- cast is uninterruptible.

Concrete source that grants access outside normal scroll crafting/loot: `NÃO VERIFICADO` in this pass.

## Contract

Pre-cast applies Darkness to LivingEntities in 15-block radius for the cast duration, Darkness to caster, `PORTENT_EFFECT` to caster for 100 ticks, and a grayscale shader to ServerPlayer.

Spawn point is ~6 blocks behind the caster. Stats:

- attack = `4.5 * spellPower`;
- max health = `20.5 * spellPower`.

The Gaoler is posted through `SpellSummonEvent` then initialized by `SummonManager`.

### King's Effigy branch

With King's Effigy equipped, the Gaoler behaves as a managed summon/recast and `getRecastCount=2`. Without it, the Gaoler is spawned with `isFeral=true` and immediately removed from `SummonManager` after initialization — i.e. the provider intentionally releases it from standard summon ownership.

## Dedup / safety

A Black Arcana summon bridge must preserve the managed-vs-feral branch; silently taming the no-Effigy Gaoler changes spell identity. Do not duplicate Darkness, shader, summon event, entity stats or lifecycle.

AI target rules and whether feral Gaoler can attack the caster are entity-native; public documentation says this risk exists, but final AI internals are `NÃO VERIFICADO` here.

## Source

`ConjureGaolerSpell.java`, branch `1.21@7bbd81f...`.
