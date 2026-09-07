# Guardian's Gaze

- **ID:** `discerning_the_eldritch:guardians_gaze`
- **School:** Evocation
- **Level:** 1
- **Rarity:** Epic
- **Cast:** Instant
- **Mana:** 50
- **Spell power neutral:** 10
- **Cooldown:** 10 s
- **Ray range:** 30 blocks
- **Damage neutral:** 20
- **Debuff:** Mining Fatigue II, 60 ticks / 3 s

## Acquisition gates

- `canBeCraftedBy=false`;
- `allowLooting=false`.

Specific provider route granting the spell: `NÃO VERIFICADO`.

## Contract

Raycasts 30 blocks, spawns Iron's `RayOfFrostVisualEntity` as visual beam, applies `DamageSources.applyDamage` to an entity hit with damage `2*getSpellPower`, then applies vanilla `DIG_SLOWDOWN` amplifier 1 for 60 ticks to LivingEntity targets.

## QA note

The source contains an `else if (hitResult == BLOCK)` nested inside the `if (hitResult == ENTITY)` block, so that block-specific particle branch is unreachable. A generic particle spawn still occurs inside the entity-hit branch. This is a presentation/source quirk, not a gameplay damage blocker.

## Dedup

Occupies short-cooldown Evocation ray + Mining Fatigue signature. Do not duplicate beam damage from visual entity callbacks.

## Source

`GuardiansGazeSpell.java`, branch `1.21@7bbd81f...`.
