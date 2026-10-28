# Demon Horn — consumível e moeda

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** documentação de contrato binário; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Referências PC indicam offsets de método no publisher, não código reproduzido. O conflito publisher ARR / metadado TOML MIT permanece aberto; só fatos de interoperabilidade são retidos.

## Identidade e contrato

- Registry: `acolyte:demon_horn`; classe `net.raptorzizi.acolyte.item.consumables.DemonHornItem`; superclass `Item`.
- Propriedades de comida: nutrição **3**, saturationModifier **0**, `alwaysEdible`; o item associa a respectiva `ModFoodProperties`.
- `use(Level, Player, InteractionHand)` inicia o uso da mão selecionada e retorna `consume` da stack dessa mão; animação **EAT**, duração **24 ticks** (1,2 s a 20 TPS). Alvo: o próprio consumidor `LivingEntity`; sem aquisição de alvo externo, projétil, raio ou owner local.
- Ao terminar, os efeitos customizados só são aplicados quando `Level.isClientSide=false`. Cria uma instância padrão de `MobEffectRegistry.INSTANT_MANA` do host, sem passar duração/amplificador explicitamente. Se o efeito for instantâneo, o consumidor é origem direta, origem indireta e alvo com fator 1; caso contrário chama `addEffect`. A quantidade restaurada depende da implementação/configuração de Iron's, não de uma fórmula de Acolyte.
- A devolução/consumo de stack e a parte alimentar passam a `Item.finishUsingItem`; não há `shrink` nem cooldown explícito nesses métodos locais. Nenhum dado persistente local de item/owner é escrito.

## Aquisição e economia

Entrada de brewing: `Potions.AWKWARD` + este item aponta para `PotionRegistry.INSTANT_MANA_TWO` de Iron's. O output é uma poção do host, sem novo registro de magia/poção Acolyte.

Moeda principal das ofertas do Horn Merchant; duas unidades servem ao crafting de `acolyte:demon_horns_0`. Os loots de Demon Archer/Mage/Warrior contêm uma entrada deste item em pool compartilhado com scroll; não garantir drop por morte. Ver [Horn Merchant](../entities/horn-merchant.md).

`ModPotionRegistry.addRecipes(RegisterBrewingRecipesEvent)` é consumidor **ativo**: o método tem `@SubscribeEvent` e a classe `@EventBusSubscriber(modid="acolyte")` no binário. Não é apenas um holder sem uso. Não registra uma nova identidade de poção.

## Evidência reproduzível

- `ModItemsRegistry.<clinit>` PC 8–21, `lambda$static$0` PC 0–20: identidade e associação de comida.
- `ModFoodProperties.<clinit>` PC 0–21: propriedades alimentares.
- `DemonHornItem.getUseAnimation` PC 0–3; `getUseDuration` PC 0–2; `use` PC 0–13; `finishUsingItem` PC 0–80: trigger, lado, targeting e delegação.
- `ModPotionRegistry.addRecipes` PC 0–19; anotações de classe/método verificadas com `javap -v -p`.

## Boundary de integração e validação

Acolyte possui o item e sua política local; Iron's possui atributos, efeitos, recipientes e magias do host; Minecraft/NeoForge possui inventário, equipamento e liquidação vanilla. Não há hook mutador homologado. Nomes de métodos/registries são candidatos de observação, sem garantia de API estável. Perks não devem alterar mana, repetir consumo, aplicar atributos em outro slot ou liquidar recompensas por esta ficha.

`NOT_TESTED`: conferir o hash instalado, uso/equipamento no servidor dedicado, criativo/sobrevivência, troca de slot, relog, morte e multiplayer; confirmar uma única aplicação e um único consumo no pack real. Ausência de cooldown explícito na classe não certifica ausência de cooldown herdado/do host.
