# Ars Nouveau — Item Pickup

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_pickup`
- Display name: Item Pickup
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: AOE

## Provider-native behavior

Item Pickup collects nearby `ItemEntity` instances into the caster inventory manager and can collect experience orbs for a real player caster. The source uses NeoForge item/XP pickup events and removes pickup delay before insertion. Search radius is `2 + AOE multiplier` around the resolved location.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:hopper` ×2.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this remote pickup/inventory insertion path. Black Arcana must not double-insert items, duplicate XP award, or bypass pickup events when Ars owns the causal spell.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectPickup`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectPickup.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPickup.java) do Ars 5.13.1.
- **Geometria:** `onResolve` calcula `expansion=2+getAoeMultiplier()` e coleta entidades numa AABB centrada no BlockPos do hit (não raio esférico). Obtém `InventoryManager` do caster com `extractSlotMax(-1)`.
- **Itens:** para cada `ItemEntity` zera pickup delay; publica `ItemEntityPickupEvent.Pre(player,item)`, respeita `pre.canPickup().isFalse()`, tenta `manager.insertStack(stack)` e substitui stack residual no mundo, depois publica `ItemEntityPickupEvent.Post`. Esse Post não garante quantidade inserida nem aquisição integral; pickups cancelados não são equivalentes a Mana refunds.
- **XP:** percorre `ExperienceOrb` na mesma AABB e só dá experiência se shooter é `Player` real e `spellContext.castingTile==null`; publica `PlayerXpEvent.PickupXp` cancelável antes de `giveExperiencePoints(orb.value)` e `remove(DISCARDED)`.
- **Perks:** não reemitir eventos do NeoForge nem recolher o mesmo stack/XP novamente; Mastery por cast não deve usar número de orbs como contagem de casts.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.
