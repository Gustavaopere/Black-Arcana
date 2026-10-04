# Cold Sweat 2.4.3.1 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO SEMANTIC MAGIC PROVIDER`

## Identity gate

Current physical sibling dossier:

- `ColdSweat-2.4.3.1.jar`;
- mod id `cold_sweat`;
- runtime `2.4.3.1`;
- physical SHA-1 `9605a2053e771110591da43d7e689be693f73948`.

NON-MERGE PR #564 downloads CurseForge File `506194 / 8888797` and fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Exact audit evidence:

- HEAD: `1dbd03fb4e1f969a3567320792b9f489cbca4154`;
- run: `37170970559` — SUCCESS;
- artifact: `11291516824`;
- digest: `sha256:096c379baf58a90d4c0f281c5311d441a620481a69a899efdd864a1e72e66122`;
- publisher SHA-1: `9605a2053e771110591da43d7e689be693f73948`;
- publisher SHA-256: `e605022f1a9a8229e9840e1ee8570a4bd7f8cfee3c432b978bbccfe56a8c6ce9`;
- bytes: `2,738,635`.

Result: exact physical/publisher equality is proven.

## Bounded archive inventory

- entries: **1,449**;
- classes: **695**;
- resources: **754**;
- item-like classes: **25**;
- provider-data paths: **178**;
- name/path scan hits on broad magic/soul/portal/enchant tokens: **199**;
- temperature/soul/device candidate classes: **139**.

The broad token count is intentionally not interpreted as magic content: most hits are temperature capabilities/effects, Soulspring presentation/resources, config GUI assets or vanilla-style interoperability.

## Exhaustive item activation index

Exactly seven item classes expose the audited activation methods:

- `FilledWaterskinItem` — `use`, `useOn`, `onUseTick`, `finishUsingItem`, `inventoryTick`;
- `InsulatedMinecartItem` — `useOn`;
- `MinecartInsulationItem` — `use`;
- `SoulSproutItem` — `finishUsingItem`;
- `SoulspringLampItem` — `inventoryTick`;
- `ThermometerItem` — `use`;
- `WaterskinItem` — `use`, `useOn`.

No spell/ritual/glyph registry emerges from the exact item/action surface.

## Exact semantic seams

### Thermometer

`ThermometerItem.use(...)` reads the provider/world temperature at the player position, converts it to the configured display units and displays the measurement. This is sensing/UI utility, not a supernatural action.

### Soul Sprout

`SoulSproutItem.finishUsingItem(...)` clears the consumer's fire state and then delegates to normal item-consumption settlement. This is a consumable survival effect, not a cast identity.

### Soulspring Lamp

`SoulspringLampItem.inventoryTick(...)` is server-side periodic equipment/inventory behavior. It checks whether the lamp is held/offhand/Curios-mounted, reads the provider's world/burning-point temperature state, dimension allowlist and lamp fuel, then applies/maintains provider temperature-modifier behavior and consumes fuel. No explicit player cast/use method exists for the lamp in the exact activation index.

### Waterskins

Waterskin actions fill from water/cauldrons/fluid handlers and perform configured drink/pour actions using stored water temperature. Filled Waterskins also normalize stored temperature over time. These are survival/thermal item mechanics.

### Minecart insulation

Minecart Insulation applies the insulation display state to a targeted minecart; Insulated Minecart places/spawns an insulated minecart on rails. These are equipment/vehicle utilities.

## Device/data surface

The exact artifact packages recipes/advancements/loot/tags for Hearth, Boiler, Icebox, Soulspring Lamp, Waterskin and Thermometer plus provider compat recipes. These surfaces establish thermal infrastructure/acquisition, not spell/ritual identities.

The audit found **45** bounded data references for the selected thermal/soul/device owners.

## Semantic disposition

Cold Sweat 2.4.3.1 is classified:

`ZERO_SEMANTIC_TEMPERATURE_SURVIVAL_INFRA`

Strict contribution: **+0**.

Temperature effects/modifiers, Soulspring thermal equipment, Hearth/Boiler/Icebox devices, Waterskins, sensing, insulation and compatibility infrastructure remain outside the semantic-magic numerator.

## Clean-room boundary

The durable catalog retains hashes, counts, class/registry identifiers and concise behavior-level classifications required for cataloging. It does not redistribute the JAR, source implementation bodies, assets or protected upstream text.
