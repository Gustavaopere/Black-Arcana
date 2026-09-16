# Thunder Fanburst

- ID: `legendary_spellbooks:thunder_fanburst`
- School: Lightning
- Levels: 1–10
- Min rarity: Common
- Cooldown: 8 s
- Mana neutral: 55 / 60 / 65 / 70 / 75 / 80 / 85 / 90 / 95 / 100
- Spell power neutral: 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11
- Bolt count: 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12
- Lifetime field: 30 / 35 / 40 / 45 / 50 / 55 / 60 / 65 / 70 / 75 ticks
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Dispara o fanburst de bolts/lightning entities pelo provider. O count usa `min(2 + spellLevel,20)` e o lifetime `min(25 + 5 × spellLevel,100)`.

## Acquisition

Pool do Cloud Golem: níveis 3–10, weight 10. O Stormbound Grimoire possui afinidade específica com esta spell.

## QA

No source 0.3.2, o mapa SUNNY do Stormbound concede +1 nível a Thunder Fanburst, mas o tooltip constrói a linha correspondente como +2. O runtime `AffinityData` é authority do pin; validar a apresentação na build instalada.

## Regra para o Black Arcana

Não corrigir a divergência por override de nível no Black Arcana. Integrations devem observar o nível final provider-native.

## Source

`ThunderFanburstSpell.java`, `StormboundSpellbookItem.java` @ source pin 0.3.2.
