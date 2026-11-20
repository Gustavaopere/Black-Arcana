# Cinco classes de item — catálogo estático 1.0.10

Artefato publisher 8856293, 75.279.314 bytes. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O censo cobre 1.555 classfiles. A evidência principal é o bytecode e os recursos do JAR 1.0.10.

## Evidências dos contratos individuais

| Eixo | AlwaysCombinableOnAnvil | BiomeTreatItem | BlockItemWithScaffolding |
|---|---|---|---|
| `identity` | Interface vazia, dois implementadores, um teste de tipo em CommonEvents | Um binding de registry, uma fábrica, oito corpos próprios, duas formas de stack | Corpo de colocação e fábrica compartilhada por dois bindings do registro |
| `behavior` | Registro de CommonEvents no bus, cópia da entrada, edição do mapa e pedido de resultado | Teste de uso, término, criação da stack vinculada, som, partículas e cor | Direção, caminhada, seleção de posição e cálculo de suporte |
| `parameters` | Níveis iguais somam 1, máximo do encantamento, flag por chamada e tabela de pesos | Pilha 1, perfis de nutrição 20/1 com modificador 0,1, condição de fome zero ou criativo | Limite horizontal de 12 posições, distância de suporte 0–12, direção conforme interação |
| `targeting` | Mesma identidade Item nas duas entradas, resultado na cópia de Left | Bioma da posição do jogador. Conversão e alvo do Crucible descritos na ação existente | Posição efetiva do contexto e primeiro destino substituível em um eixo |
| `costs` | Soma por peso e nível mais penalidade de incompatibilidade. Menu de referência liquida XP | Receita, ramo de vínculo antes do consumo, consumo delegado e uso distinto no Crucible | Seleção sem débito próprio. A colocação e o consumo pertencem ao BlockItem |
| `integration` | Pedidos do evento e liquidação na referência de menu. Runtime e hook pendentes | Fronteira entre stack, FOOD, CUSTOM_DATA, troca de mão e seleção no Crucible | Fronteira entre contexto, posição, obstrução e colocação de referência |
| `validation` | Replay dos corpos e do switch, anotação e registro do listener | Replay dos oito métodos e do ancestral, fábrica, recursos e perfis fixados | Replay dos corpos, seleção de factory, mapa dos dois bindings e tag do publisher |

[Combinação na bigorna](systems/anvil-combination.md) · [Biome Treat](items/biome-treat.md) · [Colocação de andaimes](systems/scaffolding-placement.md)

A fronteira da bigorna usa Minecraft 1.21.1 e NeoForge 21.1.250. A fronteira de colocação usa a referência derivada de desenvolvimento de Minecraft 1.21.1 e NeoForge 21.1.248, JAR SHA-256 `0e588600c7c5084989f201f9e5c3a2e74fc4a7c6dccaa970b65a21bd6d004d08`. Nela `BlockItem.place` tem Code SHA-256 `91e09154f8bf9704eaa87d424aceb5585158324aeb34711f3dac685f7ff0b336` e `canPlace` tem `25aa53fa3b01dae1e5866432320e200ad8f3e27ea42f88fee966a50629fa94bb`. As referências delimitam a chamada e a liquidação e não estabelecem equivalência com o engine transformado do modpack. [Bigorna](EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.md) · [FOOD](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.md)

## Disposições de apresentação

| Classe | Evidência própria e bindings | Disposição |
|---|---|---|
| `BlockItemWithISTER` | Dois métodos. `initializeClient` chama `getISTERProperties` (4), converte para `IClientItemExtensions` (7) e entrega ao consumer (10). Tipo 3 de `getBlockSupplier` (bootstrap 6 em 74) leva à factory 439 para `siren_light`, `copper_valve`, `beholder` e `gobthumper`. O tipo 9 em 116 aponta à factory 445 com `UNCOMMON`; o inicializador do publisher não passa valor 9. | Apresentação de item. Complementa o contrato existente de extensão de cliente, zero fichas adicionais. |
| `BlockItemWithSupplierLore` | Dois métodos. O tipo 1 (bootstrap 4 em 60) leva à factory 437 para 29 IDs `cave_painting_*`. `appendHoverText` resolve a chave de bloco (15), concatena namespace e caminho (32, 42), acrescenta `block.<namespace>.<path>.desc` em cinza (47–56) e chama super (68). As 29 chaves existem no `en_us.json` empacotado. | Apresentação de tooltip conforme o item de bloco. Zero fichas adicionais. |

O helper de registro delega a `getBlockSupplier` no offset 15 e registra o item no 18. A lista integral dos bindings classificados está no selo. As disposições avaliam as funções próprias das classes. As mecânicas de bloco, incluindo Beholder, conservam suas fichas e limites. [Extensão de cliente](systems/client-extension.md)

## Reprodução e fechamento

O workflow executa os três probes preservados e compara seus SHA-256 com o selo. Em seguida, reproduz o registro do listener, os bindings das factories, a tag de andaimes e as chaves de idioma. Selo de catálogo SHA-256 `3d0970896d8b7fc69539e063a774ea03be4a1b86b891452c7aa1731f1bdfed02`.

[Selo](EXACT-ADJACENT-ITEMS-CATALOG-1.0.10.json) · [Descoberta](EXACT-ADJACENT-ITEMS-DISCOVERY-1.0.10.md) · [Fronteiras nativas](EXACT-ADJACENT-ITEMS-BOUNDARY-1.0.10.md) · [Auditor](../../../../docs/qa/alexscaves_1010_adjacent_items_catalog.py) · [Workflow](../../../../.github/workflows/alexscaves-1010-adjacent-items-probe.yml)

Quinto símbolo do lote: `BlockItemWithSupplierLore`. Próximo símbolo: `server/item/BurrowingArrowItem`. Três contratos individuais, duas disposições de apresentação, zero novas raízes mágicas. O universo integral do provider continua aberto. `STATIC_TECHNICAL_CATALOG_ONLY`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`.
