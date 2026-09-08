# Ars Nouveau — Augments

Augments modify compatible Forms/Effects. This inventory is source-pinned to `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` for installed line 5.13.1.

## Exact inventory — 13/13

| Registry ID | Page | Tier | Default mana | Core source-pinned modifier/role |
|---|---|---:|---:|---|
| `ars_nouveau:glyph_accelerate` | [Accelerate](accelerate.md) | 2 | 10 | +1.0 acceleration |
| `ars_nouveau:glyph_decelerate` | [Decelerate](decelerate.md) | 2 | 5 | -0.5 acceleration |
| `ars_nouveau:glyph_split` | [Split](split.md) | 3 | 20 | additional compatible projectiles |
| `ars_nouveau:glyph_amplify` | [Amplify](amplify.md) | 1 | 20 | +1.0 amplification |
| `ars_nouveau:glyph_aoe` | [AOE](aoe.md) | 2 | 35 | +1.0 AOE |
| `ars_nouveau:glyph_extend_time` | [Extend Time](extend-time.md) | 2 | 10 | +1.0 duration |
| `ars_nouveau:glyph_pierce` | [Pierce](pierce.md) | 2 | 40 | compatible depth/penetration |
| `ars_nouveau:glyph_dampen` | [Dampen](dampen.md) | 2 | 0 | -1.0 amplification |
| `ars_nouveau:glyph_extract` | [Extract](extract.md) | 2 | 30 | extraction/Silk-Touch-like compatible behavior |
| `ars_nouveau:glyph_fortune` | [Fortune / Luck](fortune.md) | 2 | 80 | provider loot/drop increase |
| `ars_nouveau:glyph_duration_down` | [Reduce Time](reduce-time.md) | 2 | 15 | -1.0 duration |
| `ars_nouveau:glyph_sensitive` | [Sensitive](sensitive.md) | 1 | 10 | enables provider Sensitive targeting flag |
| `ars_nouveau:glyph_randomize` | [Randomize](randomize.md) | 1 | 0 | enables provider randomized behavior |

`Default mana` is not final-pack proof: Ars Nouveau configuration owns effective casting cost. Compatibility is not inferred from this table; Forms/Effects individually declare which Augments apply.

Notable exact-line identity detail: the display concept **Reduce Time** still uses `ars_nouveau:glyph_duration_down` in 1.21.1/5.13.1. The source only notes a possible registry-key rename for 1.22.

Status: `13/13 AUGMENTS SOURCE-CATALOGED / RUNTIME+PACK-CONFIG QA PENDING`.
