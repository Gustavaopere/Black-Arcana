# Client Extension — ABI e fornecimento de apresentação de itens (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **Execução do callback:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perks executáveis:** `NOT_CERTIFIED`. **Política:** `NO_MUTATION`. O provider permanece `OPEN`; esta ficha de suporte acrescenta **+0 raízes mágicas**.

## 1. Identidade e autoridade

`com.github.alexmodguy.alexscaves.server.item.ACClientExtensionItem` é uma interface de suporte à apresentação de itens. Declara **zero campos, zero superinterfaces e um método público abstrato**: `initializeClient(Consumer<IClientItemExtensions>)`. Não é item registrado, spell, ação de jogador nem scheduler. Seu contrato próprio não contém implementação, valores de combate ou estado por jogador.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft **1.21.1**, CurseForge projeto **1645389**, arquivo **8856293**, **75.279.314 bytes**. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A classe da interface tem SHA-256 `d3139782c378b7b8eee0b580c912f36095675e31db98310475fbe1b60f5a0362`. A [prova comum](../EXACT-CLIENT-EXTENSION-1.0.10.md) e o [manifesto nativo](../EXACT-CLIENT-EXTENSION-1.0.10.json) delimitam esta ficha. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas como corroboração adjacente.

O censo das **1555 entradas `.class`** do JAR encontra referências tipadas à interface somente nela própria e em **19 implementadores diretos: 18 nativos e um Citadel relocado** no mesmo artefato. A inclusão de `com.github.alexmodguy.alexscaves.citadel.item.ItemCustomRender` fecha esse censo; não abre outro mod, provider ou ficha individual.

Há ainda **três implementadores por herança** em `server.item`: `ExtinctionSpearItem`, `FrostmintSpearItem` e `LimestoneSpearItem` estendem `SpearItem`, herdando a interface e seu callback sem declaração própria. Portanto há **22 classes concretas atribuíveis à interface**, **19 corpos próprios de callback** e **20 classes com referência tipada direta ao alvo**, incluindo o próprio alvo. Esses conjuntos distintos não acrescentam fichas de itens nem certificam o gameplay das lanças derivadas.

## 2. Comportamento declarado e limite de ativação

O descritor JVM do método é **`(Ljava/util/function/Consumer;)V`**; a assinatura genérica exige `Consumer<net.neoforged.neoforge.client.extensions.common.IClientItemExtensions>`. A interface não fornece corpo default, dispatcher, registro nem chamada do callback.

Cada um dos 19 implementadores diretos declara um corpo concreto de **16 bytes**, com a mesma sequência:

| Offset | Operação do callback |
|---|---|
| `@0` | Carrega o `Consumer` recebido |
| `@1` | Lê o campo estático do proxy da família correspondente |
| `@4` | Chama `getISTERProperties()Object` ou `getArmorProperties()Object` |
| `@7` | Faz `checkcast IClientItemExtensions` sobre o resultado |
| `@10` | Executa `Consumer.accept(Object)` uma vez |
| `@15` | Retorna `void` |

Os corpos encaminham o objeto fornecido pelo proxy; não criam uma extensão por implementador. Não possuem ramo, loop, cache próprio, teste de lado, guard de nulo ou tratamento próprio de exceção. O retorno do getter e os efeitos de `Consumer.accept` pertencem a outros owners. Os getters base de `CommonProxy` e `CitadelProxy` retornam **`null`** (`@0–1`); o cast não substitui esse valor por uma extensão. Os overrides de cliente descritos abaixo fornecem objetos concretos, caso esse seja o proxy utilizado na execução.

**Não há testemunha de chamada tipada ou registro deste callback no JAR.** A varredura global de `CONSTANT_Methodref` e `CONSTANT_InterfaceMethodref` encontra **zero referências a método chamado `initializeClient`, com qualquer owner ou descritor**. Isso é distinto das **23 declarações** com esse nome: esta interface, seus 19 implementadores e a interface paralela de fluidos com dois implementadores. O censo também não encontra referência a `RegisterClientExtensionsEvent`. Declarações e getters demonstram corpos invocáveis; não demonstram que o engine os registrou ou chamou. Chamadas externas ao artefato, reflexão, transformações do pack e execução física permanecem `NOT_VERIFIED`. Esse resultado não prova desuso universal nem defeito de renderização.

## 3. Implementadores, parâmetros e saídas delimitadas

Os nomes sem prefixo nas duas primeiras linhas pertencem a `com.github.alexmodguy.alexscaves.server.item`. Todos recebem somente o mesmo `Consumer`; nenhum recebe stack, nível de perk, player, mão, alvo ou configuração numérica no callback.

| Família / quantidade | Todos os implementadores diretos | Delegação real e objeto fornecido pelo override de cliente |
|---|---|---|
| ISTER nativo / **12** | `BlockItemWithISTER`, `CaveMapItem`, `DreadbowItem`, `GalenaGauntletItem`, `OrtholanceItem`, `PrimitiveClubItem`, `RaygunItem`, `ResistorShieldItem`, `SeaStaffItem`, `ShotGumItem`, `SpearItem`, `SugarStaffItem` | `AlexsCaves.PROXY` → `CommonProxy.getISTERProperties()`; `ClientProxy` devolve seu campo `isterProperties`, do tipo `ACItemRenderProperties` |
| Armadura nativa / **6** | `DarknessArmorItem`, `DivingArmorItem`, `GingerbreadArmorItem`, `HazmatArmorItem`, `PrimordialArmorItem`, `RainbounceBootsItem` | `AlexsCaves.PROXY` → `CommonProxy.getArmorProperties()`; `ClientProxy` devolve seu campo `armorProperties`, do tipo `ACArmorRenderProperties` |
| ISTER Citadel relocado / **1** | `com.github.alexmodguy.alexscaves.citadel.item.ItemCustomRender` | `Citadel.PROXY` → `CitadelProxy.getISTERProperties()`; `CitadelClientProxy` cria `CitadelItemRenderProperties` a cada chamada |

`ClientProxy.<init>()V` cria **um `ACItemRenderProperties`** (`@5–12`) e **um `ACArmorRenderProperties`** (`@16–23`) para seus campos finais. Seus dois getters devolvem esses campos (`@0–4`), sem distinguir item, stack ou jogador. Já `CitadelClientProxy.getISTERProperties()` aloca uma nova propriedade a cada chamada (`@0–7`). Essas são diferenças reais de fornecimento e tempo de vida; o callback não as uniformiza.

| Extensão fornecida | Saída / responsabilidade observada |
|---|---|
| `com.github.alexmodguy.alexscaves.client.render.item.ACItemRenderProperties` | Implementa `IClientItemExtensions`; `getCustomRenderer()` cria **novo `ACItemstackRenderer` em cada chamada** (`@0–7`). A propriedade compartilhada pelo proxy não é um renderer compartilhado por esse getter |
| `com.github.alexmodguy.alexscaves.client.render.item.ACArmorRenderProperties` | Implementa `IClientItemExtensions`; `getHumanoidArmorModel(entity,stack,slot,defaultModel)` encaminha entity, stack e defaultModel para `getACArmorModel`, faz cast para `HumanoidModel` e retorna (`@0–10`). O parâmetro `slot` não é lido nesse corpo |
| `com.github.alexmodguy.alexscaves.citadel.client.CitadelItemRenderProperties` | Implementa `IClientItemExtensions`; seu construtor cria um `CitadelItemstackRenderer` e o guarda em campo final (`@5–12`); `getCustomRenderer()` retorna esse campo (`@0–4`). O cache é por instância da propriedade, não por item ou player |

Os tipos de renderer retornados são compatíveis com `net.minecraft.client.renderer.BlockEntityWithoutLevelRenderer`. A API `IClientItemExtensions` pertence ao NeoForge; as propriedades e renderers acima pertencem ao provider ou à cópia Citadel relocada. Esta ficha prova o fornecimento e os retornos delimitados, sem certificar os corpos de desenho de `ACItemstackRenderer`, `CitadelItemstackRenderer` ou todos os métodos da API externa.

Na família de armadura, `getACArmorModelBase(stack,defaultModel)` inicializa modelos se `init==false` (`@0–6`), lê `stack.getItem()` e faz a seguinte seleção, nessa ordem:

| Tipo do item no stack | Campo estático retornado / modelo |
|---|---|
| `PrimordialArmorItem` | `PRIMORDIAL_ARMOR_MODEL` / `PrimordialArmorModel` (`@9–22`) |
| `HazmatArmorItem` | `HAZMAT_ARMOR_MODEL` / `HazmatArmorModel` (`@23–36`) |
| `DivingArmorItem` | `DIVING_ARMOR_MODEL` / `DivingArmorModel` (`@37–50`) |
| `DarknessArmorItem` | `DARKNESS_ARMOR_MODEL` / `DarknessArmorModel` (`@51–64`) |
| `RainbounceBootsItem` | `RAINBOUNCE_ARMOR_MODEL` / `RainbounceArmorModel` (`@65–78`) |
| `GingerbreadArmorItem` | `GINGERBREAD_ARMOR_MODEL` / `GingerbreadArmorModel` (`@79–92`) |
| Nenhum dos seis tipos | O `defaultModel` recebido (`@93–94`) |

`initializeModels()` marca `init=true` **antes** de construir os seis modelos (`@0–1`), usando `Minecraft.getInstance().getEntityModels().bakeLayer` com as seis constantes correspondentes de `ACModelLayers` (`@4–136`). Os modelos ficam em campos estáticos compartilhados; o método não contém recuperação própria para falha parcial. Isso descreve os corpos, sem comprovar bootstrap, disponibilidade das layers ou execução física bem-sucedida.

`getACArmorModel` aplica `applyACArmorAnimations(entity,modeloSelecionado)` (`@0–9`). Se entity é nula, essa função devolve o modelo sem encaminhar animações (`@0–5`); para modelos Primordial, Hazmat e Darkness chama o respectivo `withAnimations(entity)` (`@6–59`); para os outros modelos devolve o argumento (`@60–61`). O interior de `withAnimations`, a renderização customizada de armadura, glow, texturas e disponibilidade das layers são responsabilidades posteriores fora do contrato certificado nesta ficha.

## 4. Targeting, dano, alcance e ownership

**Dano, tipo de dano, cura, knockback de combate, vítima, raio, alcance, LOS, seleção de bloco, projétil e área: não aplicáveis ao contrato próprio da interface e ao encaminhamento dos 19 callbacks.** Nenhum desses corpos escolhe entidade, consulta mundo, cria `DamageSource` ou aplica resultado de combate. Isso não equivale a dano zero dos itens que implementam a interface; cada item mantém seu comportamento próprio.

O argumento `LivingEntity` da saída de armadura é contexto para o modelo e para o encaminhamento de animação. Não constitui prova de aquisição de alvo, owner de projétil, autorização de combate ou player beneficiário de perk. O stack permite selecionar a classe do item no helper de modelo; o `EquipmentSlot` recebido pela entrada de armadura não é consultado no corpo delimitado. O defaultModel é fallback de apresentação, sem valor de defesa associado.

Os campos de propriedade do proxy e os modelos estáticos não possuem chave de UUID, skill tree ou perk. A existência de um modelo distinto por tipo não garante isolamento de estado entre jogadores. Dimensões do modelo, poses e renderers não demonstram mudança de hitbox, escala física, alcance ou colisão.

## 5. Custos, tempo e configuração

**Mana, souls, stamina, munição, durabilidade cobrada, ingrediente, cooldown, duração, intervalo de tick, velocidade de projétil, multiplicador de dano e nível máximo de perk: não aplicáveis ao contrato próprio.** Não há constantes desses parâmetros na interface ou nos corpos de encaminhamento. Ela não declara cobrança, scheduler ou evento de uso; os custos e timings de Raygun, Dreadbow, Sea Staff, armaduras e demais itens continuam em seus owners de gameplay.

O custo observável delimitado é a obtenção de propriedades e renderers: propriedades nativas guardadas por `ClientProxy`, nova propriedade Citadel por chamada do getter de cliente, novo renderer AC por `getCustomRenderer`, renderer Citadel guardado na propriedade e seis modelos de armadura estáticos inicializados sob a flag `init`. Não foram medidos CPU, memória, FPS, frequência real das chamadas ou descarte de objetos. O nome `initializeClient` não prova execução única; a implementação concreta não impõe uma contagem de chamadas.

O callback não recebe parâmetros configuráveis de perk nem garante reconfiguração de extensão já fornecida. O getter base pode fornecer `null`, e os callbacks não validam esse retorno ou o Consumer. A aceitação, rejeição, armazenamento e execução posterior da extensão dependem do consumidor externo, cujo comportamento não foi certificado aqui.

## 6. Fronteiras de integração e sete eixos de decisão

Uma integração precisa separar a declaração do callback, a prova de seu registro, o objeto de extensão entregue, o método de apresentação consultado e o comportamento de gameplay do item. O catálogo entrega os owners concretos para investigar essas etapas; não transforma `initializeClient` em hook de perk homologado.

| Eixo pretendido de integração | Contrato observado / limite |
|---|---|
| Dano / potência | Sem parâmetro ou aplicação de dano nos corpos delimitados; investigar o item ou efeito de gameplay correspondente |
| Custo / recurso | Sem cobrança própria; alocação e compartilhamento de propriedades/renderers são comportamentos de apresentação |
| Tempo / frequência | Callback sem tick, cooldown ou guard de execução única; frequência depende de chamador ainda não verificado |
| Target / área / alcance | Sem seleção de alvo; entity e stack da saída de armadura são contexto de apresentação |
| Tamanho / escala / apresentação | Extensão fornece renderer ou modelo; seus retornos não provam mudança de geometria física ou todos os detalhes visuais |
| Player / ownership | Propriedades nativas e modelos compartilhados; nenhum parâmetro ou armazenamento de perk por jogador no contrato próprio |
| Registro / sincronização / compatibilidade | Zero testemunhas de chamada tipada de `initializeClient` no JAR; execução, binding no engine, sincronização e convivência com transformações externas permanecem pendentes |

`ItemProperties.register`, registros de renderers de entidade, telas, layers e listeners de cliente são mecanismos distintos. Sua presença não constitui registro deste callback. Também não há base para tratar um getter do proxy como ponto seguro de alteração de dano, custo ou estado por jogador. A [ficha de Armor Material](armor-material.md) mantém separada a construção dos parâmetros de armadura; as fichas dos itens e ações mantêm seus contratos próprios.

**Homologação executável para Black Arcana, Enshrouded, RPG Skill Tree ou Epic Fight: `NOT_CERTIFIED`.** Nenhum mixin, consumidor, registro ou override é adicionado por esta entrega. Hooks mutadores e execução do callback `NOT_VERIFIED`; política `NO_MUTATION`.

## 7. Validação e localizadores JVM

| Owner / método delimitado | Descritor JVM / localizador |
|---|---|
| `ACClientExtensionItem.initializeClient` | `(Ljava/util/function/Consumer;)V`; público abstrato, sem `Code` |
| Os 19 `initializeClient` concretos | Mesmo descritor; corpo completo `@0–15`, getter `@4`, cast `@7`, `Consumer.accept` `@10` |
| `CommonProxy.getISTERProperties`, `getArmorProperties`; `CitadelProxy.getISTERProperties` | `()Ljava/lang/Object;`; retorno nulo `@0–1` |
| `ClientProxy.<init>` e getters de propriedades | `()V @0–26`; getters `()Ljava/lang/Object; @0–4` |
| `CitadelClientProxy.getISTERProperties` | `()Ljava/lang/Object;`; alocação `@0–7` |
| `ACItemRenderProperties.getCustomRenderer`; `CitadelItemRenderProperties.getCustomRenderer` | `()Lnet/minecraft/client/renderer/BlockEntityWithoutLevelRenderer;`; corpos `@0–7` e `@0–4`, respectivamente |
| `CitadelItemRenderProperties.<init>` | `()V`; cache do renderer, corpo `@0–15` |
| `ACArmorRenderProperties.initializeModels` | `()V`; flag e seis bakes, corpo `@0–136` |
| `ACArmorRenderProperties.getHumanoidArmorModel` | `(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/client/model/HumanoidModel;)Lnet/minecraft/client/model/HumanoidModel;`; corpo `@0–10` |
| `ACArmorRenderProperties.getACArmorModel` | `(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/client/model/Model;)Lnet/minecraft/client/model/Model;`; corpo `@0–9` |
| `ACArmorRenderProperties.getACArmorModelBase` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/client/model/Model;)Lnet/minecraft/client/model/Model;`; seleção completa `@0–94` |
| `ACArmorRenderProperties.applyACArmorAnimations` | `(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/client/model/Model;)Lnet/minecraft/client/model/Model;`; encaminhamento completo `@0–61` |

Validação entregue: identidade SHA-exata do artefato, ABI da interface, censo completo de implementadores/referências tipadas, distinção entre declarações e referências a métodos, 19 corpos de callback e saídas finitas de propriedades delimitadas no manifesto. O contrato não inclui corpos de renderers/modelos posteriores nem certifica o pipeline visual completo.

QA física pendente: seleção efetiva do proxy, identificação do consumidor/registro que chama o callback, execução e armazenamento da extensão no NeoForge do pack, nulos/falhas de inicialização, disponibilidade das model layers, retorno efetivo de renderer/modelo por contexto, reload de recursos, apresentação com vários jogadores, sincronização e coexistência com Epic Fight e demais transformações. **Nenhuma execução física foi realizada nesta entrega.**

**Contabilidade:** **uma ficha técnica de sistema; +0 raízes mágicas novas; +0 fichas individuais para as 22 classes implementadoras diretas ou herdadas; +0 providers para o Citadel relocado.** `STATIC_TECHNICAL_CATALOG_ONLY`, `SHA_EXACT_BINARY_BEHAVIOR`, `NOT_VERIFIED`, `NOT_TESTED`, `NOT_CERTIFIED` e `NO_MUTATION` mantêm limites separados. O universo integral do provider continua `OPEN`.
