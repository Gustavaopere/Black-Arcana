# Creating Space 1.7.22 — semantic surface disposition

Status: `ZERO_SEMANTIC_SPACE_ROCKET_DIMENSION_TRANSPORT`

| Surface | Exact behavior | Semantic state |
|---|---|---|
| Rocket assembly / contraption lifecycle | constructs and persists Create-based spacecraft | `EXCLUDED_TECH_VEHICLE_INFRA` |
| Rocket launch / flight | physical vehicle/aerospace state machine | `EXCLUDED_TECH_TRANSPORT` |
| Rocket schedule / destination | selects a `RocketAccessibleDimension` destination | `EXCLUDED_TRANSPORT_PARAMETER` |
| 6 planet/orbit dimension definitions | world/dimension content | `EXCLUDED_WORLD_CONTENT` |
| 6 rocket-accessible-dimension definitions | route/accessibility graph | `EXCLUDED_ROUTE_DATA` |
| Player dimension transition | server world transfer during aerospace lifecycle | `EXCLUDED_VEHICLE_WORLD_TRANSITION` |
| Vehicle dimension transition | moves rocket/vehicle with passenger preservation | `EXCLUDED_VEHICLE_WORLD_TRANSITION` |
| `CustomTeleporter` | Minecraft `DimensionTransition` adapter for space travel | `EXCLUDED_TRANSPORT_INFRA` |
| Planet/worldgen/ore content | environment/resources | `EXCLUDED_WORLDGEN` |
| 248 provider recipes | crafting/processing/equipment/rocket progression | `EXCLUDED_PROCESSING_ECONOMY` |
| Spell/ritual/glyph/ability roster | none in exact artifact | `ZERO_MAGIC_ACTION_ROSTER` |

## Accounting

- provider-owned semantic magic identities: **0**;
- strict delta: **+0**;
- folder state: **✅ cataloged**.

Rocket destinations and dimension transitions are transport parameters/consequences and are never multiplied into separate Black Arcana magic objects.
