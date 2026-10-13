# Ars Nouveau — Flare

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_flare`
- Display name: Flare
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 40
- Compatible augments: Amplify, Dampen, AOE, Fortune, Randomize
- Source default base damage: 7
- Source default Amplify damage scalar: +3
- Default Amplify limit: 2

## Provider-native behavior

Flare only damages living targets already burning, standing in fire, or carrying Ars' Blasting effect. Successful use spawns damaging Cinder entities around the target; block casts can trigger from nearby fire. If the target has Blasting, Flare removes that effect and immediately detonates the provider Blasting explosion at increased strength. AOE increases the number of spawned Cinders. Cinders use Mage Fire and do not spread normal fire to terrain.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:flint_and_steel` ×2 + `minecraft:fire_charge` ×2 + `minecraft:blaze_rod`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Flare occupies conditional fire detonation/cinder territory. Black Arcana Black Flame content must not be a cosmetic copy of this ignition-conditioned burst or duplicate Blasting settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFlare`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectFlare.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFlare.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectFlare` no Ars Nouveau 5.13.1.
- **Admissão:** `canDamage` exige fogo no alvo, `ModPotions.BLAST_EFFECT` ou estar em bloco com `BlockTags.FIRE`; dano nominal `DAMAGE+AMP_VALUE*getAmpMultiplier()` com defaults 7 e 3, via `IDamageEffect.attemptDamage`.
- **Cinder spawn:** a classe chama `spawnCinders` depois de passar em `canDamage`, **independentemente do boolean de sucesso** dentro de `damage(...)`. Gera `(int)Math.ceil(3+getAoeMultiplier())` entidades `Cinder` com bloco `MAGIC_FIRE`, `baseDamage=0.5*(DAMAGE+AMP_VALUE*ampMultiplier)`, `dropItem=false`, `hurtEntities=true` e `ShapersFocus.tryPropagateEntitySpell`.
- **Blasting:** se o alvo ainda tem `BLAST_EFFECT`, lê amplifier, remove efeito e chama `BlastEffect.explode(living,amplifier+1)`: uma causa distinta do dano direto e das Cinders, mas pertence à **mesma** cadeia de magia. Ramo bloco inicia Cinders quando bloco atingido ou vizinhos têm `BlockTags.FIRE`.
- **Perks:** área é contagem de Cinders, não raio de dano diretamente. Verificar caps sobre entidades persistentes, proc rate e WorldEffectPolicy apenas na autoridade Black Arcana. Não creditar Blast+Flare+Cinders como três casts.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.
