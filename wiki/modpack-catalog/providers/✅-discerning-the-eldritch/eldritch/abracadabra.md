# Abracadabra

- **ID:** `discerning_the_eldritch:abracadabra`
- **School:** Eldritch
- **Levels:** 1–5
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 75–135
- **Spell power neutral:** 3–11
- **Cooldown:** 75 s
- **Duration neutral:** 3–11 s

## Contract

Applies `ABRACADABRA_EFFECT` with amplifier `level-1` for `20*getSpellPower` ticks.

### Damage cap

When config `enableDamageCap` is true (default **true**), `LivingDamageEvent.Pre` clamps original incoming damage to:

`baseConfigCap / effectLevel`.

Default base cap is **80**, so level 1 cap=80, level 5 cap=16 before pack-config changes. Damage tagged `BYPASSES_INVULNERABILITY` is explicitly exempt.

### Harmful-effect prevention

When `enableHexPrevention` is true (default **true**), `MobEffectEvent.Applicable` rejects harmful effects while Abracadabra is present, except effects tagged `DTETags.BYPASS_ABRACADABRA`.

## Dedup / authority

This spell owns two distinct defensive contracts: per-hit damage ceiling and harmful-effect applicability gate. Do not reproduce either with a second event listener unless implementing an explicit upstream fix/compat.

Config runtime values override defaults; balance documentation must read pack config before treating 80 as final.

## Source

`AbracadabraSpell.java`, `AbracadabraPotionEffect.java`, `DTEServerConfig`.
