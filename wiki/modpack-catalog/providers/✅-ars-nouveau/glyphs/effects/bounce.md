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
