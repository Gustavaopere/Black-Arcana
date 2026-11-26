# Radiant Essence

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45748227744/job/139669398914), HEAD `247a4c7adec94b3c99a28fd1aadb668b07dc3ef3`, dois relatórios byte-idênticos de 156.541 bytes, SHA-256 `2bd27341d274f749e8c80b0a0e77e6f37571a92545293d910e7b47deb1cdb945`. [Dossiê](../EXACT-QUARRY-RADIANT-FOOD-1.0.10.md). Sem novo dump instalado ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:radiant_essence`; owner `RadiantEssenceItem`; factory `ACItemRegistry.lambda$static$181`, Code SHA-256 `4695bc463cfdbffb43121cd3c2adb63f7dedb49c54784503528a9123ef96a062`. [Registro](../systems/item-registry.md). Item de identidade própria com raridade e apresentação; função transitiva ainda não demonstrada. Descrição interpretativa do binário.

## Comportamento comprovado

As duas factories constroem RadiantEssenceItem sem argumentos e têm o mesmo Code SHA-256; o construtor usa Item.Properties.rarity(ACItemRegistry.RARITY_RAINBOW) @11. A classe declara somente construtor e appendHoverText. A identidade RADIANT_ESSENCE não entra no ramo de tooltip específico de LICOWITCH_RADIANT_ESSENCE. Depois delega Item.appendHoverText @42. Não há callback próprio de ativação, dano, cura, status, projétil, alcance, AOE, mana, cooldown, owner ou persistência de efeito. A classe sozinha não demonstra uso ritual, função de crafting, loot ou consumidor indireto.

Advancement data/alexscaves/advancement/alexscaves/radiant_essence.json (SHA-256 e5bda54d69d6c8b8c9ce52c87a66a04571d1ce30267674dcb222a2a64bc57092) tem critério minecraft:inventory_changed para alexscaves:radiant_essence; não é um efeito de ativação. O scan tipado de classes localiza construtores no registry e o próprio owner, mas não fecha Fieldrefs por ID, datapacks, loot, recipes ou consumidores genéricos de ItemStack.

## Integração e pendências

Item de suporte por identidade, escopo semântico não fechado. Rastrear registry fields, aquisição, tags, recipes, loot, trades e uso por outras classes antes de atribuir função mágica. Sem hook mutador, cast, mudança de estado, XP ou Mastery homologados.

## Aquisição declarativa

Sem receita localizada pelo filename no recorte; não é prova de inexistência. Loot/trade e referências transitivas pendentes.

## Localizadores de evidência

Classfile SHA-256 `eb072027b5797f7b96e83cabd58ebdfd3029e5c1e84fa789c620309dd3a57d92`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 8 | `5262492a8d82a1e4b0f6fb20c680919feeaa8232d925d767fe442248a2e6e32f` |
| `appendHoverText(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/Item$TooltipContext;Ljava/util/List;Lnet/minecraft/world/item/TooltipFlag;)V` | 20 | `2cf2cc3c9812d17f0b3d424ab2bcd09b587bfc018c23725b19fdfe91a6d4ba9b` |

## Evidência complementar — #1235

[Prova nativa](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828495853), HEAD `9c16b9c73452706148f666156a815b75696311de`, dois relatórios 765.144 bytes SHA-256 `6c8e0c98af51b60fe40d3bd0b326fb909525f1780b2086740748e158b6bd20ea`; [referência vanilla](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828496659), 149.285 bytes SHA `41e941487c560cc8deb700af7952801d31731c83986e56770c13f29d0dea8e67`. [Dossiê](../EXACT-FOOD-IDENTITY-KEYBIND-CLOSURE-1.0.10.md). 1555 classfiles, Fieldref exato e valores JSON; sem inferência de tags transitivas ou modpack transformado. Permanece parcial.

Fieldref exato encontrado no inicializador e aba criativa (lambda$static$24 @571); não há produtor/consumidor de gameplay próprio identificado por Fieldref do campo neste recorte. Recursos JSON por valores registram referências de crafting/loot/advancement a uma ou outra essência, ainda não atribuídas integralmente por valor aos dois IDs. Não inferir ritual ou consumo de energia; rastrear receitas, loot, tags e bridges genéricos.

## Reconciliação de fronteiras distribuídas

Vínculo comprovado no contrato [Conversion Crucible](../actions/conversion-crucible-biome-conversion.md): receita de Crucible usa uma Radiant Essence e Biome Treat usa duas. É custo de crafting, não evidência de sacrifício no tick, mana ou item ativável. O ritual seleciona stack de oferenda em seu próprio estado. Não transferir a exigência de Licowitch Radiant Essence para esta variante. Permanecem por atribuir recursos de loot e receitas adicionais por ID exato.

Evidência compartilhada: [matriz de reconciliação](../EXACT-CATALOG-INHERITED-BOUNDARIES-1.0.10.md). Mantidos NOT_CERTIFIED, NO_MUTATION e NOT_TESTED; nenhuma promoção por herança isolada.


## Resultado do censo causal — #1240

[Run 45903382213/job 140194260474](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213/job/140194260474): sete checks e dois relatórios byte-idênticos de 227.057 bytes SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`, 1.563 JSONs. [Dossiê](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-1.0.10.md) · [Selo por ID](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json).

Censo por identidade confirma quatro receitas que referenciam a essência (Biome Treat, Confection Oven, Conversion Crucible e Sundrop), loot de baús licowitch_tower e licowitch_tower_secret, loot da entidade Licowitch, advancement e tag gingerbread_man_steals. É ingrediente/objeto de suporte, não efeito de uso. O consumidor da tag de roubo e condições/quantidades efetivas de loot e receitas não se encerram apenas pelos caminhos JSON. Não transferir nenhuma dessas referências a Licowitch Radiant Essence.

**Fieldrefs do registry neste recorte:**

| Owner/método | Offset | Opcode | Code SHA-256 |
|---|---:|---|---|
| `ACItemRegistry.<clinit>` | 3208 | `putstatic` | `bb73db4c0f1d1c84abdf5ab1c07defd24db79e5e8c754b8c9f9ec8481a84a84a` |
| `ACCreativeTabRegistry.lambda$static$24` | 571 | `getstatic` | `c43d1cfbc0fb2efd284f7d75f30f232e5038ddfa264a58d5253e0164cb599c5d` |

**Atribuição completa de referências literais/possíveis tags no recorte data/:**

| Recurso | Caminho JSON / relação | SHA-256 |
|---|---|---|
| `data/alexscaves/advancement/alexscaves/radiant_essence.json` | `["criteria","mussel","conditions","items",0,"items",0]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `e5bda54d69d6c8b8c9ce52c87a66a04571d1ce30267674dcb222a2a64bc57092` |
| `data/alexscaves/advancement/alexscaves/radiant_essence.json` | `["display","icon","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `e5bda54d69d6c8b8c9ce52c87a66a04571d1ce30267674dcb222a2a64bc57092` |
| `data/alexscaves/loot_table/chests/licowitch_tower.json` | `["pools",0,"entries",9,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `0d9f0a4837eb424eab1be3e2a1e95acd760e2a9e26b8650b4e53d8507ef67f60` |
| `data/alexscaves/loot_table/chests/licowitch_tower_secret.json` | `["pools",0,"entries",3,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `3b1f2655803b2eb8b8b3d57bf56d58b75964b29aaa7b93fd7672f03347836f86` |
| `data/alexscaves/loot_table/entities/licowitch.json` | `["pools",0,"entries",0,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `157ba186f052f989fc31bd016ae3352eaa77c58ec1a8a639c91774f239e34526` |
| `data/alexscaves/recipe/biome_treat.json` | `["key","E","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `c7b6b504ec21125773b6f65e5a5d4a591da98dcb3266ecf04108d855658f9012` |
| `data/alexscaves/recipe/confection_oven.json` | `["key","E","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `3d0c85d36ca04ccb0aaa7fadd4048debe4c73d41195a7276c3f898845422b034` |
| `data/alexscaves/recipe/conversion_crucible.json` | `["key","E","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `7d3f31cbbca2a3a02076ad057861bf8a1d9a167864b250a16ec76d1ce9ce4271` |
| `data/alexscaves/recipe/sundrop.json` | `["key","R","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `08f21af8c4340fcbabe9e964a7e463901760793da4db97c9c6f2e5c00a32358d` |
| `data/alexscaves/tags/item/gingerbread_man_steals.json` | `["values",6]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `59c2591008e62e6bb91011202fa7aa2200fd950f9da55d309dbf0bea243682f8` |

**Estado:** NOT_CERTIFIED / NO_MUTATION / NOT_TESTED; as lacunas indicadas acima não foram promovidas.
