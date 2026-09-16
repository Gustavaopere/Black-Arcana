# IronSable 1.2.0 — physicalized base-spell overlay

These are **not new IronSable spell IDs**. They remain canonical Iron's spells; IronSable adds Sable-ship physics to their existing casts.

The official IronSable description explicitly states that damage, mana and cooldowns are untouched. Base stats therefore remain authoritative in the Iron's catalog.

| Base spell | IronSable ship overlay | Authority note |
|---|---|---|
| Telekinesis | Carries a whole ship in front of the caster. Spell level determines practical lift capacity; heavier ships still move more slowly. Creature targeting keeps normal behavior. | Iron's owns base Telekinesis; IronSable owns ship movement/capacity overlay. |
| Gust | Pushes airships away and rotates them on hit. | Do not add a second ship impulse. |
| Sonic Boom | Applies long-range ship knockback. | Base damage remains Iron's-owned. |
| Shockwave | Radial knockback for ships around the caster. | Dedup per affected ship/cast. |
| Black Hole | Pulls ships into the swirling center and holds them there. | Do not run a second generic attraction loop. |
| Gravity Fissure | Uses the same underlying black-hole-style ship behavior. | Preserve provider-native shared physics path. |
| Stomp | Lifts/launches ship hulls upward. | Do not duplicate vertical impulse. |
| Blizzard | Traps ships in orbit around the storm. | Orbit controller is IronSable-owned for ships. |
| Earthquake | Makes landed ships shake/bounce. | Grounded-ship eligibility and exact impulse remain bytecode/runtime QA targets. |
| Raise Hell | Propels ships upward. With Create Aeronautics present, the provider also documents inflation of nearby hot-air balloons while the eruption burns. | Balloon path is optional integration; ship lift remains without Create Aeronautics. |

## Deduplication rule

For these ten contracts, Black Arcana should treat IronSable as a **physics overlay provider**, not as a second spell provider. If the base spell fires and IronSable is available, any bridge should observe/coordinate provider state rather than independently reapply force.

## Unverified numerical fields

Exact force magnitudes, mass thresholds, falloff, ship caps, update rate, duration and target filters are **NÃO VERIFICADO** until the 1.2.0 JAR bytecode or live runtime is inspected.