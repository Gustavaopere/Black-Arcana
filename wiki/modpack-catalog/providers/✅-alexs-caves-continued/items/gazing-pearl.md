# Gazing Pearl — indicador passivo de reputação dos Deep Ones (1.0.10)

**Estado: ⚠️ PARCIAL.** Identificação e recorte causal SHA-exatos do publisher, sem certificação técnica individual integral. NO_MUTATION; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; perks_executable=NOT_CERTIFIED; universo integral OPEN. Não é um novo spell/cast nem concede uma nova raiz mágica.

## Identidade, descrição e proveniência

**Provider:** Alex's Caves Continued, mod ID alexscaves, Minecraft 1.21.1/NeoForge/Java 21; runtime 1.0.10. **Item:** alexscaves:gazing_pearl / ACItemRegistry.GAZING_PEARL, classfile com/github/alexmodguy/alexscaves/server/item/GazingPearlItem. **JAR publisher observado:** alexscaves-1.0.10-neoforge+1.21.1.jar, 75.279.314 bytes, SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c. Novo dump do artefato instalado não foi comparado. **SHA-256 da classe:** 2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07; cinco corpos, zero campos próprios e três owners consumidores tipados (ClientProxy, ACItemRegistry e própria classe).

**Descrição funcional:** item de informação que armazena temporariamente na stack um retrato da reputação Deep One do UUID da entidade portadora, apresentando-o por tooltip e cor HSB animada. A classe da pérola não altera a reputação armazenada no mundo. A árvore pública de outra revisão (1.1.1) foi apenas referência de descoberta; os hashes acima são do publisher 1.0.10.

## Ativação, condições, tempo e estado

**acInventoryTick(ItemStack,Level,Entity,boolean)**, 46 instruções: exige servidor (Level.isClientSide @1–4); lê LastReputationTimestamp (long). Se timestamp <=0 ou se gameTime−timestamp **>100 ticks** (comparação estrita), consulta ACWorldData.get(level). Se retornar dados não nulos, solicita putLong(LastReputationTimestamp,gameTime), putBoolean(HasReputation,true), putInt(Reputation,ACWorldData.getDeepOneReputation(entity.getUUID())) e ACCompat.setTag(stack,tag). Sem dados de mundo, a rotina não escreve esse snapshot nesta janela. O dispatcher ACTickingItem é documentado separadamente em [ticking-item](../systems/ticking-item.md). Não há guarda própria Player, held ou selected no corpo da Gazing Pearl; a entidade recebida pelo callback fornece o UUID.

**appendHoverText**, 38 instruções: lê HasReputation e Reputation da stack, chama DeepOneReaction.fromReputation, seleciona chave de tradução pela categoria em minúsculas Locale.ROOT, solicita Component.translatable cinza/itálico e delega ao ancestral. Sem flag verdadeira, o texto específico não é adicionado. Valor traduzido final e frequência de atualização visual no cliente dependem da engine/instalação.

**getPearlColor(ItemStack):int**, **73 instruções**: fórmula HSB do publisher agora auditada estaticamente e reproduzida pelo [checker SHA-exato](../../../../../docs/qa/alexscaves_1010_gazing_pearl_color_checks.py), sem certificar apresentação física. Com tag e `HasReputation=true`, lê `Reputation=R` e calcula a **matiz `H=float(100-R)/200.0F`**, com subtração inteira antes da conversão, `S=0.7F+0.3F * ((float)(1+sin((double)((float)t/4000.0F)))*0.5F)` e brilho `B=1.0F`; chama `java.awt.Color.HSBtoRGB(H,S,B)` @63. Sem a flag, usa `H=float(t1%10000L)/10000.0F` e a mesma fórmula de saturação com uma **segunda leitura independente** de `currentTimeMillis()` (`t2`); `HSBtoRGB` @110. Não há clamp explícito de H/S no método, nem limite baseado em Mastery. A conversão JVM `l2f` ocorre antes de dividir milissegundos por 4000: em 22/11/2026, a distância entre valores `float32` adjacentes da época Unix é **131.072 ms** (conferência numérica Java 21), podendo produzir mudanças visuais em degraus. **Resultado de renderização e sincronismo entre clientes NOT_TESTED**. Ver [dossiê](../EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md).

**Construtor** (10 instruções) solicita stacksTo(1) e Rarity.UNCOMMON. **shouldCauseReequipAnimation** (16) retorna false quando ambas as stacks são Gazing Pearl; eventuais effects externos do render/engine permanecem não verificados. Duração de status, cooldown, mana, dano, projétil, alcance e AOE próprios: **N/A nos cinco métodos locais**; não confundir com contratos dos Deep Ones.

## Reação nativa, targeting e consumidores

**DeepOneReaction** classfile SHA-256 5898cd4286885ad85e92065f68bff883131e921af295b781b806e076ff1e54dc: nove métodos, sete campos e sete consumidores. O fromReputation(int) usa os limiares JVM −10, 10 e 30:

| Reputação inteira | Resultado |
|---|---|
| até −10 | AGGRESSIVE |
| −9 a 10 | STALKING |
| 11 a 30 | NEUTRAL |
| 31 ou mais | HELPFUL |

A classificação é o dado que o tooltip consulta. Os métodos de IA validPlayer/getMinDistance/getMaxDistance e consumidores DeepOneReactToPlayerGoal, DeepOneTargetHostilePlayersGoal e DeepOneBaseEntity pertencem a **outro** contrato de reação dos mobs. Distância/hostilidade nativas não são buffs da pérola nem autorização para perk de manipulação de IA.

**Target:** UUID da entidade portadora recebido pelo callback; não há seleção de entidade por mira, hitbox, área ou cálculo de alcance no item. **Owner:** a stack armazena snapshot Reputation/HasReputation e timestamp; não persiste um owner UUID próprio no recorte. **Persistência:** ACCompat acessa tag da stack; reload, desconexão, passagem entre dimensões, relógio recuado, datapacks, multiusuário e sincronização de ItemStack estão **NOT_TESTED**. A consulta é temporalmente defasável durante o intervalo de >100 ticks.

## Custos, recursos e fronteiras de perk

O publisher inclui receita shapeless **1 Gazing Pearl + 1 Marine Snow → 1 Pearl** em data/alexscaves/recipe/pearl_from_gazing_pearl.json, SHA-256 663ecb4f1b80e92a251e541e6a9b2c312efecccfd322f959d81ecc2e8b4e14d2 (282 bytes). A receita **consome a Gazing Pearl como ingrediente**, não demonstra sua aquisição inicial nem crafting efetivo no pack. Modelo de item em assets/alexscaves/models/item/gazing_pearl.json, SHA-256 a1fd223aa8c09ce52ff113c20cbeb6efec3f1b027297254f28c9303c43930d03. Nenhum gasto de mana, cooldown, desgaste por tick ou consumo por consulta é solicitado nos corpos do item.

**Perks de reputação:** ACWorldData.getDeepOneReputation(UUID) é fonte do snapshot; não há setter mutador autorizado nesta ficha. Alterar o NBT da pérola não altera reputação real. **Perks de cadência:** não duplicar dispatcher ACTickingItem nem escrever timestamp para simular progresso. **Atributos, alvo e Mastery:** nenhum evento de dano/cast/kills da pérola; não premiar XP por leitura ou cor. Black Arcana mantém autoridade do runtime mágico e world safety, e RPG Skill Tree integra progressão/Mastery somente por boundary real. Sem hook confirmado: **NO_MUTATION/fail-closed**.


## Fronteira nativa de reputação — ACWorldData (recorte SHA-exato)

O [dossiê de armazenamento e consumidores](../EXACT-GAZING-PEARL-WORLDDATA-1.0.10.md) e o [manifesto SHA-exato](../EXACT-GAZING-PEARL-WORLDDATA-1.0.10.json) documentam agora o percurso comprovado do publisher 1.0.10: `ACWorldData.get(Level)` usa o armazenamento do Overworld quando invocado de `ServerLevel`, chama `ACPlatform.computeIfAbsent` com chave `alexscaves_world_data` e solicita `setDirty()` para instância não nula. `getDeepOneReputation(UUID)` devolve 0 para UUID nulo/ausente. `setDeepOneReputation(UUID,int)` aplica clamp de **−100 a 100**, depois `Map.put`. O setter não chama `setDirty` por si, enquanto `get` pode marcá-lo. Não inferir gravação física/transferência ao cliente apenas pelo flag.

A persistência **declarada** usa `DeepOneReputations` como lista de CompoundTags `{UUID, Reputation}`, serializada por `acSave` e reconstruída por `load`. O load insere valores diretamente **sem clamp**, então um inteiro lido pode sair do intervalo do setter. A pérola **não possui chamada de setter**: sua rotina inventaria o getter para criar/atualizar um snapshot dentro da `ItemStack`.

**Consumidores tipados do storage reputacional no JAR:** `DeepOneBaseEntity.getReputationOf` e `setReputationOf` (ambos com guarda server-side), `MineGuardianEntity.dropAllDeathLoot` e `GazingPearlItem.acInventoryTick`. O Mine Guardian, se morto por fonte atribuída a um `Player` e com reputação anterior `R<0`, solicita `R+1+nextInt(3)` ao setter, isto é incremento de **1 a 3**. Isso é efeito sobre a **reputação autoritativa do mundo solicitado pelo mob**; a pérola apenas lê mais tarde o valor no próximo refresh, e o resultado físico da morte/loot/salvamento **NOT_TESTED**.

A guarda de atualização da pérola depende de `gameTime−LastReputationTimestamp>100` se o timestamp é positivo. Se o tempo retroceder, o refresh pode ficar suspenso; se os dados globais vierem nulos, o snapshot anterior não é limpo neste caminho. Não transformar essa mecânica de UI/inventário em cast, XP ou perk de reputação. Sem hook comprovado: `NO_MUTATION`.

## Ponte de persistência ACPlatform / SavedData — evidência adicional

O [dossiê SHA-exato da ponte ACPlatform](../EXACT-GAZING-PEARL-ACPLATFORM-1.0.10.md), [manifesto de offsets e consumidores](../EXACT-GAZING-PEARL-ACPLATFORM-1.0.10.json) e [checker fail-closed](../../../../../docs/qa/alexscaves_1010_gazing_pearl_acplatform_checks.py) ampliam a fronteira `GazingPearlItem.acInventoryTick → ACWorldData.get(Level) → ACPlatform.computeIfAbsent → DimensionDataStorage.computeIfAbsent`. **É infraestrutura compartilhada**, não nova magia/efeito de combate.

No JAR publisher `1.0.10`, o wrapper estático possui **11 instruções**: constrói `SavedData.Factory(Supplier,BiFunction,DataFixTypes)`, fornece `null` para `DataFixTypes`, encaminha o nome de armazenamento e chama `DimensionDataStorage.computeIfAbsent`. A assinatura recebe duas `Function`, mas seu corpo utiliza somente a **primeira** (local 1); o parâmetro na posição local 2 não é consumido. A função sintética `lambda$computeIfAbsent$1` possui **5 instruções**, chama `Function.apply(CompoundTag)`, ignora o `HolderLookup.Provider` local 2 e retorna `SavedData` após cast. A vinculação concreta por `BootstrapMethods` ainda necessita investigação.

A inspeção completa dos 1.555 classfiles do publisher revelou **dois consumidores diretos** desse descriptor: `ACWorldData.get` (chave `alexscaves_world_data`, offset @41) e `CitadelServerData.get` (chave própria `alexscaves_citadel_world_data`, @31). Este último **não** concede propriedades de reputação à Gazing Pearl. `ACWorldData.get` solicita `setDirty` com instância não nula; de acordo com a [documentação oficial NeoForge 1.21.1](https://docs.neoforged.net/docs/1.21.1/datastorage/saveddata/), isto sinaliza salvamento necessário, **não** comprova gravação imediata, carregamento após reinício ou sync com cliente.

**Limites inalterados:** nenhum teste físico no modpack, dump da cópia instalada, comprovação dos internals exatos de `DimensionDataStorage`, efeito de cache, persistência real, Player-only gates, alteração autorizada de reputação ou hook mutador. `NO_MUTATION`, `static_contract=NOT_CERTIFIED`, `physical_qa=NOT_TESTED`. A ficha segue **⚠️ parcial**, sem alterar contadores.

## Bootstrap de carregamento — ligação invokeddynamic

[Manifesto JVM da ponte](../EXACT-GAZING-PEARL-ACPLATFORM-BOOTSTRAP-1.0.10.json) e [dossiê](../EXACT-GAZING-PEARL-ACPLATFORM-BOOTSTRAP-1.0.10.md) demonstram que o `invokedynamic` de `ACPlatform.computeIfAbsent` @7 (constant pool #136) usa `BootstrapMethods[0]`, `LambdaMetafactory.metafactory` e `REF_invokeStatic ACPlatform.lambda$computeIfAbsent$1`. A assinatura adaptada é `(CompoundTag,HolderLookup.Provider):SavedData`, mas o corpo de cinco instruções apenas chama `Function.apply(CompoundTag)` e não consome o Provider. A segunda `Function` do wrapper também não é carregada. Isso fecha o vínculo local de classfile, **não comprova execução da engine, persistência após reload, sync da pérola ou hook de progressão**; `NO_MUTATION` e ⚠️ parcial permanecem.

## Engine exata distribuída — NeoForge 21.1.248 / SavedData

O [dossiê de bytecode da distribuição oficial](../EXACT-NEOFORGE-211248-GAZING-PEARL-SAVEDDATA-ABI.md) e seu [manifesto SHA-exato](../EXACT-NEOFORGE-211248-GAZING-PEARL-SAVEDDATA-ABI.json) cobrem as classes `DimensionDataStorage`, `SavedData` e `SavedData.Factory` da distribuição `--installServer` **21.1.248**, todas provenientes do overlay NeoForge. São **15 métodos com corpo JVM** mais a declaração abstrata `SavedData.save(CompoundTag,Provider)`. O hash da distribuição do servidor é `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`; o relatório auditado é SHA-256 `8a16f6041ad4f917295d8d757a531f449c307bcde6cc31d6f5af4da925b847ac`.

O `get(Factory,name)` da engine consulta cache, só tenta arquivo em cache miss real e admite resultado nulo; `computeIfAbsent` cria e armazena objeto via `Supplier.get` quando `get` retorna nulo. `readSavedData` tem handler de Exception que registra falha e retorna nulo, então um save ilegível **pode levar à criação de um estado novo em memória**; isso não é prova de corrupção ou sobrescrita física. No carregamento `readTagFromDisk`, `DataFixTypes=null` desvia de `DataFixTypes.update` (@108→139).

O `SavedData.save(File,Provider)` só solicita serialização se `dirty=true`, chama `IOUtilities.withIOWorker` @54 e depois `setDirty(false)` @59. A implementação desse worker, conclusão/durabilidade de escrita, sync de `ItemStack`, rollback e persistência pós-reinício **ainda não foram demonstrados**. O arquivo é da distribuição do servidor, não prova de classe carregada via ModLauncher ou de paridade com o modpack físico. Nada nessa cadeia autoriza mutação de reputação por perks: **`NO_MUTATION` / ⚠️ parcial**.

## Evidências, hashes e gates

[Dossiê causal](../EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md), [manifesto SHA-exato de 14 métodos](../EXACT-GAZING-PEARL-DISCOVERY-1.0.10.json), [sonda read-only](../../../../../docs/qa/alexscaves_1010_gazing_pearl_discovery.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-gazing-pearl-discovery.yml). Run [44936198921](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921), job 136943226304 PASS, report SHA-256 d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5; artefato 14719307762, ZIP SHA-256 99adb9c94f95711e5cac1a80c8156a5476e467ddf5761e222ef2ec5a8592ce02, expiração declarada 05/12/2026.

**Pendente para ✅:** os [BootstrapMethods do adaptador ACPlatform foram mapeados no publisher](../EXACT-GAZING-PEARL-ACPLATFORM-BOOTSTRAP-1.0.10.md), e [o recorte estático da engine distribuída NeoForge 21.1.248](../EXACT-NEOFORGE-211248-GAZING-PEARL-SAVEDDATA-ABI.md) foi extraído; faltam o contrato de `IOUtilities.withIOWorker`, a classe efetivamente carregada, o arquivo persistido e demais consumidores/reação da IA, recursos/traduções e `ItemStack` herdado; checar renderização e efeitos aceitos; bytes da instalação, QA física e hooks. O método local `ACPlatform.computeIfAbsent` foi auditado estaticamente no publisher, sem certificação integral. A sonda de hash não certifica resultados no mundo. Clean-room: não foram copiados bytecode/assets/implementações de terceiros ao runtime.
