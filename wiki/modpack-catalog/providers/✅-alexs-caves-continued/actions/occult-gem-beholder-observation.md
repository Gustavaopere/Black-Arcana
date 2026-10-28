# Occult Gem + Beholder — Remote Observation

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:occult_gem` + `alexscaves:beholder`
- Trigger: use of an Occult Gem previously bound to a valid Beholder
- State: `COUNTED_EXACT`

## Semantic identity

The provider starts a remote Beholder observation session and creates the Beholder Eye viewpoint tied to the player. Binding is preparation; view/chunk state, Eye lifetime and camera synchronization are downstream lifecycle.

## Exact acquisition

Exact provider data closes Occult Gem through Forlorn/Watcher loot and the Beholder through its crafting relation.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles, sounds and world settlement remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Contrato causal Occult Gem / Beholder — fonte pública fixada (não homologado no JAR físico)

**Teto de evidência (2026-10-28).** As identidades são `COUNTED_EXACT` pelo relatório de auditoria da versão instalada `alexscaves` 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Os parâmetros abaixo resultam de inspeção **read-only** do fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`; a igualdade binária desse commit com o JAR físico **não foi demonstrada**. Rotular esses parâmetros `SOURCE_SNAPSHOT_ONLY`, e **não** `COMPLETE_PERK_READY`. Configs efetivas, chamadas packet/runtime, hooks mutadores e QA física permanecem `NOT_VERIFIED`.

| Parâmetro / seam | Evidência method-pinned do snapshot |
|---|---|
| Vinculação | `OccultGemItem.useOn` grava `BeholderPos`, `BeholderDimension` e `BeholderTracked` em dados do item ao interagir com um Beholder. O caso sem player (automação) retorna ao fluxo-base na revisão pública |
| Guard de `use` | `isActive` considera haver **um dos dois** campos, mas `getBeholderPosition` requer **ambos** e dimensão decodificável. Portanto `isActive=true` **não garante** observação possível |
| Dimensão e servidor | A ativação no método `use` exige `globalPos.dimension()==level.dimension()` e `ServerLevel`; não há autorização genérica de cross-dimension view neste ramo |
| Início da sessão | Após resolver posição e carregar chunks, valida bloco `BEHOLDER` + `BeholderBlockEntity`; chama `startObserving`, que cria `BeholderEyeEntity` associado ao **UUID do jogador**, registra `currentlyUsingEntityId` e sincroniza a visão através do provider |
| Primeiro carregamento forçado | `OccultGemItem.loadChunksAround(..., true)` percorre **3 × 3 chunks** em torno do Beholder, passando o **UUID do jogador** como ticket; ocorre **antes** da checagem se o bloco ainda é um Beholder válido. Não declarar ticket liberado nesse método apenas porque `use` encerrou |
| Carga da entidade de câmera | `BeholderEyeEntity` mantém `LOAD_CHUNK_DISTANCE=2`, mas calcula `dist=max(2, server.viewDistance/2)`; percorre `(2*dist+1)^2` posições de chunk sob **ticket da própria entidade**, além do chunk do jogador, quando o controle de câmera foi assumido |
| Limpeza observada | Em `BeholderEyeEntity.tick`, se não existe jogador controlador e `loadingChunks` está ativo, chama `loadChunksAround(false)` e descarta após `tickCount>3`. Isso descreve **um caminho** de descarregamento, não prova de limpeza integral para disconnect, unload, remoção precoce ou ticket original vinculado ao UUID do jogador |
| Persistência | `OccultGemItem` armazena posição e dimensão; `BeholderBlockEntity` salva `UsingEntityID`; `BeholderEyeEntity` salva `UsingPlayerUUID`. São três donos de estado distintos — não um único NBT/canal transferível |
| Validade da ligação | `OccultGemItem.acInventoryTick` só revalida bloco a cada **20 ticks** sob condição de carregamento e remove campos inválidos; não presumir validação contínua nem remoção imediata de tickets |

### World safety, lifecycle e perks

É especialmente perigoso atrelar perks de range, duração ou múltiplas câmeras a esse `use`: há tickets de chunk com **proprietários diferentes** e um raio de carregamento dependente da view distance do servidor. O recorte público não demonstra simetria de liberação de tickets de UUID original versus tickets de entidade, nem validação de cancelamento/teleport/desconexão em todos os caminhos. Priorizar testes de **desconexão**, Beholder destruído, dimensão divergente, retirada do item, término de sessão, un/load de chunks e múltiplos jogadores antes de habilitar adapter; nunca multiplicar a instância de câmera, tickets, sincronização ou cost settlement. Sem boundary segura **⛔ fail-closed**.

**Fontes:** [`OccultGemItem.use/useOn/acInventoryTick/loadChunksAround`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/OccultGemItem.java), [`BeholderBlockEntity.startObserving`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/block/blockentity/BeholderBlockEntity.java), [`BeholderEyeEntity.tick/loadChunksAround`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/BeholderEyeEntity.java); [relatório de identidade exata](../EXACT-1.0.10-ARTIFACT-AUDIT.md).
