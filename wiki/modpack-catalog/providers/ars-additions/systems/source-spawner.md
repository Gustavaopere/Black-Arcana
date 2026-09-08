# Source Spawner

Status: `SOURCE-PINNED 21.3.0 / SEMANTICS+BOUNDS AUDITED / RUNTIME+PACK QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry block: `ars_additions:source_spawner`.

Source acquisition from the 21.3.0 Enchanting Apparatus provider:

- reagent: `ars_nouveau:drygmy_charm`;
- pedestal items: `ars_nouveau:summoning_focus` and `ars_nouveau:conjuration_essence`.

## Provider-native operation

`SourceSpawnerTile` delegates server execution to `SourceSpawner`, a `BaseSpawner` implementation with persisted delay/range/count/disabled values.

Source defaults in the exact pin:

- initial delay: 20 ticks;
- min spawn delay: 200 ticks;
- max spawn delay: 800 ticks;
- spawn count: 4;
- max nearby entities: 6;
- required player range: 16;
- spawn range: 4.

When a spawn cycle is eligible, the provider scans `BlockPos.withinManhattan(pos, 10, 10, 10)` for Ars Mob Jars containing living entities. Entity types on `source_spawner_denylist` are excluded. Optional Source Spawner recipes may also alter the cloned entity NBT through provider tag modifiers.

The entity is spawned first and removed again if required Source cannot be taken. Source payment uses provider `AddonSourceUtil.takeSource` with radius **5**.

Default Source cost, when no recipe override supplies a fixed amount:

`200 + boss bonus + persistent-category bonus + health term`

where:

- boss bonus = 10,000 when the entity type is tagged `c:bosses`;
- persistent-category bonus = 1,000 when the entity category is persistent;
- health term = `maxHealth × 50` for mobs.

The spawner also enforces peaceful-mode rejection for hostile categories, collision checks and maximum-nearby-entity limits.

## Performance boundary

The Mob Jar search is bounded to the local 10-block Manhattan volume and occurs at an eligible spawn cycle, not as an unrestricted global entity scan every tick.

## Black Arcana boundary

Source Spawner owns entity cloning/spawn settlement, recipe modifiers and Source consumption. Black Arcana must not duplicate the spawn, re-charge Source, award offensive cast credit merely from the spawned entity or introduce a parallel global scan around this provider system.
