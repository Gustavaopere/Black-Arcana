# Leyline Rifts — comportamento público confirmado

## Loop de mundo

A publicação oficial descreve pilares de leyline que podem surgir à noite. O jogador os encontra e carrega para abrir um **Leyline Rift**, encontro em ondas que concede loot temático, experiência e chance de **Ley Crystal**. O texto também descreve variações temáticas de rift, incluindo amethyst surges, void tears e chaotic echoes.

IDs de estruturas/entities/loot tables, chances numéricas, número de waves e regras de spawn permanecem `NÃO VERIFICADO` sem o JAR.

## Regras adicionadas/explicitadas em 1.0.3

### Morte

Morrer durante um encontro ativo falha a luta imediatamente. A release explicita ausência de completion loot/crystal nessa situação. O wave boss bar é limpo em morte, respawn, logout e mudança de dimensão.

### Abandono

Sair a mais de **60 blocos** de um rift ativo colapsa o encontro imediatamente.

### Leash das waves

Mobs do encontro que se afastam mais de **40 blocos** do rift são puxados de volta à arena.

### Persistência

Os mobs da wave deixam de desaparecer apenas porque o jogador morreu brevemente; o changelog explica que isso evitava um falso clear.

### Ferramenta administrativa

`/leylines spawnpillar` requer permission level 2 e cria um pilar temporário em posição próxima. `/leylines spawnpillar here` tenta primeiro a coluna atual. A própria publicação classifica o comando como ferramenta de admin/debug.

## Authority

Estas regras pertencem ao provider Leylines. Black Arcana não deve:

- marcar completion após morte;
- conceder a recompensa do rift por listener paralelo;
- manter contador independente de wave;
- implementar leash adicional;
- manter segundo abandonment radius;
- usar o comando debug como rota normal de progressão.

## Pendências de bytecode/runtime

- IDs reais de pillar/rift/entities;
- storage/persistence do encounter state;
- server authority e networking;
- lógica de ownership em multiplayer;
- tratamento de múltiplos jogadores próximos;
- loot tables, chances e quantidade de waves;
- cleanup em unload/restart/crash;
- interação com claims/dimensões/sublevels.

Todos permanecem `NÃO VERIFICADO` até extração do JAR e QA.
