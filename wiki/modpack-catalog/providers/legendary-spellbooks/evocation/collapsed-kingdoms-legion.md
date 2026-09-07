# Collapsed Kingdom's Legion

- ID: `legendary_spellbooks:collapsed_kingdoms_legion`
- School: Evocation
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 120 s
- Cast-time field: 45 ticks
- Mana neutral: 180 / 220 / 260
- Spell power neutral: 8 / 12 / 16
- Summons per cast: 3
- Summoned HP: 65 / 80 / 95 each from `50 + 15 × spellLevel`
- Summoned damage seed: provider uses spell power
- Summon lifetime: 10 minutes provider-native
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Invoca uma unidade de cada tipo: Haunted Guard, Haunted Knight e Fractured Apostle. A spell registra as três entidades no lifecycle de `BaseSummonSpell`/Iron's `SummonManager`; variantes visuais de Guard/Knight dependem do nível.

## Acquisition

Pool do Possessed Paladin: níveis 1–3, weight 10.

## Regra para o Black Arcana

Não manter segundo ownership ledger, timer, despawn, damage scaling ou recompensa por permanência dos summons.

## Source

`CollapsedKingdomsLegionSpell.java`, `BaseSummonSpell.java` @ source pin 0.3.2.
