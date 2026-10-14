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
