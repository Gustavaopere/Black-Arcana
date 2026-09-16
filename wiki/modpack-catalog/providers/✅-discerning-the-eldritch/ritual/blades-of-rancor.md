# Blades Of Rancor

- **ID:** `discerning_the_eldritch:blades_of_rancor`
- **School:** Ritual
- **Levels:** 1–5
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 90–110
- **Spell power neutral:** 5–13
- **Cooldown:** 20 s
- **Recast count:** `spellLevel`
- **Recast window:** 8 s
- **Complexity:** `isComplex=false`, `isSuperComplex=false`

## Acquisition implication

Because it is not complex, `AbstractRitualSpell.allowLooting()` returns true. Crafting remains disabled. This is the one registered DTE Ritual here that participates in generic loot eligibility by the base contract.

## Damage/projectile

`damage = 0.45*spellPower + weaponDamage` → neutral spell component 2.25–5.85 plus weapon.

Creates `BladeOfRancorProjectile` with cursor homing enabled, no gravity, and recasts. Damage source sets **iFrames=0**.

## Dedup

This is a rapid Ritual homing-blade sequence with weapon scaling and zero iFrames; do not duplicate projectile chain or remove iFrame behavior through a second damage settlement.

## Source

`BladesOfRancorSpell.java`, DTE 1.4.4 branch.
