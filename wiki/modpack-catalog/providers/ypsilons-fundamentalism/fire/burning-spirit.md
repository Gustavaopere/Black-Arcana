# Burning Spirit

- ID: `ypfundamentals:grantstrength`
- classe: `BurningSpiritSpell`
- escola: Fire
- rarity: Epic
- níveis: 1–3
- cast: LONG, 20 ticks / 1 s
- mana: 100 / 120 / 140
- cooldown: 54 s
- neutral spell power: 30 / 40 / 50
- duração: 30 / 40 / 50 s

## Efeito

Aplica `Life Flame` com amplifier `level-1`. A cada 40 ticks remove Poison, Wither e freeze do caster e atinge não-aliados em raio 2/4/6. Pulse damage do source = `3 × amplifier`: 0 / 3 / 6. Qualquer dano direto causado por um LivingEntity sob Life Flame incendeia o alvo por 3/4/5 s.

## Obtenção

Pipeline padrão de spell permitido; loot/receita concretos: **NÃO VERIFICADO**.

## QA

No nível 1 o pulse AoE calcula dano 0. Não corrigir silenciosamente. Target/alliance e frequência precisam de runtime acceptance.

## Dedup

O effect/event layer do provider é authority; não duplicar cleanse, pulse ou ignite-on-hit.