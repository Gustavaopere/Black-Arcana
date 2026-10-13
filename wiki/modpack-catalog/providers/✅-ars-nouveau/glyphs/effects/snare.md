# Ars Nouveau — Snare

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_snare`
- Display name: Snare
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default base duration: 8 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Snare applies Ars' Snare mob effect to living targets, immediately zeroes their motion, and supports duration adjustment through Time augments. When used on an Ars `EnchantedFallingBlock`, it attempts to ground/place the block and propagates block-shaping spell behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:cobweb` ×4.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this immobilization/status effect and its block-shaping interaction. Black Arcana should not double-apply movement suppression or replay block settlement when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSnare`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectSnare.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSnare.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectSnare` no Ars 5.13.1, método `onResolveEntity`.
- **Ramo entidade viva:** `onResolveEntity` usa `applyConfigPotion(...,ModPotions.SNARE_EFFECT,spellStats)`, zera deslocamento `setDeltaMovement(0,0,0)` e marca `hurtMarked=true`. **Ramo block entity:** se alvo é `EnchantedFallingBlock`, chama `groundBlock(true)` e propaga `ShapersFocus.tryPropagateBlockSpell` quando um bloco é posicionado. **Tempo:** `addPotionConfig(8)`, `addExtendTimeConfig(1)` no default; Time augments Extend Time/Duration Down. **Perks:** status e forçar block settlement são resultados distintos; não repetir alteração de velocidade em ticks como se fosse cast novo.
- **Limite de integração:** ✅ source pin da lógica local, ⚠️ execução auxiliares/config dependem do provider real; ⛔ hook externo de mutação não comprovado. Black Arcana só governa suas world mutations; RPG Skill Tree depende de bridge real. QA Survival PENDING.
