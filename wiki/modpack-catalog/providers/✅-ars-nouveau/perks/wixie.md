# Ars Nouveau — The Wixie / Potion Duration

**Estado: contrato técnico estático documentado**, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

| Campo | Contrato e limites verificados no source |
|---|---|
| Identidade e versão | `ars_nouveau:thread_wixie`, `com.hollingsworth.arsnouveau.common.perk.PotionDurationPerk`, Ars Nouveau **5.13.1**, minimumSlot **ONE=1** herdado [perk] [registry] [contract] [slot]. É Thread de equipamento, distinto do familiar e da automação Wixie. |
| Comportamento e causalidade | Modifier em `PerkAttributes.WIXIE`: **0,15×slotValue**, **ADD_MULTIPLIED_BASE**, ID `ars_nouveau:thread_wixie` [perk]. `EventHandler.onPotionAdd` no evento **MobEffectEvent.Added** modifica a própria instância de efeito recebida; não cria uma segunda instância, não lança outra magia e não verifica se o efeito veio de um item Potion [potion]. |
| Fórmulas, defaults e caps | Attribute path `ars_nouveau.perk.wixie`, base **1**, range declarado **0…1024**, syncable [attributes]. Com apenas o modifier do Thread, slots1/2/3 correspondem a1,15/1,30/1,45. Se bonus>0: **durationNova=(int)(durationRecebida×bonus)**. Há truncamento/conversão para int, sem arredondamento para cima, clamp próprio de duração ou tratamento especial local do sentinel de duração infinita [potion]. |
| Targeting, resultado e duração | Apenas servidor. Efeito **beneficial** lê WIXIE do alvo; todo efeito **não beneficial**, inclusive categoria neutral, lê WIXIE de effectSource apenas se este for LivingEntity. Sem essa fonte ou sem atributo, bonus permanece0 e pula a multiplicação. `valueOrZero` devolve0 na ausência de atributo [potion] [perk-util]. Não há range/área/projétil/dano/cooldown próprios; a duração pertence ao MobEffectInstance receptor. |
| Custos e aquisição | Enchanting Apparatus: **1 Blank Thread +3 Wixie Shards +2 Abjuration Essence +2×#c:crops/nether_wart +1 Blaze Rod**; resultado1, `sourceCost:0`, `keepNbtOfReagent:false` [recipe] [recipe-json]. Nenhuma taxa própria de mana/Source por status nem XP de aprendizagem de glyph no callback. |
| APIs e autoridade | Ars mantém Threads, slots, atributos e seus consumidores. `IPerk.applyAttributeModifiers` é uma API real e devolve modifiers novos; o caminho de armadura atribui o retorno a cada instância [contract] [armor]. Acesso nativo não certifica uma bridge segura de RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. RPG mantém progressão por contrato; Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém sistemas ambientais. Não repetir o resultado nem criar Mastery/cast pago por chamada do consumidor. A extensão em Added e uma futura alteração dos stats de duração são fases diferentes; não aplicar ambas como bônus duplicado sem contrato e deduplicação. |
| Evidência e validação | `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; release **5.13.1**, publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. O SHA identifica a release; os109 IDs compilados de glyphs/rituais **não cobrem Threads**, nem provam equivalência dos métodos desta ficha. Config instalada, equipamentos/addons, execução física e listeners externos não foram testados: `physical_qa=NOT_TESTED`. |

## Fonte do bônus, sincronização e limites

O método seleciona o atributo do alvo ou do applier conforme `isBeneficial()`, não pela escola do glyph ou pela intenção de cura/debuff. O source registra os PerkAttributes automaticamente em Player, mas outros LivingEntities podem não possuí-los [attributes-registration]; `valueOrZero` deliberadamente não usa o default como fallback. Um atributo existente em zero também não executa a multiplicação.

A mutação é leitura/escrita direta de `event.getEffectInstance().duration`. Depois, se o effect holder estiver na tag `TO_SYNC`, o handler envia `PotionSyncPacket` com a duração atual [potion]. Isso não prova sync universal, prioridade sobre outros mods ou aprovação de reatribuir o payload inteiro como substituto. A persistência do Thread está no ARMOR_PERKS/holder/lista de slots; ele não mantém TTL ou carga próprios [component] [holder] [slots] [instances].

O consumidor não chama `PerkUtil.countForPerk`: lê o atributo efetivo. Modifiers de outras origens, colisões de IDs, layout de equipamento e outras fases de evento podem mudar o valor; não multiplicar manualmente pelo número de peças nem assumir maxSlot em substituição ao atributo nativo.


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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/PotionDurationPerk.java#L13-L34
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L29-L31
[attributes-registration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L48-L54
[potion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java#L426-L448
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeProvider.java#L959-L965
[recipe-json]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_wixie.json#L1-L38
