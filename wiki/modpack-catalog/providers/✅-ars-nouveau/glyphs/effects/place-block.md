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

## Certificação técnica estática para perks — Place Block (2026-10-25)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** `ars_nouveau:glyph_place_block` ↔ `EffectPlaceBlock` no JAR publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`: binário comprova **identidade classe/ID**, não equivalência integral do método. Fonte imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectPlaceBlock.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPlaceBlock.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java), [InventoryManager.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java), [ExtractedStack.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/ExtractedStack.java).

| Campo relevante | Evidência técnica / limitação |
|---|---|
| Âncora geométrica | `onResolveBlock` obtém `SpellUtil.calcAOEBlocks(shooter,hitPos,hit,spellStats)`, usando `getAoeMultiplier()` e `count(AugmentPierce)` (largura `1+floor(AOE)`, altura `1+ceil(AOE)`, profundidade `1+Pierce` no overload). `world.isInWorldBounds(pos1)` é consultado **antes** de mudar a posição para `pos1.relative(hitDirection)` quando `!rayTraceResult.isInside()`; não existe segunda checagem explícita dos bounds depois dessa translação. |
| Alvo entidade e face | `onResolveEntity` transforma `EntityHitResult` em `BlockHitResult(entity.position, Direction.DOWN, entity.blockPosition().below(), true)` e usa o caminho de bloco. Para blocos, o hit normal pode deslocar a posição ao bloco adjacente; não tratar AOE como placement garantido no próprio bloco atingido. |
| Sensitive/orientação | `AugmentSensitive` count1 posiciona `ANFakePlayer` no `spellContext.getUnwrappedCaster().position`, e `count>1` reflete essa posição em relação ao `lookLoc`, com `fakePlayer.lookAt(...EYES,lookLoc)`. `attemptPlace` usa `getNearestViewDirection()` e `UnbiasedDirectionalPlaceContext`; default cap Sensitive=2. Isso é mudança de orientação/posicionamento, não aumento de alcance. |
| Gate e evento | Para cada posição, exige `BlockState.canBeReplaced()` e publica `BlockEvent.EntityPlaceEvent` via `NeoForge.EVENT_BUS.post`, criado com `BlockSnapshot` **antes da extração de item**; evento cancelado impede `place`. A validação de `world.isInWorldBounds` não é repetida após offset do hit. O callback de EntityPlaceEvent é uma barreira nativa do provider, **não** mutator externo certificado para perks. |
| Inventário e mutação | `spellContext.getCaster().getInvManager()` fornece `InventoryManager.extractItem` ou `extractRandomItem` (Randomize) de um `BlockItem`, **1 unidade por posição elegível**. Se `ExtractedStack.isEmpty()`, retorna sem place; caso contrário `attemptPlace` delega `BlockItem.place(context)`, obtém `InteractionResult`. `ShapersFocus.tryPropagateBlockSpell` ocorre se resultado **diferir de `InteractionResult.FAIL`**; isso não garante necessariamente confirmação de colocação em todos os consumers de `InteractionResult`. Sempre chama `extractItem.returnOrDrop(world,shooter.getOnPos())` para a sobra. |
| Liquidação/limites de perk | `returnOrDrop` é do provider e não constitui transação atômica certificada em face de callbacks de outros mods. Amplificar AOE/Pierce multiplica tentativas, extrações e events; nenhuma perk pode duplicar `BlockItem`, retornar outra cópia de inventário, reaplicar placement ou contar EntityPlaceEvent cancelado como sucesso. Default mana `getDefaultManaCost()=10`, sem prova de cooldown individual. `WorldEffectPolicy` governa colocação **própria** BA e não intercepta automaticamente Ars; RPG Skill Tree apenas atributos/Mastery/gates por contrato real. |

**QA pendente:** quantidade efetiva por posição, ordem de hotbar/config, limites de mundo após offset, fake player claims, EntityPlaceEvent + outros callbacks internos de BlockItem.place, resultado FAIL versus consumo efetivo, interação de Sensitive com diversos hits, inventories de máquinas, chunk unload, `ShapersFocus` e multiplayer. **Fail-closed** sem contrato mutador de custos/targeting. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
