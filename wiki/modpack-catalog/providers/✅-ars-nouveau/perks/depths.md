# Ars Nouveau — Thread of Depths

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Release **5.13.1**, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Classe `com.hollingsworth.arsnouveau.common.perk.DepthsPerk`; registry ID **`ars_nouveau:thread_depths`** [perk] [registry].

Thread passivo de respiração e natação. O nome `countForPerk` não significa soma ou número de cópias: neste release ele devolve o **maior valor de slot** que contém este perk nas armaduras equipadas [maximum]. Esse máximo controla o ar; o modifier de natação usa o slot local de cada instância.

## Contrato individual para perks

| Campo | Evidência e limites do contrato |
|---|---|
| Identidade e versão | Thread registrado por APIRegistry na registry de perks, classe DepthsPerk, ID `ars_nouveau:thread_depths`, Ars Nouveau 5.13.1. Slot mínimo **ONE**, valor 1 herdado de IPerk; não é tier de glyph ou nível de spell [registry] [contract] [slots]. |
| Comportamento e causalidade | `PerkLivingEntity.decreaseAirSupply` injeta no HEAD de LivingEntity e, quando a condição passa, retorna `thisEntity.getAirSupply()`, preservando o ar atual e evitando o corpo original da chamada. `DepthsPerk.applyAttributeModifiers` é outro caminho: slot local≥3 adiciona Swim Speed; slots menores devolvem modifiers sem alteração [air] [perk]. |
| Parâmetros e scaling | Defina `m=max(slot.value)` das ocorrências equipadas e `r=nextDouble()`. Preserva ar se `m≥3` ou `r≤0,33m`. Slots máximos 1/2 correspondem ao limiar0,33/0,66 por chamada, não a duração garantida. Com m≥3 há short-circuit antes do RNG. A comparação literal usa≤, inclusive no caso m=0; não reescrevê-la como outra distribuição. Natação: `NeoForgeMod.SWIM_SPEED`, amount **2,0**, operação `ADD_VALUE`, modifier ID `ars_nouveau:thread_depths`, EquipmentSlotGroup fornecido pelo armor, somente se `slotValue≥3` [air] [perk]. |
| Targeting, geometria e resultado | A entidade que veste a armadura, consultada em cada chamada de diminuição de ar; sem seleção de terceiros, alcance, área, projétil, DamageType ou duração própria. Retorno é o ar atual da entidade, não necessariamente o argumento pCurrentAir modificado por outro injector. Sem guard local explícito de lado no mixin. Interação final com Respiration, outros mixins e Swim Speed depende do pipeline instalado [air]. |
| Custos, aquisição e gates | `ars_nouveau:blank_thread` como reagent; pedestais: `#minecraft:fishes`×3, `ars_nouveau:water_essence`×2, `minecraft:pufferfish`×1. Resultado 1 `thread_depths`, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação exige slot disponível e `validForSlot`; AlterationTile retira 1 Thread por split, inicia timer 40 quando necessário e grava o componente ao retirar a armadura [install]. Sem mana por cast, Source contínuo, XP de aprendizagem de glyph ou cooldown autônomos demonstrados neste perk passivo. |
| API, autoridade e integração | IPerk expõe applyAttributeModifiers e validForSlot; a leitura de equipamento/atributo/mixin é provider-native. Minimum slot não homologa um bridge RPG. Ars governa slots, atributos, inventário e efeitos; RPG Skill Tree governa progressão por contrato; Black Arcana conserva casting, Corruption, Strain e WorldEffectPolicy próprios. `mutating_hook=NOT_VERIFIED`: não duplicar o resultado por inspeção do Thread [contract] [armor]. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Fonte imutável e release SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; o SHA identifica o publisher `ars_nouveau-1.21.1-5.13.1.jar`, não prova a registry/classfile deste Thread ou paridade integral de métodos. A auditoria existente de 109 IDs cobre glyphs/rituais; não cobre Threads. Config instalada, outros mods/listeners e execução física: `physical_qa=NOT_TESTED`. |

## Consumidores, slots e persistência

Uma perk futura de fôlego precisa escolher qual receptor altera: máximo entre slots, limiar de RNG, retorno de ar ou atributo de natação. Somar cópias como se fossem o `m` usado pelo mixin altera a semântica. O Swim Speed+2 não é um multiplicador universal de velocidade nem prova de stacking entre peças com o mesmo modifier ID. Não existe cast adicional por tick de ar.

`getLangDescription` associa ausência de perda de ar a slot3; a execução chega a esse resultado pelo máximo equipado, enquanto a geração do modifier de natação continua local por instância. Não substituir essa distinção pelo texto do tooltip [perk] [maximum].

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/DepthsPerk.java#L13-L39
[air]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/perks/PerkLivingEntity.java#L22-L29
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_depths.json#L1-L32
[holder-codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L31
