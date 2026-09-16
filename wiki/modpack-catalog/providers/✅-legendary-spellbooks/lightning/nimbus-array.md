# Nimbus Array

- ID: `legendary_spellbooks:nimbus_array`
- School: Lightning
- Levels: 1–7
- Min rarity: Rare
- Cooldown: 10 s
- Mana neutral: 80 / 90 / 100 / 110 / 120 / 130 / 140
- Spell power neutral: 2 / 3 / 4 / 5 / 6 / 7 / 8
- Nimbus count: 2 / 4 / 6 / 8 / 10 / 12 / 14
- Lifetime: 25 / 30 / 35 / 40 / 40 / 40 / 40 ticks
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria uma array de clouds/nimbus com count `min(2 × spellLevel,15)` e lifetime `min(20 + 5 × spellLevel,40)`. A versão simples permanece craftável no config.

## Acquisition

Pool do Cloud Golem: níveis 1–6, weight 10.

## Regra para o Black Arcana

Não confundir com Triple Nimbus Array; são registros distintos. Não duplicar arrays ou lifespan tracking.

## Source

`NimbusArraySpell.java` @ source pin 0.3.2.
