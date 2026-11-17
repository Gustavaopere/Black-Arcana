# Alex's Mobs Continued 2.1.13 — Transmutation Table C2S: evidência individual

**Estado:** 🟡 auditoria SHA-exata read-only / descoberta inicial; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`.

## Motivação e proveniência

Após a integração da PR #1106 (Dimensional Carver), a próxima ação do recorte observado de Alex's Mobs é **Item Transmutation**, hoje 0/3 contratos estáticos. A [ficha existente](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/actions/item-transmutation.md) documenta `MenuTransmutationTable.clickMenuButton`, `MenuTransmutationTable.transmute` e `TileEntityTransmutationTable`, mas não demonstra o **handler nativo completo** de `MessageTransmuteFromMenu` nem a proveniência do remetente, da seleção e da sessão.

Autoridade física: modlist atual do sibling `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod ID `alexsmobs`, Minecraft 1.21.1 NeoForge / Java 21; SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`, 27.452.738 bytes. Auditoria exata anterior PR #511 / GitHub Actions 36949047824. Não usar `Codx-org/AlexsMobsContinued` 2.2.3 como prova da versão instalada.

## Questão técnica central

A ficha já comprova que `clickMenuButton` envia seleção e que o menu faz settlement de item/XP/reroll após guardas específicos. **Isso não comprova que o receptor C2S autentica o jogador da conexão, vincula o menu atual, valida o índice sem confiar em dados do cliente, impede replay ou evita duplo settlement.** Sem essas garantias, nenhuma perk pode modificar custo, opções, output, XP ou reroll com segurança.

## Protocolo verificável

O [probe](alexsmobs_213_transmutation_c2s_probe.py), [13 testes sintéticos](alexsmobs_213_transmutation_c2s_probe_test.py) e [workflow](../../.github/workflows/alexsmobs-213-transmutation-c2s.yml) auditam **três classes** no publisher físico:

- `com/github/alexthe666/alexsmobs/message/MessageTransmuteFromMenu.class`;
- `com/github/alexthe666/alexsmobs/inventory/MenuTransmutationTable.class`;
- `com/github/alexthe666/alexsmobs/tileentity/TileEntityTransmutationTable.class`.

O auditor confere duplamente SHA do JAR, tamanho e major JVM 65, lista de métodos/descritores, SHA do corpo interpretado, contagens de branches e callsites relevantes. Publica somente janelas **curtas e delimitadas** de operandos, sem copiar corpo inteiro ou redistribuir JAR de terceiros.

O primeiro run imprime `UNSEALED_TRANSMUTATION_C2S_DISCOVERY`; após inspeção das evidências reais, fixar o manifesto `EXACT-TRANSMUTATION-C2S-2.1.13.json`, atualizar esta nota e a ficha individual, e repetir `--snapshot`. A aplicação de regras de segurança exigirá reconstrução dos branches/ligações **efetivamente** observados e testes negativos; uma mera referência de `getSender` não prova que o retorno seja usado como autoridade no settlement.

## Estados e gates

- **Inventário:** três raízes semânticas presentes (1 `COUNTED_EXACT` transmutation, 2 `CONDITIONAL`); não criar novas raízes para as três alternativas de output.
- **Contrato estático:** manter 0/3 enquanto faltarem eixos e certificação individual.
- **Recepção C2S:** avaliar compatibilidade do contexto, playerId, containerMenu, slot, escolha e persistência; declarar desconhecido tudo que não estiver demonstrado.
- **Perks e Mastery:** no máximo mapeamento de candidatos conceituais; `NO_MUTATION` / fail-closed.
- **QA física:** `AMC-T01..T03` e teste de multiplayer, mudança de inventário, disconnect/reload, seleção inválida e replay continuam `NOT_TESTED`.
- **Stage:** 06 permanece ativo; a auditoria não implementa nem promove a Stage.

Nenhuma alteração em Raygun, X-Ray, ACArmorMaterial, Enshrouded ou RPG Skill Tree é feita nesta etapa.

## Resultado físico SHA-exato — CI #44157210140

O [run de descoberta no publisher 2.1.13](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44157210140) confirmou JAR físico SHA-1/SHA-256 e tamanho, **15/15 testes sintéticos**, três classes principais, duas referências externas, quatro referencias validadas ao nome do pacote nas classes externas e **35 callsites selecionados** nos owners principais. Foi criado [EXACT-TRANSMUTATION-C2S-2.1.13.json](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json). A primeira descoberta de três classes mostrou que o packet não tem método `handle` próprio; a segunda localizou o **Handler aninhado** e a **classe registradora** por inspeção do mesmo JAR.

### 1. Estrutura da mensagem e registro

| Classe binária | SHA-256 do classfile | Declaração/relevância |
|---|---|---|
| `MessageTransmuteFromMenu.class` | `19f5adc1a384c085a2cd511fac3c9afcecf2d4eecc58ac46ea57fbd4c1a34e84` | **4 métodos**: construtores `(II)V`, `()V`, `read(FriendlyByteBuf)` e `write(Message,FriendlyByteBuf)`. Mensagem é portadora de `playerId` e `choice`, não handler |
| `MessageTransmuteFromMenu$Handler.class` | `b2ebdc3a88d6aecf68290ae2376fa4c3ee8885b3aff71260cbf0b4986f199146` | `handle(MessageTransmuteFromMenu,AMNetContext)` e `lambda$handle$0(AMNetContext,Message)` são o processamento de contexto observado |
| `AlexsMobs.class` | `8601044e454d365bf8605c4dc8f94b7e1ab4dbf50b2b51b3cec36dc677279af6` | `setup(FMLCommonSetupEvent)` possui `ldc_w MessageTransmuteFromMenu.class @375`, próximo de `registerMessage(Class,BiConsumer,Function,BiConsumer) @393`; vinculação exata de lambdas registradas ainda não demonstrada por bootstrap |
| `AMNetContext.class` | `6f33af8ea8e4b16f84473b9db291c395a1d76c9ea8dfb515bc345b99558b28e7` | Interface declara `setPacketHandled(boolean)`, `enqueueWork(Runnable)`, `getSender(): ServerPlayer`, `isClientSide(): boolean`. **Implementação concreta do adaptador não foi analisada** |
| `MenuTransmutationTable.class` | `e4f3700261fe9bbb0a8895359dc98739337595cb07b3c0fe0a9480f6de4d5e76` | Nove métodos, incluindo envio e settlement |
| `TileEntityTransmutationTable.class` | `4879c9f0072866d0d594731538e0eaa509696505ea7b6ade79c19d4a885a1783` | Doze métodos, incluindo alternativas, seleção e pós-settlement |

**Codec de inteiros observado:** `read(FriendlyByteBuf)` invoca `readInt` duas vezes; `write(..., FriendlyByteBuf)` invoca `writeInt` uma vez para `playerId` e outra para `choice`. A versão não fornece evidência de autenticação por codec, rejeição antecipada de índice ou nonce antirreplay. Os campos transportados são dados enviados pelo cliente, não autoridade.

### 2. Receptor e guardas SHA-exatos

No `MessageTransmuteFromMenu$Handler.handle`, o fluxo marca pacote tratado via `AMNetContext.setPacketHandled` e agenda a rotina via `AMNetContext.enqueueWork`, que captura contexto e mensagem em `invokedynamic`.

A rotina `lambda$handle$0` tem **28 instruções JVM**, com os seguintes 12 pivôs **obrigatórios e verificados pelo auditor**:

| Offset JVM | Instrução | Significado estático delimitado |
|---|---|---|
| `@1` | `AMNetContext.getSender()` | Consulta o `ServerPlayer` do contexto |
| `@8`/`@13` | `isClientSide()` / `ifeq 23` | Há separação explícita de lado lógico no caminho de seleção do jogador |
| `@19` | `CommonProxy.getClientSidePlayer()` | No ramo cliente, consulta jogador local; **não substitui o sender servidor** |
| `@24` | `Player.getId()` | Lê ID do jogador resolvido |
| `@28`/`@31` | `Message.playerId` / `if_icmpne 61` | Se os IDs diferem, desvia para a saída, sem entrar no menu |
| `@35`/`@38`/`@41` | `Player.containerMenu` / `instanceof MenuTransmutationTable` / `ifeq 61` | O menu ativo deve ter o tipo correto; caso contrário, sai |
| `@55`/`@58` | `Message.choice` / `MenuTransmutationTable.transmute(Player,int)` | A escolha do pacote é encaminhada diretamente à tentativa de settlement no menu |

**Resultado demonstrado:** no bytecode publisher existe uma comparação efetiva de `playerId` com o jogador escolhido pela lógica do contexto, um gate de **tipo do menu ativo** e encaminhamento do `choice` apenas depois desses guards. Isso é mais forte que a conjectura anterior de receptor ainda não examinado. **Não demonstra**: que `AMNetContext.getSender` é sempre impossível de falsificar no bridge concreto, que o menu ativo pertence à posição/tabela originalmente aberta, validação de escolha estrita (não apenas clamp), nonce/idempotência nem correção da transação sob concorrência.

### 3. Settlement e bypass de guardas indevidos

`MenuTransmutationTable.clickMenuButton(Player,int)` consulta `Level.isClientSide @4` e no caminho cliente constrói `MessageTransmuteFromMenu(player.getId(),choice)` (`new @10`, `<init>(II)V @19`).

`MenuTransmutationTable.transmute(Player,int)` possui sete branches. Seleção via `TileEntityTransmutationTable.getPossibility(int) @18`; verifica `Level.isClientSide @44; ifne @47 → 152`, ausência de tabela, razão de tamanhos, presença das alternativas, entrada válida e nível XP suficiente ou `Abilities.instabuild`. Quando os guards deixam prosseguir, grava `ItemStack.setCount @122`, `Slot.set @131`, `Player.giveExperienceLevels @138` e `TileEntityTransmutationTable.postTransmute @149`.

`TileEntityTransmutationTable.getPossibility(int)` consulta `Mth.clamp(choice,0,2)` no `@3`. Assim, uma seleção numérica inválida **pode ser normalizada** ao extremo; não existe prova de rejeição explícita no getter. O protocolo de pacotes e as políticas da config/de sessão exigem testes negativos para concluir segurança.

### 4. Integração de perks e QA restante

A boundary de recepção possui guardas **estáticos**, mas ainda não existe extensão mutadora aprovada; valor XP efetivo depende da configuração do pack, e o lado cliente continua não autoritativo para settlement. Black Arcana não duplica `setCount`, `Slot.set`, `giveExperienceLevels` ou `postTransmute`; o RPG Skill Tree continua provider somente de progressão/gates.

Permanecem: revisão exata do `AMNetContext` concreto e registry bootstrap `registerMessage`, teste de sessão/menu/posição/owner, seleção inválida, replay, cliques paralelos, inventário modificado, persistência de UUID/possibilidades, datapacks e prova de execução dedicada `AMC-T01..T03`.

**Estados preservados:** `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Apenas uma das três raízes de Alex's Mobs foi detalhada nesta auditoria, sem promoção de `0/3` contratos estáticos e sem criação de nova ação.
