# Ars Nouveau — Animate Block

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_animate_block`
- Display name: Animate Block
- Schools: Manipulation + Conjuration
- Default tier: 2
- Default mana cost: 200
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default duration: 60 s
- Source default Extend Time increment: 60 s

## Provider-native behavior

Animate Block converts an eligible block into an Ars combat summon, preserving block state and block-entity data where present. Skull blocks use a specialized head summon. Existing Ars enchanted falling blocks can also be converted. The summon is tamed/aggressive toward the caster's recent target and provider documentation states it returns to a falling-block form on death. Unlike several other Ars summons, this glyph explicitly does not grant Summoning Sickness.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `#c:obsidians` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this block-animation summon lifecycle, state capture and restoration/conversion behavior. Black Arcana should not duplicate the summon or take ownership of stored block data.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectAnimate`).

## Engenharia para perks — caminho causal individual

- **Fonte exata:** [`EffectAnimate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectAnimate.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectAnimate` (Ars 5.13.1).
- **Block ingress:** `onResolveBlock` só passa se `EnchantedFallingBlock.canFall(world,pos,shooter,stats)`; antes de substituir o bloco pelo estado legado do fluido, registra `BlockState` e `BlockEntity.saveWithoutMetadata(world.registryAccess())` (ou NBT vazio) para o summon.
- **Entity ingress:** `onResolveEntity` converte `EnchantedFallingBlock` não removido em summon, copiando `getBlockState()`, `blockData`, velocidade atual, `hurtMarked` e reset de fall distance; descarta o falling block original para evitar duplicação.
- **Summon e duração:** `animateBlock(...)` seleciona `AnimHeadSummon` quando bloco é `AbstractSkullBlock`, senão `AnimBlockSummon`; `ticks=(int)(20*(GENERIC_INT.get()+EXTEND_TIME.get()*durationMultiplier))`, defaults 60s e 60s. Marca tame/aggressiveness/target do shooter e delega `summonLivingEntity`. Não aplica Summoning Sickness nesta classe.
- **Perks:** propriedade, restauração dos blocos, data components e drop pós-morte residem no summon downstream; não implantar segunda cópia do BlockEntity nem pagar Mastery por bloco e summon separadamente.
- **Estado:** ✅ assinatura/fórmula do source pin; ⚠️ config carregada, auxiliar e testes físicos pendentes. Contratos de `EffectResolveEvent.Pre` são existentes, porém o adapter RPG, clamps, causalidade e escrita externa **não** foram validados: ⛔ fail-closed até testes.
