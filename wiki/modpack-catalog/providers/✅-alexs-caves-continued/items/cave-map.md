# Cave Biome Map — `alexscaves:cave_map`

**Contrato estático:** `CERTIFIED_STATIC_7_AXES` / `STATIC_TECHNICAL_CATALOG_ONLY`. **Política:** `NO_MUTATION`. **Hook mutador:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perk executável:** `NOT_CERTIFIED`. Provider `OPEN`, zero novas raízes mágicas.

## Identidade

O **Mapa de Biomas das Cavernas** recebe o alvo de um Cave Codex, busca o bioma no servidor e grava na própria stack os dados que o cliente usa para desenhar o mapa. `CaveMapItem` estende `Item` e implementa `UpdatesStackTags`, `ACClientExtensionItem` e `ACTickingItem`. A classe tem três campos constantes e 12 corpos próprios. SHA-256 da classe `949abbb18960cc013ab5a1b9c73c643005792c214ddbd0c927c96843f73f2b01`. A evidência é do JAR publisher 1.0.10, arquivo CurseForge 8856293, Minecraft 1.21.1 e Java 21. [Identidade do artefato e descoberta das seis classes](../EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md)

`ACItemRegistry.<clinit>` carrega o literal `cave_map` em `@375`, resolve o bootstrap 17 em `@378`, pede o registro em `@383` e atribui `CAVE_MAP` em `@386`. `lambda$static$4()` constrói `CaveMapItem` com pilha máxima 1 (`@12`) e raridade `UNCOMMON` (`@18`). O construtor próprio repassa as propriedades a `Item`. [Contrato do registro de itens](../systems/item-registry.md)

## Comportamento dos 12 corpos próprios

| Corpo | Instruções | Fluxo observado |
|---|---:|---|
| `<init>` | 4 | Delega `Item.Properties` ao pai em `@2`. |
| `initializeClient` | 6 | Solicita `PROXY.getISTERProperties` em `@4` e entrega a extensão de cliente ao `Consumer` em `@10`. |
| `use` | 66 | Lê a stack da mão. `Loading` ou `Filled` resulta em `PASS` (`@144`). Nos demais casos retorna `SUCCESS` (`@138`), com criação da tarefa somente no ramo de servidor e quando `ACWorldData.get` retorna dados. |
| `createMap` | 22 | Cria stack de `CAVE_MAP`, grava o ID do bioma como `BiomeTargetResourceKey` (`@37`) e publica seu componente em `@42`. |
| `isLoading` | 12 | Lê `Loading` do componente. Retorna falso se a tag estiver ausente ou o booleano for falso. |
| `isFilled` | 12 | Aplica a mesma leitura a `Filled`. |
| `getBiomeBlockPos` | 21 | Lê `BiomeX`, `BiomeY` e `BiomeZ`, ou retorna `BlockPos.ZERO` quando a tag está ausente. |
| `getBiomeTarget` | 19 | Lê `BiomeTargetResourceKey`, analisa o identificador em `@29` e cria a chave de `Registries.BIOME` em `@32`. Retorna `null` para tag ausente ou string nula. O corpo não trata erro de parsing. |
| `acInventoryTick` | 167 | Verifica periodicamente o bioma das coordenadas armazenadas. Quando diverge ou a chave é nula, registra diagnóstico e solicita regeneração em `@354`. |
| `createBiomeArray` | 75 | Decodifica `MapBiomes` pela tabela `MapBiomeList` em um vetor de 16.384 inteiros, com vetor vazio se a tag estiver ausente. |
| `getSeed` | 10 | Lê `RandomSeed` como `long`, com zero se a tag estiver ausente. |
| `appendHoverText` | 27 | Para alvo presente, troca `:` por `.` no ID, monta `biome.<namespace>.<path>` e acrescenta o texto traduzível em cinza. Delega ao pai em `@59`. |

No primeiro uso que cria `MapUUID`, o servidor chama `sendMSGToAll(UpdateItemTagMessage)` em `@74` antes de gravar o novo `CUSTOM_DATA` em `@101`. O bridge `ACCompat.getOrCreateTag` devolve uma cópia ou tag nova. A chamada em `@74` antecede a escrita do UUID e de `Loading=true` na stack. Com UUID existente, o uso reutiliza o valor. Se a consulta a `ACWorldData` retorna `null`, o ramo ainda retorna `SUCCESS` após gravar `Loading`, sem ter enfileirado uma tarefa.

Na regeneração, o callback exige servidor, `selected=true`, `Filled=true`, `Loading=false` e entidade `Player`. A checagem ocorre quando `(tickCount + entityId) % 1800 == 0` e a distância horizontal entre o jogador e a posição gravada é estritamente menor que **200 blocos**. Em `@122` o callback consulta `Level.getBiome` nessa posição. Se a chave esperada não coincidir ou for nula, obtém os dados do mundo, reutiliza ou cria o UUID e pede outro preenchimento. Ao criar UUID nesse ramo, ele grava a tag em `@188` antes de enviar a mensagem em `@203`. O ramo conserva `Filled` e não escreve `Loading=true`. [Dispatcher de inventário, contrato de `selected` e limites de cadência](../systems/ticking-item.md)

## Parâmetros da busca e da grade

| Parâmetro | Valor estático e aplicação |
|---|---|
| `cave_map_search_attempts` | Padrão **128.000**, intervalo **64–2.147.483.647** (`ACServerConfig.<init> @556–565`). `hasWork` relê o valor e compara `samples < limite`. Cada `doWork` elegível incrementa `samples` uma vez por posição X/Z. |
| `cave_map_search_width` | Padrão **64**, intervalo **4–256** (`@582–591`). O inicializador do worker lê esse valor para `SAMPLE_INCREMENT`, o passo horizontal da busca. |
| Passo vertical da busca | `doWork @98` pede `Mth.outFromOrigin` com origem no Y atual do jogador, limites de `minBuildHeight + 1` e `maxBuildHeight`, passo **64**. |
| Controle de execução | `ACWorldWorkerManager.tick(true)` guarda o relógio no pré-tick. No pós-tick, o laço usa uma janela de referência de `max(10, 50 − tempo já decorrido)` ms e verifica o prazo entre chamadas ao worker. O cronômetro próprio da tarefa mede tempo para os logs. |
| Grade final | **128 × 128** células com passo de **7 blocos** no plano. À coluna `x` e linha `z` de 0 a 127 correspondem `((centroX / 7) − 64 + x) × 7` e `((centroZ / 7) − 64 + z) × 7`, com divisão inteira JVM. O índice é `z × 128 + x`. |

O tamanho da grade descreve a amostragem do mapa preenchido. A extensão da busca depende da trajetória do worker, do orçamento de tentativas e do resultado da amostragem. O gerenciador verifica o prazo entre chamadas. O preenchimento da grade ocorre no corpo de conclusão e pode ocupar uma chamada inteira.

## Seleção do alvo e conclusão

Uso e regeneração partem da posição em blocos do veículo raiz do jogador no nível de servidor atual. O worker lê a chave da stack e usa `ACBiomeRegistry.MAGNETIC_CAVES` quando `getBiomeTarget` retorna `null`. Começa na origem e avança em espiral horizontal, alternando as direções a partir de norte e aumentando o comprimento dos trechos. `doWork` filtra cada coluna com `ACBiomeRarity.isQuartInRareBiome` usando a seed do nível. Para as colunas que passam, consulta `BiomeSource.getNoiseBiome` nas alturas candidatas e valida a chave contra o registro do nível. Guarda a última altura correspondente da coluna.

`calculateBiomeCenter` refina o ponto encontrado. No caminho geral sonda para cima e para baixo em passos de 8 blocos, com limites de 32 e 64, e atribui Y absoluto por `atY(floor(subida × 0,25) − descida)`. Para `ABYSSAL_CHASM`, sobe em passos de 1 enquanto o bioma coincide, até 256, e recua 10 blocos. A sondagem lateral usa passo 8, limite 800 por direção e aplica os deslocamentos `leste − oeste` e `sul − norte` no ponto intermediário. A grade final amostra abaixo do centro (`Y − 5`) para Abyssal Chasm. Nos demais casos, sobe de `minBuildHeight + 1` até abaixo do nível do mar em passos de 32, parando ao encontrar o alvo e conservando a última amostra quando não encontra.

No sucesso, o worker solicita a escrita da grade, das coordenadas `BiomeX/Y/Z`, de um `RandomSeed` novo obtido do gerador aleatório do nível e de `Filled=true`. Na ausência de posição encontrada, solicita mensagem de erro com a distância inteira entre a origem e a última posição amostrada, ou zero sem amostra anterior. Nos dois caminhos põe `Loading=false`, remove `MapUUID`, publica o componente e envia a atualização com UUID do jogador e da tarefa. Uma falha de regeneração pode conservar o conteúdo já presente no mapa. A busca por ruído e a verificação posterior por `Level.getBiome` consultam superfícies diferentes. Geração, conteúdo de chunks e posição final em uma seed efetiva permanecem em aberto. [Selo suplementar do worker, fila e configuração](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.json)

## Custos e receita

`data/alexscaves/recipe/cave_map.json` declara `type=alexscaves:cave_map`, SHA-256 `9611e69fc6b862a347693523beb9453f8022d1a8fb115f4030e35f1fb01236a6`. `RecipeCaveMap` define uma grade 3 × 3 com oito `minecraft:paper` ao redor de um `alexscaves:cave_codex`. `assemble` encontra o primeiro Codex, lê seu `CaveBiome` (`@92`) e cria o mapa vinculado (`@104`) quando a chave existe. Sem chave, retorna `ItemStack.EMPTY`. A liquidação dos ingredientes depende da transação de crafting do engine. `use` e o tick não debitam stack, durabilidade, mana, stamina ou XP. O trabalho agendado consome tempo de processamento do servidor. [Leitura do Cave Codex](../systems/cave-info-item.md)

## Integração e formato do mapa

O mapa usa `DataComponents.CUSTOM_DATA`. O worker grava `MapBiomes` como vetor de bytes e `MapBiomeList` como tabela de entradas `BiomeID`/`BiomeHash`. Cada byte da grade referencia o identificador numérico de bioma no registro do nível por meio dessa tabela. O decoder percorre até `min(16384, tamanho do vetor)` e deixa o restante zerado. Ele pressupõe que cada byte lido tenha entrada na tabela. O `CaveMapRenderer` lê coordenadas, vetor e seed para a apresentação do mapa na mão e em moldura.

`ACWorldData.get` usa o armazenamento do Overworld para dados compartilhados. A tarefa retém o `ServerLevel` recebido na solicitação para buscar o bioma. `fillOutCaveMap` chama a conclusão do worker anterior, quando presente (`@18`), antes de criar e enfileirar o próximo (`@43`). Na conclusão, o consumidor de `UpdateCaveBiomeMapTagMessage` procura no inventário do jogador a primeira stack `CAVE_MAP` com `MapUUID` correspondente e só então solicita a troca do componente. O modelo empacotado usa `builtin/entity`. O advancement usa `minecraft:inventory_changed` com o ID do item. O valor `Filled` visto no JSON está no ícone e não compõe o critério. [Manifesto de descoberta, consumidores e recursos](../EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.json)

## Validação

A certificação cobre os corpos próprios, os bindings e recursos do publisher e as rotas nativas delimitadas de receita, busca, preenchimento, atualização e apresentação. Configuração efetiva, coordenadas encontradas, sincronização ao mover a stack, reinício, concorrência de pedidos, renderização, persistência e progressão observada dependem do ambiente carregado e continuam sem QA física. O dispatcher e as mensagens não estabelecem autoridade mutadora ou crédito de Mastery. [Prova dos sete eixos e reprodução](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md)
