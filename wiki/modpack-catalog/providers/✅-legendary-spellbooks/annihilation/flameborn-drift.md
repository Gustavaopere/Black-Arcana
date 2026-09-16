# Flameborn Drift

- ID: `legendary_spellbooks:flameborn_drift`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–7
- Min rarity: Rare
- Cooldown: 8 s
- Mana neutral: 120 / 130 / 140 / 150 / 160 / 170 / 180
- Spell power neutral: 4 / 5 / 6 / 7 / 8 / 9 / 10
- Dash power formula: `2.0 + 0.1 × spellPower`
- Flameborn-dash effect: 12 ticks
- Invulnerable time assigned: 15 ticks
- Extra HP-damage field: `0.25 × spellLevel` as exposed by the spell UI/code path
- Crafting: habilitado no config
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Dash forward envolto em green fire; collision with a creature stops the dash and resolves the provider's AoE. Grounded casts add a small upward component. Spin/dash state and collision damage are provider-native.

## Acquisition

Não aparece no custom boss-scroll provider; crafting não é desabilitado.

## Regra para o Black Arcana

Não somar outro impulso, janela de invulnerabilidade ou collision AoE ao mesmo cast.

## Source

`FlamebornDriftSpell.java` @ source pin 0.3.2.
