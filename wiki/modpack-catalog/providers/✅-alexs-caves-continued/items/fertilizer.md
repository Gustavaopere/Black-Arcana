# Fertilizer — Adubo

**Catálogo** ✅ Contrato técnico estático de `alexscaves:fertilizer` em Alex's Caves Continued 1.0.10. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED` e `NO_MUTATION`. O uso é uma utilidade de cultivo e acrescenta **zero raízes mágicas**. [Disposição de ações](../ITEM-ACTION-DISPOSITION-1.0.10.md)

## 1. Identidade

`server.item.FertilizerItem` estende `Item` e declara três corpos sem campos próprios. `ACItemRegistry.<clinit> @2259–2273` registra `fertilizer` no campo `FERTILIZER`. `lambda$static$123 @0–7` constrói a única classe vinculada a esse ID. O construtor `FertilizerItem.<init> @0–11` fornece `Item.Properties` padrão. No censo tipado de 1.555 classes, somente `ACItemRegistry` referencia `FertilizerItem` de fora da própria classe e não há subclasses. A classe tem SHA-256 `85d4d977a80551b86aaad35ee35103787d3b61ff3042a159e3af1e02f802b994` no JAR publisher 8856293, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. [Prova e reprodução](../EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.md) · [Registro de itens](../systems/item-registry.md)

## 2. Uso e seleção

| Caminho | Seleção e retorno |
|---|---|
| Cultivo | `useOn @0–37` lê a stack da mão, o mundo, a posição clicada e o jogador do `UseOnContext`. Chama `applyFertilizer` para a posição clicada. O helper retorna verdadeiro quando o bridge sinaliza sucesso ou quando o alvo passa pelo caminho local de cultivo. |
| Vegetação aquática | Se o helper falha, `useOn @80–117` verifica se a face clicada é sólida com `isFaceSturdy`. A posição candidata do fallback é `clickedPos.relative(clickedFace)`. A face é encaminhada com a stack original para `BoneMealItem.growWaterPlant`. |
| Retorno | Cada caminho bem-sucedido pede no servidor o evento de mundo `1505` com dado `0`, na posição tratada (`@53` ou `@134`). Em seguida retorna `ACCompat.sidedSuccess` em `@76` ou `@157`, que na referência 1.21.1 devolve `SUCCESS` no cliente e `CONSUME` no servidor. Se nenhum caminho aceita a tentativa, retorna `PASS` em `@161–164`. |

O alvo inicial é um bloco selecionado por interação. O fallback desloca o ponto inicial um bloco na direção da face. O item não declara raio de combate, projétil, dano, linha de visão própria ou alvo de entidade. O alcance da interação e as permissões de uso pertencem ao chamador e ao ambiente carregado.

## 3. Cultivo e evento NeoForge

`applyFertilizer @0–33` lê o estado inicial e chama `ACPlatform.onApplyBonemeal`. Na referência NeoForge, `EventHooks.fireBonemealEvent` posta `BonemealEvent` com jogador, mundo, posição, estado e a stack fornecida. O construtor do evento consulta `isValidBonemealTarget` quando o estado contém um `BonemealableBlock`. O bridge do publisher devolve `-1` se o evento está cancelado, `1` se está ativo e marcado como bem-sucedido, e `0` nos demais casos. `BonemealEvent.setSuccessful` grava o resultado e cancela o evento. Assim, um resultado de sucesso marcado dessa maneira e ainda cancelado faz o caminho de cultivo retornar falso e permite que `useOn` avalie o fallback aquático. A referência de `BoneMealItem` com o patch NeoForge usa `isSuccessful()` quando o evento está cancelado. [Prova do bridge e evento](../EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.md) · [NeoForge 21.1.250, fontes](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.250/neoforge-21.1.250-sources.jar)

Com retorno zero do bridge, o helper exige que o bloco inicial implemente `BonemealableBlock` e que `isValidBonemealTarget` aceite o estado inicial (`@34–66`). Num `ServerLevel`, solicita até **quatro** chamadas a `performBonemeal`, usando o `RandomSource` do mundo (`@69–126`). Depois de cada chamada relê o estado, saindo com sucesso se o bloco resultante já não implementa a interface. As iterações usam a instância de bloco inicial com o estado mais recente. O helper não repete a validação de alvo nem chama `isBonemealSuccess`. Um alvo válido também retorna verdadeiro fora de `ServerLevel`, sem executar o laço. São até quatro pedidos, e os resultados dependem da implementação de cada bloco.

## 4. Vegetação aquática e custo

Na referência Mojang 1.21.1, `BoneMealItem.growWaterPlant` aceita `Blocks.WATER` com quantidade de fluido **8** na posição adjacente. Em `ServerLevel`, o helper tenta até **128** iterações de dispersão com a aleatoriedade do mundo, verificações de colocação e sobrevivência e seleção por bioma. Ao fim, pede `ItemStack.shrink(1)` em `@471` e retorna verdadeiro. O valor de retorno indica que o ponto de partida atende às condições, mesmo se nenhuma colocação ocorreu. Fora de `ServerLevel`, aceita a mesma condição de água sem executar o laço nem pedir redução da stack. O patch NeoForge 21.1.250 de `BoneMealItem` atua no caminho de cultivo da classe. [Prova dos helpers Minecraft e NeoForge](../EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.md) · [Minecraft 1.21.1, cliente](https://piston-data.mojang.com/v1/objects/30c73b1c5da787909b2f73340419fdf13b9def88/client.jar) · [Mapeamento](https://piston-data.mojang.com/v1/objects/2244b6f072256667bcd9a73df124d6c58de77992/client.txt)

O próprio Adubo pede `shrink(1)` após sucesso de cultivo (`@69`) ou de vegetação aquática (`@150`) se `Player.isCreative()` for falso. Essas duas chamadas do publisher são ramos alternativos, sem guarda própria de lado. No caminho aquático de servidor há dois pontos de redução possíveis sobre a mesma stack para o jogador fora do criativo, um no helper Mojang e outro no publisher. O criativo pula apenas a redução explícita do publisher. O chamador Minecraft de uso em modo criativo preserva a contagem anterior, e o caminho NeoForge de servidor decide a liquidação de contagem e de estados de bloco capturados. A contagem física após uso precisa ser medida no pack. Nos dois ramos bem-sucedidos o corpo do item chama `isCreative` sem testar se `getPlayer()` é nulo. Não há cobrança própria de mana, durabilidade, XP ou cooldown. [Referências de liquidação](../EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.md)

## 5. Aquisição e apresentação

A receita `data/alexscaves/recipe/fertilizer.json` é `minecraft:crafting_shapeless`. Pede duas `alexscaves:guano` e uma `minecraft:bone_meal`, com saída de uma unidade pela contagem padrão. A receita publisher de `alexscaves:thornwood_sapling` usa uma unidade de Adubo e dois `alexscaves:thornwood_branch` em coluna. A aba Forlorn Hollows inclui o item por `ACCreativeTabRegistry.lambda$static$18 @135–147`. O livro do bioma exibe as duas receitas nas páginas 1 e 2 de `assets/alexscaves/books/forlorn_hollows/resources.json`. O modelo de inventário herda `minecraft:item/generated` e usa `alexscaves:item/fertilizer`. [Arquivos e hashes](../EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.md)

## 6. Integração e validação

O contrato estático cobre o binding, os três corpos próprios, o bridge de evento, os dois caminhos de crescimento e os recursos empacotados. A aceitação de alteração de bloco, os efeitos dos listeners, o débito final, a sincronização e o comportamento com proteções de mundo dependem do ambiente de execução. A inspeção dos pedidos de cultivo e do callback de evento não autoriza alterações por perks nem certifica regras de proteção ou rollback de Black Arcana. [Prova do publisher e das referências](../EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.md)
