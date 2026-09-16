# Ars Creo 5.4.0 — exact registry surface

Status: `SOURCE-PINNED 5.4.0 / RUNTIME+PACK QA PENDING`

Source checkpoint: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`.

## Provider-owned registries

Exact `ModBlockRegistry` registers:

- blocks: **1** — `ars_creo:starbuncle_wheel`;
- BlockEntityTypes: **1** — `ars_creo:starbuncle_wheel` -> `StarbuncleWheelTile`;
- items: **1** — the `AnimBlockItem` for `ars_creo:starbuncle_wheel`.

Exact `CreativeTabRegistry` registers:

- creative tabs: **1** — `ars_creo:general`.

Exact Create compatibility registration adds two `DisplaySource` entries in the Create registry:

- `ars_creo:turret`;
- `ars_creo:source_jar`.

## No provider-owned registries found for

The exact 5.4.0 source tree does not expose an Ars Creo registry for:

- Ars glyph/spell parts;
- rituals;
- entities;
- mob effects;
- enchantments;
- custom recipe serializers/types;
- custom fluids.

`ModEntities.java` is present as a placeholder source file but does not establish a registered entity surface.

## Cross-provider registrations

Ars Creo also attaches behavior to existing provider objects rather than registering copies:

- Ars Nouveau spell turrets, Source Jars, Portal Block, Ritual Brazier/Block and Potion Jar;
- Create movement/interaction behaviors, stress capacity, Display Sources and FluidHandler capability.

Those existing blocks/entities remain owned by their native providers.

## Editorial correction

The current Notion dossier lists eight Ars Creo blocks and eight block entities, including `source_motor`, `source_gearbox`, converter/correspondent blocks and related machinery. Those entries are **not present in the exact 5.4.0 registry/tree** and are retained only as stale/editorial history. They are not runtime catalog entries for the installed JAR.
