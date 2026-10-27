# Ars Nouveau — The Whirlisprig / Saturation

**Estado: contrato técnico estático documentado**, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

| Campo | Contrato e limites verificados no source |
|---|---|
| Identidade e versão | `ars_nouveau:thread_whirlisprig`, `com.hollingsworth.arsnouveau.common.perk.SaturationPerk`, Ars Nouveau **5.13.1**, minimumSlot **ONE=1** herdado [perk] [registry] [contract] [slot]. A grafia do campo Java é `WHIRLIESPRIG`; o ID do Thread usa `whirlisprig`. |
| Comportamento e causalidade | `applyAttributeModifiers` instala um modificador de WHIRLIESPRIG com ID `ars_nouveau:thread_whirlisprig` e operação **ADD_MULTIPLIED_TOTAL** [perk]. No `LivingEntityUseItemEvent.Finish`, o handler servidor aceita item com FoodProperties e entidade Player, então multiplica a saturação atual pelo valor efetivo desse atributo [food]. |
| Fórmulas, default e caps | Mapa literal: **s=0→0; s=1→0,3; s=2→0,6; qualquer outro s→1,0**. Attribute path `ars_nouveau.perk.saturation`, base **1**, range declarado **0…10000**, syncable [perk] [attributes]. Com só este modifier e slots padrão1/2/3: valores1,3/1,6/2,0. O caso3 é+100%, não+90%: descrição “30% each level” não substitui a expressão executada. |
| Targeting, resultado e lifecycle | Afeta o Player que conclui uso de alimento; sem radius, dano, projétil, duração ou cooldown de cast. Fórmula do callback **Sdepois=(float)(Santes×perkValue)**, onde Santes é a saturação total lida nesse instante, não apenas a parcela do alimento. Nenhum clamp local é aplicado na atribuição direta a `FoodData.saturationLevel` [food] [perk-util]. Regras vanilla posteriores e efeitos de outros listeners não foram inferidos. |
| Custos e aquisição | Enchanting Apparatus: **1 Blank Thread +3 Whirlisprig Shards +2 Earth Essence +1 Golden Apple**; resultado1, `sourceCost:0`, `keepNbtOfReagent:false` [recipe] [recipe-json]. Sem cobrança própria por comida, mana ou XP de glyph; quantidade/consumo do alimento pertencem à cadeia normal de uso. |
| APIs e autoridade | Ars mantém Threads, slots, atributos e seus consumidores. `IPerk.applyAttributeModifiers` é uma API real; a implementação default devolve o objeto recebido, e o caminho de armadura consome o retorno de cada instância [contract] [armor]. Acesso nativo não certifica uma bridge segura de RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. RPG mantém progressão por contrato; Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém sistemas ambientais. Não repetir o resultado nem criar Mastery/cast pago por chamada do consumidor. Uma perk de nutrição não deve multiplicar novamente o mesmo estado após o handler Ars sem fase e deduplicação demonstradas. |
| Evidência e validação | `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; release **5.13.1**, publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. O SHA identifica a release; os109 IDs compilados de glyphs/rituais **não cobrem Threads**, nem provam equivalência dos métodos desta ficha. Config instalada, equipamentos/addons, execução física e listeners externos não foram testados: `physical_qa=NOT_TESTED`. |

## Atributo efetivo e repetição

O callback usa `PerkUtil.perkValue`: se a entidade não tiver instância de atributo, devolve o default do próprio atributo; aqui é1 [perk-util]. O valor não é o countForPerk nem uma soma manual dos slots. AnimatedMagicArmor chama o método de atributos por instância, com ID fixo do Thread; não se deduz empilhamento irrestrito entre peças nem soma dos multiplicadores a partir da descrição [armor].

O guard de execução está em servidor + item com FoodProperties + Player. Não há contador, estado de fome próprio, token ou deduplicador adicional por refeição na classe. ARMOR_PERKS/holder persistem a composição de equipamento [component] [holder] [instances] [slots]; a saturação alterada pertence ao FoodData do jogador, não a uma tag do Thread. Não confundir esse Thread com o familiar Whirlisprig ou com crescimento de plantas.


**Invalidação:** mudança de release, source, receita, slots, equipamento, atributo, listener ou consumidor exige reauditoria. Nenhum hook executável foi implementado nesta ficha.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[contract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L24-L74
[slot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L18-L36
[armor]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L112-L125
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L16-L21
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L54-L62
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L23-L27
[perk-util]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L22-L32
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/SaturationPerk.java#L13-L40
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L29-L31
[food]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java#L323-L331
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeProvider.java#L939-L944
[recipe-json]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_whirlisprig.json#L1-L32
