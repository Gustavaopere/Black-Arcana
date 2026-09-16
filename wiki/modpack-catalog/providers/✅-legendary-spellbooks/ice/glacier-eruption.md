# Glacier Eruption

- ID: `legendary_spellbooks:glacier_eruption`
- School: Ice
- Levels: 1–7
- Min rarity: Rare
- Cooldown: 6 s
- Mana neutral: 30 / 35 / 40 / 45 / 50 / 55 / 60
- Spell power neutral: 3 / 4 / 5 / 6 / 7 / 8 / 9
- Spike count: 4 / 5 / 6 / 7 / 8 / 9 / 10 from `min(3 + level, 15)`
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Erupção de ice spikes provider-native. O addon possui mixins próprios para entidades de Ice Spike e é a authority de posicionamento/impacto; Black Arcana não deve instalar uma segunda conversão sobre as mesmas spikes.

## Acquisition

Pool do Frostbitten Golem: níveis 2–7, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não duplicar spike count, dano, freeze/frost riders ou callbacks já tratados pelo addon.

## Source

`GlacierEruptionSpell.java`, Ice Spike mixins @ source pin 0.3.2.
