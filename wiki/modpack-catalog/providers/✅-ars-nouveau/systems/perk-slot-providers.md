# Ars Nouveau — providers e topologia de slots de armadura

**Estado:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.

Fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**. JAR de referência `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Grau `PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`: source imutável e proveniência da release; os109 IDs compilados de glyphs/rituais não provam a identidade ou os corpos binários deste sistema. Esta ficha agrega contratos, sem criar um glyph, Thread ou registry ID autônomo.

## Identidade e superfícies nativas

Sistema agregado de `com.hollingsworth.arsnouveau.api.registry.PerkRegistry`, `api.perk.IPerkHolder`, `common.items.data.ArmorPerkHolder`, `common.block.tile.AlterationTile` e `common.armor.AnimatedMagicArmor`. O componente persistente é `DataComponentRegistry.ARMOR_PERKS` (`ars_nouveau:armor_perks`); sua identidade não é a de uma magia. Os doze registros de [APIRegistry.postInit][providers] são defaults do source, não doze nodes do RPG Skill Tree.

| Campo de certificação | Contrato estático e limite |
|---|---|
| Identidade e versão | PerkRegistry associa **Item → listas de PerkSlot por tier**; ARMOR_PERKS serializa ArmorPerkHolder. Fonte5.13.1 pinada; sem prova binária específica desses registries/codecs. |
| Comportamento e causalidade | Tabela de provider → tier do holder → slots ordenados → pares slot/perk → atributos, ticks e listeners. Aplicação na AlterationTile tem seus próprios gates e writes de componente. |
| Parâmetros e caps | Doze providers, três tiers declarados por item, até três slots nessas tabelas; valores1/2/3 distintos de tier de glyph. getSlotsForTier ordena por valor **decrescente** e indexa tier diretamente, sem clamp local. |
| Targeting e resultado | Atua em ItemStack/equipamento e entidade portadora; sem projétil, raio, dano ou duração globais. Cada Thread define o consumidor; distância e dano não pertencem à topologia de slots. |
| Custos e aquisição | Instalação usa um Thread por split(1); upgrade de tier declara2500/5000 Source e ingredientes próprios. Não há mana/XP de glyph nem cooldown de cast desse sistema. |
| API e integração | registerPerkProvider/getPerkProvider, holders e componentes são APIs reais. Alterar uma lista/tier ou componente não equivale a instalação segura, atualização de atributos ou preservação de estado por adapter RPG/Black Arcana. |
| Evidência e validação | Source imutável + SHA da release, sete campos documentados; hooks mutadores NOT_VERIFIED e QA físico NOT_TESTED. Certifica o contrato desta ficha, não todo o universo de itens/perks integráveis. |

## Topologia declarada por item

[PerkSlot][slots] declara ONE/TWO/THREE com valores1/2/3. As colunas abaixo reproduzem a **ordem declarada** das listas de [APIRegistry][providers]. O holder tem tier0/1/2, apresentado na UI como tier1/2/3; a execução ordena os slots antes de associar perks.

| Provider item constant | Armor Tier1 (índice0) | Armor Tier2 (índice1) | Armor Tier3 (índice2) |
|---|---|---|---|
| BATTLEMAGE_BOOTS | [1] | [1,1] | [1,1,2] |
| BATTLEMAGE_HOOD | [1] | [1,1] | [1,1,2] |
| BATTLEMAGE_LEGGINGS | [1] | [1,2] | [1,1,3] |
| BATTLEMAGE_ROBES | [1] | [1,2] | [1,1,3] |
| ARCANIST_HOOD | [1] | [1,2] | [1,1,3] |
| ARCANIST_BOOTS | [1] | [1,2] | [1,2,2] |
| ARCANIST_LEGGINGS | [1] | [1,3] | [1,2,3] |
| ARCANIST_ROBES | [1] | [1,3] | [1,2,3] |
| SORCERER_BOOTS | [1] | [1,2] | [1,2,3] |
| SORCERER_ROBES | [2] | [2,3] | [2,2,3] |
| SORCERER_LEGGINGS | [2] | [2,3] | [2,2,3] |
| SORCERER_HOOD | [1] | [1,2] | [1,2,3] |

`PerkRegistry.registerPerkProvider` faz put no mapa e devolve true, sem validar a topologia [registry]. O retorno de `getPerkProvider` pode ser null. `ArmorPerkHolder.getSlotsForTier` retorna lista vazia sem provider; com provider usa `slotsForTier.get(getTier())`, copia e ordena por `-value` [holder]. Um tier externo inválido não recebe clamp nessa função.

[IPerkHolder.getPerkInstances][pairing] associa cada slot ordenado ao perk de mesmo índice, até o limite de slots e de perks disponíveis. Exemplo: a lista declarada [1,1,2] vira [2,1,1]; o primeiro perk armazenado recebe slot2. Este pareamento não verifica minimumSlot nem rejeita duplicatas por si só. `IPerk.validForSlot` compara o slot ao mínimo (defaultONE); Totem/Gliding e extensões podem ter regras próprias [minimum].

## Instalação, tier, atributos e persistência

[AlterationTile][alteration] separa armadura e Threads ao colocar o item. `addPerkStack` rejeita holder ausente, tamanho já≥3 ou capacidade esgotada; consulta o próximo slot ordenado e `perk.validForSlot`, então usa `stack.split(1)`. O timer40 é animação/client tick, não cooldown mecânico de cast [alteration-save]. Não presumir aplicação gratuita em creative por analogia com outras classes: esse split não tem um guard creative local.

Ao retirar a armadura, `removeArmorStack` cria um **novo mapa** de perkTags. Só coloca getInitTag quando o perk não tinha tag no holder anterior; depois usa `setPerkTags(perkTags)` no componente da cópia. O caminho não copia indiscriminadamente as tags anteriores; portanto alteração não comprova preservação de carga/cooldown/estado de cada Thread. `setArmorStack` também limpa a lista de perks na stack recebida antes de copiá-la. As operações não são uma transação genérica para o RPG reaplicar.

[ArmorPerkHolder.CODEC][holder] serializa color/perks/tier/perkTags. O codec de perks e [PerkMap][tags] usam StarbunclePerk como fallback para ID desconhecido; não tratar dado legado inválido como Blank seguro. Setters criam holders novos, e o chamador deve escrever o componente no ItemStack. [DataComponentRegistry][component] marca ARMOR_PERKS como persistent; isso é uma declaração de serialização, não QA de save/reload em modpack.

[AnimatedMagicArmor][armor] chama `IPerk.applyAttributeModifiers` por `instance.getPerk()` para cada PerkInstance, no grupo do slot de equipamento. Acrescenta atributos ADD_VALUE: `MAX_MANA +=30*(holderTier+1)` com ID `max_mana_armor_<tipo>` e `MANA_REGEN_BONUS +=holderTier+1` com ID `mana_regen_armor_<tipo>`. Tier inválido não deve ser usado para extrapolar bônus sem revalidar holder/config. `inventoryTick` só executa a rotina de armadura nos índices `[Inventory.INVENTORY_SIZE, Inventory.INVENTORY_SIZE+4)`, servidor: tenta Repairing e depois cada ITickablePerk. Não aplicar ticks novamente em um adapter.

[PerkUtil][aggregation] distingue três medidas: lista de todas as instâncias de armor, `countForPerk` como **maior valor de slot** e `getHolderForPerk` como último matching holder iterado (atualiza maxCount, mas não o compara antes de reatribuir). [PerkEvents][events] também tem dispatch por instância e tratamento de equip/remove por sets; não há uma regra universal de soma ou deduplicação para todo Thread.

[ArmorUpgradeRecipe][upgrade] exige holder tier==destino−1, escreve novo tier em ARMOR_PERKS e devolve cópia. O datagen declara [first_armor_upgrade][upgrade-recipes] com dois blaze rods,2500 Source, tier1; second_armor_upgrade com dois ender pearls e chorus fruit,5000 Source, tier2. São valores de receita de mundo, sujeitos ao datapack e pipeline do Apparatus; não débito de mana do jogador ou XP/Mastery.

## Autoridade e validade

Ars Nouveau mantém composição, recursos, itens, atributos e dados do jogador. RPG Skill Tree governa sua progressão por contrato real; Black Arcana mantém casting, Corruption, Strain, WorldEffectPolicy e causalidade próprios; Enshrouded mantém seus sistemas ambientais. APIs nativas existem, mas um adapter que preserve fase, caps, custos, persistência e deduplicação não foi validado. Não duplicar cast, cobrança, XP ou Mastery por tick, refresh, item equipado ou alteração de metadados.

Mudança de source, JAR, config, receitas, listeners ou codecs exige reauditoria. Config instalada, compatibilidade de addons, multiplayer, cliente/servidor, reload e persistência física permanecem pendentes. Não houve alteração de runtime, implementação de bridge ou promoção de Stage.

[providers]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L202-L269
[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/PerkRegistry.java#L19-L49
[slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L18-L36
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L72
[pairing]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[stack-codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/StackPerkHolder.java#L20-L55
[tags]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/PerkMap.java#L15-L44
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L21-L28
[minimum]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L52-L74
[alteration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L75-L151
[alteration-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L165-L205
[armor]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L92-L134
[aggregation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L50-L105
[events]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L37-L95
[upgrade]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/ArmorUpgradeRecipe.java#L25-L69
[upgrade-recipes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeProvider.java#L911-L916

## Auditoria de engenharia — slot providers (checkpoint de 26/10/2026, reconciliado)

**No checkpoint de 26/10/2026, a revisão de source estava concluída e a certificação no manifesto pendente.** O contrato estático e as sete evidências atuais estão documentados acima; hooks mutadores e QA físico continuam pendentes. JAR físico `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. A auditoria compilada de **109 glyphs/rituais não certifica automaticamente armor slot providers**. Links: [APIRegistry.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java), [PerkRegistry.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/PerkRegistry.java), [PerkSlot.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java), [ArmorPerkHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java), [StackPerkHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/StackPerkHolder.java), [AnimatedMagicArmor.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java), [PerkUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java).

| Dimensão | Contrato observado e impacto em perks |
|---|---|
| **Registry e 12 providers** | `APIRegistry` registra os doze `BATTLEMAGE_*`, `ARCANIST_*`, `SORCERER_*` por `PerkRegistry.registerPerkProvider(ItemLike,List<List<PerkSlot>>)`. `PerkRegistry.itemPerkProviderMap` é `ConcurrentHashMap<Item,List<List<PerkSlot>>>`. `getPerkProvider(ItemStack)` retorna a topologia cadastrada para o **Item**, sem aplicar gates RPG externamente. `registerPerkProvider` faz `put` e sempre retorna `true`, sem validação de conflito nesta classe. Isso **não autoriza sobrescrever** os mapas estáticos Ars como técnica de integração. |
| **Slot, armor tier e compatibilidade** | `PerkSlot.ONE/TWO/THREE` têm `value()=1/2/3` e IDs `ars_nouveau:one/two/three`. `ArmorPerkHolder.getSlotsForTier(stack)` procura `getPerkProvider(stack)`; se nulo, retorna lista vazia. Quando existe provider, usa `slotsForTier.get(getTier())` e ordena cópia por `Comparator.comparingInt((a)->-a.value())`, **ordem descendente**. O acesso a `getTier()` **não faz bounds check explícito** no método. `ArmorPerkHolder` persiste `color/perks/tier/perkTags` no data-component, separado de uma árvore de habilidades. |
| **Atributos por equipamento** | `AnimatedMagicArmor.getDefaultAttributeModifiers` percorre `getPerkInstances(stack)` e chama `perk.applyAttributeModifiers(...,instance.getSlot().value(),EquipmentSlotGroup.bySlot(...))`. Em seguida, para cada peça, adiciona `PerkAttributes.MAX_MANA` `30*(perkHolder.getTier()+1)` e `PerkAttributes.MANA_REGEN_BONUS` `perkHolder.getTier()+1`, ambos `ADD_VALUE` por slot de armadura. Esse bônus inato do equipamento **não é** o valor de Thread Magic Capacity e não deve ser contabilizado duas vezes. |
| **Equipamento e lifecycle** | `PerkEvents.equipmentChangedEvent` reage a `LivingEquipmentChangeEvent`, considera apenas `EquipmentSlot.Type.HUMANOID_ARMOR`, compara instâncias antigas/novas, remove duplicatas de `toPerks` em relação a perks já vestidas e calcula `removedPerks/addedPerks` como conjuntos para hooks `onRemoved/onAdded`. `PerkUtil.getPerksFromLiving` pode retornar várias instâncias de uma perk; `countForPerk` calcula **máximo** do `PerkSlot.value()`, não soma; `getHolderForPerk` seleciona a última entrada encontrada em iteração, não necessariamente a de maior slot. |
| **Fonte de risco** | Tier de armor `0/1/2` é índice da lista; Thread slot `ONE/TWO/THREE` é valor `1/2/3`, e RPG Skill Tree tier é outra dimensão. Um tier inválido ou mods que registrem providers externos exigem validação antes de chamar `getSlotsForTier`. Componente `ARMOR_PERKS` e atributos são mutados pelo Ars; `WorldEffectPolicy` do Black Arcana é autoridade apenas de world effects próprios, não desses item components. |

**QA/segurança:** validar com todos os 12 itens reais e slots, compatibilidade com addons de armaduras, remoção/adição de Threads repetidas, interação do `UNBREAKING`, slot out-of-bounds de NBT antigo, ordenação das instâncias e stacking de atributos. Sem hooks mutadores comprovados: `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; nenhum Stage 06.05/09 promovido. A pendência de certificação desse checkpoint é reconciliada pelo contrato estático e pelo manifesto atual; as pendências de integração e QA física permanecem.
