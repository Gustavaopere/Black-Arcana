# Create Mechanical Companion 1.9 — semantic surface disposition

Status: `ZERO_SEMANTIC_MECHANICAL_COMPANION_INFRA`

| Surface | Exact behavior | Semantic state |
|---|---|---|
| Mechanical Wolf Link | Curios lifecycle anchor; persists UUID/modules/name, automatically reconstructs/respawns companion and dismisses on unequip | `EXCLUDED_COMPANION_LIFECYCLE` |
| Blueprint Painting | `useOn` places decorative provider painting | `EXCLUDED_DECORATION` |
| Quantum Drive | module-driven automatic teleport of the Mechanical Wolf under provider cooldown/AI logic | `EXCLUDED_TECH_COMPANION_MOVEMENT` |
| Booster Rocket | companion speed/movement module | `EXCLUDED_TECH_MOVEMENT` |
| Tesla Tail | reactive companion combat/damage module | `EXCLUDED_TECH_COMBAT` |
| Mounted Crossbow | companion targeting/ranged-combat module | `EXCLUDED_TECH_COMBAT` |
| Mob Radar | companion detection/utility module | `EXCLUDED_TECH_UTILITY` |
| Mounted Light | companion lighting/utility module | `EXCLUDED_TECH_UTILITY` |
| Regenerative Casing | passive companion healing module | `EXCLUDED_PASSIVE_GEAR` |
| Plates/Fangs/other modules | companion armor/damage/equipment state | `EXCLUDED_GEAR` |
| Recipes / Illager Workshop loot/worldgen | acquisition and world content | `EXCLUDED_CRAFTING_WORLDGEN` |
| Spell/magic/ritual/etc. roster | exact archive audit = zero | `ZERO_MAGIC_ROSTER` |

## Accounting

- provider-owned semantic magic objects: **0**;
- strict delta: **+0**;
- folder state: **✅ cataloged**.

Mechanical theme, automatic respawn and companion teleport do not create a spell identity under the catalog metric.
