# Annihilation Beam

- ID: `legendary_spellbooks:annihilation_beam`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–3
- Min rarity: Epic
- Cooldown: 45 s
- Cast: Long, 40 ticks; cast-time reduction desabilitada pelo provider
- Mana neutral: 200 / 250 / 300
- Spell power neutral: 8 / 14 / 20
- Max-HP damage: 1% / 2% / 3%
- Beam duration: 80 / 60 / 40 ticks
- Length: 30 / 40 / 50 blocks
- Crafting: desabilitado
- CastSource: somente Spellbook ou Command; scroll falha explicitamente
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria `SpellAnnihilationBeamEntity`, aplica o efeito Beam ao caster durante a duração e combina spell power com dano percentual de vida máxima. O guia do provider registra que o caster fica travado durante o disparo.

## Acquisition

Pool do The Obliterator: níveis 1–3, weight 10. `Annihilator's Protocol` também vem pré-carregado com Beam III.

## Regra para o Black Arcana

Não contornar o gate de CastSource, não aplicar segundo beam tick e não duplicar HP damage.

## Source

`AnnihilationBeamSpell.java` @ source pin 0.3.2.
