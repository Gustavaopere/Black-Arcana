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

## Certificação estática por pipeline e consumidores — 25/10/2026

**✅ COMPLETE_PERK_READY apenas no escopo `STATIC_TECHNICAL_CATALOG_ONLY` — NÃO é certificação de perk jogável. ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ID e a classe no JAR publisher foram auditados separadamente da semântica lida no commit de source.

| Campo exigido | Contrato source-pinned, limites e classificação para perks |
|---|---|
| Identidade/versionamento | Ars Nouveau `5.13.1`; `ars_nouveau:glyph_harm`; classe `EffectHarm`; escola Elemental Earth, tier I. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java) e [registry do publisher SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento, causalidade e settlement | `onResolveEntity` ignora `ItemEntity`. Se houver **Extend Time ou Duration Down** e o hit for `LivingEntity`, aplica `MobEffects.POISON` via `IPotionEffect.applyConfigPotion`, **em vez de** dano instantâneo. No outro ramo chama `IDamageEffect.attemptDamage`, que valida aliado/vida, aplica modifiers e publica `SpellDamageEvent.Pre/Post` somente nas condições respectivas; invulnerability frames e cancelamento não equivalem a dano liquidado. |
| Parâmetros, escalas e caps | Ramo direto usa `DAMAGE+AMP_VALUE*ampMultiplier`, defaults **5,0 + 2,0×amp** antes dos modifiers do helper. Ramo Poison usa config base **5 s** e Extend Time **5**; `ticks=5×20+5×stats.getDurationInTicks()` com defaults carregados e amplifier `(int)ampMultiplier`. Getters sem config retornam **30/8** (fallback, não default). A **presença** de qualquer Time augment define o ramo mesmo se modificadores de duração se compensarem. Limite default de Amplify = **2** na definição do glyph. |
| Targeting, geometria, projétil, tipo e duração | Só `EntityHitResult`; sem hitbox, raio, projeção ou AoE próprios. Efeito condicionado ao tipo de entidade e ramificação; Poison tem duração, dano direto não. O DamageType final vem de `buildDamageSource`/provider `IDamageEffect`, não de nome de escola. A Form de Ars estabelece entrega/seleção. |
| Custos, aprendizagem e limites da receita | Mana default **15**; tier I; XP receita default 27; starter default sim; recipe `ars_nouveau:earth_essence` + `minecraft:iron_sword` ×3. [Acquisition 85/85](../../ACQUISITION.md). Cast/cooldown e mana efetiva da composição são autoridade/config Ars Nouveau. Augments: Amplify, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), Fortune, Randomize. No branch Poison não afirmar que Fortune/Randomize criem dano extra; no branch de dano o helper aplica random rolls e level de luck quando a fonte é `SpellDamageSource`. |
| Integração e segurança | **⛔** Não lançar segundo dano quando Poison substituir hit, nem tratar `Pre`, invocação do helper ou visual como hit confirmado. Sem hook seguro e deduplicação de cast/settlement, RPG/Black Arcana não podem alterar switch, mana ou conceder Mastery. Contrato de perks RPG Skill Tree e hook mutador para este caminho não verificados. Não trocar target, type, raio, mana nem recipients com API presumida. Black Arcana conserva seu runtime, hazards e `WorldEffectPolicy` para efeitos próprios. |
| Grau de evidência/testes | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; JAR publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` prova **ID/classe registrada**, não todos os métodos do classfile ou gameplay atual. Config final, order de eventos, integrações de outros mods, PvP/claims, servidor e cliente: **NOT_TESTED**. |

**Regra de reauditoria:** alterações de JAR/source, config, modificadores, geometria/ordem de eventos ou consumidor downstream exigem nova verificação técnica antes de liberar qualquer hook. Efeitos/raios/VFX não são eventos novos de cast/Mastery.
