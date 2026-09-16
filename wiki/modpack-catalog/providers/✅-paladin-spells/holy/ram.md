# Ram

- **Status:** PRESENTE — released
- **ID:** `paladin_spells:ram`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 15–60
- **Cooldown:** 10 s
- **Spell power neutral:** 4–13
- **Role:** armor-scaling short dash + melee-like AoE hit

## Damage and movement

`damage = 1.25*armor + getSpellPower + 2*spellLevel`

With neutral spell power this simplifies to:

`damage = 1.25*armor + 3*level + 3`

so level 1 = `1.25*armor + 6`, level 10 = `1.25*armor + 33` before external armor/spell-power changes.

Dash scale:

`multiplier = getSpellPower/3`

The spell normalizes horizontal look direction, scales by that multiplier, writes `ImpulseCastData`, directly changes delta movement and creates a swept AABB by expanding the caster box toward the dash vector plus 1.5 blocks.

Every alive `LivingEntity` in that box except the caster is:

- hurt with `entity.damageSources().mobAttack(entity)`;
- knocked back at 1.5 strength.

## Authority / PvP risk

There is no ally/team/friendly-fire filter in the spell's target predicate. Therefore party/PvP behavior is `LIVE QA REQUIRED`; a global game rule may still alter damage settlement.

The spell uses **mobAttack**, not an Iron's spell damage source, which matters for perks that trigger specifically from spell-damage provenance. Do not relabel Ram damage as spell damage without an explicit bridge contract.

## Static movement quirk

When grounded, source calls `vec.add(0,0.25,0)` without assigning the returned immutable `Vec3`. The intended extra Y component may therefore be lost. The spell separately raises caster position by 1.5 blocks, so this is a source-level quirk, not proof that the dash fails in gameplay.

## Mandatory matrix

- range/duration: dash scale formula above; exact traveled blocks depend on movement/collision and are `NÃO VERIFICADO`;
- damage type/provenance: vanilla `mobAttack` confirmed;
- targets: all alive LivingEntity except caster in swept box; FF policy external `NÃO VERIFICADO`;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- sound: `RAM`; VFX/animation details beyond movement `NÃO VERIFICADO`;
- dedup: occupies armor-scaling Holy charge/dash attack;
- fail-closed: do not duplicate hit scan, movement impulse, damage or knockback.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `RamSpell`.
