# Quad Tornado

- ID: `legendary_spellbooks:quad_tornado`
- School: Lightning
- Levels: 1–5
- Min rarity: Epic
- Cooldown: 12 s
- Cast-time field: 40 ticks
- Mana neutral: 120 / 130 / 140 / 150 / 160
- Tornado count: 3 / 4 / 5 / 6 / 7 from `2 + spellLevel`
- Duration: 30 / 40 / 50 / 60 / 70 ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria múltiplos tornados móveis/radiais. Apesar do nome `Quad`, o número real varia com o nível e só é quatro no nível 2; o catálogo preserva a fórmula do source em vez de normalizar o nome para uma contagem fixa.

## Acquisition

Pool do Cloud Golem: níveis 1–4, weight 11.

## Regra para o Black Arcana

Não tratar o nome como contrato de quatro entidades. Não duplicar movement/physics ou damage callbacks.

## Source

`QuadTornadoSpell.java` @ source pin 0.3.2.
