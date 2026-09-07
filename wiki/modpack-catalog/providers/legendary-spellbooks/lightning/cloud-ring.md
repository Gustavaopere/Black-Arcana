# Cloud Ring

- ID: `legendary_spellbooks:cloud_ring`
- School: Lightning
- Levels: 1–5
- Min rarity: Epic
- Cooldown: 15 s
- Cast-time field: 40 ticks
- Mana neutral: 60 / 70 / 80 / 90 / 100
- Spell power neutral: 2 / 5 / 8 / 11 / 14
- Ring count: 1 / 2 / 3 / 4 / 5
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Gera anéis de cloud entities em torno do caster/área segundo a geometria do provider. O count usa `min(spellLevel,10)`; as clouds e seus efeitos não são uma surface para um segundo pipeline de dano.

## Acquisition

Pool do Cloud Golem: níveis 1–4, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não duplicar rings, clouds ou lightning callbacks.

## Source

`CloudRingSpell.java` @ source pin 0.3.2.
