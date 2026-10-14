# Ars Nouveau — Interact

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_interact`
- Display name: Interact
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Sensitive, Amplify, Dampen
- Default augment limits: Sensitive 1, Amplify 1, Dampen 1

## Provider-native behavior

Interact emulates player interaction against blocks/entities. Sensitive selects off-hand interaction, Amplify switches block interaction to left-click/attack semantics, and Dampen performs shift-click semantics. Non-player/tile casting uses Ars' fake-player and inventory-manager path, including bucket handling and item return/drop behavior. Block use is denied by provider blacklist/claim checks before interaction.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:lever` + `#minecraft:wooden_pressure_plates` + `#minecraft:buttons`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this remote interaction/automation primitive. Black Arcana must not replay the interaction, duplicate inventory mutations or bypass provider/NeoForge interaction semantics when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInteract`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectInteract.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java) do Ars 5.13.1.
- **Natureza da invocação:** `onResolveEntity` chama `player.interactOn` no ramo não-Sensitive, e no Sensitive usa a mão definida por `getHand` (offhand de player real, main hand de `ANFakePlayer`) com `ItemStack.interactLivingEntity`/`Entity.interact`. `Dampen` temporariamente simula Shift/CROUCH e restaura flags após o uso.
- **Block path:** exige `BlockUtil.destroyRespectsClaim` na posição e rejeita `INTERACT_BLACKLIST`. `Amplify` usa `BlockState.attack(...)` em vez de `useItemOn`; no uso normal pode acionar block interaction, bucket pickup/empty, critérios e estatísticas vanilla. `Sensitive` escolhe offhand no player real. `Augment` Sensitive/Amplify/Dampen limit 1 cada.
- **Fake inventory:** para caster não-real `setupFakeInventory` obtém stack da `InventoryManager`, configura `ANFakePlayer`, executa ação e devolve os stacks ao manager/solta sobras. Alterar esses efeitos por perk pode duplicar ou perder itens e permissões; o evento geral de Effect não prova interação bem-sucedida.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.
