# Annihilation Shockwave

- ID: `legendary_spellbooks:annihilation_shockwave`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 16 s
- Cast: Long, 10 ticks; cast-time reduction desabilitada
- Mana neutral: 120 / 130 / 140 / 150 / 160 / 170
- Spell power neutral: 6 / 8 / 10 / 12 / 14 / 16
- Max-HP component: 0.5% / 1% / 1.5% / 2% / 2.5% / 3%
- Wave count: 3 / 4 / 5 / 6 / 7 / 8
- Outer distance: 6 / 7.5 / 9 / 10.5 / 12 / 13.5 blocks
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Stomp que gera ondas em leque de `AnnihilationFlameStrike`. Cada strike recebe spell power e o componente de vida máxima; o provider marca as entidades como source de spell.

## Acquisition

Pool do The Obliterator: níveis 1–5, weight 18. Crafting não é desabilitado no config da spell.

## Regra para o Black Arcana

Não processar as FlameStrikes novamente como spell nova nem duplicar o HP damage.

## Source

`AnnihilationShockwaveSpell.java` @ source pin 0.3.2.
