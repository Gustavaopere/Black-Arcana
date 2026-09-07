# Brightburst

- ID: `asterismarcanum:brightburst`
- escola: Astral
- rarity: Rare
- níveis: 1–6
- cast: INSTANT
- mana: 25 / 30 / 35 / 40 / 45 / 50
- cooldown: 20 s
- neutral spell power: 1 / 2 / 3 / 4 / 5 / 6
- radius: 12 / 14 / 16 / 18 / 20 / 22
- neutral damage: 1.5 / 2 / 2.5 / 3 / 3.5 / 4

## Efeito

Explosão defensiva centrada no caster. Busca LivingEntities no raio, exclui o próprio caster, aliados e passageiros do mesmo veículo, causa dano Astral e empurra os alvos para fora.

O knockback cresce com spell power/distância e é reduzido por Knockback Resistance do alvo.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer. Também permanece sob o pipeline configurável de crafting de scrolls de Iron's.

## Authority e dedup

O `onCast` server-side é o único settlement de AoE/dano/impulso. Perks podem observar o hit causal, mas não repetir dano nem push.

## QA

Validar party, passengers e entidades com knockback resistance extrema.