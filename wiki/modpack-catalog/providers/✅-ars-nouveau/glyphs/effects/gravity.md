# Ars Nouveau — Gravity

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_gravity`
- Display name: Gravity
- School: Elemental Air
- Default tier: 2
- Default mana cost: 15
- Compatible augments: Amplify, Dampen, AOE, Pierce, Extend Time, Reduce Time (`glyph_duration_down`)
- Source default potion duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

On blocks, Gravity converts eligible targets into Ars `EnchantedFallingBlock` entities. On living entities without Extend Time it applies immediate downward velocity of `-1.0 - amplification`. With Extend Time it applies Ars' Gravity effect instead; provider documentation states this disables player flight while active and causes rapid falling with doubled fall damage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:anvil` ×2 + `#c:feathers` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this gravity/falling control primitive and its falling-block interaction. Black Arcana Space/Displacement or forbidden-control spells must be mechanically distinct and must not replay provider motion/block conversion.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectGravity`).

## Dossiê de engenharia para perks — cadeia e interfaces

- **Source pin:** [`EffectGravity.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGravity.java), Ars Nouveau 5.13.1.
- **Blocos:** `SpellUtil.calcAOEBlocks` com AOE/Pierce; cada candidato tenta `EnchantedFallingBlock.fall(...)`, seguido de `ShapersFocus.tryPropagateEntitySpell` quando não nulo. **Entidades:** com Extend Time aplica `ModPotions.GRAVITY_EFFECT` por `IPotionEffect`; sem ele muda movimento por `deltaMovement.add(0,-1.0-getAmpMultiplier(),0)`. **Defaults status:** potion 30 segundos, extend 8, com ticks resolvidos pelo helper. **Perks:** transformação de bloco, impulso vertical e buff/debuff são casos diferentes, com decisões do executor e world/claim owner em Ars. Não repetir efeitos via Black Arcana.
- **Estado:** ✅ classe exata lida; ⚠️ helpers/config real e Survival pendentes; mutabilidade via RPG Skill Tree ⛔ sem interface comprovada que altere esses parâmetros. Ars conserva authority de recursos/efeitos.
