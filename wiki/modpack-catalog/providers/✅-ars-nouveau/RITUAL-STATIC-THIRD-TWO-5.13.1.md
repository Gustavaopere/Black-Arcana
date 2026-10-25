# Ars Nouveau 5.13.1 — Ritual Binding e Awakening: contrato estático de execução

**Escopo documental:** 2 rituais adicionais, sem alterar o conjunto 24/24 de identidades já provadas no JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Código-fonte upstream `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. As assinaturas, métodos e consumidores foram auditados na fonte; equivalência integral de bytecode do JAR e gameplay não foram exercitados.

| Ritual | Entrada do provider e parâmetros | Consequência / risco para perks |
|---|---|---|
| [Binding](rituals/binding.md) | `RitualBinding.tick`, progresso ≥3, servidor a cada 20 game ticks; `new AABB(getPos()).inflate(5)`; predicado por `FamiliarRegistry` | Para **cada** holder que reconhecer a entidade: `RemovalReason.DISCARDED`, `getOutputItem()`, `ItemEntity` e advancement a até 8 blocos. Loop interno **sem break**, portanto não deduzir item único se vários holders reconhecerem a mesma entidade. |
| [Awakening](rituals/awakening.md) | `RitualAwakening.tick` a cada 20 game ticks; `isBookwyrms` prioriza qualquer `WritableBookItem`; sem livro, `getProgress()>5`, `withinManhattan(3,1,3)`, DFS até 350 e tamanho ≥50 | Livro: 1 `BOOKWYRM_CHARM` por progress slot até a soma das contagens; mundo: árvores de 4 famílias geram Weald, ou `BUDDING_AMETHYST` vira amethyst golem. Helper de destruição e `world.setBlock` não provam preflight de claims nem retorno efetivo de cada mutação. |

## Evidência, autoridade e riscos

- [`RitualBinding.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualBinding.java), [`RitualAwakening.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualAwakening.java) e [`AbstractRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/AbstractRitual.java) no commit fixo.
- `AbstractRitual.getSourceCost()=0` herdado por ambos: **0 Source declarado não é custo total zero**. Consumidores de itens, persistência, transação do brazier, config física, outros holders e save/reload requerem auditoria específica.
- `Entity.remove`, drops, Spawn e `world.setBlock` continuam provider-native. Partículas, ticks, holders e múltiplos blocos não são casts adicionais nem devem aumentar Mastery sem gatilho inequívoco.
- `WorldEffectPolicy` do Black Arcana não intercepta automaticamente o Ars. RPG Skill Tree atua exclusivamente como provider de progressão/atributos/Mastery/gates, via boundary comprovado.
- **Prova:** `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Necessário validar configuração, consumidores downstream, multiplayer, proteção de mundo, addons e retorno do cliente/servidor antes de qualquer perk mutadora. Stage 06.05 e Stage 09 não mudam.

Este lote avança as fichas de ritual de **10/24 para 12/24**, condicionado à validação dos índices/manifesto e ao merge na `main`. 0/164 providers completos permanece inalterado.
