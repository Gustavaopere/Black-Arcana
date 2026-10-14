# Ars Nouveau — Glide

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_glide`
- Display name: Glide
- School: Elemental Air
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source config default duration: 180 s
- Source config default Extend Time increment: 120 s

## Provider-native behavior

Applies Ars' Glide effect, allowing elytra-like flight behavior. The source also exposes `canGlide`, which treats either the Glide effect or Ars' Gliding Perk as sufficient for provider gliding eligibility.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:elytra` + `#c:gems/diamond` ×3.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns temporary elytra-like gliding and a perk-based alternative path. Black Arcana mobility/familiar content should not add a generic duplicate glide buff or take over Ars' glide eligibility state.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectGlide`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectGlide.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGlide.java), Ars Nouveau 5.13.1.
- **Ramo status:** `onResolveEntity` aplica `ModPotions.GLIDE_EFFECT` a LivingEntity via `IPotionEffect`. Config declarada base 180 segundos e ExtendTime 120; getters sem config têm fallbacks 30/8, uma divergência de inicialização que deve ser mantida separada. Após carga default, `ticks=3600+120*(int)(20*durationMultiplier)` pelo helper.
- **Caminho alternativo:** `EffectGlide.canGlide(LivingEntity)` retorna `hasEffect(GLIDE_EFFECT) || PerkUtil.countForPerk(GlidingPerk.INSTANCE,entity)>0.0`. **Este `GlidingPerk` é do Ars Nouveau**, não API de perks do sibling RPG Skill Tree; integração externa não pode reutilizar o nome para afirmar compatibilidade.
- **Perks:** glide por potion e por perk interna Ars representam condições distintas para uma checagem provider; sem hook RPG que declare equivalência, manter fail-closed para novo gate.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.
