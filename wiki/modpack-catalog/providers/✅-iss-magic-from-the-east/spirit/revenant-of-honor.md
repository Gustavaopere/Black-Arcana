# Revenant of Honor

- **ID:** `iss_magicfromtheeast:revenant_of_honor`
- **School:** Spirit
- **Levels:** 1–5
- **Min rarity:** Rare
- **Cast:** Long, 20 ticks
- **Mana neutral:** 80–220
- **Cooldown:** 240 s
- **Summon lifetime:** 10 min
- **Recast count:** 2
- **Spirit Samurai HP:** `50 + 12.5×level` = 62.5–112.5
- **Attack damage:** `6 + 3×level` = 9–21
- **Armor:** 10

## Contract

Summons one `SpiritSamuraiEntity` at a targeted block within 4 blocks. The creature is posted through `SpellSummonEvent`, equipped with the provider's Soul Katana during finalize-spawn, and registered in `SummonManager`.

The samurai follows/copies its owner's combat targets and uses a dedicated melee animation set including several katana strikes plus a long technique sequence. It is non-pushable, fire immune, ignores drowning/fall damage, uses the spell's damage source for melee hits, and is protected from ordinary damage during its rise animation/provider-friendly damage checks.

## Dedup / authority

Identity = durable named melee companion with dedicated katana moveset, rather than a generic humanoid summon. AI cadence/moveset and lifecycle stay provider-native.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`RevenantOfHonorSpell.java` + `SpiritSamuraiEntity.java`, source 1.1.5.
