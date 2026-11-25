# Defaults de componentes, builder de entidade Ink Bomb e codec de receita — 21.1.250

**DISCOVERY_ONLY / NO_MUTATION**. Publisher Alex's Caves Continued 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Modlist #019, Minecraft 1.21.1, Java 21, distribuição oficial NeoForge 21.1.250. Não é observação física.

## Evidência prévia reutilizada

- Run [45471957912](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45471957912/job/138721970278), relatório 1.956.222 bytes SHA-256 `5a5c4a201604224306a2b5cded87cb82523bce8cf0e82aaf998954125afe0c65`. Item$Properties.<init> Code `91fd20ff4ac88d8a1516a2bd89ed6c288a6546839db4a268fb15d30671e879f3` inicializa requiredFeatures e canRepair=true, não escreve tamanho de stack. buildAndValidateComponents Code `ce196929d6466b4ddf1d652d18a7827b1e79831f5bfd93997d81f874a5975b10` delega buildComponents @1 e validateComponents @6. Default de componentes não pode ser inferido apenas do construtor.
- Run [45478837398](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45478837398/job/138746190157), relatório 658.305 bytes SHA-256 `1a4dc80b88f1484d3a059ddfb3782ec7c5299452c9923cf30244a27e155c645e`. ItemStack.lambda$static$3 Code `dc6750c881e2b856e770b6292081224e4048a6cbea15468efcffb0cd4e04c226` projeta count com intRange(1,99) e orElse(1) @38. Isso isoladamente não prova que o serializer shapeless usa esse codec.
- Run [45473794747](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45473794747), 178.620 bytes SHA-256 `534c8c6a7534d203d994ea1e4f4948b03c5a0ed01c79a5d97aa6a5eb2fdf79c2`: factory ACEntityRegistry.lambda$static$43 Code `5f095071ddceb4d09df9169080fcd8cda9d0fdbe185340560e692aa7b63d0fe7`, categoria MISC, sized(0.6F,0.6F), setShouldReceiveVelocityUpdates(true), setUpdateInterval(1), sem argumento explícito de trackingRange. Não atribuir valores default até localizar o builder.

## Sonda nova

`docs/qa/alexscaves_1010_item_entity_defaults_250_probe.py` reutiliza pins de oito classes e sete Code hashes prévios (três engine, quatro registry). Seleciona Item$Properties.buildComponents, Item, ItemStack, builder/mapa de componentes, EntityType$Builder, EntityType, ShapelessRecipe$Serializer e quatro factories. Os métodos candidatos não são afirmações de APIs; a declaração e Code vêm do JAR. A projeção de DataComponents.<clinit> fixa os quatro pivôs de escrita e uma janela limitada de 100 instruções anteriores à escrita de COMMON_ITEM_COMPONENTS, não pretende descrever toda a inicialização. A sonda não chama métodos da engine; workflow exige duas execuções idênticas. Primeiro resultado pendente.

Escopo útil para as fichas Ink Bomb/Glow Ink Bomb, default de componentes, aquisição de Hot Chocolate Bottle. Sem mudança de fichas concorrentes, certificado, runtime, hook ou QA.
