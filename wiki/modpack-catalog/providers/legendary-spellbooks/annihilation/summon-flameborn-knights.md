# Summon Flameborn Knights

- ID: `legendary_spellbooks:summon_flameborn_knights`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–5
- Min rarity: Legendary
- Cooldown: 240 s
- Long cast field: 60 ticks
- Mana neutral: 250 / 300 / 350 / 400 / 450
- Spell power neutral: 8 / 11 / 14 / 17 / 20
- Summons: 1 Flameborn Guard + 1 Flameborn Warrior
- Guard HP: 56 / 64 / 72 / 80 / 88
- Warrior HP: 60 / 70 / 80 / 90 / 100
- Summon lifetime: 10 minutes provider-native
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Invoca duas entidades próprias e registra ambas pelo `SummonManager` do Iron's. O recast/lifecycle pertence ao provider; `BaseSummonSpell` cria o ledger de entidades e o recast de encerramento.

## Acquisition

Pool do The Obliterator: níveis 1–4, weight 18. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não criar segundo ownership timer, segundo despawn ou recompensa por tick de summon.

## Source

`SummonFlamebornKnightsSpell.java`, `BaseSummonSpell.java` @ source pin 0.3.2.
