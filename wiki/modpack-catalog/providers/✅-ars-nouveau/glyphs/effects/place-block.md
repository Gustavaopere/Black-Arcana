# Ars Nouveau — Place Block

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_place_block`
- Display name: Place Block
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: AOE, Pierce, Randomize, Sensitive
- Default Sensitive limit: 2

## Provider-native behavior

Place Block consumes a block item through the Ars inventory manager and places it using a fake-player placement context. AOE/Pierce expand target coverage; Randomize chooses among eligible block items; Sensitive changes placement facing, and two Sensitive augments invert that facing. NeoForge `BlockEvent.EntityPlaceEvent` is posted before placement.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dispenser`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns the inventory extraction and placement transaction for this spell. Black Arcana must not duplicate block consumption/placement or bypass placement/protection events. Independent Black Arcana block placement remains subject to its own `WorldEffectPolicy`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectPlaceBlock`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectPlaceBlock.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPlaceBlock.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectPlaceBlock` no Ars 5.13.1, método `onResolveBlock`.
- **Geometria e proteção:** `SpellUtil.calcAOEBlocks`, world bounds, replaceable, e publicação de `BlockEvent.EntityPlaceEvent` via `NeoForge.EVENT_BUS`; evento cancelado impede tentativa. Em entity hit converte para block hit abaixo do alvo. **Orientação:** Sensitive count 1 reposiciona `ANFakePlayer` pelo caster; count >1 espelha facing, limit default 2. **Inventário:** `InventoryManager.extractItem` ou `extractRandomItem` com Randomize extrai **1 BlockItem por posição elegível**; `attemptPlace` delega `BlockItem.place` e `ExtractedStack.returnOrDrop` devolve sobra. **Propagação:** `ShapersFocus.tryPropagateBlockSpell` apenas quando tentativa não retorna `InteractionResult.FAIL`. **Perks:** não duplicar placement/item count e não contornar evento de proteção.
- **Limite de integração:** ✅ source pin da lógica local, ⚠️ execução auxiliares/config dependem do provider real; ⛔ hook externo de mutação não comprovado. Black Arcana só governa suas world mutations; RPG Skill Tree depende de bridge real. QA Survival PENDING.
