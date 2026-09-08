# Memory Crystal

Status: `SOURCE-PINNED 21.3.0 / DATA MODEL+HANDLER AUTHORITY AUDITED / ACQUISITION UNPROVEN / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:memory_crystal`.

The exact source pass confirms registry, model, documentation and runtime behavior, but has not yet proven a normal acquisition recipe. Acquisition therefore remains unclaimed.

## Data contract

`MemoryCrystalData.MAX_SLOTS` is exactly **10**.

Each slot contains:

- optional `CompoundTag` payload;
- `locked` boolean.

The component also stores the selected slot, clamps invalid selected indices and normalizes the slot list to exactly ten entries. `memory_crystal_data` is a persistent and network-synchronized data component.

## Provider behavior

Shift-interaction with a supported block/entity either saves state into the selected empty slot or loads the selected stored state back through a registered `MemoryHandler`. Slot selection and clear/lock actions are driven by a radial UI, while the authoritative item data is server-carried.

The exact 21.3.0 static registry installs five handlers:

1. Turret;
2. Starbuncle;
3. Rune;
4. Spell Sensor;
5. Item Detector.

`MemoryHandlerRegistry.register` is public, so other mods may add compatible handlers at runtime.

Each saved payload includes a `HandlerID` identifying the handler used to interpret the data. Unknown/corrupt handler ids are surfaced rather than silently coerced into a different type.

## Black Arcana boundary

This is provider configuration/state transfer. Black Arcana must not deserialize arbitrary Memory Crystal NBT as its own spell state, assume every stored payload belongs to Ars Additions, or copy provider configuration into Black Arcana persistence. A future integration must use an explicit supported handler/API contract.
