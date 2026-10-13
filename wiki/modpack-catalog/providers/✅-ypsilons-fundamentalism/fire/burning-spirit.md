# Burning Spirit

**✅ Revalidação SHA-exata 2026-10-13:** spell ID estático `ypfundamentals:grantstrength` confirmado no JAR físico/publicador 1.1.7.1 (`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`), escola default Fire, [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS. `COUNTED_EXACT` somente registry e classe, +0 novas raízes. [Dossiê](../EXACT-BINARY-SPELLS-1.1.7.1.md). Progressão, mana/config, multiplayer e Survival ⚠️.


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