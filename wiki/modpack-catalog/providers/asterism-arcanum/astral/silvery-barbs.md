# Silvery Barbs

- ID: `asterismarcanum:silvery_barbs`
- escola: Astral
- rarity: Rare
- níveis: 1–5
- cast: INSTANT
- mana: 25 / 30 / 35 / 40 / 45
- cooldown: 1 s
- neutral spell power: 2 / 3 / 4 / 5 / 6
- raycast range: 25
- radius nominal: 4 / 5 / 6 / 7 / 8

## Efeito

Raycasta um ponto até 25 blocos e, na área, aplica Luck II por 20 ticks + `silvery_barbs_tag` a aliados e `IMagicSummon` pertencentes ao caster.

No `LivingIncomingDamageEvent`, se Luck e tag continuam presentes, o provider aplica Glowing brevemente e cancela o damage event.

## Semântica real importante

O tag não é consumido quando um hit é cancelado. Portanto a leitura estática permite **múltiplos incoming hits cancelados durante a janela de ~1 s**, e não apenas um hit. Se o tag ainda existe quando Luck terminou, o próximo damage event remove o tag sem cancelar.

A spell também mantém `public static float radius`, mutado durante uso/consulta. Isso é estado global da singleton e merece QA multiplayer.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Authority = Luck/tag + provider damage handler. Não criar segundo shield, charge ou cancelamento de evento.

## QA obrigatório

Multi-hit no mesmo tick/janela, dois casters com níveis diferentes, party/PvP e summons.