# Harm

- Registry ID: `ars_nouveau:glyph_harm`
- Source class: `EffectHarm`
- School: Elemental Earth
- Default tier: **1**
- Default mana: **15**
- Default damage config: **5.0** base + **2.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Without a Time augment, Harm attempts provider-owned magic damage against a non-item target. If Extend Time or Reduce Time is present and the target is living, Harm switches to a Poison application path instead of immediate damage. Amplify increases immediate damage or Poison strength. The exact source caps Amplify to 2 by default.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time, Fortune, Randomize. Harm is explicitly a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:iron_sword` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**.
- When starter remains enabled by config, Ars treats Harm as already known; otherwise its Glyph-learning path remains provider-owned.
- Runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns this damage/Poison branch, invulnerability-frame interactions and provider damage source. Black Arcana must not double-process damage, lifesteal, mastery or Arcane Danger when observing Ars-owned Harm damage.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectHarm.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectHarm` no Ars 5.13.1, método `onResolveEntity`.
- **Alvo/efeito:** `onResolveEntity` ignora `ItemEntity`; com Extend Time ou Duration Down **e** alvo vivo, usa `IPotionEffect.applyConfigPotion` com `MobEffects.POISON`, substituindo dano instantâneo; sem isso, tenta `IDamageEffect.attemptDamage`. **Dano bruto:** `DAMAGE.get()+AMP_VALUE.get()*spellStats.getAmpMultiplier()`, defaults configurados 5.0 e 2.0. **Poison:** defaults do construtor de config 5 (base) e 5 (Extend Time), efeito/ticks resolvidos por helper; amplificação local limitada a 2. **Perks:** não somar dano direto e Poison como dois casts nem assumir evento de mutação externa.
- **Limite de integração:** ✅ fonte estática identificada; ⚠️ parâmetros condicionados à configuração carregada; ⛔ nenhum hook externo de mutação verificado. Mana, targeting e settlement pertencem a Ars; RPG Skill Tree não substitui o resolver. Gameplay/Survival e adapter real: PENDING.

## Fórmula de duração — IPotionEffect exato

- **Helpers:** [`IPotionEffect.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IPotionEffect.java), [`SpellStats.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java).
- **Poison com Time augment:** `IPotionEffect.applyPotion` calcula `ticks=baseDurationSeconds*20+durationBuffSeconds*stats.getDurationInTicks()`; `SpellStats.getDurationInTicks()=(int)(20*durationMultiplier)`. Para config default carregada de Harm (base=5, extend=5), a expressão é `ticks=100+5*(int)(20*durationMultiplier)`; amplifier `(int)spellStats.getAmpMultiplier()`. Só o ramo Poison usa esses ticks.
- **Estado:** fórmula source-pinned; runtime e configuração carregada ainda exigem QA. Nenhuma alteração externa do MobEffect é autorizada apenas por esses getters.
