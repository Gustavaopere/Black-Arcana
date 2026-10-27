# Ars Nouveau — Feather

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Release **5.13.1**, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Classe `com.hollingsworth.arsnouveau.common.perk.FeatherPerk`; registry ID **`ars_nouveau:thread_feather`** [perk] [registry].

Thread passivo de mitigação de dano de queda. O Thread escreve um atributo; o evento de dano lê o valor efetivo desse atributo, não o slot diretamente [perk] [damage].

## Contrato individual para perks

| Campo | Evidência e limites do contrato |
|---|---|
| Identidade e versão | Thread registrado por APIRegistry na registry de perks, classe FeatherPerk, ID `ars_nouveau:thread_feather`, Ars Nouveau 5.13.1. Slot mínimo **ONE**, valor 1 herdado de IPerk; não é tier de glyph ou nível de spell [registry] [contract] [slots]. |
| Comportamento e causalidade | `FeatherPerk.applyAttributeModifiers` retorna modifiers com `PerkAttributes.FEATHER`. `AnimatedMagicArmor.getDefaultAttributeModifiers` encadeia esse retorno por instância e EquipmentSlotGroup do armor. `EventHandler.entityHurt(LivingDamageEvent.Pre)` lê FEATHER por `PerkUtil.valueOrZero` e modifica o DamageContainer existente quando a fonte é exatamente `DamageTypes.FALL` [perk] [armor] [damage] [value]. |
| Parâmetros e scaling | Por instância: amount=`0,2*slotValue`, operação `ADD_VALUE`, modifier ID **ars_nouveau:thread_feather**. Slots nativos 1/2/3 fornecem0,2/0,4/0,6 ao modifier do item. O atributo `PerkAttributes.FEATHER` é um RangedAttribute sincronizável declarado com default0, mínimo0 e máximo1; esse intervalo é do atributo, não um cap separado por item. No handler, com A=amount no ponto de execução e F=valor efetivo, `A←A−A*F` para FALL; depois `container.setNewDamage(max(0,A))` [perk] [attribute] [damage]. |
| Targeting, geometria e resultado | A vítima do evento de dano que possui o atributo. Ars adiciona seus PerkAttributes ao tipo PLAYER no evento de atributos; `valueOrZero` devolve0 se a entidade não tiver esse atributo. Sem alvo, raio, projétil ou duração próprios. O teste é DamageTypes.FALL, não toda fonte customizada com aparência de queda. O método não tem guard de lado local; execução final pertence ao pipeline do evento [attribute] [value] [damage]. |
| Custos, aquisição e gates | `ars_nouveau:blank_thread` como reagent; `#c:feathers`×4 e `ars_nouveau:abjuration_essence`×2 nos pedestais. Resultado 1 `thread_feather`, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação exige slot disponível e `validForSlot`; AlterationTile retira 1 Thread por split, inicia timer 40 quando necessário e grava o componente ao retirar a armadura [install]. Sem mana por cast, Source contínuo, XP de aprendizagem de glyph ou cooldown autônomos demonstrados neste perk passivo. |
| API, autoridade e integração | IPerk expõe applyAttributeModifiers e validForSlot; a leitura de equipamento/atributo/mixin é provider-native. Minimum slot não homologa um bridge RPG. Ars governa slots, atributos, inventário e efeitos; RPG Skill Tree governa progressão por contrato; Black Arcana conserva casting, Corruption, Strain e WorldEffectPolicy próprios. `mutating_hook=NOT_VERIFIED`: não duplicar o resultado por inspeção do Thread [contract] [armor]. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Fonte imutável e release SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; o SHA identifica o publisher `ars_nouveau-1.21.1-5.13.1.jar`, não prova a registry/classfile deste Thread ou paridade integral de métodos. A auditoria existente de 109 IDs cobre glyphs/rituais; não cobre Threads. Config instalada, outros mods/listeners e execução física: `physical_qa=NOT_TESTED`. |

## Consumidores, slots e persistência

Para perks futuras, ler o atributo efetivo evita reconstruir percentuais a partir de peças. A quantidade atual do DamageContainer já pode refletir amplificações/reduções anteriores no próprio handler; a mitigação não é uma porcentagem isolada de um dano original imutável. Interceptar novamente o mesmo evento no RPG/Black Arcana pode duplicar a redução. O handler atualiza a transação recebida; não emite um novo golpe nem cancela o evento como prova de imunidade [damage].

O listener aplica primeiro os ajustes de Shocked/Hex e Defence/Warding, depois Feather e o clamp final. A ordem de outros listeners e as regras de duplicate IDs na composição de atributos não foram reproduzidas em jogo; somar percentuais de várias peças não é uma garantia de stacking [damage].

`IPerkHolder.getPerkInstances` associa perks aos slots disponíveis por índice; `ArmorPerkHolder.getSlotsForTier` busca o provider de slots e ordena os valores em ordem decrescente. O layout depende do item/tier, descrito em [perk-slot-providers](../systems/perk-slot-providers.md). Este Thread não sobrescreve minimumSlot nem getInitTag: mínimo 1 e ausência de tag própria são os defaults inspecionados [instances] [holder] [contract]. Não inferir que toda armadura de outro mod execute o caminho de AnimatedMagicArmor.

`ARMOR_PERKS` é registrado como componente persistente com ArmorPerkHolder.CODEC; o holder serializa color/perks/tier/perkTags. Nos caminhos que usam `countForPerk`, a seleção max-slot é recalculada pelo PerkUtil ao ler os armor slots; os modifiers de atributos usam o slot local passado pelo armor. Persistir o Thread não é persistir um cast, um cooldown ou uma prova de aplicação física do atributo [persistence] [holder-codec] [maximum]. Não creditar ticks, chamadas do mixin ou eventos de queda como novos casts/Mastery.

**Invalidação:** mudança de release/source, receitas, slots, atributos, mixins, listeners ou composição de equipamento exige reauditoria. Este documento não implementa perks, não promove Stage e não certifica todo o provider.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[contract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L24-L74
[slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L12-L35
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L49-L72
[maximum]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L60-L81
[armor]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L112-L125
[install]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L99-L150
[persistence]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L25-L25
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/FeatherPerk.java#L13-L34
[attribute]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L23-L54
[damage]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java#L259-L300
[value]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L26-L33
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_feather.json#L1-L32
[holder-codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L31
