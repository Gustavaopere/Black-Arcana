# Gazing Pearl — ACWorldData reputação Deep One, descoberta transitiva 1.0.10

**Status:** 🟡 EM AUDITORIA; contrato da Gazing Pearl continua **⚠️ PARCIAL**, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`. Este dossiê de suporte **não cria magia, cast, perk ou nova raiz semântica**, e não modifica o runtime.

## Fonte de autoridade

- Modlist sibling: `Gustavaopere/neoforge-rpg-skilltree/PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`, versão física `alexscaves-1.0.10-neoforge+1.21.1.jar`, mod id `alexscaves`, Minecraft/NeoForge 1.21.1; SHA-1 físico registrado `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- Publisher JAR 1.0.10 previamente observado: 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A igualdade dos bytes da cópia instalada com a cópia publisher **NÃO VERIFICADA**.
- Caller confirmado pelo [relatório local da Gazing Pearl](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md): `GazingPearlItem.acInventoryTick` @44 invoca `ACWorldData.get(level)` e @83 invoca `ACWorldData.getDeepOneReputation(entity.getUUID())`. O snapshot é mantido na stack; não é a autoridade sobre reputação global.

## Descoberta read-only pendente de artefato

A [sonda SHA-exata](../../../../docs/qa/alexscaves_1010_gazing_pearl_worlddata_probe.py) e seu [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-worlddata-discovery.yml) vão enumerar métodos e campos nativos de `com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData`, especialmente produtores/consumidores de reputação Deep One, e sites de invocação JVM de classes referenciadoras. A sonda exige os 1.555 classfiles do publisher, igualdade dos hashes do artefato e presença do caller @83; executa **somente `javap` e leitura ZIP**, não classes do mod.

**Nenhuma conclusão nova sobre setters, persistência, fórmula de reputação, SavedData, client sync ou permissão de perks é autorizada antes do relatório JAR e análise de cada body/caller.** O escopo da sonda limita-se a referências tipadas ao owner exato `ACWorldData` em classfiles no JAR publisher; consumidores por reflexão, mixins dinâmicos, datapacks, comandos, subclasses ou motores externos podem ficar de fora.

## Primeira execução SHA-exata — mapa e fronteiras de reputação

[Run #45009745694](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45009745694), [artifact #14748749822](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45009745694/artifacts/14748749822): `report.json` de **38.119 bytes**, SHA-256 `63bae11dbc53695d47ef70aba4537e98786508761fb654cef01294e53c77e877`. O classfile `ACWorldData` possui SHA-256 `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5`, herda `SavedData` e declara **17 métodos, 6 campos**, incluindo o campo privado `deepOneReputations:java.util.Map`. A primeira sonda expôs seis corpos selecionados. A segunda execução ampliará a prova para `acSave`, `lambda$get$0` e corpos dos consumidores exatos, com report e SHA próprios.

**Leitura nativa observada (não é prova de execução da engine):**

- `ACWorldData.get(Level)`, 27 instruções, Code SHA `bd22587b8dbae8d2faae621a1df5bdbd1e454ce2741779f3f38cac48b5163893`: rejeita níveis que não são `ServerLevel` (retorna `null`), toma `server.getLevel(Level.OVERWORLD)` @8–14, usa `ServerLevel.getDataStorage` @19 e `ACPlatform.computeIfAbsent` com chave `alexscaves_world_data` @41. Quando o resultado é não nulo, invoca `setDirty()` @53 **inclusive quando a chamada externa foi apenas uma leitura**. Isso não demonstra que cada acesso grava imediatamente em disco; `SavedData` e `ACPlatform` requerem contrato próprio.
- `getDeepOneReputation(UUID)`, 13 instruções, Code SHA `3e8885a28a91d8d1a833fe29728852c1836bf7210cabb11d08ae3b434d48936f`: retorna **0** para UUID nulo ou ausente do mapa (via `Map.getOrDefault(uuid,Integer.valueOf(0))` @17), sem criar entrada. Este método não modifica a reputação.
- `setDeepOneReputation(UUID,int)`, 11 instruções, Code SHA `33005bf29cb2f8ad51dfae2bf763852d3b08885aaa9d32964022a2c987a885cf`: aplica `Mth.clamp(value,-100,100)` @10 e `Map.put(uuid,Integer.valueOf(clamped))` @16. O setter **não chama `setDirty()` em seu próprio corpo**; o caller `ACWorldData.get(Level)` já pode tê-lo solicitado, mas outros fluxos não devem ser presumidos.
- `load(CompoundTag)`, 58 instruções, Code SHA `064fbae435ec957a69aa659ff02248ecd37a9c2fd9132f36228d13b73cb666a5`: cria objeto novo, inspeciona a lista `DeepOneReputations` (tipo NBT `10`), e para cada elemento faz `Map.put(ACCompat.getUUID(entry,"UUID"),Integer.valueOf(ACCompat.getInt(entry,"Reputation")))` @64. **Não aplica clamp no carregamento**, diferentemente do setter. Isso permite que valores presentes no NBT fora do intervalo do setter sejam reconstruídos sem normalização nesse método; não afirmar que tal save ocorreu no modpack.
- `save(CompoundTag,HolderLookup.Provider)`, 4 instruções, Code SHA `e28e62cbedd95ba00f0233a962677948eb311aa07d72f0e192a22da817d29c7f`: delega diretamente a `acSave(tag)` @2. O método `acSave` ainda não estava na seleção da primeira sonda; **serialização completa fica pendente da próxima versão do relatório**.

**Censo das três referências tipadas observadas no JAR publisher, sem alegação de universo de eventos/reflexão:** `DeepOneBaseEntity.getReputationOf` invoca getter @28 e `setReputationOf` invoca setter @25; `MineGuardianEntity.dropAllDeathLoot` invoca getter @51 e setter @82; `GazingPearlItem.acInventoryTick` invoca getter @83. Sem analisar os corpos completos dos consumidores, não atribuir condições, dano, recompensa, delta de reputação ou autoridade de PvP.

**Boundary temporal na pérola:** `acInventoryTick` só consulta `ACWorldData.get` quando está no lado servidor e o timestamp guardado é não positivo, ou `getGameTime()-LastReputationTimestamp > 100 ticks`. Se o tempo atual regredir e o timestamp anterior continuar positivo, o delta não supera 100 até alcançar o valor exigido. Se `ACWorldData.get` retornar `null`, o item não substitui nem limpa o snapshot nesse tick. Esta é uma consequência dos saltos JVM @26/@40/@51, não QA física de regressão de relógio ou transferência de dono.

**Estado:** os valores derivados acima são estáticos, reproduzíveis e limitados ao publisher 1.0.10; cópia instalada, `ACPlatform.computeIfAbsent`, `SavedData`, lifecycle, setter via mobs, sincronização e QA física continuam **NOT_VERIFIED/NOT_TESTED**. Nenhum hook per-player seguro autorizado; `NO_MUTATION`.


## Próximos gates

1. Executar CI e preservar report com hash, tamanho, classfile SHA, métodos + offsets, referências tipadas e sites de invoke.
2. Inspecionar o relatório para distinguir getter, mutação de reputação e armazenamento/serialização sem atribuir APIs ou semântica presumidas.
3. Adicionar manifesto/contrato técnico SHA-exato e checker fail-closed de invariantes e casos negativos, se as evidências sustentarem; reexecutar CI final.
4. Auditar canais client/servidor, SavedData e ciclo de vida; QA física e comparação da cópia instalada seguem **NOT_TESTED/NOT_VERIFIED**, sem promoção da ficha para ✅.

O Black Arcana mantém sua autoridade sobre o runtime mágico; RPG Skill Tree é somente sibling/provider de progressão. Sem hook nativo seguro por usuário: **NO_MUTATION / fail-closed**.
