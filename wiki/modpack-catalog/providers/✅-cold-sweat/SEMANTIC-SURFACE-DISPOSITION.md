# Cold Sweat 2.4.3.1 — semantic surface disposition

Status: `EXACT CURRENT / ZERO SEMANTIC MAGIC IDENTITIES`

| Surface | Exact activation/lifecycle | State | Reason |
|---|---|---|---|
| Filled Waterskin | use / useOn / use tick / finish / inventory tick | `EXCLUDED` | drink/pour/fill/stored-temperature survival utility |
| Waterskin | use / useOn | `EXCLUDED` | water filling and fluid-handler utility |
| Thermometer | use | `EXCLUDED` | reads/displays environmental temperature |
| Soul Sprout | finishUsingItem | `EXCLUDED` | consumable clears fire, then normal food/item settlement |
| Soulspring Lamp | inventoryTick | `EXCLUDED` | automatic fueled thermal modifier while equipped/carried; no discrete cast root |
| Minecart Insulation | use | `EXCLUDED` | applies insulation state to minecart |
| Insulated Minecart | useOn | `EXCLUDED` | spawns/places insulated minecart on rails |
| Hearth | block/device lifecycle | `EXCLUDED` | provider thermal emitter/device infrastructure |
| Boiler | block/device lifecycle | `EXCLUDED` | provider heat-device infrastructure |
| Icebox | block/device lifecycle | `EXCLUDED` | provider cold-device infrastructure |
| Insulation / temperature effects/modifiers | event/capability/config lifecycle | `EXCLUDED` | passive/environmental body-temperature framework |

## Accounting

- exact semantic magic identities: **0**;
- `COUNTED_EXACT`: **0**;
- `CONDITIONAL`: **0**;
- `EXCLUDED` provider surfaces above: **11 summarized families**;
- strict semantic contribution: **+0**.

Supernatural theming is not used as a substitute for causal identity. In particular, `Soulspring Lamp` remains thermal equipment because its exact active seam is periodic provider-owned temperature behavior, not a player-selected spell or rite.
