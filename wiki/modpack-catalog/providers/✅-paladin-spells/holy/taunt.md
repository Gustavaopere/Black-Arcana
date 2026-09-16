# Taunt

- **Status:** PRESENTE — released
- **ID:** `paladin_spells:taunt`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–120
- **Cooldown:** 20 s
- **Spell power neutral:** 10–55
- **Radius neutral:** 30–120 blocks
- **Duration neutral:** 15–60 s

## Source 1.1.1

`range = 10 + 2*getSpellPower`

`duration = 5 + getSpellPower`

The spell scans `Mob` in the inflated caster box and keeps mobs alive, within true radius and not the caster. Only mobs implementing `Enemy` receive `TAUNT_EFFECT`. The caster UUID is written to `taunt_target_uuid`.

`TauntEffect` ticks every tick server-side, resolves that UUID and repeatedly:

- `mob.setTarget(taunter)`;
- `mob.setAggressive(true)`;
- when taunter is Player, `mob.setLastHurtByPlayer(player)`.

Angry-villager particles are used as current feedback.

## Authority / gates

`TAUNT_EFFECT` + stored UUID + `TauntEffect` are the forced-aggro authority. Bridges must not run a second target-forcing loop.

- non-Mob entities: excluded;
- Mob not implementing `Enemy`: excluded by spell;
- PvP players: not targets of the taunt scan;
- bosses/summons: eligible only if they satisfy the actual Mob/Enemy/provider behavior; individual modded-class coverage `NÃO VERIFICADO`.

## Mandatory matrix

- damage/heal: none;
- range/duration: formulas above;
- scaling/caps: Holy/generic/config power can change both; additional caps absent in class;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- VFX/audio: `TAUNT` sound, `TOUCH_GROUND_ANIMATION`, Angry Villager particles;
- QA: modded Enemy classification needs integration testing;
- dedup: occupies AoE hostile aggro-control signature.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `TauntSpell` + `TauntEffect`.
