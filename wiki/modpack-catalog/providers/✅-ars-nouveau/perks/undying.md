# Undying

- Registry ID: `ars_nouveau:thread_undying`
- Source class: `TotemPerk`
- Minimum slot: Tier 3 (`PerkSlot.THREE`).
- Initial persistent perk tag: `isActive=true`.
- Death trigger: `LivingDeathEvent` for a player with an active Undying holder.
- Provider response: set health to 1, remove all effects, then grant Regeneration 900 ticks amplifier 1, Absorption 100 ticks amplifier 1, Fire Resistance 800 ticks amplifier 0; broadcast entity event 35; set `isActive=false`; cancel death.
- Rearm: `SleepFinishedTimeEvent` sets `isActive=true` for players carrying the perk and persists the updated `ARMOR_PERKS` component.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Totem of Undying + Phantom Membrane + 2 Abjuration Essence; `sourceCost: 0`.
- Source da aquisição: [receita datagen](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeProvider.java#L1040-L1045); o [builder](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeBuilder.java#L24-L37) mantém `sourceCost` inteiro em0 quando a receita não fornece override.

## Authority / integration

Undying owns its death-cancellation charge, persistent armed state and sleep reset. Black Arcana death interception must never consume or recreate this charge, and competing death-prevention systems require deterministic ordering/deduplication rather than multiple resurrection settlements.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.

## Certificação técnica estática — Thread of Undying (2026-10-26)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Modlist física: `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [TotemPerk.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/TotemPerk.java#L10-L36), [PerkEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L158-L194), [PerkUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L60-L105), [ArmorPerkHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L16-L72). **A auditoria de 109 registros binários verifica glyphs e rituais, NÃO a identidade/binário dos perk classes.** Evidência classificada `PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`.

| Eixo de integração | Contrato observado |
|---|---|
| ID, tier e carga | `TotemPerk.INSTANCE` usa `ars_nouveau:thread_undying`; `minimumSlot()` retorna `PerkSlot.THREE`. `getInitTag()` cria `CompoundTag` com `isActive=true`. Isso é **estado de carga do perk**, não mana, cooldown do caster ou carga Black Arcana. |
| Death pipeline | `PerkEvents.totemEvent(LivingDeathEvent)` só prossegue para `Player`, busca `PerkUtil.getHolderForPerk(TotemPerk.INSTANCE,entity)` e exige `holder.getB().getTagForPerk` com `isActive=true`. Em sequência: `setHealth(1.0F)`, `removeAllEffects()`, aplica `REGENERATION` **900 ticks, amplifier1**, `ABSORPTION` **100 ticks, amplifier1**, `FIRE_RESISTANCE` **800 ticks, amplifier0**; `broadcastEntityEvent((byte)35)`; grava `isActive=false` no holder `DataComponentRegistry.ARMOR_PERKS` e `event.setCanceled(true)`. Cuidado com listeners concorrentes de morte e ordem de priorização: fonte não garante exclusividade de ressuscitação no modpack. |
| Rearm e holder | `PerkEvents.sleepEvent(SleepFinishedTimeEvent)` percorre `event.getLevel().players()`, reativa `isActive` nos holders existentes e regrava o componente de cada item; **não** exige que um player específico tenha efetivamente dormido no método examinado. `PerkUtil.getHolderForPerk` itera armor slots, atribuindo `selectedStack` e `highestHolder` a cada instância encontrada, sem condicionar a atribuição a `instance.getSlot().value()>maxCount`: apesar do nome, **o holder selecionado é o último correspondente iterado**, não necessariamente aquele com maior slot. Reequipamento/ordem de slots podem afetar a carga consumida. |
| Aquisição e orçamento | A ficha-base documenta Enchanting Apparatus com Totem of Undying/Phantom Membrane/2 Abjuration Essence e `sourceCost: 0` na receita, **distinto de custo/runtime de disparo**. Nenhum custo de mana no handler de death; a fonte não certifica custos de outros providers de death-safety. |
| Authority/causalidade | Ars controla o componente `ARMOR_PERKS`, a carga, os efeitos e a suspensão da morte. `WorldEffectPolicy` Black Arcana regula somente world effects próprios; Black Arcana não deve aplicar segundo Totem, consumir carga externamente ou premiar Mastery por um mesmo evento de death-prevention. RPG Skill Tree só atribui perks e gates via contrato efetivo. |

**QA pendente:** conflitos com Totem vanilla/outros mods, evento cancelado por outro handler, movimentação do item entre armor slots, player não-dorminte durante `SleepFinishedTimeEvent`, NBT/data component em restart/relog, morte em dimensão distinta e reentrância. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Não promover Stage 06.05/09.
