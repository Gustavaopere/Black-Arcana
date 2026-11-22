# Gazing Pearl — ACWorldData reputação Deep One, descoberta transitiva 1.0.10

**Status:** 🟡 EM AUDITORIA; contrato da Gazing Pearl continua **⚠️ PARCIAL**, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`. Este dossiê de suporte **não cria magia, cast, perk ou nova raiz semântica**, e não modifica o runtime.

## Fonte de autoridade

- Modlist sibling: `Gustavaopere/neoforge-rpg-skilltree/PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`, versão física `alexscaves-1.0.10-neoforge+1.21.1.jar`, mod id `alexscaves`, Minecraft/NeoForge 1.21.1; SHA-1 físico registrado `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- Publisher JAR 1.0.10 previamente observado: 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A igualdade dos bytes da cópia instalada com a cópia publisher **NÃO VERIFICADA**.
- Caller confirmado pelo [relatório local da Gazing Pearl](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md): `GazingPearlItem.acInventoryTick` @44 invoca `ACWorldData.get(level)` e @83 invoca `ACWorldData.getDeepOneReputation(entity.getUUID())`. O snapshot é mantido na stack; não é a autoridade sobre reputação global.

## Descoberta read-only e limites do recorte

A [sonda SHA-exata](../../../../docs/qa/alexscaves_1010_gazing_pearl_worlddata_probe.py) e seu [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-worlddata-discovery.yml) enumeram métodos e campos nativos de `com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData`, especialmente produtores/consumidores de reputação Deep One, e sites de invocação JVM de classes referenciadoras. A sonda exige os 1.555 classfiles do publisher, igualdade dos hashes do artefato e presença do caller @83; executa **somente `javap` e leitura ZIP**, não classes do mod.

**Nenhuma conclusão nova sobre setters, persistência, fórmula de reputação, SavedData, client sync ou permissão de perks é autorizada antes do relatório JAR e análise de cada body/caller.** O escopo da sonda limita-se a referências tipadas ao owner exato `ACWorldData` em classfiles no JAR publisher; consumidores por reflexão, mixins dinâmicos, datapacks, comandos, subclasses ou motores externos podem ficar de fora.

## Primeira execução SHA-exata — mapa e fronteiras de reputação

[Run #45009745694](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45009745694), [artifact #14748749822](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45009745694/artifacts/14748749822): `report.json` de **38.119 bytes**, SHA-256 `63bae11dbc53695d47ef70aba4537e98786508761fb654cef01294e53c77e877`. O classfile `ACWorldData` possui SHA-256 `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5`, herda `SavedData` e declara **17 métodos, 6 campos**, incluindo o campo privado `deepOneReputations:java.util.Map`. A primeira sonda expôs seis corpos selecionados. A segunda execução efetivamente ampliou a prova para `acSave`, `lambda$get$0` e os quatro corpos consumidores exatos; ver seção subsequente.

**Leitura nativa observada (não é prova de execução da engine):**

- `ACWorldData.get(Level)`, 27 instruções, Code SHA `bd22587b8dbae8d2faae621a1df5bdbd1e454ce2741779f3f38cac48b5163893`: rejeita níveis que não são `ServerLevel` (retorna `null`), toma `server.getLevel(Level.OVERWORLD)` @8–14, usa `ServerLevel.getDataStorage` @19 e `ACPlatform.computeIfAbsent` com chave `alexscaves_world_data` @41. Quando o resultado é não nulo, invoca `setDirty()` @53 **inclusive quando a chamada externa foi apenas uma leitura**. Isso não demonstra que cada acesso grava imediatamente em disco; `SavedData` e `ACPlatform` requerem contrato próprio.
- `getDeepOneReputation(UUID)`, 13 instruções, Code SHA `3e8885a28a91d8d1a833fe29728852c1836bf7210cabb11d08ae3b434d48936f`: retorna **0** para UUID nulo ou ausente do mapa (via `Map.getOrDefault(uuid,Integer.valueOf(0))` @17), sem criar entrada. Este método não modifica a reputação.
- `setDeepOneReputation(UUID,int)`, 11 instruções, Code SHA `33005bf29cb2f8ad51dfae2bf763852d3b08885aaa9d32964022a2c987a885cf`: aplica `Mth.clamp(value,-100,100)` @10 e `Map.put(uuid,Integer.valueOf(clamped))` @16. O setter **não chama `setDirty()` em seu próprio corpo**; o caller `ACWorldData.get(Level)` já pode tê-lo solicitado, mas outros fluxos não devem ser presumidos.
- `load(CompoundTag)`, 58 instruções, Code SHA `064fbae435ec957a69aa659ff02248ecd37a9c2fd9132f36228d13b73cb666a5`: cria objeto novo, inspeciona a lista `DeepOneReputations` (tipo NBT `10`), e para cada elemento faz `Map.put(ACCompat.getUUID(entry,"UUID"),Integer.valueOf(ACCompat.getInt(entry,"Reputation")))` @64. **Não aplica clamp no carregamento**, diferentemente do setter. Isso permite que valores presentes no NBT fora do intervalo do setter sejam reconstruídos sem normalização nesse método; não afirmar que tal save ocorreu no modpack.
- `save(CompoundTag,HolderLookup.Provider)`, 4 instruções, Code SHA `e28e62cbedd95ba00f0233a962677948eb311aa07d72f0e192a22da817d29c7f`: delega diretamente a `acSave(tag)` @2. O método `acSave` ainda não estava na seleção da primeira sonda; **serialização completa fica pendente da próxima versão do relatório**.

**Censo das três referências tipadas observadas no JAR publisher, sem alegação de universo de eventos/reflexão:** `DeepOneBaseEntity.getReputationOf` invoca getter @28 e `setReputationOf` invoca setter @25; `MineGuardianEntity.dropAllDeathLoot` invoca getter @51 e setter @82; `GazingPearlItem.acInventoryTick` invoca getter @83. Sem analisar os corpos completos dos consumidores, não atribuir condições, dano, recompensa, delta de reputação ou autoridade de PvP.

**Boundary temporal na pérola:** `acInventoryTick` só consulta `ACWorldData.get` quando está no lado servidor e o timestamp guardado é não positivo, ou `getGameTime()-LastReputationTimestamp > 100 ticks`. Se o tempo atual regredir e o timestamp anterior continuar positivo, o delta não supera 100 até alcançar o valor exigido. Se `ACWorldData.get` retornar `null`, o item não substitui nem limpa o snapshot nesse tick. Esta é uma consequência dos saltos JVM @26/@40/@51, não QA física de regressão de relógio ou transferência de dono.

**Estado:** os valores derivados acima são estáticos, reproduzíveis e limitados ao publisher 1.0.10; cópia instalada, `ACPlatform.computeIfAbsent`, `SavedData`, lifecycle, setter via mobs, sincronização e QA física continuam **NOT_VERIFIED/NOT_TESTED**. Nenhum hook per-player seguro autorizado; `NO_MUTATION`.


## Segunda execução — serialização, delta de reputação e consumidores nativos

**Evidência do publisher SHA-exato:** [CI #45009967780](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45009967780), [artifact #14749775926](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45009967780/artifacts/14749775926). `report.json` com **77.203 bytes**, SHA-256 `2816bb57380330b09075b3c9877d21fe0dd7751c2a8013e43d3507e8cdc46118`. O classfile mantém SHA-256 `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5`. O relatório varre **1.555 classes** e audita oito métodos do owner e quatro corpos de consumidores com **cinco invocações** ao getter/setter reputacional. Ver [manifesto de métodos e callsites](EXACT-GAZING-PEARL-WORLDDATA-1.0.10.json) e [checker de invariantes](../../../../docs/qa/alexscaves_1010_gazing_pearl_worlddata_checks.py). O check final da HEAD necessita sua própria execução GitHub Actions.

### Ciclo de serialização e persistência declarada

- `acSave(CompoundTag)`: 68 instruções, Code SHA `fc86c0bf51203469f869f5144f9b3b690b6c0cd6bb5d97258fb24e821a62d587`, instruction SHA `2eedabc2fd6993477a16ac8a56c723d956497a776928618fd967040b6e150c8b`. **Somente quando `deepOneReputations` não está vazio** (`Map.isEmpty @4`, salto `ifne @9 ->119`), cria `ListTag`; percorre `Map.entrySet()` (@24), escreve `UUID` via `ACCompat.putUUID` (@78) e `Reputation` inteiro via `CompoundTag.putInt` (@98), adiciona cada CompoundTag ao ListTag (@104), grava `DeepOneReputations` na tag resultante (@115). O método também grava flags/tempo do boss e IDs rastreados, não apenas reputação. A ordem da iteração do mapa **não é garantida** pelo recorte. Quando o mapa está vazio, esse método não acrescenta `DeepOneReputations` à tag recebida.
- `save(CompoundTag,HolderLookup.Provider)`: delega `acSave(tag)` @2; `lambda$get$0(ACWorldData)` cria `new CompoundTag` @1 e chama `acSave` @8, suportando uma das funções do `ACPlatform.computeIfAbsent`. O provedor de armazenamento externo, gravação real em disco, erros de I/O, reinício, sincronização, migração e compatibilidade com outros mutadores **não foram inspecionados**.
- `load(CompoundTag)`: para cada entrada de `DeepOneReputations`, insere o valor integer lido sem clamp, mesmo que fora de −100..100. `setDeepOneReputation(UUID,int)` **aplica clamp apenas nas gravações via setter**. Daí **não há invariante global demonstrada de valores de reputação em intervalo no NBT restaurado**. Não é prova de adulteração efetivamente ocorrida.

### Consumidores: guards, dono, efeitos solicitados

| Owner e método | Condições comprovadas no bytecode 1.0.10 | Efeito solicitado |
|---|---|---|
| `DeepOneBaseEntity.getReputationOf(UUID)` — 18 instruções | `Level.isClientSide` @4, retorna 0 no cliente @32; no servidor `ACWorldData.get` @14 e null guard @19 | Getter da reputação de UUID @28, 0 quando dados ausentes |
| `DeepOneBaseEntity.setReputationOf(UUID,int)` — 15 instruções | `isClientSide` @4, aborta no cliente @7; `ACWorldData.get` @14, testa null @19 | Setter delegado @25, com clamp no storage |
| `MineGuardianEntity.dropAllDeathLoot(ServerLevel,DamageSource)` — 41 instruções | Chama o super loot @3; guarda lado servidor @13, `DamageSource.getEntity instanceof Player` @22–27; lê `Player.getUUID` @48, reputação @51 e somente prossegue quando `R < 0` (`ifge @58 ->85`) | `setDeepOneReputation(UUID, R + RandomSource.nextInt(3) + 1)` @82; incremento discreto **+1, +2 ou +3** antes do clamp |
| `GazingPearlItem.acInventoryTick(...)` — 46 instruções | Lado servidor @4; tempo anterior não positivo ou `deltaTime>100` @26/@40; `ACWorldData.get` @44 e null guard @51 | Apenas snapshot de `getDeepOneReputation(entity.getUUID())` @83 para dados na **ItemStack**; nenhuma chamada à rotina de setter |

Os dois métodos da `DeepOneBaseEntity` contêm guardas client/server explícitas, mas isso **não transforma automaticamente seus métodos públicos em API segura para perks**. Na rotina de morte do Mine Guardian, a pré-condição é o agressor de `DamageSource.getEntity` ser `Player` e reputação corrente negativa; não inferir que `DamageSource.getDirectEntity` seja considerado, nem que o resultado já foi persistido ou sincronizado. O valor `nextInt(3)` é limitado no código por argumento 3, mas a distribuição efetiva/seed não foi verificada.

### Limites de certificação e QA

O contrato staticamente rastreado agora cobre o armazenamento local `Map<UUID,Integer>`, o getter default 0, o clamp do setter [−100,100], o roundtrip NBT de reputação (com a ressalva de load sem clamp), os três consumidores tipados, cinco callsites e guards de cada método relevante. Isto **não é a certificação individual da Gazing Pearl**: `BootstrapMethods`/`SavedData` da engine (o corpo local de `ACPlatform.computeIfAbsent` já foi observado), outros eventos/consumidores por reflexão, comportamento da IA, recompensas efetivas, authoritative session, tempo/cópia da stack, envio client/server, datapacks, custo/targeting de outras habilidades e QA física permanecem pendentes. Sem inventar um hook mutador.


## Terceira etapa — ponte ACPlatform para SavedData

A [auditoria SHA-exata da ponte](EXACT-GAZING-PEARL-ACPLATFORM-1.0.10.md) fecha apenas o **método local** `ACPlatform.computeIfAbsent` do publisher 1.0.10 e o corpo de sua função sintética, com dois callers tipados (`ACWorldData.get` e `CitadelServerData.get`). O wrapper cria `SavedData.Factory` usando o `Supplier` e a primeira `Function`, deixa a segunda `Function` sem acesso direto, fornece `DataFixTypes=null` e delega à `DimensionDataStorage.computeIfAbsent`. O lambda adaptador executa `Function.apply(CompoundTag)` e não utiliza `HolderLookup.Provider`. Há um [manifesto de 2 métodos e 2 callers](EXACT-GAZING-PEARL-ACPLATFORM-1.0.10.json), com hashes/offsets e checker fail-closed para o JAR identificado.

A [documentação oficial NeoForge 1.21–1.21.1](https://docs.neoforged.net/docs/1.21.1/datastorage/saveddata/) confirma o papel de `computeIfAbsent`, do `SavedData.Factory`, do nome de arquivo `.dat` e de `setDirty`, sem demonstrar o comportamento físico no servidor do modpack. A ponte é uma dependência transitiva da Gazing Pearl, **não** um hook mutador por jogador. Persistem a pendência de `BootstrapMethods`, engine exata, cache/salvamento/reload, sincronização de stack, bytes da instalação e QA. **NO_MUTATION; Gazing Pearl permanece ⚠️ PARCIAL**.

## Próximos gates

1. Executar o checker SHA-exato com casos negativos e CI integral na HEAD final; verificar preservação de hash e estados fail-closed.
2. Manter separados os contratos estáticos já observados de getter/setter/serialização e as semânticas externas de `ACPlatform`/`SavedData`, que ainda exigem auditoria.
3. Verificar a semântica do dispatcher, consumidores indiretos, config efetiva e autoridade de qualquer integração antes de permitir perks.
4. Auditar canais client/servidor, SavedData e ciclo de vida; QA física e comparação da cópia instalada seguem **NOT_TESTED/NOT_VERIFIED**, sem promoção da ficha para ✅.

O Black Arcana mantém sua autoridade sobre o runtime mágico; RPG Skill Tree é somente sibling/provider de progressão. Sem hook nativo seguro por usuário: **NO_MUTATION / fail-closed**.
