# Overgrown Shockwave

- ID: `legendary_spellbooks:overgrown_shockwave`
- School: Nature
- Levels: 1–4
- Min rarity: Epic
- Cooldown: 30 s
- Mana neutral: 150 / 165 / 180 / 195
- Spell power neutral: 4 / 8 / 12 / 16
- Provider recasts: 1 / 2 / 3 / 4
- Recast window: 80 ticks
- Shockwave count: 3 / 4 / 5 / 6
- Outer radius reported by provider formula: 5.75 / 7.25 / 8.75 / 10.25 blocks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

A primeira ativação abre um recast window com count igual ao spell level; cada resolução gera as ondas/poisonous shockwaves provider-native. O count usa `min(spellLevel + 2,10)` e a geometria deriva dele.

## Acquisition

Pool do Overgrown Colossus: níveis 1–4, weight 10.

## Regra para o Black Arcana

Não transformar recasts em novos casts independentes para cooldown, mastery ou proc. Não duplicar as shockwaves já criadas pelo provider.

## Source

`OvergrownShockwaveSpell.java` @ source pin 0.3.2.
