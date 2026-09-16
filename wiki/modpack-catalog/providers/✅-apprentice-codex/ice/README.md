# Apprentice's Codex 0.9.7.1 — Ice

Exact source pin: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

Exact registry count: **3/3**.

| ID | Name | Max level | Min rarity | Cooldown | Cast |
|---|---|---:|---|---:|---|
| `apprenticecodex:frost_rune` | Frost Rune | 5 | Uncommon | 8 s | Long |
| `apprenticecodex:inscribe_ice` | Inscribe Ice | 5 | Uncommon | 2 s | Instant |
| `apprenticecodex:totem_of_permafrost` | Totem of Permafrost | 5 | Uncommon | 12 s | Instant + recast lifecycle |

All three use Iron's canonical Ice school and Iron's mana.

## Capability summary

- **Frost Rune** — server-validated terrain rune/trap with owner, damage and finite lifetime.
- **Inscribe Ice** — fan of ice daggers; repeated inscriptions cause a high-damage burst that can propagate through nearby inscriptions.
- **Totem of Permafrost** — server-placed temporary area totem dealing cold damage and Slowness in a fixed radius; recast can remove the stored totem.

These cover rune/trap, stacking-mark/burst and temporary area-denial niches. Black Arcana must not duplicate them as generic Ice spells merely by changing names or particles.