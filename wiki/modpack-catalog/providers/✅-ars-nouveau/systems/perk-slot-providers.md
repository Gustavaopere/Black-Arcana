# Ars Nouveau — Armor Perk Slot Providers

State: `SOURCE-PINNED 5.13.1 / 12 PROVIDERS VERIFIED`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

`PerkRegistry.registerPerkProvider(...)` defines the allowed perk-slot topology for Ars armor. The lists below are provider data, not RPG Skill Tree nodes. Slot values are Ars' `PerkSlot.ONE/TWO/THREE` = 1/2/3.

The three nested lists registered per armor item correspond to that item's perk-holder tiers 0/1/2; the item UI/code presents armor tier as `perkHolder.getTier() + 1`, so this page labels them Armor Tier 1/2/3.

| Provider item constant | Armor Tier 1 | Armor Tier 2 | Armor Tier 3 |
|---|---|---|---|
| `BATTLEMAGE_BOOTS` | `[1]` | `[1,1]` | `[1,1,2]` |
| `BATTLEMAGE_HOOD` | `[1]` | `[1,1]` | `[1,1,2]` |
| `BATTLEMAGE_LEGGINGS` | `[1]` | `[1,2]` | `[1,1,3]` |
| `BATTLEMAGE_ROBES` | `[1]` | `[1,2]` | `[1,1,3]` |
| `ARCANIST_HOOD` | `[1]` | `[1,2]` | `[1,1,3]` |
| `ARCANIST_BOOTS` | `[1]` | `[1,2]` | `[1,2,2]` |
| `ARCANIST_LEGGINGS` | `[1]` | `[1,3]` | `[1,2,3]` |
| `ARCANIST_ROBES` | `[1]` | `[1,3]` | `[1,2,3]` |
| `SORCERER_BOOTS` | `[1]` | `[1,2]` | `[1,2,3]` |
| `SORCERER_ROBES` | `[2]` | `[2,3]` | `[2,2,3]` |
| `SORCERER_LEGGINGS` | `[2]` | `[2,3]` | `[2,2,3]` |
| `SORCERER_HOOD` | `[1]` | `[1,2]` | `[1,2,3]` |

## Perk application semantics

`AnimatedMagicArmor#getDefaultAttributeModifiers` walks the perk instances stored in the armor's `ARMOR_PERKS` component and calls each perk's `applyAttributeModifiers(..., instance.getSlot().value(), EquipmentSlotGroup.bySlot(...))`. It then also adds Ars-owned armor-derived `MAX_MANA` and `MANA_REGEN_BONUS` attributes based on armor tier.

The server-side equipped-armor tick also invokes `ITickablePerk.tick(...)` for tickable perks and calls `RepairingPerk.attemptRepair(...)`.

## Deduplication / authority

- Slot topology belongs to Ars Nouveau.
- A Tier-3 Ars perk slot is **not** equivalent to an RPG Skill Tree perk tier.
- RPG Skill Tree may only gate/provide progression through a real bridge; it must not rewrite `ARMOR_PERKS`, reinterpret slot values or duplicate Ars attribute modifiers.
- Black Arcana must observe provider-native outcomes rather than replaying Thread logic.
- External armor/perk integrations must preserve item identity and event causality; fail closed if a safe API boundary cannot be verified.

## Auditoria de engenharia — slot providers (2026-10-26; PR independente)

**⚠️ Revisão do source concluída; certificação no manifesto pendente.** JAR físico `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. A auditoria compilada de **109 glyphs/rituais não certifica automaticamente armor slot providers**. Links: [APIRegistry.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java), [PerkRegistry.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/PerkRegistry.java), [PerkSlot.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java), [ArmorPerkHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java), [StackPerkHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/StackPerkHolder.java), [AnimatedMagicArmor.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java), [PerkUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java).

| Dimensão | Contrato observado e impacto em perks |
|---|---|
| **Registry e 12 providers** | `APIRegistry` registra os doze `BATTLEMAGE_*`, `ARCANIST_*`, `SORCERER_*` por `PerkRegistry.registerPerkProvider(ItemLike,List<List<PerkSlot>>)`. `PerkRegistry.itemPerkProviderMap` é `ConcurrentHashMap<Item,List<List<PerkSlot>>>`. `getPerkProvider(ItemStack)` retorna a topologia cadastrada para o **Item**, sem aplicar gates RPG externamente. `registerPerkProvider` faz `put` e sempre retorna `true`, sem validação de conflito nesta classe. Isso **não autoriza sobrescrever** os mapas estáticos Ars como técnica de integração. |
| **Slot, armor tier e compatibilidade** | `PerkSlot.ONE/TWO/THREE` têm `value()=1/2/3` e IDs `ars_nouveau:one/two/three`. `ArmorPerkHolder.getSlotsForTier(stack)` procura `getPerkProvider(stack)`; se nulo, retorna lista vazia. Quando existe provider, usa `slotsForTier.get(getTier())` e ordena cópia por `Comparator.comparingInt((a)->-a.value())`, **ordem descendente**. O acesso a `getTier()` **não faz bounds check explícito** no método. `ArmorPerkHolder` persiste `color/perks/tier/perkTags` no data-component, separado de uma árvore de habilidades. |
| **Atributos por equipamento** | `AnimatedMagicArmor.getDefaultAttributeModifiers` percorre `getPerkInstances(stack)` e chama `perk.applyAttributeModifiers(...,instance.getSlot().value(),EquipmentSlotGroup.bySlot(...))`. Em seguida, para cada peça, adiciona `PerkAttributes.MAX_MANA` `30*(perkHolder.getTier()+1)` e `PerkAttributes.MANA_REGEN_BONUS` `perkHolder.getTier()+1`, ambos `ADD_VALUE` por slot de armadura. Esse bônus inato do equipamento **não é** o valor de Thread Magic Capacity e não deve ser contabilizado duas vezes. |
| **Equipamento e lifecycle** | `PerkEvents.equipmentChangedEvent` reage a `LivingEquipmentChangeEvent`, considera apenas `EquipmentSlot.Type.HUMANOID_ARMOR`, compara instâncias antigas/novas, remove duplicatas de `toPerks` em relação a perks já vestidas e calcula `removedPerks/addedPerks` como conjuntos para hooks `onRemoved/onAdded`. `PerkUtil.getPerksFromLiving` pode retornar várias instâncias de uma perk; `countForPerk` calcula **máximo** do `PerkSlot.value()`, não soma; `getHolderForPerk` seleciona a última entrada encontrada em iteração, não necessariamente a de maior slot. |
| **Fonte de risco** | Tier de armor `0/1/2` é índice da lista; Thread slot `ONE/TWO/THREE` é valor `1/2/3`, e RPG Skill Tree tier é outra dimensão. Um tier inválido ou mods que registrem providers externos exigem validação antes de chamar `getSlotsForTier`. Componente `ARMOR_PERKS` e atributos são mutados pelo Ars; `WorldEffectPolicy` do Black Arcana é autoridade apenas de world effects próprios, não desses item components. |

**QA/segurança:** validar com todos os 12 itens reais e slots, compatibilidade com addons de armaduras, remoção/adição de Threads repetidas, interação do `UNBREAKING`, slot out-of-bounds de NBT antigo, ordenação das instâncias e stacking de atributos. Sem hooks mutadores comprovados: `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; nenhum Stage 06.05/09 promovido. A ficha permanece ⚠️ no índice até a certificação reconciliada com o manifesto e as PRs paralelas.
