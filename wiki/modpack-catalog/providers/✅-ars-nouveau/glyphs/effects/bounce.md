# Ars Nouveau — Bounce

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_bounce`
- Display name: Bounce
- School: Abjuration
- Default tier: 1
- Default mana cost: 50
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies Ars' Bounce effect, causing targets to bounce upward after falling. Provider documentation states that amplification preserves additional forward-facing motion on each bounce.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `#c:slime_balls` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this bounce/mobility status. Black Arcana should not add a generic duplicate bounce buff or take over provider motion-state interpretation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBounce`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectBounce.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBounce.java), Ars Nouveau 5.13.1.
- **Ramo único:** `onResolveEntity` valida `LivingEntity` e chama `IPotionEffect.applyConfigPotion(living,ModPotions.BOUNCE_EFFECT,stats)`; não altera velocidade nesta classe. Base de configuração 30s, Extend Time 8s; com os defaults carregados, `ticks=600+8*(int)(20*durationMultiplier)`, amplifier `(int)ampMultiplier` do helper.
- **Efeito downstream:** preservar movimento adicional em bounce com Amplify é semântica de `BOUNCE_EFFECT`, não uma fórmula direta de `EffectBounce`; necessita classe de Potion/avaliação com movimento. Perk RPG não deve aplicar impulsos em paralelo com o tick do provider.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.

## Certificação estática: status e Dispel — 25/10/2026

**✅ Ficha técnica source-pinned completa somente para planejamento; ⛔ `mutating_hook=NOT_VERIFIED` e ⚠️ `physical_qa=NOT_TESTED`.** Certificação documental não prova que existe perk implementada ou modpack validado.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e release | `ars_nouveau:glyph_bounce`, `EffectBounce`, Ars Nouveau **5.13.1**, tier I. [Source no commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBounce.java); [identidades no publisher JAR](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, causalidade e efeitos downstream | `onResolveEntity` se o hit é LivingEntity aplica `ModPotions.BOUNCE_EFFECT` por `IPotionEffect.applyConfigPotion`. **Não** chama `setDeltaMovement`/`knockback`/impulso nessa classe. `getBookDescription` afirma bouncing após queda e que Amplify preserva movimento horizontal adicional; esse comportamento é downstream em `BOUNCE_EFFECT`/consumidores e não tem fórmula definida neste método. |
| Parâmetros, caps e augments | Config defaults 30 s + contribuição Extend Time 8, com getters fallback 30/8. Formula do helper `ticks=600+8*stats.getDurationInTicks()` usando config default e `amplifier=(int)getAmpMultiplier()`. Augments compatíveis via `getPotionAugments()` — não inferir valor de impulso ou acumulador de velocidade com base no amplifier. Vanilla physics/colisão e addons podem alterar a manifestação. |
| Target, geometria, dano e duração | `EntityHitResult` de alvo LivingEntity. Sem bloco, projétil, DamageType, alcance/área ou golpe próprio. Movimento da vítima após aterrissagem não é executado pelo glyph no instante do cast. |
| Custos e aprendizagem | Mana default **50**, tier I, recipe datagen `ars_nouveau:abjuration_essence` + `#c:slime_balls` ×3, XP default **27**, starter default **não**; [aquisição 85/85](../../ACQUISITION.md). Cooldown, pagamento e admissão pertencem à magia composta/provider; tempo de status não é cooldown. |
| Authority, eventos e integração | Efeito de quique/tick não equivale a casts adicionais; uma perk genérica de mobilidade não deve somar impulso ao mesmo status sem API e deduplicação confirmadas. Ao criar mecânica própria, Black Arcana governa apenas sua movimentação. RPG Skill Tree é sibling de progressão/perks apenas por contrato comprovado. Black Arcana conserva seus próprios casting, Corruption, Strain, WorldEffectPolicy e causalidade, não assume a semântica nativa de Ars. |
| Evidência/validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, **prova compilada somente de ID/classe**. Config instalada, correspondência exata do bytecode de todos os métodos, consumer behavior e clientes/modpack físicos: **não verificados**; `physical_qa=NOT_TESTED`. |

**Invalidação:** mudança de JAR, source, receitas, configs ou listeners de eventos exige reauditoria. Nenhum spell, hook, cast, status mutável ou cap de gameplay foi implementado neste checkpoint.
