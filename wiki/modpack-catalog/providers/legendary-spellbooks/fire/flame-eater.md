# Flame Eater

- ID: `legendary_spellbooks:flame_eater`
- School: Fire
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 10 s
- Mana neutral: 100 / 120 / 140 / 160 / 180 / 200
- Spell power neutral: 10 / 13 / 16 / 19 / 22 / 25
- Target/recast capacity: `1 + spellLevel` → 2 / 3 / 4 / 5 / 6 / 7
- Target range: 32 blocks
- Fire-column lifetime: 30 / 40 / 50 / 60 / 70 / 80 ticks = 1.5 / 2 / 2.5 / 3 / 3.5 / 4 s
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

O provider usa recasts para acumular alvos e resolve colunas de fogo sobre os UUIDs armazenados. O target ledger, recast count e as fire columns são parte da própria spell.

## Acquisition

Pool do Lava Eater: níveis 3–6, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não criar segundo target ledger, não disparar coluna adicional ao mesmo recast e não recontar um target provider-native como novo cast.

## Source

`FlameEaterSpell.java` @ source pin 0.3.2.
