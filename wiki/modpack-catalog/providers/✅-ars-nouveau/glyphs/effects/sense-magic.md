# Ars Nouveau — Sense Magic

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_sense_magic`
- Display name: Sense Magic
- School: Abjuration
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source config default duration: 60 s
- Source config default Extend Time increment: 15 s

## Provider-native behavior

Applies Ars' Magic Find effect. Provider documentation states that Magic Find reveals magical mobs by glow within 75 blocks and reveals spells inscribed on Runes. When targeting a block entity implementing `IPedestalMachine`, the spell invokes that provider highlighting path.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `ars_nouveau:dowsing_rod` + `ars_nouveau:starbuncle_shards`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this magical sensing/reveal capability. Black Arcana Familiars & Divination must provide a materially distinct forbidden/divinatory contract rather than duplicate Magic Find.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSenseMagic`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectSenseMagic.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSenseMagic.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectSenseMagic` no Ars Nouveau 5.13.1.
- **Alvos:** `onResolveEntity` aplica `ModPotions.MAGIC_FIND_EFFECT` exclusivamente a `LivingEntity` por `IPotionEffect.applyConfigPotion`. No bloco, só executa `IPedestalMachine.lightPedestal(world)` quando o BlockEntity atingido implementa essa interface.
- **Config vs fallback:** `buildConfig` usa duração base **60 segundos** e `Extend Time` **15 segundos**. Porém `getBaseDuration()` retorna fallback 30 segundos e `getExtendTimeDuration()` fallback 8 segundos quando os campos `POTION_TIME/EXTEND_TIME` são nulos. Registrar separadamente: default configurado 60/15; fallback pré-config 30/8, não os fundir. O helper calcula ticks usando os getters efetivos.
- **Resto do comportamento:** glow a mobs mágicos dentro de 75 blocos e revelação de runas são especificações do `MAGIC_FIND_EFFECT`/renderização, não callbacks explícitos da classe do glyph. Mana declarada 50, tier II, compatível Extend Time e Duration Down.
- **Perks:** detectar alvo mágico e renderizar glow não comprovam descoberta persistida, cast bem-sucedido por alvo, nem concessão de XP. Sem um resultado oficial observável, não criar source paralelo de progressão.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.
