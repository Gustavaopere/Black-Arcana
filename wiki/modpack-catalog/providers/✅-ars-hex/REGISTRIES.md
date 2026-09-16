# Ars Hex 5.0.4b — Registries

Status: `SOURCE REGISTRY SURFACE CLOSED / ACTIVE-vs-DORMANT SEPARATED / INSTALLED QA OPEN`

## Base DeferredRegisters

`ModRegistry` creates and registers buses for:

- items;
- blocks;
- sound events;
- entity types;
- particle types.

The base class itself contains no production entries. Compat modules populate these registers conditionally.

## Active in the current provider set — source eligibility

The physical pack contains Malum and Iron's.

### NeoForge/item registry

Malum module:

- `ars_hex:enchanter_scythe` — 1 item.

No active Ars Hex block, entity type or sound registration was identified from the Malum/Iron's modules.

### Particle registry

Iron's module — 5:

- `wisp_iss`;
- `snowflake_iss`;
- `electricity_iss`;
- `fire_iss`;
- `firefly_iss`.

### Ars glyph registry

Malum module — 1:

- `ars_hex:glyph_soul_shatter`.

### Ars perk registry

Malum module — 3:

- `ars_hex:thread_soul_ward`;
- `ars_hex:thread_magic_proficiency`;
- `ars_hex:thread_soul_spoils`.

Iron's and Hexerei perk placeholders in `ArsNouveauRegistry` are commented and are **not** counted.

## Dormant Hexerei module — source surface, not current runtime

If `hexerei` were loaded, exact source calls would register:

### Items — 3

- `ars_hex:archwood_broom`;
- `ars_hex:magebloom_brush`;
- `ars_hex:wet_magebloom_brush`.

### Entity types — 1

- `ars_hex:archwood_broom` — `MobCategory.MISC`, source size 1.175 × 0.3625, tracking range 10, update interval 1.

### Particles — 12

- `broom_leaves`;
- `broom_leaves_2`;
- `broom_leaves_3`;
- `fog_spell`;
- `blood_spell`;
- `owl_teleport`;
- `owl_teleport_barn`;
- `owl_teleport_snow`;
- `moon_leaves`;
- `moon_leaves_2`;
- `moon_leaves_3`;
- `star_brush`.

The module also installs Hexerei renderers/client extensions, BroomType integration, documentation and Mixing Cauldron recipe-page adaptation. These paths are gated by `ModList.isLoaded("hexerei")` in the provider bootstrap.

Hexerei is absent from the physical modlist, so none of the above are promoted to active current-pack registries.

## Excluded / non-production source artifacts

### `ars_hex:archwood_staff`

A manual `hexcasting`-conditioned recipe and language/tag resources reference this id, but no Java registration for the item was located in the audited 5.0.4b source checkpoint. `hexcasting` is also absent from the physical pack.

Classification: `DORMANT/ORPHAN RESOURCE — NOT PRODUCTION REGISTRY`.

### `ExampleCosmetic`

An example item class exists in source, but no production registration was identified. It is excluded from provider counts.

## Active source-count summary

For the currently installed optional-provider set, the source eligibility surface is:

- 1 Ars Hex item;
- 5 Ars Hex particle types;
- 1 Ars glyph;
- 3 Ars perks;
- 0 Ars Hex blocks identified;
- 0 Ars Hex entity types identified from active modules;
- 0 Ars Hex sound events identified.

These are source-derived eligibility counts, not a claim that the physical JAR/runtime registries were enumerated live. JAR extraction/runtime registry QA remains open.
