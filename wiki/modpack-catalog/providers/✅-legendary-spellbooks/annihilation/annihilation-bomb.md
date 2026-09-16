# Annihilation Bomb

- ID: `legendary_spellbooks:annihilation_bomb`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 20 s
- Cast: Long, 27 ticks; cast-time reduction desabilitada
- Mana neutral: 125 / 140 / 155 / 170 / 185 / 200
- Spell power neutral: 6 / 10 / 14 / 18 / 22 / 26
- Max-HP damage: 0.5% / 1% / 1.5% / 2% / 2.5% / 3%
- Secondary projectile count: 30 / 35 / 40 / 45 / 50 / 55
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Lança uma `SpellAnnihilationBombEntity`; no impacto, o provider resolve a detonação e a dispersão dos orbs secundários. A spell já carrega dano mágico e componente percentual de HP.

## Acquisition

Pool do The Obliterator: níveis 1–4, weight 14.

## Regra para o Black Arcana

Não adicionar segunda explosão, segunda dispersão ou dano percentual paralelo.

## Source

`AnnihilationBombSpell.java` @ source pin 0.3.2.
