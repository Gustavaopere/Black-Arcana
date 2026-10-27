# Ars Nouveau — Thread of High Step

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Release **5.13.1**, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Classe `com.hollingsworth.arsnouveau.common.perk.StepHeightPerk`; registry ID **`ars_nouveau:thread_high_step`** [perk] [registry].

Thread passivo que adiciona ao atributo nativo STEP_HEIGHT. É um modifier do item aplicado pelo caminho de armadura, não um teleport, impulso ou aumento direto de jump boost [perk] [armor].

## Contrato individual para perks

| Campo | Evidência e limites do contrato |
|---|---|
| Identidade e versão | Thread registrado por APIRegistry na registry de perks, classe StepHeightPerk, ID `ars_nouveau:thread_high_step`, Ars Nouveau 5.13.1. Slot mínimo **ONE**, valor 1 herdado de IPerk; não é tier de glyph ou nível de spell [registry] [contract] [slots]. |
| Comportamento e causalidade | `StepHeightPerk.applyAttributeModifiers` retorna `ItemAttributeModifiers` com `Attributes.STEP_HEIGHT`. O armor encadeia o resultado para cada PerkInstance, passando seu slot.value e o grupo do EquipmentSlot. A passagem desse retorno é necessária: o contrato de IPerk observa que withModifierAdded cria nova instância [perk] [armor] [contract]. |
| Parâmetros e scaling | amount=`slotValue`, operação **ADD_VALUE**, modifier ID **ars_nouveau:thread_high_step**, EquipmentSlotGroup recebido. Slots nativos 1/2/3 produzem+1/+2/+3 de contribuição para STEP_HEIGHT, somada segundo a engine ao valor base/outros modifiers; não fixam o atributo final em1/2/3. A constante UUID `46937d0b-123c-4786-95b5-748afd50f398` é declarada, mas o override auditado usa getRegistryName como ID efetivo; não usa esse UUID [perk]. |
| Targeting, geometria e resultado | Portador do equipamento no slot correspondente. STEP_HEIGHT é consumido pela movimentação/colisão vanilla; este Thread não faz raycast, procura blocos, executa setPos ou verifica uma altura/obstáculo específico. Sem alcance, área, projétil, DamageType ou duração próprios. Default/range da definição vanilla de STEP_HEIGHT não foram inferidos deste arquivo; geometria final depende da engine e do pack [perk] [armor]. |
| Custos, aquisição e gates | `ars_nouveau:blank_thread` como reagent e `ars_nouveau:air_essence`×3 nos pedestais. Resultado 1 `thread_high_step`, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação exige slot disponível e `validForSlot`; AlterationTile retira 1 Thread por split, inicia timer 40 quando necessário e grava o componente ao retirar a armadura [install]. Sem mana por cast, Source contínuo, XP de aprendizagem de glyph ou cooldown autônomos demonstrados neste perk passivo. |
| API, autoridade e integração | IPerk expõe applyAttributeModifiers e validForSlot; a leitura de equipamento/atributo/mixin é provider-native. Minimum slot não homologa um bridge RPG. Ars governa slots, atributos, inventário e efeitos; RPG Skill Tree governa progressão por contrato; Black Arcana conserva casting, Corruption, Strain e WorldEffectPolicy próprios. `mutating_hook=NOT_VERIFIED`: não duplicar o resultado por inspeção do Thread [contract] [armor]. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Fonte imutável e release SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; o SHA identifica o publisher `ars_nouveau-1.21.1-5.13.1.jar`, não prova a registry/classfile deste Thread ou paridade integral de métodos. A auditoria existente de 109 IDs cobre glyphs/rituais; não cobre Threads. Config instalada, outros mods/listeners e execução física: `physical_qa=NOT_TESTED`. |

## Consumidores, slots e persistência

O ponto comprovado para design é o modifier STEP_HEIGHT com amount e operação explícitos. Um bridge futuro deve preservar o EquipmentSlotGroup e resolver duplicate IDs/stacking da API em vez de somar um segundo aumento pelo RPG. Não apresentar a declaração do UUID legado como contrato de remoção: sua remoção teria que usar a identidade que o consumidor realmente aplica [perk] [armor].

Não há onAdded/onRemoved específico de High Step nem estado de cooldown no perk. O benefício passa pelo pipeline dos atributos de equipamento; o retorno à configuração sem o Thread depende da recomposição nativa dos modifiers, não de um timer desta classe. Testes de obstáculos, montagem, outros providers de Step Height e reload permanecem pendentes [perk] [contract].

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/StepHeightPerk.java#L15-L37
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_high_step.json#L1-L23
[holder-codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L31
