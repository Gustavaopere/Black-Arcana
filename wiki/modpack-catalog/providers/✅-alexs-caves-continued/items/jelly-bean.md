# Jelly Bean

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; provider OPEN. Não representa nova raiz mágica ou cast certificado.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10; Minecraft 1.21.1 / NeoForge 21.1.250 documental / Java 21. Modlist física sibling #019; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Não houve comparação nova com dump físico instalado nem observação do runtime transformado. [Dossiê de descoberta SHA-exata](../EXACT-JELLY-KEYBIND-LIMESTONE-1.0.10.md) e [replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45651673635/job/139337522318): 186.937 bytes, SHA-256 `61a6010adbe0c6f41968a6ffc8f85e8c4c6e013175007f6be93280d3cf2da0ed`, duas saídas byte-idênticas, seis checks. O dossiê detalha consumidores, hashes de métodos e offsets. Replay da HEAD consolidada obrigatório.

## Identidade e descrição funcional

`alexscaves:jelly_bean`, factory `ACItemRegistry.lambda$static$198`, Code SHA `546da6af37d6cc4834693c322a2cd13c1852123744a3bd55006b0bee3fd5ed63`; [registro](../systems/item-registry.md). Owner `JellyBeanItem` (SHA-256 `9842c28cd2eff05621a23be37ce5917ca88a19bf0bd99f0da9b5a5cc62a4355f`), estende PotionItem; nove corpos próprios. É um consumível com efeitos provenientes da stack, não um efeito único universal.

## Ativação, parâmetros, custos e alvos

Construtor solicita ACFoods.JELLY_BEAN, ACFoodBuilder.food e stack máximo 16. getUseDuration retorna 16 ticks; som GENERIC_EAT. getBeanColor usa Rainbow e hue=(currentTimeMillis%4000)/4000F, saturação 1 e brilho 0,8, senão potionColor; somente apresentação.

finishUsingItem (72 instruções, Code `285ba91b3197410e4ea9e455598f972ce7a7c2be1d1febc8aa9702959b493e18`): no servidor itera potionEffects, solicita efeito instantâneo com amplificador da instância e fator 1D, ou cópia de MobEffectInstance em addEffect; descarta retorno. Player recebe estatística ITEM_USED e shrink(1) quando não instabuild; consumidor não-Player não tem shrink no corpo. Solicita EAT e critério de consumo para ServerPlayer. Não invoca explicitamente o finishUsingItem ancestral neste corpo. Alvo é o consumidor, sem projétil ou AOE ofensiva própria demonstrada. Nutrição final, componentes, tipos de efeitos, duração/amplificadores efetivos, aquisição, custo final, cooldown/mana herdados e possíveis efeitos de terceiros: NÃO VERIFICADOS.

## Consumidores, estado, integração e pendências

onUseTick solicita partícula JELLY_BEAN_EAT com vetores aleatórios e posição do consumidor, server sendParticles ou Level.addParticle; não hit. Tooltip usa dados de efeitos/amplificadores e formata modificadores percentuais para operações multiplicativas. ClientProxy.lambda$onItemColors$22 chama getBeanColor. Advancement inventory_changed usa identidade do item; Rainbow no ícone é dado de apresentação, não prova de produtor da stack.

Próximos gates: produtores de POTION_CONTENTS e Rainbow, valores de ACFoods, PotionItem/consumo/codec e liquidação efetiva de efeitos; autoridade, owner e persistência da stack. Sem hook real autorizado, não alterar componentes, multiplicar efeito, reexecutar consumo ou creditar Mastery. NO_MUTATION; universo aberto.

## Evidência complementar — #1235

[Prova nativa](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828495853), HEAD `9c16b9c73452706148f666156a815b75696311de`, dois relatórios 765.144 bytes SHA-256 `6c8e0c98af51b60fe40d3bd0b326fb909525f1780b2086740748e158b6bd20ea`; [referência vanilla](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828496659), 149.285 bytes SHA `41e941487c560cc8deb700af7952801d31731c83986e56770c13f29d0dea8e67`. [Dossiê](../EXACT-FOOD-IDENTITY-KEYBIND-CLOSURE-1.0.10.md). 1555 classfiles, Fieldref exato e valores JSON; sem inferência de tags transitivas ou modpack transformado. Permanece parcial.

ACFoods.JELLY_BEAN N1 m bits 3d4ccccd, sem efeito próprio declarado; finishUsingItem não chama super, não prova atualização de FoodData. PotionItem.use referencial delega ItemUtils.startUsingInstantly. GummyBearEntity.createJellybean Code `32a3e91f97ff7fb2d1d43eca02dfdf79a41ad80bca76b93f80578165307788cd` resolve digestingEffect em BuiltInRegistries.POTION @7; se nulo cria ItemStack JELLY_BEAN; senão ACEffectRegistry.createJellybean Code `5726e6ef99a36f1d369980be69c04f1105182ca41f3e9c68bd6378f032626b18` encaminha item e Potion a ACCompat.potionStack @12. ACCompat.potionEffects Code `cfb23f71a3385db6d2a487c4d733f5fdc6fec2e9be5177807a28c82c6610e704` chama contentsOf→PotionContents.getAllEffects; applyInstantenousEffect Code `061e7ceb46bd78233f4e56ba3a28a9fa1eb1561754dd2e2fe2db2a143446cf1a` delega MobEffect.applyInstantenousEffect, argumento Level não é encaminhado. Pendentes contentsOf/potionStack, componente e producers digestingEffect/Rainbow, codecs e efeitos específicos. Sem novo efeito universal.


## Resultado do censo causal — #1240

[Run 45903382213/job 140194260474](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213/job/140194260474): sete checks e dois relatórios byte-idênticos de 227.057 bytes SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`, 1.563 JSONs. [Dossiê](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-1.0.10.md) · [Selo por ID](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json).

Censo por valor exato atribui somente dois recursos data/ ao ID: advancement jelly_bean (critério de inventário e ícone) e tag `create:not_potion`, não prova regra ativa de Create no modpack. GummyBearEntity continua produtor condicionado ao componente, e a tag não remove o override PotionItem. A ausência de receita direta nesta varredura não prova inexistência de obtenção. Pendem contentsOf/potionStack, produtores Rainbow/digestingEffect e consumidor externo dessa tag.

**Fieldrefs do registry neste recorte:**

| Owner/método | Offset | Opcode | Code SHA-256 |
|---|---:|---|---|
| `ClientProxy.onItemColors` | 104 | `getstatic` | `3249fa89f491fcb3d7e484ad238786a747b0d8b72cda962c143ad829d3de137d` |
| `GummyBearEntity.createJellybean` | 24 | `getstatic` | `32a3e91f97ff7fb2d1d43eca02dfdf79a41ad80bca76b93f80578165307788cd` |
| `ACItemRegistry.<clinit>` | 3497 | `putstatic` | `bb73db4c0f1d1c84abdf5ab1c07defd24db79e5e8c754b8c9f9ec8481a84a84a` |
| `ACEffectRegistry.createJellybean` | 0 | `getstatic` | `5726e6ef99a36f1d369980be69c04f1105182ca41f3e9c68bd6378f032626b18` |

**Atribuição completa de referências literais/possíveis tags no recorte data/:**

| Recurso | Caminho JSON / relação | SHA-256 |
|---|---|---|
| `data/alexscaves/advancement/alexscaves/jelly_bean.json` | `["criteria","mussel","conditions","items",0,"items",0]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `1b485b00a3cb83e02cbaa72325a52cba07e9805236a18da2f1906f80993ade96` |
| `data/alexscaves/advancement/alexscaves/jelly_bean.json` | `["display","icon","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `1b485b00a3cb83e02cbaa72325a52cba07e9805236a18da2f1906f80993ade96` |
| `data/create/tags/item/not_potion.json` | `["values",0]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `89f9d44bd9edd2465cdb9cfc604fa094d661540a16a478989ce8e460a14dc23d` |

**Estado:** NOT_CERTIFIED / NO_MUTATION / NOT_TESTED; as lacunas indicadas acima não foram promovidas.
