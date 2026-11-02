# Raygun 1.0.10 — caminhos consumidores dos ramos X_RAY e GAMMA_RAY

## Autoridade e escopo

Continua o recorte de branches da [PR #1017](https://github.com/Gustavaopere/Black-Arcana/pull/1017), integrado à `Black-Arcana/main@414a8b751394e19d6b94e4916bb104dc6820c53f` com **24/24 workflows pós-merge aprovados**. A modlist física do sibling fixa Alex's Caves Continued **1.0.10**, JAR publisher SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.

A [sonda read-only](alexscaves_1010_raygun_branch_consumers_probe.py) valida a classe `RaygunItem.class` SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` e o digest de `onUseTick(Level,LivingEntity,ItemStack,int):void` `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`. Extraem-se **apenas símbolos de invocação, branches, constantes selecionadas e índices locais** de três regiões delimitadas do método compilado:

- `[569,669)`: região opcional de busca adicional por `X_RAY`, `LivingEntity.getBoundingBox @575`, `ProjectileUtil.getEntityHitResult @640` e guarda `ifnull @647`.
- `[920,962)`: seleção `GAMMA_RAY` `4/0 @922–932`, escrita no **slot JVM 23 @932**, e enumeração `Level.getEntities @943`.
- `[1125,1161)`: outra seleção `GAMMA_RAY` `4/0 @1138–1148`, junto do envio visual posteriormente observado.

Um censo de `iload/istore 23` no método identifica **usos estáticos** do slot receptor de `@932`; não supõe que todos os acessos compartilhem uma única definição ou aconteçam em cada disparo.

## Gate de evidência

O [workflow específico](../../.github/workflows/alexscaves-1010-raygun-branch-consumers.yml) deve executar 14 testes sintéticos, baixar o JAR publisher exato, verificar SHA-1/SHA-256/bytes da classe e do método, e produzir o manifesto de inspeção sem reproduzir métodos completos de terceiros. A primeira execução é explicitamente `UNSEALED`. A versão observada de `EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json` deve ser incorporada do log CI e validada em nova HEAD final com `--seal`, com todos os demais workflows pré-merge verdes.

## Limites de interpretação

**Anotações de bytecode não são testes físicos nem contratos de mutabilidade.** Branches estáticos e valores `4/0` não fornecem por si só o tipo de visual, amplifier, quantidade de alvos, cooldown, efeito em bloco ou semântica de status. Mesmo uma chamada a `ProjectileUtil.getEntityHitResult` não prova que uma perk possa mudar o alcance preservando critérios de exclusão, LOS e autorização do servidor.

Persistem: `WorldEffectPolicy`, claims/PvP, estado/charge do provider, validação C2S e deduplicação dos acertos/XP, teste físico do modpack. **⚠️ parcial/condicionado, `NO_MUTATION`, `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`**. Sem promover Stage 06 ou contadores **28/30**.
