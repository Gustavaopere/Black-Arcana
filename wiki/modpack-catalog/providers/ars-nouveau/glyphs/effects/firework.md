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
