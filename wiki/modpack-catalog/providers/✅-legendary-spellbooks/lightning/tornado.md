# Tornado

- ID: `legendary_spellbooks:tornado`
- School: Lightning
- Levels: 1–10
- Min rarity: Common
- Cooldown: 6 s
- Cast-time field: 25 ticks
- Mana neutral: 60 / 65 / 70 / 75 / 80 / 85 / 90 / 95 / 100 / 105
- Duration: 15 / 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 ticks
- Target helper range: 12 blocks; provider fallback raycast: 42 blocks
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Spawna um tornado estacionário provider-native no alvo/posição resolvida. A duração usa `min(10 + 5 × spellLevel,100)`. O addon também possui `TornadoEntityHandler`; motion/damage/lifecycle permanecem autoridade do provider.

## Acquisition

Pool do Cloud Golem: níveis 3–10, weight 6. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não somar outro vortex/impulse ao mesmo tornado nem duplicar sua duração.

## Source

`TornadoSpell.java`, `TornadoEntityHandler.java` @ source pin 0.3.2.
