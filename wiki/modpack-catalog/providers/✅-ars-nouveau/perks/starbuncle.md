# Ars Nouveau — Thread of the Starbuncle

Status: `SOURCE-PINNED 5.13.1 / CONTRATO TÉCNICO ESTÁTICO / RUNTIME QA PENDING`

Perk passiva de velocidade de movimento. O valor do slot alimenta um modificador de atributo na armadura; não é um bônus por nível do jogador nem um proc de dano.

## Contrato individual para perks

| Campo | Contrato source-pinned e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_starbuncle`, `com.hollingsworth.arsnouveau.common.perk.StarbunclePerk`, Ars5.13.1; registrado em produção [registry]. MínimoONE herdado, slots nativos1/2/3 [slot] [slot-values]. Thread de armadura, distinto do familiar Starbuncle. |
| Comportamento e causalidade | `AnimatedMagicArmor.getDefaultAttributeModifiers` lê ARMOR_PERKS e chama `applyAttributeModifiers` para cada PerkInstance, reatribuindo o objeto retornado [armor-attributes]. `StarbunclePerk` devolve `modifiers.withModifierAdded` para `Attributes.MOVEMENT_SPEED`, com EquipmentSlotGroup recebido pelo caller [perk]. Não usa callbacks de dano/cast ou uma entidade adicional. |
| Parâmetros, identificador e operação | Amount **0.2*s**, onde s é valor do slot:0.2/0.4/0.6. Operação **ADD_MULTIPLIED_TOTAL**; id efetivamente passado ao AttributeModifier é `INSTANCE.getRegistryName()` (`ars_nouveau:thread_starbuncle`) [perk]. A constante UUID `46937d0b-123c-4786-95b5-748afd50f398` está declarada, mas não é usada nessa construção. Não converter amount diretamente em blocos/s ou soma final entre peças. |
| Targeting, duração e limites | Efeito no usuário conforme atributo/equipmentSlotGroup da peça; sem alvo adquirido, alcance, área, projétil, DamageType, duração em ticks ou cooldown próprios. O getter retorna modifiers para consumo da engine; não é chamada de setDeltaMovement. Default/faixa do atributo vanilla e regra final de colisão/empilhamento de ids não foram inspecionados neste recorte; o código não aplica clamp local ao amount [perk] [armor-attributes]. |
| Custos, aquisição e gates | Apparatus: Blank Thread; Starbuncle Shards×3, Sugar×3, Manipulation Essence×2; resultado1, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação tem slot disponível, mínimoONE e consome1 Thread por `split(1)` [install]. Perk passiva sem mana, XP de glyph ou custo por passo nesta classe; equipamento e receita continuam autoridades Ars. |
| API, persistência e integração | `IPerk.applyAttributeModifiers` é uma API nativa real; o caller reatribui a lista retornada, exigência distinta de mutar um evento [armor-attributes]. O holder serializa perks/tier/perkTags e seus slots são determinados pelo provider [component] [armor-slots]. O aviso de duplicatas em troca de equipamento não remove automaticamente entradas do componente [equipment]. Não aplicar novamente +20% ao detectar o mesmo modifier numa bridge RPG/Black Arcana. |
| Validação e condições | Source/receita conferidos, com release SHA apenas como proveniência. A aditividade entre cópias, limites finais de MOVEMENT_SPEED, impacto sobre movimento real e addons exigem prova da engine/config/cliente; nenhuma classe compilada deste Thread foi certificada pelo audit109. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Codec e definição de uma perk nova

`StackPerkHolder.PERK_CODEC` resolve o registry id e usa `StarbunclePerk.INSTANCE` como fallback quando o id não é encontrado [codec-fallback]. Isso é um comportamento de decode; não cria um novo registro nem demonstra que qualquer item inválido foi aceito no modpack. Uma migração/bridge precisa preservar ids e não confundir um fallback com a intenção original do equipamento.

A área semântica já ocupada é velocidade multiplicativa passiva por slot de armadura. Uma magia original de movimento com duração, trajetória ou custo próprios precisaria manter sua própria causalidade e não contabilizar o atributo equipado como cast ou impulso adicional.

A [matriz de providers de slots](../systems/perk-slot-providers.md) localiza as peças e layouts suportados; a [visão dos Threads](README.md) mantém o inventário de aquisição.

## Evidência e fronteira de integração

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`: proveniência da release, sem prova específica de registry/classfile ou equivalência de métodos deste Thread. A auditoria binária dos109 IDs cobre glyphs e rituais, não Threads.

O Ars conserva equipamentos, slots, atributos, eventos e recursos nativos. RPG Skill Tree governa progressão/perks apenas por contrato comprovado; Black Arcana conserva casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded conserva seus sistemas ambientais. APIs existentes não equivalem a um adapter seguro para alterar este comportamento ou premiar cada evento/tick como cast novo. Não duplicar efeitos, mana ou crédito de Mastery ao observar o mesmo caminho. Config instalada, addons, ordem de listeners, cliente/servidor, persistência física e integração executável continuam pendentes. Mudança de source, JAR, receita, equipamento ou consumidores exige reauditoria.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[slot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L52-L75
[slot-values]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L29-L36
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[armor-slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L54-L62
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L50-L81
[equipment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L38-L85
[install]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L123-L150
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L26
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/StarbunclePerk.java#L15-L35
[armor-attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L112-L125
[codec-fallback]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/StackPerkHolder.java#L20-L36
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_starbuncle.json#L1-L38
