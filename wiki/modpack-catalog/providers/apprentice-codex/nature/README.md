# Apprentice's Codex 0.9.7.1 — Nature

Exact source pin: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

Exact registry count: **12/12**.

| ID | Name | Max level | Min rarity | Cooldown | Cast |
|---|---|---:|---|---:|---|
| `apprenticecodex:compound_phial` | Compound Phial | 10 | Common | 1 s | Long |
| `apprenticecodex:tiny_lumberjack` | Tiny Lumberjack | 3 | Rare | 20 s | Continuous |
| `apprenticecodex:graced_rain` | Graced Rain | 3 | Epic | 20 s | Continuous |
| `apprenticecodex:world_flatter` | World Flatter | 3 | Rare | 20 s | Continuous |
| `apprenticecodex:earth_forge` | Earth Forge | 1 | Uncommon | 1 s | Instant |
| `apprenticecodex:grind_runner` | Grind Runner | 3 | Rare | 20 s | Continuous |
| `apprenticecodex:treasure_divination` | Treasure Divination | 3 | Epic | 30 s | Continuous |
| `apprenticecodex:healing_bloom` | Healing Bloom | 3 | Rare | 300 s | Long |
| `apprenticecodex:harvest_moon` | Harvest Moon | 4 | Uncommon | 20 s | Long |
| `apprenticecodex:extract` | Extract | 1 | Rare | 0.5 s | Long / flask-bound |
| `apprenticecodex:heavenly_fist` | Heavenly Fist | 3 | Rare | 20 s | Instant |
| `apprenticecodex:terra_resonance` | Terra Resonance | 3 | Rare | 10 s | Long |

## Capability summary

- **Compound Phial** — thrown Nature damage/splash projectile.
- **Tiny Lumberjack** — summoned saw for mobs/log cutting.
- **Graced Rain** — healing/growth cloud anchored to entity, block or position.
- **World Flatter** — armor-penetrating drill plus block excavation.
- **Earth Forge** — bounded dirt-platform creation through a queued placement job.
- **Grind Runner** — summoned wheel that damages/grinds and optionally uses Create processing semantics.
- **Treasure Divination** — bounded loaded-chunk treasure proximity scan.
- **Healing Bloom** — one managed bloom per player, healing/light/fruit production.
- **Harvest Moon** — bounded job-based mature-crop harvesting without destroying crops.
- **Extract** — Alchemist's Flask dose extraction into a thrown potion.
- **Heavenly Fist** — targeted AoE slam with optional Create pressing/compacting processing.
- **Terra Resonance** — bounded gemstone resonance/search job through walls.

Nature contains several world-processing capabilities. Their provider validation, jobs, budgets and optional-Create semantics remain authoritative. Black Arcana must not reuse them as a shortcut around `WorldEffectPolicy` for Black Arcana-originated effects.