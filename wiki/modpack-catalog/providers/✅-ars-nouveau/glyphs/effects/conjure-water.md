# Ars Nouveau — Conjure Water

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_conjure_water`
- Display name: Conjure Water
- School: Elemental Water
- Default tier: 2
- Default mana cost: 80
- Compatible augments: AOE, Pierce, Extend Time, Sensitive
- Default Sensitive limit: 1
- Source default Soaked duration: 20 s
- Source default Extend Time increment: 10 s

## Provider-native behavior

Conjure Water places water at eligible block targets outside ultra-warm dimensions and extinguishes burning entities. With duration amplification through Extend Time it can apply Ars `Soaked`; Sensitive can place water at a target entity's feet. Block placement respects claim checks and supports `LiquidBlockContainer` waterlogging/placement semantics.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:water_bucket`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns generic magical water placement/extinguishing and its Soaked status. Black Arcana must not duplicate provider water placement or use this as permission to bypass its own world-effect policy for independent fluid mutations.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectConjureWater`).

## Engenharia para perks — caminho causal individual

- **Fonte exata:** [`EffectConjureWater.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectConjureWater.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectConjureWater` (Ars 5.13.1).
- **Ramo entidade:** `entity.clearFire()` se estiver incendiado. Só aplica `ModPotions.SOAKED_EFFECT` a `LivingEntity` quando `getDurationMultiplier()>0`; `Sensitive` tenta água aos pés se dimensão não `ultraWarm()`.
- **Ramo bloco:** aborta em dimensão ultra-warm; `SpellUtil.calcAOEBlocks` recebe AOE/Pierce, depois `placeWater(...)` valida `destroyRespectsClaim` e `world.isInWorldBounds(pos)` na posição do hit. Se `LiquidBlockContainer.canPlaceLiquid` usa waterlogging; caso contrário tenta a posição adjacente `pos.relative(direction)` se substituível por água. A validação de claims da posição adjacente não aparece de modo explícito neste helper: requer QA do caminho completo.
- **Tempo:** `buildConfig` define base potion 20s e incremento Extend Time 10s; `getBaseDuration()` usa fallback 30s **somente quando** `POTION_TIME==null`, uma divergência entre fallback e config default a registrar; `IPotionEffect.applyPotion` calcula ticks a partir da config efetivamente inicializada.
- **Perks:** extinguir fogo, colocar fluido e aplicar Soaked são branches e admissões diferentes; expansão de volume de água por perks não deve bypassar proteção de terreno nem o `WorldEffectPolicy` para spells Black Arcana.
- **Estado:** ✅ assinatura/fórmula do source pin; ⚠️ config carregada, auxiliar e testes físicos pendentes. Contratos de `EffectResolveEvent.Pre` são existentes, porém o adapter RPG, clamps, causalidade e escrita externa **não** foram validados: ⛔ fail-closed até testes.

## Certificação técnica estática para perks — Conjure Water (2026-10-25)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** `ars_nouveau:glyph_conjure_water` ↔ `EffectConjureWater` verificado por ID/classe no JAR Ars Nouveau 5.13.1 (SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`); **não** equivale à prova de bytecode dos métodos. Sources fixados `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectConjureWater.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectConjureWater.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java).

| Campo de alteração por perks | Evidência do caminho efetivo |
|---|---|
| Alvo entidade | `onResolveEntity` executa `entity.clearFire()` quando `entity.isOnFire()`, independentemente de `ultraWarm` nessa verificação. Se `LivingEntity` e `spellStats.getDurationMultiplier()>0`, chama `applyConfigPotion(livingEntity,ModPotions.SOAKED_EFFECT,spellStats)`. `Sensitive` tenta `placeWater` em `entity.blockPosition()`, direção `UP`, apenas se `!world.dimensionType().ultraWarm()`. Portanto extinguir fogo, Soaked e criar água são branches **diferentes** e não garantidamente simultâneos. |
| Alvo bloco/área | `onResolveBlock` obtém `SpellUtil.calcAOEBlocks(shooter,hitPos,hit,getAoeMultiplier(),count(AugmentPierce))` e retorna sem executar no Nether/qualquer `dimensionType().ultraWarm()`. O overload usa largura `1+floor(AOE)`, altura `1+ceil(AOE)`, profundidade `1+Pierce`; a direção do hit orienta a lista. Não é projectile com raio próprio. |
| Checagem de claims | `placeWater` chama `BlockUtil.destroyRespectsClaim(getPlayer(shooter,world),world,pos1)` e `world.isInWorldBounds(pos1)` **somente para a posição original**. Se o bloco original é `LiquidBlockContainer` e `canPlaceLiquid(...Fluids.WATER)`, chama `placeLiquid` na própria posição e propaga `ShapersFocus`; `placeLiquid` não tem retorno conferido aqui. |
| Posição adjacente | Se não seguiu o ramo LiquidBlockContainer, verifica `getBlockState(pos1.relative(direction)).canBeReplaced(Fluids.WATER)`, muda `pos1` para a posição adjacente e executa `world.setBlockAndUpdate(pos1,Blocks.WATER.defaultBlockState())`. **Não há segundo `destroyRespectsClaim` nem `isInWorldBounds` explícito para o BlockPos adjacente**, e o boolean de `setBlockAndUpdate` é ignorado antes de `ShapersFocus.tryPropagateBlockSpell`. Portanto não declarar sucesso por cada bloco nem claims asseguradas para o destino adjacente. |
| Duração e mana | `getDefaultManaCost()=80`, `defaultTier()=TWO`; compatíveis `AugmentAOE`, `AugmentPierce`, `AugmentExtendTime`, `AugmentSensitive` (default Sensitive max1). `buildConfig` chama `addPotionConfig(builder,20)` e `addExtendTimeConfig(builder,10)`; `getBaseDuration()` usa fallback `30` apenas quando `POTION_TIME==null`, diferente do default configurado **20 segundos**. Duração efetiva depende da configuração ativa, não de converter cegamente 20/30 em ticks. |
| Causalidade e authority | As mutações de líquido, status `SOAKED_EFFECT` e `clearFire` são provider-owned. Mana/custos, ShapersFocus, SpellResolver e callbacks de `EffectResolveEvent.Pre` não constituem adapter mutador RPG validado. `WorldEffectPolicy` de Black Arcana rege **seus próprios** casts e fluidos; não intercepta automaticamente o Ars. Nenhuma perk pode multiplicar água, AOE/Pierce ou aumentar duração sem world-budget, protection checks **do destino efetivo** e contrato real de Source/mana. |

**QA ainda necessária:** claims e outros protectors em BlockPos adjacente, limite de construção por translação, estados waterloggable, ultra-warm e fire-exit, confiabilidade do retorno de mutação, duração carregada e Soaked, custos, modded fluids, propagação e chunk lifecycle. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
