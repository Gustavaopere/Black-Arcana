# Ars Nouveau — Blank Thread / Empty Perk

**Estado: contrato técnico estático documentado**, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

| Campo | Contrato e limites verificados no source |
|---|---|
| Identidade e versão | `ars_nouveau:blank_thread`, `com.hollingsworth.arsnouveau.common.perk.EmptyPerk`, Ars Nouveau **5.13.1**. A registry registra a instância; ItemsRegistry cria seu PerkItem e o atribui a BLANK_THREAD [empty] [registry] [item-registry]. Não é glyph ou familiar. |
| Comportamento e causalidade | Entrada vazia e reagent de fabricação. EmptyPerk só especializa nome/descrição; os defaults de IPerk devolvem modifiers sem alterações, sem onAdded/onRemoved próprios ou getInitTag próprio [empty] [contract] [defaults]. Nenhum dano, cura, projétil ou status é aplicado por essa classe. |
| Parâmetros e limites | `minimumSlot()` herdado **ONE=1**; `validForSlot` compara o mínimo com o valor do slot, sem preço de cast [contract] [slot]. Não possui scalar, raio, duração ou atributo próprios. O tier do holder e o valor do slot não são XP/tier de glyph. |
| Targeting e lifecycle | Sem alvo, hitbox, LOS, área, cooldown ou duração autônomos. Caso usado no caminho genérico da AlterationTile, o PerkItem entra na lista de Threads: não há veto específico a EmptyPerk; ocupa uma posição e `stack.split(1)` transfere1 item. O limite é3 e a capacidade do provider de slots [alteration]. No-op não significa slot disponível ilimitado. |
| Custos e aquisição | Shaped `xxx / yyy / xxx`: **6×magebloom_fiber +3×#c:nuggets/gold →1 Blank Thread** [recipe] [recipe-json]. Crafting, sem taxa própria de Source ou mana e sem XP de aprendizagem de glyph. É reagent das receitas de Threads especializadas; custos dessas receitas pertencem aos respectivos objetos. |
| APIs e autoridade | Ars mantém Threads, slots, atributos e seus consumidores. `IPerk.applyAttributeModifiers` é uma API real e devolve modifiers novos; o caminho de armadura atribui o retorno a cada instância [contract] [armor]. Acesso nativo não certifica uma bridge segura de RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. RPG mantém progressão por contrato; Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém sistemas ambientais. Não repetir o resultado nem criar Mastery/cast pago por chamada do consumidor. A [matriz de slots](../systems/perk-slot-providers.md) é uma autoridade distinta da entrada vazia; não usar Blank como unlock, remoção ou regra de progressão inventada. |
| Evidência e validação | `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; release **5.13.1**, publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. O SHA identifica a release; os109 IDs compilados de glyphs/rituais **não cobrem Threads**, nem provam equivalência dos métodos desta ficha. Config instalada, equipamentos/addons, execução física e listeners externos não foram testados: `physical_qa=NOT_TESTED`. |

## Armazenamento e no-op comprovado

O componente `ARMOR_PERKS` usa codec persistente de ArmorPerkHolder; o holder serializa lista de perks, tier e perkTags [component] [holder]. Slots são ordenados por valor decrescente e associados à lista por índice [slots] [instances]. EmptyPerk não cria tag de carga, timestamp ou contador próprios. Alterar um holder por setter devolve outro objeto; não se deve presumir gravação no ItemStack apenas por construir uma instância.

`StackPerkHolder.PERK_CODEC` resolve IDs desconhecidos com fallback **StarbunclePerk**, não EmptyPerk [codec]. Portanto Blank não é uma sentinela de recuperação universal de dados inválidos, e uma migração não deve substituir qualquer perk desconhecida por Blank sem contrato.


**Invalidação:** mudança de release, source, receita, slots, equipamento, atributo, listener ou consumidor exige reauditoria. Nenhum hook executável foi implementado nesta ficha.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[item-registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ItemsRegistry.java#L281-L287
[contract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L24-L74
[slot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L18-L36
[armor]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L112-L125
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L16-L21
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L54-L62
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L23-L27
[empty]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/EmptyPerk.java#L8-L29
[defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L95-L103
[alteration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L123-L151
[codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/StackPerkHolder.java#L20-L37
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/RecipeDatagen.java#L660-L665
[recipe-json]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/blank_thread.json#L1-L21
