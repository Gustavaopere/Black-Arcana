# Cumulo Charge

- ID: `legendary_spellbooks:cumulo_charge`
- School: Lightning
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 15 s
- Cast-time field: 40 ticks
- Mana neutral: 200 / 250 / 300
- Spell power neutral: 10 / 18 / 26
- Target helper range: 48 blocks
- Entity duration: 120 / 140 / 160 ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Spawna `CumuloChargeEntity` com target opcional e duração `min(100 + 20 × spellLevel,300)`. Projectile/entity logic, chain/effect resolution and damage source remain provider-native.

## Acquisition

Pool do Cloud Golem: níveis 1–3, weight 12. O Stormbound Grimoire possui afinidades para Cumulo Charge em SUNNY e THUNDER.

## Regra para o Black Arcana

Não criar segundo projectile, chain callback ou target resolver para o mesmo cast.

## Source

`CumuloChargeSpell.java`, `CumuloChargeEntity.java`, `StormboundSpellbookItem.java` @ source pin 0.3.2.
