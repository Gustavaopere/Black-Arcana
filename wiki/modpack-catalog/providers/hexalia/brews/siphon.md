# Brew of Siphon

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE+ITEM-ATTRACTION VERIFIED / DOCUMENTED MINING-SPEED+EXHAUSTION PATH NOT LOCATED / RUNTIME QA REQUIRED`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_siphon`
- Effect ID: `hexalia:siphon`
- Acquisition: Small Cauldron
- Base duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `hexalia:dream_paste`
2. `hexalia:siren_paste`
3. `minecraft:iron_ingot`
4. `minecraft:redstone`

Result: `hexalia:brew_of_siphon`.

## Item attraction path

`SiphonEffect` applies only to a Player who is **not crouching**.

Each tick:

- attraction radius = `HexaliaConfig.siphonRadius() + amplifier`;
- the source default for `siphonRadius` is `5.0` blocks;
- sanitized config range is `0.5..64.0`;
- nearby `ItemEntity` instances are queried inside the player's inflated bounding box.

At base amplifier 0, the default source radius is therefore `5.0`.

### Inventory has a free slot

The effect calls the item's player-touch pickup path directly for nearby item entities.

### Inventory is full

For the first processed item in this branch:

- direction is computed toward the player's eye position;
- `effectiveAmplifier = min(amplifier + 1, 3)`;
- item Y is nudged by `direction.y × 0.015 × effectiveAmplifier`;
- existing velocity is scaled by `0.95`;
- normalized pull velocity `0.10 × effectiveAmplifier` is added toward the player.

At base amplifier 0, `effectiveAmplifier=1`.

## Registered attribute surface

The Siphon MobEffect registers:

- `ATTACK_SPEED` `+0.4`;
- operation `ADD_VALUE`.

This is directly present in the 1.3.6 effect registration.

## Public-description/source mismatch

Hexalia localization/Grimoire describes Siphon as:

- increasing mining speed;
- attracting nearby items;
- increasing exhaustion while breaking/mining blocks.

The exact 1.3.6 source path audited here directly proves item attraction/pickup and the attack-speed modifier. Repo-wide searches for a Siphon-specific break-speed handler or exhaustion mutation did not locate such a path.

Therefore:

- item attraction/pickup: `SOURCE-CONFIRMED 1.3.6`;
- attack speed +0.4: `SOURCE-CONFIRMED 1.3.6`;
- mining-speed increase: `PUBLIC DESCRIPTION / IMPLEMENTATION PATH NOT LOCATED`;
- mining/block-break exhaustion: `PUBLIC DESCRIPTION / IMPLEMENTATION PATH NOT LOCATED`.

Runtime QA is required before the latter two are treated as active pack behavior.

## Deduplication / authority

Hexalia owns this prepared magnetism/item-siphon brew. Black Arcana must not:

- run a second item-attraction loop while Siphon is active;
- award Mastery every tick for attracted items;
- infer a mining action from item pickup;
- synthesize the documented-but-unlocated exhaustion/mining behavior.

Any future Black Arcana telekinesis/resource-collection mechanic needs distinct authority and bounded execution rather than cloning Siphon's continuous item field.
