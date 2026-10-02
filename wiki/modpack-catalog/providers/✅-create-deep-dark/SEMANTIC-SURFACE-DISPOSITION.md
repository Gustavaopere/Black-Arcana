# Create: Deep Dark 3.0.2 — semantic surface disposition

Status: `EXACT-CURRENT / ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING`

| Surface | Exact role | State | Reason |
|---|---|---|---|
| Echo full armor set | tick-driven Resistance/Strength refresh while all four pieces are equipped | `EXCLUDED` | passive equipment state, no player cast root |
| Echo Sword | LivingIncomingDamageEvent applies Weakness/Darkness on ordinary melee hit | `EXCLUDED` | on-hit weapon proc, not a standalone action |
| Molten Echo | collision applies Darkness and ignition | `EXCLUDED` | environmental/fluid hazard |
| Echo Cake | Create processing/superheat fuel path | `EXCLUDED` | fuel/processing economy, no magic action identity |
| Echo Upgrade / Echo equipment smithing | progression/equipment acquisition | `EXCLUDED` | setup/economy surface |
| Sculk Flour / XP processing | Create crushing/processing | `EXCLUDED` | processing economy |
| Warden loot/progression additions | event/loot/progression handling | `EXCLUDED` | mob loot/progression, not a player magic action |

## Exhaustive activation result

The exact 37-class artifact exposes **zero** provider overrides in the catalog's player-action signature set (`use`, `useOn`, `releaseUsing`, `onUseTick`, `finishUsingItem`, `interactLivingEntity`, `hurtEnemy`, `inventoryTick`, `onArmorTick`, `onItemUseFirst`).

## Result

- exact independent semantic magic identities: **0**;
- strict delta: **+0**;
- disposition: **`ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING`**.
