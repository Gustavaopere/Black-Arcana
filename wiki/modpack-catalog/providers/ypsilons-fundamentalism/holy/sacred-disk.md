# Sacred Disk

- ID: `ypfundamentals:sacred_disk`
- escola: Holy
- rarity: Common
- níveis: 1–3
- cast: LONG, 5 ticks / 0.25 s
- mana: 10 em todos os níveis
- cooldown: 1 s
- neutral damage: 3 / 4 / 5
- projectile speed: 1.2

## Efeito

O disco causa dano ao tocar entidades. Ao tocar bloco entra em retorno imediatamente; sem bloco, inicia retorno após 40 ticks / 2 s. Durante retorno busca continuamente a posição atual do owner e é descartado ao chegar a ~0.5 bloco.

A class não mantém um set explícito de vítimas já atingidas; múltiplos contatos outward/return e comportamento de iFrames precisam de runtime QA.

## Obtenção

Pipeline padrão permitido; fonte concreta: **NÃO VERIFICADO**.

## Dedup

Não criar boomerang/return lifecycle paralelo.