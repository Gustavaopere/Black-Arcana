# Esoteric Edge

- **ID:** `discerning_the_eldritch:esoteric_edge`
- **School:** Eldritch
- **Levels:** 1–5
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 70–130
- **Spell power neutral:** 20–40
- **Cooldown:** 25 s

## Damage

`damage = 0.77 * getSpellPower + Utils.getWeaponDamage(caster)`.

Neutral spell-only component: 15.4–30.8, then current weapon damage is added. Player spell/Holy? No: Eldritch generic/school/config power modifiers feed `getSpellPower` before the 0.77 factor.

The cast creates a provider `EsotericEdge` projectile/entity, fires it from the caster and injects the computed damage. Flight/collision/lifetime/piercing details remain entity-native.

## Dedup / authority

This is not a generic Eldritch projectile: its identity is **hybrid spell-power + equipped-weapon damage**. A new magic sword wave with the same scaling is high overlap.

Do not add a second weapon-damage contribution in Black Arcana. Projectile hit settlement, friendly-fire and exact damage type details beyond the spell's source remain `NÃO VERIFICADO`.

## Presentation

Ace's Spell Utils right-horizontal sword slash animation; `ESOTERIC_EDGE_SLASH_2` finish sound.

## Source

`EsotericEdgeSpell.java`, branch `1.21@7bbd81f...`.
