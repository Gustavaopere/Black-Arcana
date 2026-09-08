# Ars Nouveau — Firework

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_firework`
- Display name: Firework
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Extend Time, Amplify, Split
- Default Amplify limit: 2

## Provider-native behavior

Firework creates firework rockets at a block or living target. If the caster inventory already contains a Firework Rocket, Ars mirrors that stack; otherwise it generates a provider firework from spell duration/amplification. Split adds additional rockets, Amplify adds Firework Stars, and Extend Time increases flight time. Turret casting has a dedicated launch direction path.

## Authority / deduplication

Ars Nouveau owns this firework-generation/casting surface and inventory lookup. Black Arcana should not duplicate a generic magical firework spell or replay projectile spawning when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFirework`).
