# Floater e Frostmint Spear — contratos do publisher 1.0.10

A autoridade é o JAR publisher **8856293**, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O [selo reproduzível](EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.json) fixa os registros do item e entidade, os corpos e as referências tipadas do censo das **1.555 classes**, os recursos e as referências de engine. SHA-256 do selo `91263ad8a2f50d34ecdbd7dabceab19b4b27b483cbc3f3ac1f6e15154a870012`.

## Floater

`ACItemRegistry.<clinit> @1953–1967` vincula o fornecedor `lambda$static$103` a `alexscaves:floater`. `ACEntityRegistry.<clinit> @891–905` e `lambda$static$51` registram a entidade homônima **0,98 × 0,98**. A factory pede atualização de deltas de velocidade e argumento de tracking 20. No NeoForge 21.1.250, `setUpdateInterval(1)` usa um fornecedor próprio, enquanto `updateInterval(10)` grava apenas o campo usado pelo fornecedor padrão. O getter da referência usa o primeiro valor. [Ficha do Flutuador](items/floater.md)

O item exige água ou coluna de bolhas e ausência de agachar em `use`. Cria a entidade, copia posição/rotação, pede inserção no servidor e pede montagem do veículo raiz. Os dois booleanos são descartados. O pedido de uma unidade fora do criativo vem em seguida. A interação com uma entidade já existente testa o resultado de montar o próprio jogador no servidor. Os métodos do Mojang e o patch NeoForge de `Entity` delimitam o guard de tipo, a admissão de passageiro e o evento cancelável `EntityMountEvent`. A mudança física não é inferida de `InteractionResult`.

`FloaterEntity.tick` aplica **−0.04D** à velocidade Y sob gravidade, **+0.2D** enquanto `wasEyeInWater` e fator **0.9D** à velocidade após movimento. O contador de ticks secos aumenta no servidor e conserva o valor durante ticks molhados. A partir do **sexto** tick seco acumulado, o tick pede evento 3 e descarte. A entidade não serializa esse contador nos seus callbacks próprios. A apresentação de descarte, a montagem e o movimento permanecem sob avaliação do engine. O selo inclui os dois corpos do item e os 14 da entidade, além de fábrica, consumidores, receita, recursos visuais e contrato de montagem.

## Frostmint Spear

`ACItemRegistry.lambda$static$192` fornece o item `alexscaves:frostmint_spear`, stack até **16**. O segundo binding `frostmint_spear_inventory` é uma representação de inventário. `ACEntityRegistry.lambda$static$82` fornece `FrostmintSpearEntity` de **0,5 × 0,5**. O arremesso usa `p > 0.1D`, velocidade **2.5F × p** e pede consumo da stack fora de `instabuild`. O [contrato da lança](equipment/frostmint-spear.md) conecta o `SpearItem` herdado, os atributos de mão principal, a receita e os custos ao comportamento próprio.

O construtor do projétil com atirador não lê a stack recebida. Entrega uma **stack padrão nova** e argumento de arma `null` à superclasse. Em `onHitEntity`, pede **6F** mais bônus para vítima viva a partir de outro stack padrão, com fonte `trident`. O retorno do dano delimita as operações diretas de pós-impacto. `onHit` pode executar uma área antes de delegar o impacto a `AbstractArrow`, com guarda de lado servidor, idade superior a 1 tick e latch de explosão desligado.

`FrostmintSpearEntity.explode` define raio **2F**, modo `KEEP` e `fromSpear=true`. `FrostmintExplosion.explode` usa limite radial **4**, caixa candidata maior e exposição para compor o dano de explosão. A área pula EnderMan e aplica o filtro de explosão do engine. Para itens derrubados, a flag da lança pula o pedido de dano. O retorno booleano de `hurt` é descartado na área, e o ramo de movimento e congelamento segue seus próprios filtros. `interactsWithBlocks()` retorna falso com `KEEP`. O hash sela o corpo todo, e os trechos do manifesto preservam os operandos de seleção, dano, movimento, estado e o gate do finalizador.

O melee, o pós-impacto direto e a área pedem `setTicksFrozen(getTicksRequiredToFreeze() + 200)` e ativam o accessor. A declaração `LivingEntityMixin` implementa esse accessor. A anotação do método pode ser conferida com `javap -v -p` sobre a classe selada. `ac_livingTick` é injetado no fim de `LivingEntity.tick` e pode limpar a flag diante de contador não positivo ou alvo que não pode congelar. Contador, efeitos visuais e dano aceito são estados distintos, com duração física pendente.

## Reprodução e escopo

```sh
python3 docs/qa/alexscaves_1010_floater_frostmint_catalog.py \
  --jar /caminho/alexscaves-1.0.10.jar \
  --client /caminho/client-1.21.1.jar --mappings /caminho/client-1.21.1.txt \
  --universal /caminho/neoforge-21.1.250-universal.jar \
  --userdev /caminho/neoforge-21.1.250-userdev.jar \
  --javap "$JAVA_HOME/bin/javap" --output /tmp/alexscaves-floater-frostmint.json
```

O verificador exige os hashes e os tamanhos dos artefatos, recompõe o relatório e compara o resultado byte a byte com o selo. Os patches oficiais NeoForge, o JAR Mojang e as mappings são referências upstream versionadas. A [CI dedicada](../../../../.github/workflows/alexscaves-1010-floater-frostmint-catalog.yml) baixa as entradas fixadas e executa a mesma reprodução.

As duas fichas recebem `STATIC_TECHNICAL_CATALOG_ONLY`, com **zero raízes mágicas adicionadas**. A aplicação no runtime instalado, a sincronização em servidor, a autoria efetiva do dano e o comportamento com outros mods seguem pendentes. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Provider aberto.
