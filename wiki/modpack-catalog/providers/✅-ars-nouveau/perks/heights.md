# Ars Nouveau — Heights

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Release **5.13.1**, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Classe `com.hollingsworth.arsnouveau.common.perk.JumpHeightPerk`; registry ID **`ars_nouveau:thread_heights`** [perk] [registry].

Thread passivo com dois consumidores: potência de salto e distância de queda registrada no evento. Ambos usam **o maior slot equipado** obtido por `PerkUtil.countForPerk`, não número de cópias nem soma de slots [maximum].

## Contrato individual para perks

| Campo | Evidência e limites do contrato |
|---|---|
| Identidade e versão | Thread registrado por APIRegistry na registry de perks, classe JumpHeightPerk, ID `ars_nouveau:thread_heights`, Ars Nouveau 5.13.1. Slot mínimo **ONE**, valor 1 herdado de IPerk; não é tier de glyph ou nível de spell [registry] [contract] [slots]. |
| Comportamento e causalidade | `JumpHeightPerk` fornece identidade/descrição, sem override de modifier próprio. `PerkLivingEntity.getJumpPower` injeta no RETURN de `LivingEntity.getJumpBoostPower` e soma ao retorno. `EventHandler.fallEvent(LivingFallEvent)` reduz separadamente a distância do evento. São fases distintas da engine, não um spell de movimento com cast [perk] [jump] [fall]. |
| Parâmetros e scaling | Com `m=max(slot.value)` das ocorrências do Thread nas armaduras: retorno do jump boost=`retorno anterior +0,1f*m`; distância do LivingFallEvent=`distância anterior−m/0,1`, isto é, −10*m na unidade de distância de queda. Slots nativos 1/2/3 dão+0,1/+0,2/+0,3 de jump boost power e−10/−20/−30 na distância registrada. A primeira fórmula não equivale a uma altura final de salto em blocos. Não há clamp local em zero na subtração Heights [jump] [fall] [maximum]. |
| Targeting, geometria e resultado | A entidade vestindo o Thread, consultada no mixin e no evento LivingFallEvent, sem requisito Player nesses dois métodos. Nenhuma seleção de alvo, AOE, projétil, DamageType ou tempo de status próprios. O evento ajusta distância antes dos consumidores downstream de queda; não aplica dano/cura diretamente. Ambos os métodos não têm guard de lado local [jump] [fall]. |
| Custos, aquisição e gates | `ars_nouveau:blank_thread` como reagent; `minecraft:spider_eye`×1, `minecraft:rabbit_hide`×3 e `ars_nouveau:air_essence`×2. Resultado 1 `thread_heights`, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação exige slot disponível e `validForSlot`; AlterationTile retira 1 Thread por split, inicia timer 40 quando necessário e grava o componente ao retirar a armadura [install]. Sem mana por cast, Source contínuo, XP de aprendizagem de glyph ou cooldown autônomos demonstrados neste perk passivo. |
| API, autoridade e integração | IPerk expõe applyAttributeModifiers e validForSlot; a leitura de equipamento/atributo/mixin é provider-native. Minimum slot não homologa um bridge RPG. Ars governa slots, atributos, inventário e efeitos; RPG Skill Tree governa progressão por contrato; Black Arcana conserva casting, Corruption, Strain e WorldEffectPolicy próprios. `mutating_hook=NOT_VERIFIED`: não duplicar o resultado por inspeção do Thread [contract] [armor]. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Fonte imutável e release SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; o SHA identifica o publisher `ars_nouveau-1.21.1-5.13.1.jar`, não prova a registry/classfile deste Thread ou paridade integral de métodos. A auditoria existente de 109 IDs cobre glyphs/rituais; não cobre Threads. Config instalada, outros mods/listeners e execução física: `physical_qa=NOT_TESTED`. |

## Consumidores, slots e persistência

Uma perk de mobilidade precisa separar alteração de jump boost power, altura física final e distância usada para calcular queda. Alterar o max slot afeta os dois consumidores correlacionados. O ramo seguinte do mesmo fallEvent, condicionado ao Belt of Levitation, subtrai mais 6 e aplica `max(0,...)`; esse clamp não pertence ao ajuste isolado de Heights e pode modificar o valor negativo que Heights deixou [fall].

O Thread não implementa um atributo próprio de jump nem um novo LivingDamageEvent. Feather pode atuar depois no dano FALL enquanto Heights já atuou na distância; tratar os dois como um único percentual duplicaria ou perderia etapas. Mixin order, vanilla physics e outros mods continuam por validar [jump] [fall].

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/JumpHeightPerk.java#L7-L23
[jump]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/perks/PerkLivingEntity.java#L31-L35
[fall]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java#L302-L309
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_heights.json#L1-L32
[holder-codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L31
