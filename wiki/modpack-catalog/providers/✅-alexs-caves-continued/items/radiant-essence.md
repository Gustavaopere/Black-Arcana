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
