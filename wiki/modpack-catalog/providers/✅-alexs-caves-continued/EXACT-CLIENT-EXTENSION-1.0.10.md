# ACClientExtensionItem 1.0.10 — ABI declarada, callbacks e fronteira de registro

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
static_technical_contract=CERTIFIED_STATIC_7_AXES
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
registration_execution=NOT_VERIFIED
mutation=NO_MUTATION
provider_universe_closed=false
```

A [ficha de extensões de cliente](systems/client-extension.md) documenta a interface, os 19 implementadores diretos encontrados e os corpos de inicialização que encaminham propriedades obtidas dos proxies ao consumer. O [manifesto SHA-exato](EXACT-CLIENT-EXTENSION-1.0.10.json) acrescenta as saídas delimitadas dessas propriedades. A conclusão é do **contrato estático declarado**, sem certificação de registro efetivamente executado, rendering integral ou hook de gameplay.

## Artefato e universo desta prova

| Campo | Valor |
|---|---|
| Release | `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto 1645389 / arquivo 8856293 |
| Plataforma | Minecraft 1.21.1, NeoForge, Java 21 |
| Tamanho | 75.279.314 bytes |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Interface | `com/github/alexmodguy/alexscaves/server/item/ACClientExtensionItem` |
| Interface SHA-256 | `d3139782c378b7b8eee0b580c912f36095675e31db98310475fbe1b60f5a0362` |
| Método abstrato | `initializeClient(java.util.function.Consumer<IClientItemExtensions>)` |
| Descritor JVM | `(Ljava/util/function/Consumer;)V` |
| Censo de classes | 1.555 entradas `.class`, com referências tipadas e declarações separadas |
| Referências tipadas à interface | 20 owners: a própria interface e 19 implementadores diretos |
| Implementadores diretos / callbacks próprios | 18 owners nativos e `citadel/item/ItemCustomRender` no namespace realocado do artefato |
| Implementadores por herança | `ExtinctionSpearItem`, `FrostmintSpearItem` e `LimestoneSpearItem`, via `SpearItem`, sem callback próprio adicional |
| Classes concretas atribuíveis no grafo do JAR | 22: 19 diretas + 3 herdadas; não são 22 corpos próprios de inicialização |
| Chamadas de método `initializeClient` | Zero `Methodref`/`InterfaceMethodref` com esse nome, para qualquer owner/descritor no JAR |
| Corpos completos delimitados | 19 callbacks + 17 métodos de saída: 36 corpos, 304 instruções JVM |
| Selo JSON | 160.802 bytes; SHA-256 `c0527bbcfc2e178ab53c9b00b0e81b2aae56fc12221e814dd1b95af65f79730c` |

A assinatura genérica descreve o objeto aceito pelo `Consumer`; o descritor JVM sofre erasure e não codifica sozinho o tipo genérico. Declaração abstrata não possui corpo executável. O artefato realoca código Citadel para seu próprio namespace: isso não cria um segundo provider, magia ou certificado.

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é apenas adjacente. As alegações desta prova derivam do binário publisher **1.0.10**, não de equivalência presumida com aquele source ou com APIs de outra versão do Minecraft/NeoForge.

## Declarações, consumidores e resultado da busca

O auditor separa três conjuntos: referências tipadas à interface, declarações com nome `initializeClient` e referências de chamada a esse nome. O conjunto das declarações contém **23 métodos**: a interface alvo, seus 19 implementadores e a interface paralela de fluidos com os implementadores Acid e Purple Soda. Os três últimos pertencem a outra família; sua presença no censo global não os certifica como callbacks de item nem acrescenta fichas.

O grafo de superclasses acrescenta três implementadores herdados que não possuem referência tipada própria à interface nem declaram outro `initializeClient`: as três spears herdam o callback de `SpearItem`. Por isso, referências de constant pool, classes atribuíveis e corpos próprios têm contagens diferentes. Não se usam os 20 owners tipados como denominador de todos os consumidores por herança.

O conjunto de chamadas tipadas é vazio. O registro de model properties por `ItemProperties.register` em `ClientProxy.clientInit` é outra API: não é uma chamada da interface nem prova de registro de `IClientItemExtensions`. A própria existência de callbacks e de `Consumer.accept` dentro deles não demonstra quem invocaria `initializeClient`. O censo não encontra um dispatcher tipado da interface, um callsite com owner externo `Item` ou outro owner, ou um evento de registro invocando esse nome no JAR. Por isso, **`registration_execution=NOT_VERIFIED`** é uma fronteira conservada no selo, na ficha e no certificado.

Esse resultado não prova que os callbacks sejam universalmente inúteis, que o mod esteja quebrado ou que sua apresentação nunca funcione. Reflexão, transformação de classes, código externo, comportamento da engine e outros caminhos independentes de registro podem existir fora da relação tipada comprovada. Nenhum deles é presumido para preencher uma lacuna. Gate de Dist, entrega de evento, ordem de registro, deduplicação e disponibilidade física de renderer permanecem sem homologação por esta prova.

## Corpos disponíveis e saídas de apresentação

Os 19 implementadores têm seus corpos de `initializeClient` individualizados por owner, descritor, bytecode e pivôs. Cada corpo obtém propriedades do proxy, faz `checkcast IClientItemExtensions` e encaminha o objeto ao `Consumer.accept @10`; o retorno ocorre em `@15`. Doze callbacks nativos usam `getISTERProperties`, seis de armadura usam `getArmorProperties` e o callback Citadel usa seu proxy realocado. Os callbacks não alocam as objetos de extensão; a construção pertence aos getters clientes delimitados separadamente. O argumento é fornecido pelo chamador; o callback não autentica nem descobre o chamador e não cria por si só um registro em evento.

A [ficha](systems/client-extension.md) relaciona cada implementador ao getter e às classes de propriedades/saídas identificadas nos proxies. O [selo](EXACT-CLIENT-EXTENSION-1.0.10.json) distingue esses métodos completos das delegações para renderer/model/proxy. A avaliação de um getter ou a criação de um objeto de propriedades não comprova pixels exibidos, áudio, animação física ou um pipeline gráfico integral.

Os getters base de `CommonProxy` e `CitadelProxy` retornam null. No cliente, `ClientProxy` guarda propriedades nativas em campos por instância; `ACItemRenderProperties.getCustomRenderer` cria um renderer AC novo a cada chamada. `CitadelClientProxy` cria propriedades novas, cujo construtor guarda um renderer Citadel por instância. Não se confundem propriedade compartilhada, renderer novo e cache dentro da propriedade. A escolha real do proxy continua não verificada.

A entrada de armadura encaminha entity, stack e defaultModel; seu parâmetro `EquipmentSlot` não é lido nesse corpo. O seletor contempla seis classes de item e fallback recebido, com inicialização de seis modelos estáticos sob flag própria. O encaminhamento de animação trata entity nula separadamente e delega apenas os tipos de modelo delimitados. Não se certificam os corpos dos modelos, `withAnimations` ou o rendering customizado completo.

Propriedades de rendering podem delegar ao proxy e aos owners gráficos. Os métodos selados identificam essas relações e seus argumentos; não se convertem os nomes de renderer/model em parâmetros de dano, range, hitbox, cooldown ou seleção de alvo. Estado visual, material de armadura e atributos efetivos têm contratos separados. A [ficha de materiais](systems/armor-material.md) mantém suas evidências e não é recontada como um efeito desta interface.

## Sete eixos do contrato estático

| Eixo | Evidência | Limite conservado |
|---|---|---|
| Identidade | JAR/classes SHA-exatos, interface, assinatura, descritor e roster de implementadores | Fonte 1.1.1 adjacente; código externo e transformações não fechados |
| Comportamento | Corpos disponíveis dos 19 callbacks e saídas delimitadas das propriedades oferecidas | Ausência de callsite tipado não autoriza alegar execução nem inutilidade universal |
| Parâmetros | Consumer, classes construídas, argumentos e delegações de apresentação | Sem valores de combate, escala de alvo ou atributos presumidos a partir de visuais |
| Targeting | API sem aquisição de vítima, área, projétil, LOS, fonte de dano ou ownership de cast | Apresentação customizada não altera targeting por analogia |
| Custos/tempo | Inicialização não efetua casting, mana, stamina, gasto, cooldown ou reparo | Frequência/ordem real de callback e recursos gráficos dependem do chamador/engine |
| Integração | ABI disponível, implementação nativa/realocada e zero chamadas tipadas delimitadas | `registration_execution=NOT_VERIFIED`; `NO_MUTATION`, sem adapter por jogador |
| Validação | Censo tipado, corpos/pivôs, regressões negativas e reprodução do selo no JAR exato | Hooks `NOT_VERIFIED`, QA física `NOT_TESTED`; sem fechamento integral do provider |

Os campos próprios de ataque, cura, summon, alcance, área, tipo de dano, velocidade/dimensão/vida de projétil e custo de spell são **N/A para esta ABI de apresentação**. A justificativa está nos corpos e nas operações identificadas, sem inventar uma skill para preencher a rubrica. Black Arcana mantém sua autoridade de runtime e RPG Skill Tree sua progressão; a API de cliente não fornece recibos de cast, hit, kill, XP ou Mastery.

Uma futura integração precisa localizar e validar a boundary executável adequada à versão instalada. Acesso a um callback, `Consumer`, getter ou proxy não homologa hook mutador, registro dinâmico, ordem de override, cache por jogador ou sincronização. A prova não altera o código do provider, não adiciona dispatcher e não instala uma nova extensão no cliente.

## Reprodução e regressões

O [auditor](../../../../docs/qa/alexscaves_1010_client_extension_audit.py) e o [workflow dedicado](../../../../.github/workflows/alexscaves-1010-client-extension.yml) confrontam o artefato e o selo, preservando as provas de materiais e os demais arquivos anteriores. Exemplo com Java 21:

```bash
python docs/qa/alexscaves_1010_client_extension_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-CLIENT-EXTENSION-1.0.10.json' \
  --output /tmp/client-extension-evidence.json
```

Critérios: duas saídas idênticas ao selo; rejeição de artefato, corpo, referência tipada, declaração, propriedade ou alegação de segurança divergente; correspondência entre ficha, provas e certificado; contagens e índices gerados consistentes. O sucesso desses testes valida evidência estática. Os resultados efetivamente executados são registrados na PR e no relatório de verificação da entrega.

**QA física pendente:** bootstrap no cliente e servidor dedicado, chamador/evento real, registro e ordem de extensão, compatibilidade da versão NeoForge, coexistência de renderers, troca de resource pack/reload, propriedades em inventário/mão/armadura, primeira/terceira pessoa, modelos por stack e entidade, cache e ciclo de vida, multiplayer, código transformado, colisão visual versus física e integração com animações/Epic Fight. Nenhum cenário recebe PASS porque um método foi declarado ou um objeto foi construído em bytecode.

## Contagem e fila alfabética

Esta entrega acrescenta **uma ficha de suporte e um certificado estático**, com **zero raízes mágicas**, zero hooks homologados e zero promoção de Stage. O catálogo passa a **221/2395 contratos estáticos**, **471/2395 fichas catalogadas** e Alex's Caves a **83/83 fichas atualmente observadas**. A árvore `systems/` mostra **2/2 (100%)** das fichas detectadas; isso não encerra todos os sistemas de integração.

O prefixo revisado conserva `ACArmorMaterial` e a disposição de suporte do marcador vazio `ACArmorTickItem`, acrescentando o contrato declarado de `ACClientExtensionItem`. O [roster físico original](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) permanece preservado; próximo escopo sem disposição: **`server/item/ACDestroyedItem`**. Dano **11/11** e encantamentos **51/51** não mudam. Universo integral do provider, hooks e QA física continuam abertos; providers com catálogo encerrado **4/164**, homologação integral para perks **0/164**.
