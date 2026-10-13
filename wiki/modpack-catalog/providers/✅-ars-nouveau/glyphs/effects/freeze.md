# Ars Nouveau — Freeze

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_freeze`
- Display name: Freeze
- School: Elemental Water
- Default tier: 1
- Default mana cost: 15
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify, AOE, Pierce, Sensitive
- Default Sensitive limit: 1
- Source config default Slow duration: 10 s
- Source config default Extend Time increment: 5 s

## Provider-native behavior

On living targets, Freeze applies vanilla Slowness. On blocks it can convert water to Ice (or Frosted Ice with Sensitive), lava to Obsidian/Cobblestone, extinguish fire, upgrade Ice to Packed Ice and Packed Ice to Blue Ice. AOE/Pierce expand the affected block set.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:snow_block` ×2.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this fluid/ice conversion and slowing primitive. Independent Black Arcana freezing/world mutation must remain `WorldEffectPolicy`-controlled and must not replay Ars conversions.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFreeze`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectFreeze.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFreeze.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectFreeze` no Ars 5.13.1, método `onResolveBlock`.
- **Geometria:** percorre `SpellUtil.calcAOEBlocks(... getAoeMultiplier(), count(Pierce))` e aplica `extinguishOrFreeze` **na posição e nas seis direções**; toda alteração pode propagar `ShapersFocus.tryPropagateBlockSpell`. **Mutações:** água acima → Ice/Frosted Ice com Sensitive; lava acima → Obsidian, flowing lava → Cobblestone; fogo acima é removido; Ice→Packed Ice→Blue Ice. **Entidades:** `applyConfigPotion(...MOVEMENT_SLOWDOWN)`; config default duração 10, Extend Time 5; Sensitive limit 1. **Risco:** não há claim check individual em `extinguishOrFreeze`, mas isso não demonstra ausência de admissão externa: verificar o resolver antes de tratar como vulnerabilidade. AOE×vizinhos requer cap.
- **Limite de integração:** ✅ source pin confirmado, ⚠️ config e classes auxiliares demandam QA; ⛔ hook de mutação RPG não verificado. Provider mantém autoridade de mana/efeito/owner; sem segundo cast/proc/settlement. Survival: PENDING.
