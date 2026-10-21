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
