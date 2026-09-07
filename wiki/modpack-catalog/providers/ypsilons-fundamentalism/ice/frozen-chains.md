# Frozen Chains

- ID: `ypfundamentals:chains`
- classe: `ChainsSpell`
- escola: Ice
- rarity: Uncommon
- níveis: 1–5
- cast: LONG, 200 ticks / 10 s
- mana: 65 / 80 / 95 / 110 / 125
- cooldown: 45 s
- target: entity, helper range 50
- duração: 14 / 18 / 22 / 26 / 30 s
- dano: nenhum dano direto na spell class

## Efeito

Respeita `CANT_ROOT`. Cria `ChainsEntity`, monta o alvo nela e aplica Chained, Slowness IV e Weakness VI. `ChainedEffect` cancela casts de players/magic entities em cada tick, cancela início de uso de item e cancela `EntityTeleportEvent`.

## Obtenção/aprendizado

A spell não desabilita o pipeline padrão de loot/crafting do Iron's. Fonte/weight/receita concreta da release: **NÃO VERIFICADO**.

## Authority / dedup

Authority de imobilização/cancelamento = `ChainsEntity` + `ChainedEffect`. Não adicionar root, anti-cast ou anti-teleport paralelo.

## QA

PvP, bosses além de `CANT_ROOT`, interação com teleport de outros addons e cleanup por unload: runtime QA.

## Fonte

Pin `a9b8f822...`; `ChainsSpell.java`, `ChainedEffect.java`.