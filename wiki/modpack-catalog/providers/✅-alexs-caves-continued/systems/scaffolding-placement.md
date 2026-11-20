# BlockItemWithScaffolding — seleção de posição para andaimes

**Versão:** Alex's Caves Continued 1.0.10, publisher file 8856293. **Escopo:** contrato técnico estático da seleção de contexto e do cálculo de suporte. **Hooks:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perks executáveis:** `NOT_CERTIFIED`. `NO_MUTATION`.

`BlockItemWithScaffolding` estende `BlockItemWithSupplier` e declara o construtor, `mustSurvive` e `updatePlacementContext`. O SHA-256 da classe é `3dcd18424a03d342c3ea78f116d9de2c5181fffc0bc5213ea9db36f87b1e6e3b`. O tipo 2 de `ACBlockRegistry.getBlockSupplier` (contexto 66, bootstrap 5 no offset 67) leva à factory 438. O inicializador passa esse tipo para `alexscaves:metal_scaffolding` (344/352/353) e `alexscaves:rusty_scaffolding` (2263/2271/2272).

## Seleção do candidato

O método lê a posição efetiva do contexto de colocação e seu estado. Se o bloco nessa posição não for instância de `MetalScaffoldingBlock`, devolve o contexto original quando `getDistance` difere de 12 e `null` quando vale 12 (28–49).

| Entrada sobre um andaime metálico | Direção escolhida |
|---|---|
| Uso secundário, hit marcado como interno | Oposto da face clicada |
| Uso secundário, fora do bloco | Face clicada |
| Uso normal, face superior | Direção horizontal do contexto |
| Uso normal, demais faces | Para cima |

A busca começa no vizinho na direção escolhida (105–117). Avança enquanto encontra andaimes metálicos (222, 246–268). O contador sobe apenas para direção horizontal, com teto 12 (121–123). No eixo vertical aplicam-se os limites do mundo, sem incremento desse contador. O primeiro bloco de outro tipo precisa aceitar substituição para o método devolver `BlockPlaceContext.at` (231–245). O servidor rejeita posição fora dos limites e pode enviar `build.tooHigh` ao jogador (126–206). A saída é um contexto ou `null`. A posição selecionada, os limites de mundo e a confirmação de colocação continuam sob a autoridade do engine.

## Suporte e colocação

`MetalScaffoldingBlock.getDistance` inicia em 12. Abaixo da posição, herda a distância de um andaime vanilla ou metálico. Fora desses ramos, tag `alexscaves:scaffolding` ou face superior sólida podem retornar 0 (19–102). Na horizontal, só considera vizinhos da tag com estado do tipo metálico ou `ScaffoldingBlock`. Calcula `min(atual, distância do vizinho + 1)` e encerra cedo ao encontrar 1 (150–242).

`mustSurvive` retorna false neste item. Na referência de `BlockItem.canPlace`, isso dispensa o teste condicional de sobrevivência, enquanto a obstrução continua verificada. `BlockItem.place` avalia a capacidade de colocação, solicita o contexto (34), trata `null` como falha (42) e segue para estado e solicitação de colocação (48, 63). Portanto o contador de extensão e a distância de suporte têm funções distintas na colocação.

O código próprio seleciona uma posição de bloco e não debita a stack. Colocação, consumo e atualização do bloco dependem dos consumidores externos e foram delimitados à referência estática. Alcance de cast, área, dano, projétil, tempo e cooldown ficam fora deste fluxo. Uma integração que altere a seleção precisa preservar limites de mundo, encaixe, suporte e autoridade de colocação antes de aprovar um hook.

[Prova, hashes e reprodução](../EXACT-ADJACENT-ITEMS-CATALOG-1.0.10.md)
