# Purple Soda Bottle e Fertilizer — contratos do publisher 1.0.10

A análise usa o JAR **8856293** com 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O [selo](EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.json) fixa as referências tipadas das 1.555 classes, os corpos selecionados, os bindings, o perfil de comida, os recursos e as referências do engine. SHA-256 do selo `12d22107063c6e0d56c8c63e3a2f038cf652e22a74efa590291c5741f2688508`.

## Garrafa de refrigerante

A única instância direta de `DrinkableBottledItem` em `ACItemRegistry` é o binding `PURPLE_SODA_BOTTLE` via `lambda$static$148`. Declara stack até **16**, nutrição **2**, saturação nominal **0.4** e **0.01F** de chance declarada para Sugar Rush por **200 ticks**. A rotina do item declara uso de **40 ticks** e som de bebida. A seleção do recebedor é o consumidor. O alcance de enchimento é o alcance de interação do jogador, com raycast de fluido fonte, permissão `mayInteract` e tag `purple_soda`. [Ficha da garrafa](items/purple-soda-bottle.md)

`finishUsingItem` @4–7 chama e descarta o retorno herdado, solicita critério e estatística próprios para `ServerPlayer` e decide a devolução de garrafa pela stack recebida. A referência Minecraft `Item.finishUsingItem` usa chamada virtual a `eat` quando há perfil FOOD. O patch NeoForge troca a leitura direta por `getFoodProperties(consumer)`. `Player.eat` também pede estatística e critério, em pontos anteriores ao consumo. O selo distingue as duas origens das chamadas. Contagem aceita de eventos, unidade consumida ou recipiente devolvido são resultados de QA.

O caminho do Sack of Sating tem alvo e liquidação de inventário próprios em `overrideOtherStackedOnMe`. Ele usa a classe da garrafa para decidir o retorno do recipiente e não executa o consumo direto ou seu sorteio. O chocolate quente herda a classe, com perfil e override próprios que continuam na fila.

## Fertilizante

`ACItemRegistry.lambda$static$123` constrói o binding `FERTILIZER`. Os três corpos da classe incluem `useOn @0–164` e `applyFertilizer @0–132`. A seleção começa no bloco clicado. O ramo de cultivo tenta até **quatro** chamadas a `performBonemeal` em `ServerLevel`, após a validação inicial. O laço atualiza o estado, conserva a instância de bloco original e encerra quando o novo bloco deixa de implementar `BonemealableBlock`. O fallback exige face sólida e parte da posição adjacente. [Ficha do Adubo](items/fertilizer.md)

`ACPlatform.onApplyBonemeal` retorna −1 para cancelamento, +1 para sucesso sem cancelamento e 0 para continuar a implementação local. A referência `BonemealEvent.setSuccessful` grava o resultado e também pede cancelamento. Já o patch `BoneMealItem.java` usa `isSuccessful` quando cancelado. Um listener precisa considerar as duas interpretações do contrato. A falha do ramo de cultivo do Adubo ainda pode encaminhar ao fallback aquático.

No Mojang 1.21.1, `BoneMealItem.growWaterPlant` exige água com nível **8**. Em servidor, percorre até **128** tentativas e chama `shrink(1)` @471 antes de retornar verdadeiro. O Adubo tem outro pedido de redução no ramo aquático @150 para o uso fora do criativo. O caminho NeoForge de colocação guarda, restaura e reaplica estado de stack conforme a resolução do evento. O caminho vanilla de modo criativo preserva a contagem. Os bytes selados permitem reproduzir os pontos de redução e a fronteira de liquidação. A contagem final e as proteções efetivas do pack continuam pendentes.

## Prova e reprodução

O selo diferencia bytecode do **publisher** de referências oficiais **Minecraft 1.21.1** e **NeoForge 21.1.250**. A referência de engine abrange o JAR cliente e suas mappings compatíveis, as classes do universal e a presença ou ausência dos patches userdev selecionados. Ela delimita o comportamento upstream. A transformação instalada e a execução física ainda precisam ser verificadas.

```sh
python3 docs/qa/alexscaves_1010_bottle_fertilizer_catalog.py \
  --jar /caminho/alexscaves-1.0.10.jar \
  --client /caminho/client-1.21.1.jar --mappings /caminho/client-1.21.1.txt \
  --universal /caminho/neoforge-21.1.250-universal.jar \
  --userdev /caminho/neoforge-21.1.250-userdev.jar \
  --javap "$JAVA_HOME/bin/javap" --output /tmp/alexscaves-bottle-fertilizer.json
```

O verificador exige as identidades fixadas e compara o relatório recomposto com o selo. A [CI dedicada](../../../../.github/workflows/alexscaves-1010-bottle-fertilizer-catalog.yml) baixa as mesmas referências e roda com Java 21. A Extinction Spear está no mesmo lote alfabético e reaproveita um [contrato binário separado já reproduzível](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.md).

Os três itens acrescentam zero raízes mágicas. `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O catálogo integral do provider continua aberto.
