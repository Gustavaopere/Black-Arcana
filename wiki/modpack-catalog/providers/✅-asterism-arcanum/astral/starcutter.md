# Starcutter

- ID: `asterismarcanum:starcutter`
- escola: Astral
- rarity: Uncommon
- níveis: 1–8
- cast: INSTANT
- mana: 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55
- cooldown: 13 s
- neutral spell power: 1–8
- neutral damage: 2 / 4 / 6 / 8 / 10 / 12 / 14 / 16
- spell-computed radius: 6.5 / 9 / 11.5 / 14 / 16.5 / 19 / 21.5 / 24

## Efeito

Raycasta um ponto e cria uma `StarcutterEntity`. Após ~30 ticks a entidade executa uma explosão Astral com line-of-sight e falloff por distância.

## Divergência de radius

A spell passa o radius calculado acima para a entidade. Entretanto `StarcutterEntity.setRadius()` executa `Math.min(pRadius, 1)`. Em condições normais o entity radius torna-se 1; o settlement usa `explosionRadius = entityRadius * 10`.

A leitura estática, portanto, indica raio efetivo próximo de 10 independentemente do scaling calculado pela spell. O raycast ainda usa o radius calculado para determinar alcance de colocação.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Authority = delayed `StarcutterEntity`. Não aumentar AoE externamente para tentar reconciliar tooltip/source e não aplicar dano de explosão uma segunda vez.

## QA obrigatório

Medir raio lvl1/lvl8, LOS, reload/chunk lifecycle e anti-magic.