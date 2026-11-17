# Transmutation Table — Item Transmutation

- Provider: **Alex's Mobs Continued** (`alexsmobs`)
- Version: `2.1.13`
- Publisher SHA-1 (histórico verificado contra modlist anterior; versão atual pendente): `50ddafdf3d12b33331e4eecb4ab514ae451baadd`
- Owner surface: `alexsmobs:transmutation_table`
- Semantic type: deliberate supernatural item-transmutation action
- State: `COUNTED_EXACT`

## Identity and trigger

The publisher JAR 2.1.13, previously matched to a physical modlist, exposes a direct player-driven Transmutation Table path:

- player opens the provider table/menu;
- an eligible input item is inserted;
- the provider exposes three current transmutation possibilities;
- the player selects one possibility;
- the selection reaches the server-side transmutation settlement.

This is one parameterized **Item Transmutation** identity. Inputs, three displayed candidates, rarity pools, XP amounts, rerolls and result items are parameters of this root rather than separate spell identities.

## Server settlement

Exact artifact evidence closes that the provider:

- replaces the input with the selected transmuted result;
- removes the configured XP-level cost;
- records the provider transmutation state;
- agenda o reroll para o próximo processamento de tick da tabela, condicionado à presença do jogador, como detalhado na auditoria de ciclo de vida.

Black Arcana must not replay the result replacement or charge a second cost.

## Exact acquisition

The exact artifact contains the provider's shaped Transmutation Table recipe. The audited acquisition surface is sufficient for catalog-level owner reachability and does not inherit the Void Worm summon gate.

## Disposition

- exact action identity: closed;
- exact owner acquisition: closed at catalog level;
- strict state: `COUNTED_EXACT`;
- strict contribution from this root: **+1**.

## Evidence boundary

The provider remains authority for candidate generation, rarity pools, effective XP cost, reroll behavior, table state and result settlement. This card does not invent current tuning values.

Source: `../EXACT-2.1.13-ARTIFACT-AUDIT.md`.

## Matriz de execução e progressão (2026-10-29)

Contrato JAR exato: seleção no menu, settlement server-owned de input/output, débito de XP e reroll são **um único evento causal**. O custo numérico e a autorização de `MessageTransmuteFromMenu` por slot/jogador/sessão **não** estão certificados por teste de modpack; validar `AMC-T01..T03` antes de reduzir XP, aumentar escolhas ou alterar candidatos. Não transformar as três opções em três spells. Mutadores **⛔ fail-closed** sem hook real. Veja [matriz de QA](../EXACT-ARTIFACT-PERK-QA-GATES-2.1.13.md) e [desvio de versão-fonte](../PUBLIC-SOURCE-VERSION-DRIFT-2026-10-29.md).

## Operandos de controle confirmados no JAR 2.1.13 (2026-10-31)

- `MenuTransmutationTable.clickMenuButton` envia `MessageTransmuteFromMenu(playerId, choice)` pelo cliente; a validação do **handler servidor** e do vínculo sessão/jogador não está certificada.
- `TileEntityTransmutationTable.getPossibility(int)` aplica **`Mth.clamp(choice, 0, 2)`**; `hasPossibilities` exige os três elementos presentes e não vazios. Não confundir clamp com rejeição de índice inválido.
- `MenuTransmutationTable.transmute` só entra no settlement se estiver server-side, houver tabela, input não vazio, possibilidades presentes, ratio de tamanhos >0 e XP suficiente **ou** `Abilities.instabuild`.
- Fórmula observada: `ratio = inputMaxStackSize / outputMaxStackSize`; `outputCount = max(1, floor(inputCount / ratio))`. Depois o provider chama `Slot.set(output)`, `giveExperienceLevels(-AMConfig.transmutingExperienceCost)` e `postTransmute`.
- `postTransmute` registra dados por UUID, soma a quantidade de entrada ao contador de transmutação, possui advancement em **1000** itens e define o UUID para reroll. XP efetivo, autorização C2S, concorrência e persistência não passaram por QA físico.

**Proveniência:** [mapa de bytecode SHA-exato](../EXACT-CONTROL-OPERANDS-2.1.13.md). Não certificar mutadores que alterem XP, pools, quantidades, ou reroll.

## Boundary C2S efetiva — auditoria SHA-exata 2.1.13

**Novas evidências:** [manifesto nativo do JAR exato](../EXACT-TRANSMUTATION-C2S-2.1.13.json) · [relatório de recepção/menu e limites](../../../../../docs/qa/alexsmobs-213-transmutation-c2s-handoff.md) · [auditor reproduzível](../../../../../docs/qa/alexsmobs_213_transmutation_c2s_probe.py). O publisher permanece `alexsmobs-2.1.13-neoforge+1.21.1.jar`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`.

A mensagem `MessageTransmuteFromMenu` é portadora de dois inteiros: **`playerId`** e **`choice`**. Seus métodos `read(FriendlyByteBuf)` e `write(Message,FriendlyByteBuf)` usam duas operações `readInt` / `writeInt`; os quatro métodos declarados da classe não contêm `handle`. O processamento real pertence à classe aninhada `MessageTransmuteFromMenu$Handler`.

**Registro candidato observado:** `AlexsMobs.setup(FMLCommonSetupEvent) @375` referencia a classe da mensagem, próxima a `registerMessage(Class,BiConsumer,Function,BiConsumer) @393`. A associação dos callbacks de registro ao tipo de payload e à direção de transporte não foi inteiramente provada via bootstrap.

**Handler:** `handle(Message,AMNetContext)` utiliza `setPacketHandled` e `enqueueWork`; o `lambda$handle$0` tem guardas compilados precisos:

- `AMNetContext.getSender @1` consulta o `ServerPlayer` disponibilizado pelo contexto; existe ramo `isClientSide @8` e, no caminho cliente, `CommonProxy.getClientSidePlayer @19`;
- `Player.getId @24`, `Message.playerId @28`, `if_icmpne @31 →61`: o ID informado **precisa coincidir com o jogador resolvido** para o caminho prosseguir;
- `Player.containerMenu @35`, `instanceof MenuTransmutationTable @38`, `ifeq @41 →61`: o menu ativo precisa ser do tipo correto;
- `Message.choice @55` é passado para `MenuTransmutationTable.transmute(Player,int) @58` apenas depois desses guardas.

**Alcance dessas checagens:** comparação de ID e verificação do tipo do menu são fatos do bytecode, não prova de autenticação final do bridge de rede, da posição da tabela, da identidade da sessão, de permissão ou da ausência de replay. A implementação concreta de `AMNetContext` ainda não foi reconstruída.

**Transmutação efetiva solicitada:** `MenuTransmutationTable.transmute` verifica lado servidor, tabela, input, possibilidades, razão de tamanho e XP suficiente ou `Abilities.instabuild`; quando os guards são satisfeitos, solicita `ItemStack.setCount @122`, `Slot.set @131`, `Player.giveExperienceLevels @138` e `postTransmute @149`. `TileEntityTransmutationTable.getPossibility @3` aplica `Mth.clamp(choice,0,2)`; a escolha fora de `0..2` pode ser **normalizada**, não necessariamente rejeitada. Nenhum resultado físico ou duplo settlement sob replay foi provado.

**Perks possíveis (conceituais somente):** custo de XP, alternativas, quantidades e reroll exigem hook real antes da transação server-owned; sem esse hook não modificar nem repetir consumo, `postTransmute`, output, XP ou Mastery. **`static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.** A ficha continua ⚠️ parcial; Alex's Mobs permanece com **0/3 contratos estáticos integrais certificados** no recorte observado.

## Investigação complementar do contexto de rede (sem certificação)

A partir da PR #1109, a prova do handler e dos guardas `playerId`/tipo de menu é preservada. A [nova investigação read-only](../../../../../docs/qa/alexsmobs-213-context-bridge-handoff.md) rastreia **candidatos** a implementadores concretos de `AMNetContext` e entradas de `BootstrapMethods` próximas ao registro nativo de mensagens no mesmo JAR publisher SHA-exato. Um nome de interface no constant pool, uma implementação direta encontrada ou um handle de lambda isolado não demonstram autenticação de conexão nem direção do pacote.

**Ainda não confirmado:** vínculo forte entre `AMNetContext.getSender` e a conexão de origem, bootstrap exato dos callbacks, identidade da sessão/tabela, rejeição de escolhas inválidas, replay/concorrência e segurança de settlement. A conclusão requer relatório real do JAR, revisão do CFG e QA negativa dirigida. Portanto **sem alteração de contagem, índice, hooks, custos, XP, reroll ou Mastery**: `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

### Evidência de implementação concreta do contexto — CI #44167951912

No JAR publisher 2.1.13 SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`, `AMNeoNetwork$1` implementa diretamente `AMNetContext`; `getSender` consulta `IPayloadContext.player()` e só retorna `ServerPlayer` (caso contrário, `null`). `isClientSide` consulta `IPayloadContext.flow().isClientbound()`, e `enqueueWork` delega ao contexto NeoForge. `AMNeoNetwork.handle` adapta o contexto e despacha por `AMNeoNetwork$Registration.handle`; os bootstrap handles #62/#63/#64 de `AlexsMobs.setup` identificam respectivamente `write/read/Handler.handle` da mensagem de transmutação.

**Importante:** `AMNeoSend.registerPlay` utiliza `PayloadRegistrar.playBidirectional`; a registration do envelope é bidirecional, não C2S-only. `AMNeoNetwork.decodePayload` valida o índice do **tipo de mensagem** (faixa `0 <= index < REGISTRATIONS.size()`), enquanto `choice` é outro inteiro, usado na seleção de saída e submetido a clamp pelo menu/tile. A [auditoria e seus limites](../../../../../docs/qa/alexsmobs-213-context-bridge-handoff.md) contêm offsets JVM, hashes de classfiles e caminho de reprodução.

Essa evidência não demonstra vínculo de mesa/sessão, impossibilidade de replay, idempotência do settlement, proteção contra concorrência ou QA física em modpack. Permanece `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; nenhuma promoção de índice ou perk.

## Settlement e ciclo de vida — auditoria do JAR 2.1.13 (PR #1111)

**Manifesto reexecutável:** [EXACT-TRANSMUTATION-SETTLEMENT-2.1.13.json](../EXACT-TRANSMUTATION-SETTLEMENT-2.1.13.json) · [handoff com offsets e limitações](../../../../../docs/qa/alexsmobs-213-transmutation-settlement-handoff.md) · [auditor read-only](../../../../../docs/qa/alexsmobs_213_transmutation_settlement_probe.py). Escopo: **3 classes e 21 métodos**, SHA do publisher e fingerprints de métodos comparados ao manifesto anteriormente selado. O novo relatório tem SHA-256 `ce2690b5568168b7d446e2dd9184ab8f17dbafa4784cd43bba353070f6975a62`; CI exige reexecução idêntica antes de aceitar o lock.

**Ordem de efeitos no método `MenuTransmutationTable.transmute`:** `ItemStack.setCount @122` → `Slot.set @131` → `Player.giveExperienceLevels @138` → `TileEntityTransmutationTable.postTransmute @149`. São calls nativos após os guards documentados; **não há prova de transação atômica, rollback ou proteção contra pacote repetido**. O override de `stillValid` existe, mas não é invocado diretamente por `transmute`; investigar a invalidação de menus provida pelo Minecraft/NeoForge antes de afirmar proteção ou bypass.

**A atualização de reroll é diferida:** `postTransmute @50` chama `TransmutationData.onTransmuteItem`, atualiza `totalTransmuteCount @79`, verifica advancement de 1.000 itens e apenas agenda `setRerollPlayerUUID @114`. No tick, `getPlayerByUUID @25` procura o jogador; se o retorno for `null`, `ifnull @30 → @82` salta `randomizeResults @79`, mas o UUID pendente é limpo em `@84` mesmo assim. Com jogador encontrado, a geração solicita `rollPossiblity` para índices 0, 1, 2. A **perda da solicitação de reroll por jogador ausente** é um resultado do CFG estático; comportamento em logout/unload/restart permanece não testado.

**NBT/persistência:** `loadAdditional`/`saveAdditional` movimentam `totalTransmuteCount`, `PlayerTransmutationData`, `TransmutationData` e arrays de alternativas; não referenciam diretamente `rerollPlayerUUID`. Os dados registrados por jogador e as alternativas persistidas não constituem prova de restauração do **agendamento transitório**. Necessário executar AMC-T01..T03, replay, concorrência, sessão inválida, saída fora de 0..2 e save/restart no modpack instalado.

**Integração:** impedir perks que alterem quantidade, custo de XP, choice, pools ou reroll até comprovar seam segura e idempotência, sem repetir efeitos ou alterar runtime alheio. `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Índices permanecem 0/3 contratos integrais no recorte de Alex's Mobs; universo integral do mod não foi homologado.

## Dados por jogador, pesos, NBT e display — auditoria SHA-exata 2.1.13

**Evidência reproduzível:** [manifesto SHA-exato](../EXACT-TRANSMUTATION-DATA-2.1.13.json) · [relatório técnico de estado e sincronização](../../../../../docs/qa/alexsmobs-213-transmutation-data-handoff.md) · [auditor read-only](../../../../../docs/qa/alexsmobs_213_transmutation_data_probe.py) · [CI do publisher](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44182648998).

O escopo examinado inclui **8 classfiles** e **6 candidatos binários** (referências de constant pool, não grafo completo). O owner `com.github.alexthe666.alexsmobs.misc.TransmutationData` possui **10 métodos** e um mapa `Object2DoubleMap<ItemStack>` inicializado por `Object2DoubleOpenHashMap`. `getWeight` e `putWeight` comparam chaves por `ItemStack.isSameItemSameComponents`; `putWeight` aplica `Math.max(0,peso)`.

### Fórmulas de pesos — bytecode físico 2.1.13

Se `n` representa `ItemStack.getCount()`, `a = AMConfig.transmutingWeightAddStep` e `r = AMConfig.transmutingWeightRemoveStep`, com valores efetivos da config **não capturados**:

- Atualização de entrada: `w_entrada' = max(0, w_entrada + ln(pow(n,a)))` — `calculateAddWeight @5/@8`, `dadd @23`, `putWeight @24`.
- Atualização de saída: `w_saida' = max(0, w_saida - ln(pow(n,r)))` — `calculateRemoveWeight @5/@8`, `dneg @11`, `dadd @38`, `putWeight @39`.
- `getTotalWeight()`: soma `DoubleStream.sum` dos pesos armazenados.
- `getRandomItem(Random)`: avalia pesos positivos com escore `-ln(U)/peso`, `U = Random.nextDouble()`; a comparação `dcmpg @80` mantém o menor escore observado e o item selecionado é copiado. Essa é a amostragem interna do objeto; **a distribuição efetiva das três opções também depende dos gates de loot, RNG e configuração**.

`TileEntityTransmutationTable.randomizeResults` gera as três possibilidades com `rollPossiblity(player,0/1/2) @3/@9/@15`. O caminho alternativo de `TransmutationData.getRandomItem @94` envolve `limitTransmutingToLootTables` e comparação de `Random.nextFloat` com limiar `min(0.01875000074505806 × getTotalWeight(), 0.20000000298023224)`; **esse limiar isolado não é uma taxa efetiva comprovada de resultados**. Os valores numéricos são os literais double do bytecode, não valores reconfigurados pelo Black Arcana.

### Persistência e sincronização

`TransmutationData.saveAsNBT/fromNBT` usa lista `TransmutationData` cujas entradas têm chaves `Item` e `Weight`. `TileEntityTransmutationTable.saveAdditional/loadAdditional` conserva `TotalCount`, `PlayerTransmutationData` por `UUID`, `TransmutationData` e opções de output, mas não referencia diretamente o UUID transitório que agenda reroll. Não há teste físico de descarregamento/recarregamento do chunk.

`MessageUpdateTransmutablesToDisplay` serializa `playerId` e três `ItemStack`; o `$Handler` verifica o ID do jogador e chama `CommonProxy.setDisplayTransmuteResult` para índices 0, 1 e 2. **Não presumir direção S2C exclusiva**, pois o envelope NeoForge auditado na PR #1110 é bidirecional.

`MenuTransmutationTable$1.setChanged` chama `MenuTransmutationTable.slotsChanged` e `SimpleContainer.setChanged`. Não apareceu `BlockEntity.setChanged` diretamente nos métodos selecionados do tile; isso **não é prova de perda de persistência**, porque consumidores indiretos não foram exauridos.

**Boundary para perks:** peso, seleção, custo de XP, reroll e opções continuam sob autoridade do provider, sem hook mutador validado. O JAR atual da modlist do sibling ainda não foi reconfirmado. `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; 0/3 contratos estáticos certificados no recorte observado.
