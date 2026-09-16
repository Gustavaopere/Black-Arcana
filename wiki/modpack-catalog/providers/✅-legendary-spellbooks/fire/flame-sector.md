# Flame Sector

- ID: `legendary_spellbooks:flame_sector`
- School: Fire
- Levels: 1–4
- Min rarity: Epic
- Cooldown: 15 s
- Mana neutral: 80 / 100 / 120 / 140
- Spell power neutral: 3 / 6 / 9 / 12
- Rings: 4 / 6 / 8 / 10
- Approx. flame count from provider formula `floor(1.5 × rings)`: 6 / 9 / 12 / 15
- Flame lifetime: 20 / 25 / 30 / 35 ticks = 1 / 1.25 / 1.5 / 1.75 s
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria setores/anéis de flame entities em torno do caster. Quantidade, duração, posicionamento e damage source permanecem provider-owned.

## Acquisition

Pool do Lava Eater: níveis 1–4, weight 18.

## Regra para o Black Arcana

Não reprocessar cada flame entity como cast separado nem adicionar AoE paralelo.

## Source

`FlameSectorSpell.java` @ source pin 0.3.2.
