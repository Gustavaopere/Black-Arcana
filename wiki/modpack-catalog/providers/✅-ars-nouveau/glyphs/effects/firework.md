# Ars Nouveau — Firework

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_firework`
- Display name: Firework
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Extend Time, Amplify, Split
- Default Amplify limit: 2

## Provider-native behavior

Firework creates firework rockets at a block or living target. If the caster inventory already contains a Firework Rocket, Ars mirrors that stack; otherwise it generates a provider firework from spell duration/amplification. Split adds additional rockets, Amplify adds Firework Stars, and Extend Time increases flight time. Turret casting has a dedicated launch direction path.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:firework_rocket` ×2 + `minecraft:firework_star`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this firework-generation/casting surface and inventory lookup. Black Arcana should not duplicate a generic magical firework spell or replay projectile spawning when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFirework`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectFirework.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFirework.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectFirework` no Ars Nouveau 5.13.1.
- **Quantidade:** `onResolveBlock` e `onResolveEntity` fazem `count(Split)+1` iterações para gerar `FireworkRocketEntity`. O branch entidade exige `LivingEntity` atingida e chama `setOwner(shooter)`; turret em bloco escolhe orientação especial (ao contrário do jogador).
- **Inventário e fallback:** `fireworkFromInv` procura `Items.FIREWORK_ROCKET` via `InventoryManager.findItem(...,InteractType.EXTRACT)` e obtém o stack daquele slot; se não encontra, gera com `getFirework((int)durationMultiplier,(int)ampMultiplier)`. O código mostrado *não* diminui o stack encontrado no inventário: é modelo/cópia sem afirmar consumo.
- **Dados do foguete:** `getFirework` constrói `DataComponents.FIREWORKS` com `numGunpowder` recebido e `numStars` explosões via `getRandomStar` (`new Random` local). Limite default Amplify=2 na ficha. Variar estética não prova dano ou tempo/altitude exatos sem seguir `FireworkRocketEntity`.
- **Perks:** Split multiplica entidades e carga visual; não cria novos casts, custos ou Mastery. RNG de cores/estrelas é provider-owned e não deve ser tratado como dano arcano determinístico.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.
