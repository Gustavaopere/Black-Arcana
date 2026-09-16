# Otherworldly Presence

- **ID:** `discerning_the_eldritch:otherworldly_presence`
- **School:** Eldritch
- **Levels:** 1–3
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 40–60
- **Spell power neutral:** 12 / 16 / 20
- **Cooldown:** 10 s
- **Metaphysical duration:** 10 s

## Contract

Uses Iron's teleport data/location helpers and `Utils.handleSpellTeleport`; dismounts passengers, resets fall distance, then applies `METAPHYSICAL_POTION_EFFECT` for 200 ticks.

Distance formula:

`softCapFormula(entityPowerMultiplier) * getSpellPower(level, null)`.

This intentionally separates the base-level power term from the caster's multiplier soft-cap.

DTE server events cancel `SpellPreCastEvent` while Metaphysical is active, so the caster cannot start another spell during the state.

The public description also states that the state prevents causing/receiving damage. That exact damage-event settlement was not located in this audit pass and remains `NÃO VERIFICADO`; do not invent an invulnerability handler in documentation.

## Dedup

This is teleport + temporary metaphysical neutral/anti-cast state, not plain teleport. Integrations should react to `METAPHYSICAL_POTION_EFFECT` rather than infer it from coordinate change.

## Source

`OtherworldlyPresenceSpell.java`, `MetaphysicalPotionEffect.java`, current DTE `ServerEvents`.
