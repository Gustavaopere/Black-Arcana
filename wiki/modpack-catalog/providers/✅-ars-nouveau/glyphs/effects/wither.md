# Ars Nouveau — Wither

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wither`
- Display name: Wither
- School: Abjuration
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Default Amplify limit: 4
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies vanilla Wither using Ars' potion-effect path. Amplify raises effect level; Time augments modify duration.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:wither_skeleton_skull` ×3.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this generic Wither application. Black Arcana curse/death content must demonstrate a distinct persistent/ritual/hazard contract rather than reskinning the same debuff.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWither`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectWither.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWither.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectWither` no Ars 5.13.1, método `onResolveEntity`.
- **Alvo:** somente `LivingEntity` recebe `MobEffects.WITHER` via `IPotionEffect.applyConfigPotion`; esta classe não executa dano instantâneo. **Duração:** `buildConfig` usa `addPotionConfig(30)` e `addExtendTimeConfig(8)`; os getters têm fallbacks locais 30/8 enquanto configs ainda não existem. **Scaling:** aplica amplificação e Time augments conforme `IPotionEffect` e `SpellStats`; Amplify limit default 4. **Perks:** ticks periódicos de Wither não são novos casts nem autorização para dupla Mastery/proc; sem hook validado para reescrever duração/stack.
- **Limite de integração:** ✅ source pin confirmado, ⚠️ config e classes auxiliares demandam QA; ⛔ hook de mutação RPG não verificado. Provider mantém autoridade de mana/efeito/owner; sem segundo cast/proc/settlement. Survival: PENDING.

## Fórmula de duração — IPotionEffect exato

- **Helpers:** [`IPotionEffect.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IPotionEffect.java), [`SpellStats.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java).
- **Wither pelo helper `IPotionEffect`:** `ticks=baseDurationSeconds*20+durationBuffSeconds*stats.getDurationInTicks()`; `getDurationInTicks=(int)(20*durationMultiplier)`. Com defaults `base=30`, `extend=8`, `ticks=600+8*(int)(20*durationMultiplier)`; amplifier `(int)getAmpMultiplier()`. Truncamento importa: não interpretar Extend Time como +8 ticks fixos por hit.
- **Estado:** fórmula source-pinned; runtime e configuração carregada ainda exigem QA. Nenhuma alteração externa do MobEffect é autorizada apenas por esses getters.
