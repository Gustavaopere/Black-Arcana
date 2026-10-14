# Ars Nouveau — Hex

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_hex`
- Display name: Hex
- School: Abjuration
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Default Amplify limit: 4
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies Ars' `Hex` effect. Provider documentation states that Hex increases damage taken while the target is poisoned, withered, burning or frozen, and halves Mana Regeneration and healing while active. Amplify increases effect level; Time augments adjust duration.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `minecraft:blaze_rod` ×3 + `minecraft:wither_rose`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns this conditional vulnerability/healing/mana-suppression curse. Black Arcana curse content must be mechanically distinct and must not double-apply Hex's provider-local amplification or mana/healing penalties.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectHex`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectHex.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHex.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectHex` no Ars Nouveau 5.13.1.
- **Aplicação:** `onResolveEntity` verifica `LivingEntity` e chama `IPotionEffect.applyConfigPotion(living,ModPotions.HEX_EFFECT,stats)`; a classe `EffectHex` não implementa dano instantâneo nem metade da cura diretamente.
- **Duração/amplificador:** defaults `addPotionConfig(30)` e `addExtendTimeConfig(8)`: no helper, `ticks=30*20+8*(int)(20*getDurationMultiplier())` com configs default, amplifier `(int)getAmpMultiplier()`. Limite default Amplify 4.
- **Efeito downstream:** vulnerability, mana regeneration e healing suppression descritos no provider são implementados em `HEX_EFFECT`/consumidores; não inventar uma fórmula local de +damage ou redução de heal sem inspecionar esses caminhos.
- **Perks:** status aplicado é distinto dos ataques que dispararem aumento de dano no futuro. Deduplicar Mastery pelo cast raiz, não por cada dano periódico.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.
