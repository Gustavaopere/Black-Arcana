# Ars Nouveau — The Drygmy / Looting

**Estado: contrato técnico estático documentado**, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

| Campo | Contrato e limites verificados no source |
|---|---|
| Identidade e versão | `ars_nouveau:thread_drygmy`, `com.hollingsworth.arsnouveau.common.perk.LootingPerk`, Ars Nouveau **5.13.1**, minimumSlot **ONE=1** herdado [perk] [registry] [contract] [slot]. Thread é distinto do familiar e da automação Drygmy. |
| Comportamento e causalidade | A armadura monta modifiers para cada PerkInstance; LootingPerk adiciona `slotValue` a `PerkAttributes.DRYGMY` por **ADD_VALUE**, ID do modificador `ars_nouveau:thread_drygmy` [armor] [perk]. Dois mixins de loot leem o atributo do atacante no cálculo de nível de encantamento [count-mixin] [chance-mixin]. |
| Parâmetros, operações e caps | Campo DRYGMY registrado com path `ars_nouveau.perk.drygmy`, base **0**, range declarado **0…1024**, syncable [attributes]. O callback não usa countForPerk/maxSlot; recebe valor da instância. O consumidor converte o valor efetivo para int. Não inferir soma irrestrita de4 peças: modifiers compartilham ID fixo e a aplicação final depende do sistema de atributos/equipamento. |
| Targeting, resultado e duração | Receptor é o atacante LivingEntity consultado pelo loot context. Sem alcance, área, alvo de cast, cooldown, dano ou duração próprios. Age em EnchantedCountIncreaseFunction e LootItemRandomChanceWithEnchantedBonusCondition; não cria drop diretamente nem garante que toda tabela use essas funções [count-mixin] [chance-mixin] [mixin-config]. |
| Custos e aquisição | Enchanting Apparatus: **1 Blank Thread** como reagent, **3 Drygmy Shard +2 Earth Essence +1 Rabbit's Foot** nos pedestais; resultado1, `sourceCost:0`, `keepNbtOfReagent:false` [recipe] [recipe-json]. Instalação/slots são Ars-owned; sem débito de mana, taxa de Source por kill ou XP de glyph nesse callback. |
| APIs e autoridade | Ars mantém Threads, slots, atributos e seus consumidores. `IPerk.applyAttributeModifiers` é uma API real; a implementação default devolve o objeto recebido, e o caminho de armadura consome o retorno de cada instância [contract] [armor]. Acesso nativo não certifica uma bridge segura de RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. RPG mantém progressão por contrato; Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém sistemas ambientais. Não repetir o resultado nem criar Mastery/cast pago por chamada do consumidor. Uma integração de loot deve observar o resultado do pipeline nativo, sem recompensar novamente cada chamada de função/condição ou duplicar Luck, encantamento e Mastery. |
| Evidência e validação | `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; release **5.13.1**, publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. O SHA identifica a release; os109 IDs compilados de glyphs/rituais **não cobrem Threads**, nem provam equivalência dos métodos desta ficha. Config instalada, equipamentos/addons, execução física e listeners externos não foram testados: `physical_qa=NOT_TESTED`. |

## Fórmula realmente consumida pelo loot

Nos dois mixins, sem instância de DRYGMY no atacante, o retorno é apenas a chamada original. Com atributo, `perkLooting=(int)attributeValue`; SpellDamageSource fornece `spellLuck`, ou0 se a fonte não for esse tipo. O nível devolvido é **max(spellLuck, originalEnchantmentLevel)+perkLooting** [count-mixin] [chance-mixin]. A chance/quantidade final continua pertencendo à função e loot table vanilla; não foi substituída por uma fórmula universal de itens nesta ficha.

Isso não passa pelo antigo LootingLevelEvent do familiar: o handler ali está comentado. O familiar vivo aplica `LOOTING_EFFECT` ao owner a cada60 ticks por600 ticks; esse efeito soma **+1 ADD_VALUE ao mesmo DRYGMY**, ID `ars_nouveau:looting_bonus` [familiar] [looting-effect]. São entradas diferentes no atributo, não duas identidades do Thread nem justificativa para um drop paralelo.

A persistência está no ARMOR_PERKS/holder e sua lista de instâncias [component] [holder] [slots] [instances]. A classe não mantém histórico de kills, proc token ou contador de loot. Mudança externa do atributo exige verificar colisão de IDs, slot/phase, atribuição do atacante e efetiva ativação dos mixins.


**Invalidação:** mudança de release, source, receita, slots, equipamento, atributo, listener ou consumidor exige reauditoria. Nenhum hook executável foi implementado nesta ficha.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[contract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L24-L74
[slot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L18-L36
[armor]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L112-L125
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L16-L21
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L54-L62
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L23-L27
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/LootingPerk.java#L13-L34
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L29-L32
[count-mixin]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/looting/EnchantedCountIncreaseFunctionMixin.java#L17-L34
[chance-mixin]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/looting/LootItemRandomChanceWithEnchantedBonusConditionMixin.java#L17-L34
[mixin-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/resources/ars_nouveau.mixins.json#L19-L45
[familiar]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarDrygmy.java#L57-L72
[looting-effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModPotions.java#L39-L43
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeProvider.java#L967-L972
[recipe-json]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_drygmy.json#L1-L32
