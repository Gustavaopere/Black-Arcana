# Create: Mechanical Spawner 1.3.2-6.0.10 — semantic surface disposition

Status: `EXACT-CURRENT / ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA`

| Surface | Exact role | State | Reason |
|---|---|---|---|
| 27 concrete spawner recipes | machine recipe converts required provider fluid/cycle into a configured mob output | `EXCLUDED` | kinetic/data-driven processing, not player cast/summon action |
| Random spawner recipe | machine chooses biome-dependent mob output | `EXCLUDED` | automated machine recipe |
| Wither spawner recipe | machine outputs Wither after fluid + processing requirements; includes custom loot | `EXCLUDED` | boss materialization is recipe settlement, not a ritual identity |
| 28 spawn-fluid mixing recipes | Create mixing creates entity-specific/random spawn fluids | `EXCLUDED` | input/economy preparation |
| Mechanical Spawner block entity | kinetic/fluid/recipe-cycle executor | `EXCLUDED` | automation infrastructure |
| Loot Collector | collects/configures machine loot settlement | `EXCLUDED` | inventory/loot infrastructure |
| KubeJS spawner recipe schema | adds/removes/changes machine recipes | `EXCLUDED` | recipe scripting infrastructure |
| Spawn-point scroll/config behavior | configures machine output position/range | `EXCLUDED` | machine setup/UI behavior |

## Exhaustive activation result

The exact 52-class artifact exposes **zero** provider overrides in the catalog player-action signature set (`use`, `useOn`, `useWithoutItem`, `releaseUsing`, `onUseTick`, `finishUsingItem`, `interactLivingEntity`, `hurtEnemy`, `inventoryTick`, `onArmorTick`, `onItemUseFirst`).

## Result

- exact independent semantic magic identities: **0**;
- strict delta: **+0**;
- disposition: **`ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA`**.
