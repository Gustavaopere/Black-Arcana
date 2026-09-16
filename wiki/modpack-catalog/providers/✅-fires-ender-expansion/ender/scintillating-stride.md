# Scintillating Stride

- ID: `firesenderexpansion:scintillating_stride`
- School: `irons_spellbooks:ender`
- Levels: 1–10
- Min rarity: Common
- Cast: Instant
- Mana neutral: 20 / 22 / 24 / 26 / 28 / 30 / 32 / 34 / 36 / 38
- Spell power neutral: 1–10
- Blast damage neutral: 5.5–10.0
- Dash force neutral: 1.02–1.20
- Radius: `clamp(spellPower/10, 1, 3)`; neutral levels remain radius 1, bonus spell power can increase it
- Recast/effect window: 100 ticks (5 s)
- Recast count: 2
- Cooldown: 10 s

## Contract

The first activation opens the recast window, pushes the caster forward/up and applies `striding_effect`. The effect records the caster's exact position and dimension.

On successful recast finish, the provider performs a local Ender damage blast around the caster, then removes Striding. Effect removal posts `SpellTeleportEvent` and uses Iron's `Utils.handleSpellTeleport` to return the entity to its recorded origin, then zeroes movement. If the caster changed dimension, the effect refuses the return and emits a failure message.

## QA finding — blast eligibility

The provider-side loop calls `DamageSources.applyDamage` for living entities in the inflated caster bounding box without an explicit self/allied filter in `ScintillatingStrideSpell`. Runtime behavior under Iron's 3.16.3 must be tested before a bridge assumes self/friendly immunity.

## Dedup / authority

Dash impulse, recorded-position ledger, return teleport and blast are one provider-native sequence. Do not add a parallel return marker or a second explosion.

## Acquisition

Default Iron's spell eligibility; exact loot/crafting distribution: **NÃO VERIFICADO**.

## Source

`ScintillatingStrideSpell.java`, `StridingEffect.java` @ pin `5e4067e...`.