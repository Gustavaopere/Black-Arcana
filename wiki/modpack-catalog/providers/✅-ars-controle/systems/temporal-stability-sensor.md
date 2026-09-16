# Temporal Stability Sensor

State: `SOURCE-PINNED 1.6.15 / NO BLOCK ENTITY / RUNTIME QA PENDING`

Registry id: `ars_controle:temporal_stability_sensor`
Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

## Registry correction

This block has no registered BlockEntityType in exact `ACRegistry.Tiles` 1.6.15. Its behavior is implemented directly by the block class.

## Acquisition

Enchanting Apparatus:

- reagent: `minecraft:clock`;
- 1 × `minecraft:ender_eye`;
- 1 × `ars_nouveau:source_gem_block`;
- recipe `sourceCost`: `0`.

## Signal semantics

On the server, analog output is calculated from `MinecraftServer.getAverageTickTimeNanos()` as:

`round(averageTickTimeNanos * 15 / 50ms)`

The block schedules itself every `10` ticks with `TickPriority.EXTREMELY_HIGH` and updates comparator output on each scheduled tick.

The source does not explicitly clamp the calculated integer to 0–15 in this method. The catalog does not infer downstream redstone clamping or saturation without runtime evidence.

## Semantic disposition

Despite its name, this is a server-performance/lag observation device. The exact path does not inspect world time, temporal magic, Arcane Danger, spell cooldowns or chronology state.

Disposition: `PROVIDER-OWNED PERFORMANCE OBSERVABILITY / DO NOT RECAST AS TIME MAGIC`.

## Boundary

- No Black Arcana time-domain authority is created by this sensor.
- Do not feed the signal into Arcane Danger or spell balance as an authoritative metric without a separately approved contract.
- If many sensors are deployed, their 10-tick extremely-high-priority scheduling is a performance QA concern.

## QA pending

1. Confirm actual comparator behavior above nominal 50 ms/tick.
2. Measure many-sensor scheduling overhead.
3. Verify signal refresh after server load/restart.
