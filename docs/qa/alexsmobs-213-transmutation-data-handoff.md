# Alex's Mobs Continued 2.1.13 — TransmutationData, NBT e sincronização das opções

**Estado:** 🟡 auditoria estática read-only do publisher histórico; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

## Continuidade e escopo

Após as PRs #1109 (receptor), #1110 (contexto NeoForge) e #1111 (settlement, reroll diferido e persistência parcial), esta tranche investiga **o objeto de dados e seus consumidores**, não repete a inspeção do pacote C2S nem implementa hook mutador.

A versão física confirmada anteriormente foi `alexsmobs-2.1.13-neoforge+1.21.1.jar`, SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8` e 27.452.738 bytes. **Não há prova nova de que a modlist atual ainda inclui esse provider:** a árvore atual do sibling não mostrou uma entrada nominal de Alex's Mobs. Análises abaixo são condicionadas ao JAR historicamente identificado; não interpretar como compatibilidade certificada com um pack diferente.

## Método reprodutível

O [auditor](alexsmobs_213_transmutation_data_probe.py), os [testes sintéticos](alexsmobs_213_transmutation_data_probe_test.py) e o [workflow SHA-exato](../../.github/workflows/alexsmobs-213-transmutation-data.yml) leem somente o JAR publisher.

Escopo principal: `TransmutationData` (métodos `onTransmuteItem`, `fromNBT`, `saveAsNBT`, `getTotalWeight`, `getRandomItem`); `AMCompat` (wrappers NBT aplicáveis); `TileEntityTransmutationTable` (`loadAdditional`, `saveAdditional`, `postTransmute`, `randomizeResults`, `tick`); `MenuTransmutationTable` (construtor/slots/removed); `MessageUpdateTransmutablesToDisplay` (codec e processamento) e classes auxiliares presentes no JAR.

O scanner faz descoberta global por referências binárias a `TransmutationData` e `MessageUpdateTransmutablesToDisplay`, mas essas ocorrências são somente **candidatos**, não prova de call graph completo. O resultado JSON contém classfile SHA-256, assinaturas, fingerprints de métodos, branches, callsites, literais limitados e sinais diretos de `setChanged`/`sendBlockUpdated`, sem publicar o corpo completo de qualquer implementação de terceiros.

O workflow verifica os hashes físicos, o selo anterior de classes nativas e os índices de certificação. A primeira execução gera discovery read-only; depois da análise do resultado é possível fixar um manifesto SHA-256 do relatório completo e reexecutar os testes.

## Perguntas de investigação

1. Como `TransmutationData` registra input/output e calcula peso acumulado, e quais fatores efetivamente mudam as probabilidades? Verificar os operandos, sem assumir que pesos declarativos bastam para calcular chances efetivas.
2. Quais tags NBT persistem os dados por jogador e as alternativas de output? Diferenciar `TransmutationData` do campo transitório `rerollPlayerUUID` já identificado na PR #1111.
3. A geração das três alternativas é sincronizada em direção servidor→cliente? Quais classes e side-gates atuam no receptor de `MessageUpdateTransmutablesToDisplay`?
4. Há chamadas diretas a `setChanged` ou `sendBlockUpdated` nos caminhos de reroll e settlement? **Ausência de chamada direta não prova falha de persistência**, que pode ser delegada ao container/slot ou ciclo de vida.
5. Quais consumidores precisam ser considerados para perks de custo, seleção, quantidade, reroll e Mastery sem criar um segundo pipeline transacional?

## Limitações e estados

Esta auditoria não faz download da modlist física local do usuário, não testa o jogo em multiplayer, não certifica replay, não mede chances efetivas em runtime e não habilita perks. Candidatos a extensões permanecem conceituais até comprovar seam real. `NO_MUTATION` e fail-closed permanecem incondicionais.

Não promover o numerador de Alex's Mobs (0/3 no recorte observado), o universo total do provider, o índice global ou Stage 06 com base apenas no scanner. Os testes AMC-T01..T03 e as validações de login/reload/datapack/servidor continuam `NOT_TESTED`.

## Resultado SHA-exato — workflow #44182648998

O [workflow de auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44182648998) passou pelos **13 testes sintéticos**, pela verificação SHA-256/tamanho do publisher 2.1.13 e pela análise de bytecode. O relatório tem **274.739 bytes**, SHA-256 `d9dbb2a9df638cc700802982c94ad7a943bac340dfc3d54cf03532d1876b2cc3`, **8 classes inspecionadas** e **6 classes candidatas** identificadas por strings no constant pool. O [manifesto de lock](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-DATA-2.1.13.json) obriga a reexecução SHA-exata. O resultado é prova estática do JAR histórico, não certificação de perks ou QA física.

### TransmutationData — identidade de peso e atualizações

`misc/TransmutationData.class`: classfile SHA-256 `6cd6976c9ec3d35f908fcf7dfe956a88e9f7b19dcb7be73da5ddc38477a0d8de`; **10 métodos próprios**. O estado usa `Object2DoubleOpenHashMap`, exposto via `Object2DoubleMap`, com keys `ItemStack`. `getWeight` e `putWeight` fazem comparação `ItemStack.isSameItemSameComponents`, não apenas item ID. `putWeight @68` usa `Math.max(0, novoPeso)`; o peso resultante armazenado não pode ser negativo nesse caminho.

`onTransmuteItem(input,output)` consulta os dois pesos originais e realiza duas atualizações aditivas. Para `n = stack.getCount()` e parâmetros **efetivos ainda desconhecidos** `a = AMConfig.transmutingWeightAddStep`, `r = AMConfig.transmutingWeightRemoveStep`:

- `calculateAddWeight(n)`: `Math.pow(n,a) @5` → `Math.log @8` → `Δentrada = ln(n^a)`. `onTransmuteItem @20` / `dadd @23` / `putWeight @24`.
- `calculateRemoveWeight(n)`: `Math.pow(n,r) @5` → `Math.log @8` → `dneg @11` → `Δsaída = -ln(n^r)`. `onTransmuteItem @35` / `dadd @38` / `putWeight @39`.
- Os valores do pack, inclusive eventuais `n=0`, configuração ilegal ou dados corrompidos, **não** foram submetidos a teste de runtime.

`getTotalWeight` chama `Object2DoubleMap.values → DoubleCollection.doubleStream → DoubleStream.sum`. `getRandomItem(Random)` percorre pesos positivos e usa `Random.nextDouble @60`, `Math.log @63`, `dneg @66`, divisão pelo peso da entry `@74`, comparação `dcmpg @80` e cópia do `ItemStack` escolhido `@97`. A regra de ordenação observada corresponde a **amostragem por menor escore exponencial**, `s = -ln(U)/w` para `w > 0`. Isso descreve a seleção deste método isolado, **não a chance final de uma opção**, que é condicionada por fluxo externo e resultados de loot.

### NBT — o que é efetivamente serializado

`TransmutationData.saveAsNBT` grava uma lista `TransmutationData` cujas entradas contêm `Item` serializado por `AMCompat.saveItem` e peso `Weight` por `CompoundTag.putDouble`. `fromNBT` procura `TransmutationData`, lê `Item` com `AMCompat.loadItem`, ignora um `ItemStack` vazio e repassa `Weight` a `putWeight` (que aplica o clamp). O wrapper `AMCompat` foi inspecionado em 12 overloads/métodos NBT relevantes dentre **167 métodos próprios**, sem assumir que a biblioteca inteira foi auditada.

`TileEntityTransmutationTable.saveAdditional/loadAdditional` armazenam `TotalCount`, `PlayerTransmutationData` com `UUID` e `TransmutationData` por jogador, além das três opções de output na entidade de bloco. O `rerollPlayerUUID` transitório já documentado pela PR #1111 não aparece como referência direta nesses métodos; persiste a necessidade de ensaio save/restart e unload.

### Geração, RNG e sincronização de três alternativas

`TileEntityTransmutationTable.randomizeResults` executa `rollPossiblity(player,0/1/2)` nos offsets `@3,@9,@15`. Também contém seleção condicional por `TransmutationData.getRandomItem @94`, com gates de RNG, presença de dados por UUID e `AMConfig.limitTransmutingToLootTables @42`. No ramo observado a comparação utiliza `Random.nextFloat @68` e um limiar calculado com `0.01875000074505806 * getTotalWeight()` e `Math.min(...,0.20000000298023224)` (`dmul @79`, `Math.min @83`, `dcmpg @86`). **Não interpretar o limiar isolado como probabilidade efetiva total** sem reconciliar os demais guards, a config e os três calls de loot.

`MessageUpdateTransmutablesToDisplay` (classfile SHA-256 `861c9c064949cf1b866b82b967127792e19c9dfde59ca2cc318320a157dad57b`) transporta `playerId` por `writeInt/readInt` e três `ItemStack` com `PacketBufferUtils.writeItemStack/readItemStack`. Seu handler aninhado (SHA-256 `4682ca818c3be1c3a8a8fc87cc27f589651f004aab3c8cc89a44a8a647b4fa46`) compara o ID de jogador resolvido e aciona `CommonProxy.setDisplayTransmuteResult` com índices **0, 1 e 2**. A ligação observada é de **atualização de display**, sem prova de autorização final, direção exclusiva ou autenticidade por inspeção desse handler. A PR #1110 já demonstrou que o envelope `AMNeoSend.registerPlay` é bidirecional.

### Notificação de mudança não equivale à persistência do tile

`MenuTransmutationTable$1.setChanged` invoca `MenuTransmutationTable.slotsChanged @5` e depois `SimpleContainer.setChanged @9`. `slotsChanged` pode agendar `setRerollPlayerUUID`. Nos métodos selecionados de `TileEntityTransmutationTable` não apareceu chamada **direta** a `BlockEntity.setChanged` ou `Level.sendBlockUpdated`. Isso **não comprova** perda de dados: são necessários rastreamento de chamadas indiretas, lifecycle do container/chunk e QA de persistência. A operação `postTransmute` altera o mapa por jogador e o contador, mas o efeito real de dirty/sync deve permanecer `NOT_VERIFIED`.

### Candidatos binários, sem fechamento de universo

A busca limitada a strings dos classfiles encontrou seis candidatos: `AlexsMobs`, `BlockTransmutationTable`, `MessageUpdateTransmutablesToDisplay`, seu `$Handler`, `TransmutationData` e `TileEntityTransmutationTable`. A ausência de um classfile desse conjunto **não demonstra inexistência de consumidor**; nomes de método, reflexão ou dependências externas não foram exauridos. O próximo recorte técnico relevante é o bloco `BlockTransmutationTable`, cujo ciclo de abertura/transformação permanece por certificar individualmente.

**Gates mantidos:** `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, sem alteração de numeradores, runtime, Stage ou sibling RPG Skill Tree. A execução CI deste relatório não realizou AMC-T01..T03 nem verificou o modpack completo.
