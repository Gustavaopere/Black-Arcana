# Mend Flesh

- **ID:** `discerning_the_eldritch:mend_flesh`
- **School:** Eldritch
- **Levels:** 1–3
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 30–40
- **Spell power neutral:** 5–7
- **Cooldown:** 30 s
- **Effect duration neutral:** 5–7 s

## Initial heal

`heal = getSpellPower / 3.5` → neutral ~1.43–2.0 HP.

Before `entity.heal`, the spell posts Iron's `SpellHealEvent(entity, entity, healing, school)`. This event is the causal hook for integrations; do not infer heal from health delta.

## Reactive effect

Applies `MEND_FLESH_EFFECT` for `20*spellPower` ticks. Upstream server config defaults:

- heal-on-hit/lifesteal behavior: **enabled**;
- heal-on-XP gain: **enabled**.

Current `ServerEvents` confirms that, when the hit behavior is enabled, a LivingEntity carrying Mend Flesh heals **1.5 HP** after dealing damage and emits sculk-soul feedback. Exact current XP-event heal amount was not isolated in this pass and remains `NÃO VERIFICADO`.

## Dedup / authority

- initial heal authority: `SpellHealEvent` + provider spell;
- reactive heal authority: `MEND_FLESH_EFFECT` + provider events/config;
- no parallel lifesteal ledger;
- avoid double-counting the initial heal and later hit-trigger heals as the same causal event.

## Source

`MendFleshSpell.java`, `MendFleshPotionEffect.java`, `DTEServerConfig`, current DTE `ServerEvents`.
