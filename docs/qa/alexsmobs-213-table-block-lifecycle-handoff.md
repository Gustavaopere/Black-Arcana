# Alex's Mobs Continued 2.1.13 — BlockTransmutationTable, menu e persistência

**Estado inicial:** 🟡 auditoria estática read-only do publisher 2.1.13 historicamente identificado; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Nenhum código do provider foi copiado.

## Continuidade após PR #1112

As PRs #1109–#1112 documentaram receptor C2S, contexto NeoForge, settlement e reroll diferido, `TransmutationData`, NBT e opções de display. Esta etapa investiga **o bloco dono da mesa e sua relação com o menu/slots/tile**, sem redescobrir as mesmas classes como se fossem novas magias.

Autoridade histórica: `alexsmobs-2.1.13-neoforge+1.21.1.jar` (mod ID `alexsmobs`), SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`, 27.452.738 bytes, CurseForge `1635121/8856498`. **Não está reconfirmado que a modlist atual possui esse mod/versionamento; o estudo não homologa compatibilidade com o pack atual.**

## Fontes e plano reproduzível

- [Auditor read-only](alexsmobs_213_table_block_lifecycle_probe.py) e [11 testes sintéticos](alexsmobs_213_table_block_lifecycle_probe_test.py).
- [GitHub Actions](../../.github/workflows/alexsmobs-213-table-block-lifecycle.yml) baixa JAR por URL fixa, impõe SHA-256/tamanho e Java 21; valida os fingerprints do tile e menu contra [snapshot C2S](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json).
- Owners inspecionados: `BlockTransmutationTable`, `MenuTransmutationTable`, `TileEntityTransmutationTable`, `MenuTransmutationTable$1` e `MenuTransmutationTable$2`. O scanner de outras classes usa apenas strings `BlockTransmutationTable/TileEntityTransmutationTable/MenuTransmutationTable` no classfile: **um candidato não prova chamada, hook ou cobertura exaustiva**.
- Relatório JSON registra hash de classfile, roster com descritores, fingerprints de métodos, offsets, branches e windows de operandos relacionados a bloco, menu, cliente/servidor, owner, slots, transmutação e notificações `setChanged`/`sendBlockUpdated`; não publica corpos integrais do código de terceiro.
- Resultados de descoberta não promovem o numerador, Stage ou hooks; após observar o JSON real, fixar digest SHA-256, documentar somente ramos efetivamente comprovados, reexecutar `--lock` no CI final e atualizar a ficha individual.

## Questões que precisam de prova

1. **Abertura do menu:** como `BlockTransmutationTable` resolve jogador, lado lógico, `MenuProvider` e `BlockEntity`, e quais guardas impedem abertura inválida?
2. **Validade de sessão:** há ligação demonstrada com `ContainerLevelAccess`, posição e tipo de bloco? `MenuTransmutationTable.stillValid` deve ser diferenciado de eventual chamada no `transmute`.
3. **Reroll e slots:** `MenuTransmutationTable$1.setChanged` já é conhecido por chamar `slotsChanged` e `SimpleContainer.setChanged`. O callback realmente informa o `BlockEntity` ou só o container de inventário?
4. **Persistência:** existência/ausência de chamadas diretas a `BlockEntity.setChanged` e `Level.sendBlockUpdated` é sinal estático. Não concluir perda de dados sem verificar callbacks indiretos, superclass, save/chunk lifecycle e reload físico.
5. **Abuso/replay:** menu de mesma classe, mas outra mesa, player ausente, chunk descarregado, input retirado, duas mensagens serializadas e alteração de dimensão precisam de QA dedicada.

## Limites/QA e integração

`BlockTransmutationTable` é **consumidor técnico** da raiz `Item Transmutation`, não uma nova magia. Black Arcana não deve duplicar custo, movimento de itens, XP nem reroll do provider. O RPG Skill Tree permanece dono apenas de progressão/perks/gates por contratos reais.

Checks CI de desassembly/compilação/GameTest do **Black Arcana** não equivalem a execução física do Alex's Mobs no modpack. AMC-T01, AMC-T02, AMC-T03, multiplayer, restauração NBT e testes de sessão continuam sem evidência de PASS. Manter `NO_MUTATION` / fail-closed; nenhum aumento de contratos (0/3 no recorte observado), nenhum avanço de Stage.

## Resultado observado — JAR publisher 2.1.13, CI #44193323159

O [workflow de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44193323159) executou **15 testes sintéticos**, validou o publisher por SHA-1/SHA-256/tamanho, reconheceu as 5 classes proprietárias de bloco/menu/slot/tile e os 1.270 classfiles da população da versão histórica. A busca por nomes binários encontrou **13 classes candidatas a consumidor**; a população inclui registry de bloco, tile e menu, GUI, renderer e message handler. Essa busca não é um grafo de chamadas completo.

O JSON resultante tem **283.162 bytes** e SHA-256 `efeeba730c2f781bb8259fb763245f40c8d70f17c0fb9830f183a250e7ada0e0`. O subrelatório de vínculos de owner tem SHA-256 `bac57871161a1dda4119203a2f59dee4ff0b3080c2d802b26a252264bb74b5e4`. Esses hashes estão no [manifesto de lock](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TABLE-BLOCK-LIFECYCLE-2.1.13.json). O auditor reexecuta a inspeção com `--lock` na CI, sem copiar bytecode/projetos de terceiros.

### 1. BlockTransmutationTable — identidade, acionamento e posição

Owner: `com/github/alexthe666/alexsmobs/block/BlockTransmutationTable.class`; classfile SHA-256 `36a9a206a89bdeb43848aaa37719e9e3dc9d00d29330b1eac760b1242e0a02c1`; **18 métodos** declarados, todos inspecionados no escopo do auditor.

- `newBlockEntity(BlockPos,BlockState)`: instancia `TileEntityTransmutationTable` (`new @0`, ctor `@6`).
- `useItemOn` chama `amUse @11`, depois faz compatibilidade de resultado de interação por `AMCompat.itemResult @14`. Um item específico na mão não é pré-requisito comprovado por esse método.
- `amUse`: `Level.isClientSide @1`; ramo cliente (`ifeq @4 →11`) retorna `InteractionResult.SUCCESS`. No ramo servidor: `BlockState.getMenuProvider @16`, `Player.openMenu @19`, `Stats.INTERACT_WITH_LOOM @25 / Player.awardStat @28`, `Level.getBlockEntity @33`; verifica `instanceof TileEntityTransmutationTable @40` com `ifeq @43 →86`. Se a entidade de bloco corresponde, cria `MessageUpdateTransmutablesToDisplay @53`, lê `playerId @59`, seleciona `getPossibility(0/1/2) @65/@71/@77`, instancia mensagem `@80` e **chama `AlexsMobs.sendMSGToAll @83`**. O fluxo servidor termina em `InteractionResult.CONSUME @86`.
- O retorno de `Player.openMenu` é descartado por `pop @22`; **o próprio `amUse` não testa explicitamente sucesso do OptionalInt antes de tentar a atualização das alternativas**. Não equivale a prova de exploração ou screen efetivamente aberto.
- `getMenuProvider` lê `Level.getBlockEntity @2`, cria `SimpleMenuProvider @7` e o callback `lambda$getMenuProvider$2` usa `ContainerLevelAccess.create(level,pos) @9`, `instanceof TileEntityTransmutationTable @15` e `MenuTransmutationTable.<init> @29`. Se a entidade não tem o tipo esperado, a ramificação usa `aconst_null @28` para o parâmetro `table`. Guardas do método `MenuTransmutationTable.transmute` já registram tabela null como saída. Isso ainda **não valida sessão/posição diante de um packet posterior**.
- `getTicker` usa `AMTileEntityRegistry.TRANSMUTATION_TABLE @1`, callback `invokedynamic tick @12` e `createTickerHelper @17`, relacionando a classe de bloco ao tick próprio do tile. Não autoriza afirmar frequência efetiva de reroll ou persistência sem teste.
- `MenuTransmutationTable.stillValid(Player)` chama helper de `AbstractContainerMenu.stillValid(access,player,AMBlockRegistry.TRANSMUTATION_TABLE) @16`. No método `transmute` anteriormente auditado não há chamada **direta** a esse helper, de modo que a invalidação automática externa e a sessão de origem permanecem `NOT_VERIFIED`.

### 2. Restrição de entrada do slot

O wrapper `MenuTransmutationTable$2.mayPlace(ItemStack)` tem **20 instruções** e quatro branches: `getMaxStackSize @14`, `if_icmple @18 →44` frente à constante `iconst_1 @17`; `ifnull @22 →40` para chave de registry não resolvida; consulta `AMConfig.transmutationBlacklist @25` e `List.contains @32`, com `ifne @37 →44` para chave presente na blacklist. Isso vincula a aceitação a tamanho máximo de stack e blacklist; não transportar exceções/defaults da config de uma versão-fonte diferente. A lista *efetivamente carregada no modpack* continua não capturada.

### 3. Efeito secundário destrutivo: explosão ao destruir a mesa

O próprio `BlockTransmutationTable.onDestroyedByPlayer` chama `explodeOnDestroy(level,pos) @2` antes de delegar a `BaseEntityBlock.onDestroyedByPlayer @15`. Esse é um **efeito secundário do bloco da mesma raiz semântica**, não uma quarta spell.

Em `explodeOnDestroy`:

- `AMConfig.transmutingTableExplodes @0` e `ifeq @3 →46` suprimem a chamada de explosão quando o booleano está falso.
- Coordenadas são centralizadas: `BlockPos.getX @9`, `getY @18`, `getZ @27`, cada uma convertida para double e somada ao literal **0,5** (`ldc2_w @13/@22/@31`).
- `Level.explode @42` usa literal de potência **3,0f** (`ldc_w @35`), argumento booleano de fogo **false** (`iconst_0 @38`) e `Level.ExplosionInteraction.BLOCK @39`.
- A classe `onDestroyedByPlayer` não exibe um segundo guard de config próprio: ele delega ao `explodeOnDestroy`. A elegibilidade física desse caminho, server side, reivindicações, eventos de proteção, cancelamento da destruição e eventual efeito em blocos **não foram testados**. A chamada `Level.explode` não prova por si só quais blocos seriam alterados depois dos demais gates do servidor.

A existência de `ExplosionInteraction.BLOCK` importa ao desenho de **World Safety**, mas a `WorldEffectPolicy` do Black Arcana governa seus próprios efeitos, **não intercepta automaticamente explosões internas de outro mod**. Até haver contrato real de interceptação/compatibilidade e testes com proteções, manter qualquer perk que dependa dessa explosão como `NO_MUTATION`.

### 4. Sinais de mudança e durabilidade do tile

O `MenuTransmutationTable$1.setChanged` nativo chama `MenuTransmutationTable.slotsChanged @5` e `SimpleContainer.setChanged @9`. `slotsChanged` agenda `TileEntityTransmutationTable.setRerollPlayerUUID @28` após guards `table != null` e `!hasPossibilities`. O callback `setChanged` observado modifica/avisa o container, **não chama diretamente `BlockEntity.setChanged`**.

Nos métodos inspecionados do `BlockTransmutationTable` e da `TileEntityTransmutationTable` foram registrados **zero** calls diretos de `setChanged` ou `sendBlockUpdated` no tile. Isso **não comprova ausência de dirty mark por superclasse, componente externo, slot, chamada indireta ou versão do runtime**; faltam inspeção externa e QA de save/unload/reload. O reroll diferido do `tick` e a ausência de persistência direta de `rerollPlayerUUID` continuam conforme PR #1111.

### 5. Matriz de riscos e QA não executada

- Config efetiva: `AMConfig.transmutingTableExplodes`, `transmutationBlacklist` e limites de custo/pools não capturados no modpack contemporâneo.
- Integração: não reenviar `MessageUpdateTransmutablesToDisplay` nem duplicar `Slot.set`, XP ou `postTransmute`; `sendMSGToAll` é um broadcast de display, e o receptor precisa limitar a apresentação pelo jogador.
- Negativos pendentes: menu aberto com block entity nula/alterada, janela e table stale, click com item blacklist, input não stackável, múltiplos jogadores, dois packets em sequência, duplicação de output/XP, replay, fechar menu antes de receber callback, destruir mesa com config ligada/desligada e claims/World Safety.
- `AMC-T01..T03`, config e datapack do pack, dedicated client/server, dimensão, unloaded chunk e persistência real ainda `NOT_TESTED`.

**Sem promoção:** `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; 0/3 contratos estáticos integrais certificados no recorte observado de Alex's Mobs; modlist física atual não reconfirmada; Stage 06 e RPG Skill Tree intocados.
