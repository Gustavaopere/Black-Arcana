# Licowitch Radiant Essence

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45748227744/job/139669398914), HEAD `247a4c7adec94b3c99a28fd1aadb668b07dc3ef3`, dois relatórios byte-idênticos de 156.541 bytes, SHA-256 `2bd27341d274f749e8c80b0a0e77e6f37571a92545293d910e7b47deb1cdb945`. [Dossiê](../EXACT-QUARRY-RADIANT-FOOD-1.0.10.md). Sem novo dump instalado ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:licowitch_radiant_essence`; owner `RadiantEssenceItem`; factory `ACItemRegistry.lambda$static$182`, Code SHA-256 `4695bc463cfdbffb43121cd3c2adb63f7dedb49c54784503528a9123ef96a062`. [Registro](../systems/item-registry.md). Item de identidade própria com raridade e apresentação; função transitiva ainda não demonstrada. Descrição interpretativa do binário.

## Comportamento comprovado

As duas factories constroem RadiantEssenceItem sem argumentos e têm o mesmo Code SHA-256; o construtor usa Item.Properties.rarity(ACItemRegistry.RARITY_RAINBOW) @11. A classe declara somente construtor e appendHoverText. A identidade LICOWITCH_RADIANT_ESSENCE habilita o texto traduzível item.alexscaves.licowitch_radiant_essence.desc @13, estilizado GRAY e ITALIC, adicionado à lista @30. Depois delega Item.appendHoverText @42. Não há callback próprio de ativação, dano, cura, status, projétil, alcance, AOE, mana, cooldown, owner ou persistência de efeito. A classe sozinha não demonstra uso ritual, função de crafting, loot ou consumidor indireto.

O advancement de Radiant Essence examinado pede alexscaves:radiant_essence, não a identidade licowitch. O scan tipado de classes localiza construtores no registry e o próprio owner, mas não fecha Fieldrefs por ID, datapacks, loot, recipes ou consumidores genéricos de ItemStack.

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

ConversionCrucibleBlockEntity.rerollWantedItem()V (100 instruções) Code `9080d12830d6ebb9aad3579a00b99e33a9a2bcb4aa757076d841e2896fdfbe03`: atualiza blocos, toca som conforme fill, isWitchMode @54; se true instancia ItemStack LICOWITCH_RADIANT_ESSENCE @76 e escreve wantStack @79. Isso é requisito selecionado, não consumo ou conversão demonstrados. Investigar aceitação de sacrifício, débito, fill, modo Witch, mudança de biome/blocos, autoria, persistência e WorldEffectPolicy. Recursos JSON com referências ainda devem ser distinguidos por valor. Sem hook mutador.

## Reconciliação de fronteiras distribuídas

Vínculo comprovado no contrato [Conversion Crucible](../actions/conversion-crucible-biome-conversion.md): witch mode com duração positiva seleciona este item em rerollWantedItem @53–82; fill é limitado a seis e conversão normal fica suprimida. ConversionCrucibleBlock.acUse @0–222, BE.tick @672–837 (scan de itens a cada cinco ticks de servidor), consumeItem @0–42: compara identidade de item, não exige igualdade integral de NBT; uso manual fornece cópia unitária e solicita redução fora de creative, stack caída é consumida diretamente. Expiração @948–1006 redefine target/cor/request/display/fill; estado inclui WantStack, DisplayStack, ConvertingToBiome, FilledLevel, BiomeColor, SplashTimer, ConversionTime, WitchModeDuration. Não demonstra owner persistido na seleção nem nova magia própria. Perk de custo, fill ou modo witch deve respeitar autoridade do Crucible e não reexecutar consumo.

Evidência compartilhada: [matriz de reconciliação](../EXACT-CATALOG-INHERITED-BOUNDARIES-1.0.10.md). Mantidos NOT_CERTIFIED, NO_MUTATION e NOT_TESTED; nenhuma promoção por herança isolada.


## Resultado do censo causal — #1240

[Run 45903382213/job 140194260474](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213/job/140194260474): sete checks e dois relatórios byte-idênticos de 227.057 bytes SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`, 1.563 JSONs. [Dossiê](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-1.0.10.md) · [Selo por ID](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json).

Censo exato de 1.563 JSONs data/ encontrou **zero** referências por ID ou fecho de tags para esta variante. Fieldrefs nativos anteriores são três: registro @3225, tooltip @1 e ConversionCrucibleBlockEntity.rerollWantedItem @65. Logo não atribuir os quatro crafts, baús, loot de Licowitch, advancement ou tag de roubo à variante; a única função causal confirmada é a oferta exigida no modo Witch do Crucible. Origem adquirível por outros caminhos (incluindo produtores genéricos) ainda não fechada. Não certificar obtenção/consumo adicional por inferência.

**Fieldrefs do registry neste recorte:**

| Owner/método | Offset | Opcode | Code SHA-256 |
|---|---:|---|---|
| `ConversionCrucibleBlockEntity.rerollWantedItem` | 65 | `getstatic` | `9080d12830d6ebb9aad3579a00b99e33a9a2bcb4aa757076d841e2896fdfbe03` |
| `ACItemRegistry.<clinit>` | 3225 | `putstatic` | `bb73db4c0f1d1c84abdf5ab1c07defd24db79e5e8c754b8c9f9ec8481a84a84a` |
| `RadiantEssenceItem.appendHoverText` | 1 | `getstatic` | `2cf2cc3c9812d17f0b3d424ab2bcd09b587bfc018c23725b19fdfe91a6d4ba9b` |

Nenhum hit de data/ no recorte literal/tag; não prova inexistência de produtores dinâmicos.

**Estado:** NOT_CERTIFIED / NO_MUTATION / NOT_TESTED; as lacunas indicadas acima não foram promovidas.
