# ACItemRegistry 1.0.10 — contrato estático delimitado de registro e callbacks locais

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
static_contract=CERTIFIED_STATIC_7_AXES
mutating_hook=NOT_VERIFIED
transformed_runtime=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
mutation=NO_MUTATION
provider_universe_closed=false
new_magic_roots=0
```

A [ficha de ACItemRegistry](systems/item-registry.md) individualiza **188 bindings de campos Supplier**, suas factories e hashes, **43 pedidos adicionais de spawn eggs**, configuração de setup e os efeitos locais de sete callbacks de dispenser. O [selo compacto](EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json) e o [auditor causal](../../../../docs/qa/alexscaves_1010_item_registry_contract_audit.py) sustentam esse recorte. São **231 pedidos estáticos de registro**, sem certificar 231 itens aceitos em runtime, 188 comportamentos completos de item ou 43 ciclos de entidade.

## Autoridade e identidade finita

| Campo | Evidência |
|---|---|
| Release | `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge 1645389/8856293 |
| Plataforma | Minecraft 1.21.1, NeoForge, Java 21 |
| Tamanho | 75.279.314 bytes |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| `ACItemRegistry.class` SHA-256 | `114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1` |
| `ACDeferredRegister.class` SHA-256 | `08743e318b3bac302e7602373ff6ca96903f3694ec9fb75457e7cc15ed4305e9` |
| Declarações do registry | 200 campos; 208 métodos com `Code`, incluindo 200 métodos sintéticos |
| Tipos dos campos | 188 Supplier, seis ACArmorMaterial, quatro Rarity, um Map, um ACDeferredRegister |
| Bridge | Três campos privados finais; cinco métodos com `Code` |
| Classes anônimas do registry | Sete; 14 corpos completos selados |
| Censo nativo de referências tipadas | 114 owners originais para registry/bridge; 116 no censo ampliado dos quatro símbolos; 1555 classfiles |
| Roster de classes SHA-256 | `2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed` |
| Contagem editorial | Uma ficha de sistema e um contrato; zero novas raízes mágicas |

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**. Ela permanece adjacente; o contrato é do binário **1.0.10** SHA-exato. Nomes de classes, métodos e campos não substituem a resolução de descritores, constantes, bootstrap handles e fluxo de operandos.

O [registro documental do pack](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/6b8e0bd4ff6cb2832a053b6bd2e0828fb6875f7d/PROJECT-INSTRUCTIONS/modlist/modlist.md#L349), no commit `6b8e0bd4ff6cb2832a053b6bd2e0828fb6875f7d`, ainda lista o JAR 1.0.10 na linha 349 (#019) e NeoForge 21.1.250 na [linha 331 (#001)](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/6b8e0bd4ff6cb2832a053b6bd2e0828fb6875f7d/PROJECT-INSTRUCTIONS/modlist/modlist.md#L331). É proveniência documental física histórica, conferida nesse commit, sem novo dump de instalação ou QA da execução.

## O que é certificado

O inicializador declara estado compartilhado, cria `DEF_REG` com `Registries.ITEM` e o literal `alexscaves`, vincula 188 resultados de `register` a campos Supplier e chama o helper de eggs outras 43 vezes. Para cada binding, o auditor precisa resolver **receptor, namespace, literal do caminho, factory site, bootstrap handle, chamada de registro e escrita no campo**, mantendo seus offsets e identidade/hash da factory. Essa relação é mais forte que procurar um literal perto de um `putstatic` ou presumir que o ID é o nome do campo convertido para minúsculas.

O escopo comportamental inclui os helpers próprios não sintéticos de registro/consulta/setup, a factory delimitada de spawn eggs, os seis callbacks locais de fábrica de projétil que recebem jogador, o bridge e os corpos finitos dos sete callbacks anônimos, além dos pivôs de lifecycle e helpers nativos de ID explicitados no selo. As demais factories dos itens entram por **declaração, identidade completa e hashes de corpo/instruções**, sem certificação integral dos efeitos do item resultante. Construtores externos chamados, seus métodos posteriores, superclasses, engine externo e transformações do pack não herdam a certificação por constarem de um handle ou de uma chamada.

Cada factory é identificada por **owner + name + descriptor + reference kind**, ligada ao seu bootstrap e ao binding que a captura. Hash de `Code` sozinho não prova equivalência: o mesmo bytecode bruto pode resolver índices de constant pool para membros diferentes. O selo conserva o class hash, hashes das instruções resolvidas para todas as factories e instruções completas somente dos corpos finitos selecionados para certificação comportamental. As tabelas alfabéticas da [ficha](systems/item-registry.md) tornam o recorte consultável por campo, literal e handle.

O número 188 descreve campos Supplier, sem fechar o inventário do provider. `spawnEgg` usa o prefixo nativo **`spawn_egg_`**, registra uma factory capturando Supplier de tipo e dois inteiros de cor e guarda o Supplier retornado em `creativeTabSpawnEggMap` junto com a chave de agrupamento. Os 43 pedidos não possuem 43 campos próprios entre os 188. O total de 231 é de **pedidos estáticos neste inicializador**, sem alegar sucesso físico ou exclusividade de todos os caminhos externos.

## Bridge, namespace e lifecycle

`ACDeferredRegister.create(registryKey,namespace)` constrói wrapper novo e `DeferredRegister.create`. `raw()` devolve o delegate. `register(path,factory)` obtém a localização por `ACIdFactories.of(namespace,path)`, monta `ResourceKey.create(registryKey,location)` e captura a chave junto com a factory em Supplier; `delegate.register` recebe o caminho original e esse Supplier. O callback capturador encaminha a `ACRegistryIds.constructing(key,factory)`. As referências não demonstram, por si só, que o objeto já foi construído ou aceito pelo loader.

O caminho selado do bootstrap é `AlexsCaves.<init> @261 DEF_REG → @264 raw() → @268 DeferredRegister.register(eventBus)`. O common setup agenda trabalho que alcança `lambda$commonSetup$0 @12 ACItemRegistry.setup()`. São callsites do publisher, sem execução física do loader, garantia de ordem de listeners externos ou validação de runtime transformado.

`ACIdFactories` tem zero campos e quatro métodos com `Code`: construtor privado e os wrappers `of(String,String)ResourceLocation`, `parse(String)ResourceLocation` e `vanilla(String)ResourceLocation`. `of` encaminha seus dois argumentos, sem conversão local, a `ResourceLocation.fromNamespaceAndPath` (`@0–5`); `parse` solicita `ResourceLocation.parse` (`@0–4`); `vanilla` solicita `ResourceLocation.withDefaultNamespace` (`@0–4`). Não há lowercase, filtro, fallback ou parser próprio nesses wrappers. A validação/normalização da localização pertence ao método externo correspondente. Class SHA-256 `53dd4fc45d0bc2ed33cea2341b2b4efa5b9f04eab9417e1f9be0b1cf86607716`.

`ACRegistryIds` declara `private static final ThreadLocal PENDING` e quatro métodos com `Code`. O inicializador cria `new ThreadLocal()` (`@0–10`). `constructing(key,supplier)` salva o valor anterior (`@0–9`), instala a chave recebida (`@10–14`), chama `Supplier.get` (`@17–23`) e, tanto no retorno normal quanto no handler de exceção, **remove** o ThreadLocal se o valor anterior era nulo ou **restaura** o valor anterior caso contrário; depois retorna o resultado ou relança a exceção (`@24–70`). O selo inclui ramos e exception table, não apenas a ordem de chamadas. Isso permite aninhamento no mesmo thread; não implementa persistência, isolamento por jogador ou troca de thread. `pending()` somente lê e converte o valor atual para `ResourceKey` (`@0–9`). Class SHA-256 `7eded908c4e715b18ed1403eaf662a21427e1bb3362e8f60775578e884368be1`.

O censo dos 1555 classfiles encontra **zero referências tipadas de método a `ACRegistryIds.pending()`**. Assim, instalar o contexto nativo é comprovado; não há prova neste publisher de que um construtor consulte `pending()` para receber um ID de item. Esse zero não exclui reflexão, mixin, transformação ou consumidor externo do pack. A chave capturada não pode ser descrita como ID efetivamente aplicado ao objeto ou como player/owner. `ACRegistryIds` é contexto de construção por thread e não um registry final aceito em runtime.

`getSpawnEggsForTab` devolve uma lista nova dos Suppliers cujas chaves armazenadas satisfazem `equals`, sem resolver os Suppliers. `getSpawnEggFor` resolve Suppliers, filtra `SpawnEggItem`, compara por identidade o `getType(ItemStack.EMPTY)` com o tipo solicitado e devolve o primeiro match; no final, devolve `Items.AIR`. Não há exception handler próprio, fallback de criação de tipo ou prova de que as consultas foram chamadas após resolução dos holders.

## Setup, efeitos locais e limites externos

`setup` solicita cinco bindings de ingrediente de reparo, 21 registros de behaviors de dispenser, uma escrita de `LecternBooks.BookData(8466460,16644332)` pelo ID observado de `CAVE_BOOK` e 17 valores de compostagem. A [ficha](systems/item-registry.md) lista cada binding/offset e valor. O corpo não faz guarda de repetição nem rollback. O [contrato de materiais](systems/armor-material.md), [alimentação](systems/foods.md), [builder](systems/food-builder.md), [atributos dinâmicos](systems/dynamic-attributes.md) e demais sistemas de item preservam suas fronteiras.

As classes `$1..$6` constroem e retornam `SeekingArrowEntity`, `CinderBrickEntity`, `InkBombEntity`, `InkBombEntity` glowing, `GuanoEntity` e `BurrowingArrowEntity`, usando nível e coordenadas da `Position` recebida. `$1/$6` atribuem pickup `ALLOWED`; `$4` solicita `setGlowingBomb(true)` e `setItem(stack)` com a referência recebida. Esses seis corpos não chamam diretamente `addFreshEntity` ou `shrink`, sem provar que a superclasse, o disparo completo ou as entidades não tenham custos ou efeitos.

`$7.execute` obtém nível/posição/estado pelo `ACPlatform`, calcula o bloco em frente pelo `FACING`, constrói `NuclearBombEntity(level,x+0.5D,y,z+0.5D)`, solicita `addFreshEntity` e **ignora o booleano**, solicita som `TNT_PRIMED/BLOCKS` com volume/pitch `1F/1F`, solicita `ENTITY_PLACE` com source nulo, chama **`stack.shrink(1)`** e devolve a mesma stack. Não há branches locais de sidedness, colisão, área protegida, player/owner ou sucesso de spawn. Esse efeito local e essa solicitação de custo são certificados; raio, dano, timer e ciclo completo de detonação permanecem no [escopo nuclear próprio](EXACT-NUCLEAR-CONTRACTS-1.0.10.md) ou pendentes.

Doze métodos sintéticos adicionais aos 188 handles diretos incluem a factory de eggs, cinco Suppliers de água e seis callbacks que recebem `Player`, consultam seu nível e o passam ao construtor de projétil. Os seis corpos locais de projétil também são selados integralmente: usam `new Entity(player.level(),player)`, com descritor de construtor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V`, e retornam o objeto, sem guardas locais, spawn request ou débito próprio. Não se afirma ausência de jogador ou de projéteis na classe inteira; tampouco se presume que esse argumento seja prova de crédito de kill/XP/Mastery ou de owner persistido. A ficha registra as identidades sem promover os corpos externos.

Identidades dos sete callbacks selados, sem certificação dos ciclos completos de entidade:

| Classe anônima | SHA-256 do classfile |
|---|---|
| `ACItemRegistry$1` | `8fcf765148b848978f8d4fae8d1fd8a1c44ecf96f787d80c202ded3c09383b29` |
| `ACItemRegistry$2` | `adc65f3faa898a0fd5098903781de3d979bbc7b3f385d0bc31a94ec1946843c2` |
| `ACItemRegistry$3` | `7cad662acb78e26cbf4dd7766e06aa07c9a70d9de40c83e79af8e2e1863f3cca` |
| `ACItemRegistry$4` | `cfa9851960ce71cdff5a7808c68fb0c6e6dba90edd9df4c97951ab70dad0234d` |
| `ACItemRegistry$5` | `52e59afa55413b17530f60de11bebd7700fad23b72b8b219657ba792ae2ebf47` |
| `ACItemRegistry$6` | `721d302ffe9969fd15510f63035c2d338be5a962a91f88519c0b527efe8b53a6` |
| `ACItemRegistry$7` | `28e78bc3d6c52bdca735bb1e8663b834f4a82d2879ad8a70b63f5c889e7b78f9` |

## Sete eixos e integração

| Eixo | Contrato estático | Limite |
|---|---|---|
| `identity` — Identidade | Artefato, classes, roster, declarações, handles e hashes SHA-exatos | Fonte 1.1.1 adjacente; sem paridade presumida |
| `behavior` — Comportamento/ativação | Bindings causais, bridge, callbacks locais e pivôs nativos de lifecycle | Pedido de registro não equivale a aceitação física |
| `parameters` — Parâmetros | Literais de namespace/caminho, cores, agrupamento, setup, posições e argumentos locais | Sem certificação integral das 188 factories/itens ou entidades |
| `targeting` — Targeting/alcance/área | Pipeline puro de registro sem alvo; callbacks locais recebem posição ou bloco em frente | Dano, raio, LOS, PvP e claims das entidades são externos |
| `costs` — Custos/tempo | Pipeline sem custo mágico/tick; `$7` solicita `shrink(1)` | Demais débitos, duração e detonação não inferidos |
| `integration` — Estado/ownership/perks | Estado JVM compartilhado, Suppliers tardios, callbacks de Player individualizados | Sem mutação per-player ou settlement de progressão homologado |
| `validation` — Validação | Auditor reproduzível, selo compacto, negativos e regressões documentais | Hook/runtime `NOT_VERIFIED`, QA `NOT_TESTED` |

**N/A de dano, área, alcance, duração e custo mágico é restrito ao pipeline de declaração/registro.** A classe contém callbacks com efeitos locais e factories que criam itens/entidades mais complexos. Esta auditoria não os certifica integralmente por associação.

Black Arcana conserva autoridade do runtime mágico; RPG Skill Tree fornece progressão. Mudar namespace, factory, Supplier/holder, mapa de eggs, material ou setup constitui alteração de construção/configuração global; não um perk isolado por jogador. Integrações com Black Arcana, Enshrouded, RPG Skill Tree ou Epic Fight permanecem **`NOT_CERTIFIED`**, sob **`NO_MUTATION`**. Nenhum novo cast, root, crédito de Mastery, hook mutador ou cenário físico é aprovado.

## Reprodução e aceitação

O [workflow dedicado](../../../../.github/workflows/alexscaves-1010-item-registry-contract.yml) usa o artefato exato e executa o [auditor](../../../../docs/qa/alexscaves_1010_item_registry_contract_audit.py), seus [negativos](../../../../docs/qa/alexscaves_1010_item_registry_contract_audit_test.py) e as [regressões documentais](../../../../docs/qa/alexscaves_1010_item_registry_contract_cards_test.py).

```bash
python docs/qa/alexscaves_1010_item_registry_contract_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json' \
  --output /tmp/item-registry-evidence.json
```

Critérios de aceitação: artefato e roster SHA-exatos; duas saídas reproduzíveis idênticas ao selo; correspondência dos 188 bindings e 43 eggs com literais/handles/receiver; preservação de declarações, hashes e semântica dos corpos finitos; rejeição de alterações causais, lifecycle, namespace, bootstrap ou callback; tabelas documentais sem omissões/duplicações; manifesto compacto **inferior a 2 MiB**. Comparação literal com um selo, hash isolado ou contagem de sites não substitui as guardas causais do auditor.

O relatório de descoberta original da #1123 permanece preservado como descoberta: **2.294.703 bytes**, SHA-256 `ac1f8d785501c5c1d2dbe1e22ee9248682af9662c6f6c4dbb972c536f33561e8`; transcript SHA-256 `a1a34eae7ac0daab3c61294efdcb5dcec6103a36846f703583304e076b8e123f`. O contrato e o selo novos não reclassificam retroativamente a descoberta. Evidências e cartões anteriores mantêm seus escopos próprios.

**QA física permanece pendente:** bootstrap/setup real, aceitação/unicidade de IDs, resolução de holders, listas criativas/eggs, comportamento completo de dispenser, aceitação/recusa de entidade e custo de stack, som/game event, reparo, compostagem, livro, reload, servidor/cliente e transformações externas. Sucesso de auditor/CI valida o recorte estático; não representa teste de uma sessão física.

**Contabilidade e continuidade:** uma ficha técnica e um contrato estático, **+0 raízes mágicas**, sem fechar o provider. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`, provider **`OPEN`**. Próximo símbolo sem disposição: **`server/item/ACRepairableItem`**.
