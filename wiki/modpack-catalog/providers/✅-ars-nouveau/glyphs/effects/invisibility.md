# Ars Nouveau — Invisibility

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_invisibility`
- Display name: Invisibility
- School: Abjuration
- Default tier: 2
- Default mana cost: 30
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies vanilla Invisibility to a living target using Ars' potion-effect timing path.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `#c:rods/blaze`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns generic temporary invisibility. Black Arcana should only add concealment magic when it has a materially different forbidden-magic contract rather than duplicating this buff.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInvisibility`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectInvisibility.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInvisibility.java) do Ars 5.13.1.
- **Alvo/efeito:** `onResolveEntity` exige `LivingEntity` e chama `IPotionEffect.applyConfigPotion(living,MobEffects.INVISIBILITY,stats,false)` — o argumento `showParticles=false` suprime as partículas do status, não o status.
- **Duração:** source config default 30s base, Extend Time 8s: `ticks=600+8*(int)(20*durationMultiplier)` pelo helper e amplifier `(int)ampMultiplier`; classe permite somente Extend Time e Duration Down. Invisibility e sua detecção real dependem do Minecraft e dos outros mods, não de uma rotina de stealth no glyph.
- **Perks:** aplicação de status não implica ocultação universal contra addons de targeting ou mobs; sem hook/QA não prometer invisibilidade total ou bônus de combate.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.

## Certificação estática: status e Dispel — 25/10/2026

**✅ Ficha técnica source-pinned completa somente para planejamento; ⛔ `mutating_hook=NOT_VERIFIED` e ⚠️ `physical_qa=NOT_TESTED`.** Certificação documental não prova que existe perk implementada ou modpack validado.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e release | `ars_nouveau:glyph_invisibility`, `EffectInvisibility`, Ars Nouveau **5.13.1**, tier II. [Source no commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInvisibility.java); [identidades no publisher JAR](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, causalidade e efeitos downstream | `onResolveEntity` exige `LivingEntity` e aplica **MobEffects.INVISIBILITY** via `IPotionEffect.applyConfigPotion(living, effect, stats, false)`. O argumento `false` controla a visibilidade das partículas no `MobEffectInstance`; **não** remove o efeito nem prova invisibilidade universal contra AI, outros mods, target locks ou visão mágica. Ausente alvo vivo: sem aplicação nesta classe. |
| Parâmetros, caps e augments | `buildConfig` define defaults `POTION_TIME=30` segundos e `EXTEND_TIME=8`; getters de fallback são 30/8 se ainda não inicializados. Helper `IPotionEffect.applyPotion`: `ticks=30*20+8*stats.getDurationInTicks()` com default carregado, `stats.getDurationInTicks()=(int)(20*durationMultiplier)` na fonte de SpellStats, e amplifier `(int)getAmpMultiplier()`. A classe permite **apenas Extend Time/Reduce Time** como augments; não extrapolar cap de Amplify ou efeito de amplificação, nem afirmar que o tempo final da config instalada corresponde ao default. |
| Target, geometria, dano e duração | `EntityHitResult` de entidade viva; a Form compõe delivery e seleção. Sem raycast, área, projétil, dano ou DamageType próprios desta classe. Duração somente do status vanilla; partículas `false` não são teste de detecção ou stealth completo. |
| Custos e aprendizagem | Mana default **30**, tier II, recipe datagen `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `#c:rods/blaze`, XP default **55**, starter default **não**; [aquisição 85/85](../../ACQUISITION.md). Cooldown, pagamento e admissão pertencem à magia composta/provider; tempo de status não é cooldown. |
| Authority, eventos e integração | O Ars paga casting e aplica status uma vez no resolver; não emitir múltiplos casts, Mastery por tick nem assumir regra universal de invisibilidade no Black Arcana. `mutating_hook=NOT_VERIFIED` para alterar duration/recipient a partir do RPG Skill Tree; status vanilla e compatibilidades com addons dependem de QA cliente/servidor. RPG Skill Tree é sibling de progressão/perks apenas por contrato comprovado. Black Arcana conserva seus próprios casting, Corruption, Strain, WorldEffectPolicy e causalidade, não assume a semântica nativa de Ars. |
| Evidência/validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, **prova compilada somente de ID/classe**. Config instalada, correspondência exata do bytecode de todos os métodos, consumer behavior e clientes/modpack físicos: **não verificados**; `physical_qa=NOT_TESTED`. |

**Invalidação:** mudança de JAR, source, receitas, configs ou listeners de eventos exige reauditoria. Nenhum spell, hook, cast, status mutável ou cap de gameplay foi implementado neste checkpoint.
