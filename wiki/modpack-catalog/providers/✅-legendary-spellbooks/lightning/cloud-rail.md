# Cloud Rail

- ID: `legendary_spellbooks:cloud_rail`
- School: Lightning
- Levels: 1–10
- Min rarity: Common
- Cooldown: 6 s
- Mana neutral: 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 / 65
- Spell power neutral: 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11
- Cloud count: 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria uma linha/rail de clouds sob a resolução do provider. O count usa `min(2 + spellLevel, 15)`; posicionamento, lightning interactions e damage/effects permanecem do addon/Iron's.

## Acquisition

Pool do Cloud Golem: níveis 4–10, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não criar segunda linha de clouds nem reprocessar cada cloud como cast independente.

## Source

`CloudRailSpell.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.
