# Dark Horn — consumível e moeda

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** documentação de contrato binário; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Referências PC indicam offsets de método no publisher, não código reproduzido. O conflito publisher ARR / metadado TOML MIT permanece aberto; só fatos de interoperabilidade são retidos.

## Identidade e contrato

- Registry: `acolyte:dark_horn`; classe `net.raptorzizi.acolyte.item.consumables.DarkHornItem`; superclass `Item`.
- Propriedades de comida: nutrição **6**, saturationModifier **0**, `alwaysEdible`; o item associa a respectiva `ModFoodProperties`.
- `use(Level, Player, InteractionHand)` inicia o uso da mão selecionada e retorna `consume` da stack dessa mão; animação **EAT**, duração **24 ticks** (1,2 s a 20 TPS). Alvo: o próprio consumidor `LivingEntity`; sem aquisição de alvo externo, projétil, raio ou owner local.
- Ao terminar, os efeitos customizados só são aplicados quando `Level.isClientSide=false`. Cria `INSTANT_MANA` do host com duração 0 e amplificador **3**; se o efeito for instantâneo, o consumidor é origem direta, origem indireta e alvo com fator 1; caso contrário chama `addEffect`. Em seguida adiciona `BAD_OMEN` vanilla por **6000 ticks** (300 s a 20 TPS), amplificador **4** (nível V), ambient=false, partículas=true e ícone=true. Não converte o amplificador de mana em uma quantidade fixa: a fórmula pertence ao host.
- A devolução/consumo de stack e a parte alimentar passam a `Item.finishUsingItem`; não há `shrink` nem cooldown explícito nesses métodos locais. Nenhum dado persistente local de item/owner é escrito.

## Aquisição e economia

Entrada de brewing: poção Awkward com `POTION_CONTENTS` correspondente + este item resulta em `minecraft:ominous_bottle` com `OMINOUS_BOTTLE_AMPLIFIER=4`. Usa `DataComponentIngredient.of(false, awkwardStack)`; não presumir o comportamento de componentes extras sem testar a versão NeoForge instalada.

Moeda das ofertas de minério e upgrade orb do Horn Merchant; aquisição referenciada no loot de Lieutenant. O loot é uma entrada de pool, não garantia de drop por morte. Ver [Horn Merchant](../entities/horn-merchant.md).

`ModPotionRegistry.addRecipes(RegisterBrewingRecipesEvent)` é consumidor **ativo**: o método tem `@SubscribeEvent` e a classe `@EventBusSubscriber(modid="acolyte")` no binário. Não é apenas um holder sem uso. Não registra uma nova identidade de poção.

## Evidência reproduzível

- `ModItemsRegistry.<clinit>` PC 24–37, `lambda$static$1` PC 0–20: identidade e associação de comida.
- `ModFoodProperties.<clinit>` PC 24–49: propriedades alimentares.
- `DarkHornItem.getUseAnimation` PC 0–3; `getUseDuration` PC 0–2; `use` PC 0–13; `finishUsingItem` PC 0–104: trigger, lado, targeting e delegação.
- `ModPotionRegistry.addRecipes` PC 22–113; anotações de classe/método verificadas com `javap -v -p`.

## Boundary de integração e validação

Acolyte possui o item e sua política local; Iron's possui atributos, efeitos, recipientes e magias do host; Minecraft/NeoForge possui inventário, equipamento e liquidação vanilla. Não há hook mutador homologado. Nomes de métodos/registries são candidatos de observação, sem garantia de API estável. Perks não devem alterar mana, repetir consumo, aplicar atributos em outro slot ou liquidar recompensas por esta ficha.

`NOT_TESTED`: conferir o hash instalado, uso/equipamento no servidor dedicado, criativo/sobrevivência, troca de slot, relog, morte e multiplayer; confirmar uma única aplicação e um único consumo no pack real. Ausência de cooldown explícito na classe não certifica ausência de cooldown herdado/do host.
