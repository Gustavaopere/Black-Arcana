# Annihilation Resonance

- ID: `legendary_spellbooks:annihilation_resonance`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 180 s
- Long cast field: 35 ticks
- Mana neutral: 120 / 140 / 160 / 180 / 200 / 220
- Effect duration: 25 / 30 / 35 / 40 / 45 / 50 s (`min(20 + 5×level,100)`)
- Tradeoff effect: -25% Attack Damage e -25% Armor via `ADD_MULTIPLIED_TOTAL`
- Trigger: critical hit while effect is active
- Blast radius: 3 blocks around the struck target
- Blast base formula: `4 × (1 + 0.75 × effectAmplifier) × entityPowerMultiplier`
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Aplica ao caster um estado de Resonance com tradeoff ofensivo/defensivo. Critical hits disparam a explosão provider-native; o handler usa o damage source da própria spell.

## Acquisition

Pool do The Obliterator: níveis 1–4, weight 14. Crafting não é desabilitado no config.

## QA

O predicado do handler usa `!attacker.isAlliedTo(target)` como condição constante ao iterar entidades próximas, em vez de verificar aliança com cada candidata. Friendly-fire real precisa de runtime QA.

## Regra para o Black Arcana

Não criar segunda detecção de crítico ou segunda explosão para a mesma ação.

## Source

`AnnihilationResonanceSpell.java`, `AnnihilationResonanceHandler.java`, `AnnihilationResonanceEffect.java` @ source pin 0.3.2.
