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

## Certificação estática: status e Dispel — 25/10/2026

**✅ Ficha técnica source-pinned completa somente para planejamento; ⛔ `mutating_hook=NOT_VERIFIED` e ⚠️ `physical_qa=NOT_TESTED`.** Certificação documental não prova que existe perk implementada ou modpack validado.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e release | `ars_nouveau:glyph_wither`, `EffectWither`, Ars Nouveau **5.13.1**, tier III. [Source no commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWither.java); [identidades no publisher JAR](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, causalidade e efeitos downstream | `onResolveEntity` valida LivingEntity, então `IPotionEffect.applyConfigPotion(living, MobEffects.WITHER, stats)`; **não** chama `IDamageEffect.attemptDamage` nem inflige dano instantâneo no método. Dano periódico após aplicação é responsabilidade do MobEffect vanilla/Minecraft. Alvos não vivos não recebem a aplicação na classe. |
| Parâmetros, caps e augments | `buildConfig` define default **30 s** base e **8** de contribuição por duration; getters fallback 30/8. Duração default via `IPotionEffect`: `ticks=600+8*stats.getDurationInTicks()`; o amplifier do MobEffect é `(int)stats.getAmpMultiplier()`. `getPotionAugments()` é a superfície compatível de Time e Amplify, e `addDefaultAugmentLimits` fixa cap default de **4 Amplify** para este glyph; não significa 4 níveis máximos de debuff em config alterada. |
| Target, geometria, dano e duração | Apenas alvo `LivingEntity` recebido da Form; sem projétil, área, range ou hitbox próprios. Tipo de dano causado por ticks de Wither é vanilla/downstream e **não está especificado no onResolveEntity**, sem pressupor eventos de dano de spell Ars a cada tick. |
| Custos e aprendizagem | Mana default **100**, tier III, recipe datagen `ars_nouveau:abjuration_essence` + `minecraft:wither_skeleton_skull` ×3, XP default **160**, starter default **não**; [aquisição 85/85](../../ACQUISITION.md). Cooldown, pagamento e admissão pertencem à magia composta/provider; tempo de status não é cooldown. |
| Authority, eventos e integração | Não conceder Mastery por tick nem processar Wither como segundo ataque do cast raiz. Black Arcana curse/DoT deve ser outro contrato com autoridade própria; não existe hook mutador de duração validado em gamepack. RPG Skill Tree é sibling de progressão/perks apenas por contrato comprovado. Black Arcana conserva seus próprios casting, Corruption, Strain, WorldEffectPolicy e causalidade, não assume a semântica nativa de Ars. |
| Evidência/validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, **prova compilada somente de ID/classe**. Config instalada, correspondência exata do bytecode de todos os métodos, consumer behavior e clientes/modpack físicos: **não verificados**; `physical_qa=NOT_TESTED`. |

**Invalidação:** mudança de JAR, source, receitas, configs ou listeners de eventos exige reauditoria. Nenhum spell, hook, cast, status mutável ou cap de gameplay foi implementado neste checkpoint.
