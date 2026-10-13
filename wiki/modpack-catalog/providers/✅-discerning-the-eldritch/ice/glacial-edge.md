# Glacial Edge / Glacial Cleave

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `discerning_the_eldritch:glacial_edge` / `net.acetheeldritchking.discerning_the_eldritch.spells.ice.GlacialEdgeSpell`, escola `SchoolRegistry.ICE_RESOURCE`. [Java 21 #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207); [dossiê](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Custos/mecânicas runtime e Survival ⚠️. +0.

- **Registry ID:** `discerning_the_eldritch:glacial_edge`
- **Class:** `GlacialEdgeSpell`
- **Public-facing alias:** Glacial Cleave
- **School:** Ice
- **Levels:** 1–8
- **Min rarity:** Rare
- **Cast:** Long, 20 ticks
- **Mana neutral:** 55–90
- **Spell power neutral:** 15–29
- **Cooldown:** 25 s
- **Base damage:** `0.25*spellPower` = neutral 3.75–7.25

## Frozen weapon bonus

If main-hand is in `DTETags.FROZEN_WEAPONS`, projectile damage is multiplied by **1.5**. Neutral spell-only component becomes ~5.625–10.875.

The spell creates provider `GlacialEdge` projectile and injects the final damage.

Its `SpellDamageSource` sets **80 freeze ticks**.

## Dedup / authority

Identity = Ice sword-wave projectile + Frozen Weapon synergy + freeze-on-damage. Do not add a second frozen-weapon multiplier or freeze settlement in Black Arcana.

Projectile travel/hitbox/friendly-fire details remain entity-native / `NÃO VERIFICADO`.

## Source

`GlacialEdgeSpell.java`, DTE 1.4.4 branch.
