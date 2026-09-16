# Crystalline Carver

- **ID:** `discerning_the_eldritch:crystalline_carver`
- **School:** Ice
- **Levels:** 1–5
- **Min rarity:** Rare
- **Cast-time field:** 20 ticks
- **Mana neutral:** 50–70
- **Spell power neutral:** 5–13
- **Cooldown:** 35 s
- **Recast count:** `spellLevel`
- **Recast window:** 160 ticks / 8 s
- **Base final damage:** `0.5*spellPower + weaponDamage`

## Combo contract

Each normal cast scans a melee region and, for LivingEntity targets:

- increments `FROSTBITE_LEVEL` attachment by 1;
- applies Iron's `CHILLED` for 60 ticks.

`onRecastFinished` performs damage settlement. If target is Chilled, stored Frostbite is added to base damage. If main-hand is tagged `FROZEN_WEAPONS`, the relevant living-target damage branch receives **1.5×**. Afterwards the target's `FROSTBITE_LEVEL` is reset to 0.

The spell changes its animation/cast type around the final state and emits a distinct final `CrystalCarveEntity` visual.

## Static shared-state QA blocker

`private boolean isFinalCast` is stored directly on the registered spell instance and mutated during cast flow. Iron's spells are registry singletons; therefore concurrent casters may potentially share this state. Whether current Iron's invocation order avoids cross-player effects must be proven by GameTest/live multiplayer test.

Until then, integrations must not use `isFinalCast` as external authority. Use recast state/attachments from the player where possible.

## Dedup

Occupies Ice multi-hit setup → Chilled/Frostbite stack → weapon-scaled finisher signature. Do not maintain a second Frostbite stack ledger.

## Source

`CrystallineCarverSpell.java`, DTE 1.4.4 branch.
