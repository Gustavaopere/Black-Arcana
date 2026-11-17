# Transmutation Table — Item Transmutation

- Provider: **Alex's Mobs Continued** (`alexsmobs`)
- Version: `2.1.13`
- Exact physical/publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`
- Owner surface: `alexsmobs:transmutation_table`
- Semantic type: deliberate supernatural item-transmutation action
- State: `COUNTED_EXACT`

## Identity and trigger

The exact installed artifact exposes a direct player-driven Transmutation Table path:

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
- rerolls provider result state after settlement.

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
