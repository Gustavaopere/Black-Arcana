# Annihilation Arrow

- ID: `legendary_spellbooks:annihilation_arrow`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–8
- Min rarity: Rare
- Cooldown: 10 s
- Long cast field: 30 ticks
- Mana neutral: 80 / 90 / 100 / 110 / 120 / 130 / 140 / 150
- Spell power neutral: 8 / 10 / 12 / 14 / 16 / 18 / 20 / 22
- Max-HP damage: `0.25% × spellLevel`
- Crafting: habilitado no config
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Dispara `AnnihilationArrowEntity`; o projectile recebe o spell power e uma parcela adicional de vida máxima do alvo. O provider é autoridade da explosão/impacto e do damage source.

## Acquisition

Não aparece no custom `LSSpellScrollLootProvider`; o config não desabilita crafting. Não inventar boss drop adicional.

## Regra para o Black Arcana

Não adicionar segundo dano percentual, explosão ou projectile callback.

## Source

`AnnihilationArrowSpell.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.
