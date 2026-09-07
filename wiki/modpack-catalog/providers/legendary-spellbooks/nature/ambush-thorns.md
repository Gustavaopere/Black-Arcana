# Ambush Thorns

- ID: `legendary_spellbooks:ambush_thorns`
- School: Nature
- Levels: 1–10
- Min rarity: Common
- Cooldown: 120 s
- Cast-time field: 30 ticks
- Mana neutral: 65 / 70 / 75 / 80 / 85 / 90 / 95 / 100 / 105 / 110
- Effect duration: 15 / 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 s
- Trigger: victim with Ambush Thorns effect receives damage
- Retaliation chance: 50%
- Retaliation formula: `20% × original incoming damage + (0.25 + 0.25 × amplifier) × entityPowerMultiplier`
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

A spell aplica `AMBUSH_THORNS_EFFECT`; o handler escuta `LivingDamageEvent.Pre`. Se houver atacante vivo e o roll `Math.random() < 0.5` passar, o atacante recebe thorns damage calculado pelo provider.

Com amplifier `spellLevel-1`, a parcela base do handler antes do entity-power multiplier é 0.25 / 0.5 / 0.75 / 1.0 / 1.25 / 1.5 / 1.75 / 2.0 / 2.25 / 2.5, além dos 20% do dano original.

## Acquisition

Pool do Ancient Guardian: níveis 3–10, weight 10; global loot modifier usa chance 0.5. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não instalar segundo thorns listener ou segunda rolagem de 50% para o mesmo dano. Qualquer observação deve deduplicar pelo pipeline provider-native.

## Source

`AmbushThornsSpell.java`, `AmbushThornsEffectHandler.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.
