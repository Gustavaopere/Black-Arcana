# Phantom Charge

- **ID:** `iss_magicfromtheeast:phantom_charge`
- **School:** Spirit
- **Levels:** 1–6
- **Min rarity:** Rare
- **Cast:** Instant
- **Mana neutral:** 45–120
- **Spell power neutral:** 6–16
- **Cooldown:** 80 s
- **Cavalry rows/entities:** `spellLevel` = 1–6
- **Tooltip damage:** `0.5 × spell power` = 3–8
- **Runtime entity damage assigned by spell:** full spell power = 6–16

## Contract

Spawns `spellLevel` `PhantomCavalryVisualEntity` projectiles in alternating left/right offsets around the caster and launches them forward. Each travels at speed 1 for ~40 ticks and performs custom continuous hit detection. On living targets it suppresses the next knockback, applies Slowness and Weakness for 80 ticks (4 s), then applies the stored Spirit damage. The entity class does not discard on an entity hit, allowing its path to threaten multiple entities.

## Dedup / authority

Identity = short-lived advancing cavalry wall with debuff-on-contact, not a conventional single projectile.

## QA — tooltip/runtime divergence

`getUniqueInfo()` displays `getSpellPower()/2`, but `onCast()` calls `phantomCavalry.setDamage(getSpellPower(...))`; the entity applies that full stored damage. Static source therefore supports **full power runtime assignment**, while UI advertises half. Preserve both until runtime verification or upstream correction.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`PhantomChargeSpell.java` + `PhantomCavalryVisualEntity.java`, source 1.1.5.
