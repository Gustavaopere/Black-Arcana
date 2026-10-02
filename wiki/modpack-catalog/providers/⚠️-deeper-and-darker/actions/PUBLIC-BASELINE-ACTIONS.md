# Deeper and Darker 1.4.1 — public baseline action cards

Status: `3 PUBLIC-RELEASE SUPERNATURAL ROOTS / PHYSICAL EXACTNESS OPEN / ALL +0 STRICT`

These are clean-room behavior cards for the official public 1.4.1 baseline. They are **not** asserted as the exact installed-pack denominator because the physical SHA-1 differs from every official public artifact tested.

## 1. Otherside Portal Activation

- owner item: `deeperdarker:heart_of_the_deep`;
- trigger: player uses the Heart adjacent to a valid reinforced-deepslate portal frame in Overworld/Otherside;
- settlement: provider validates frame and creates `deeperdarker:otherside_portal` blocks;
- public acquisition: provider Warden loot modifier;
- semantic type: supernatural portal-creation/traversal setup;
- public baseline state: `BASELINE_PRESENT`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

Portal collision/travel after creation and destination-side portal generation are consequences of this action, not additional spell identities.

## 2. Sonorous Staff Sonic Boom

- owner item: `deeperdarker:sonorous_staff`;
- trigger: hold/use and release;
- settlement: provider projects a sonic-boom line, applies provider sonic damage/knockback, durability use and cooldown;
- public acquisition: exact shaped recipe;
- modifiers: Volume and Reverberation enchantments alter the same action rather than minting new actions;
- semantic type: discrete supernatural staff attack;
- public baseline state: `BASELINE_PRESENT`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

## 3. Soul Elytra Boost

- owner item: `deeperdarker:soul_elytra`;
- trigger: dedicated client BOOST keybind -> server `soul_elytra_boost` payload;
- server admission: player must be fall-flying, chest slot must contain Soul Elytra, item must not be on cooldown, and provider config must not disable the action;
- settlement: provider creates its firework-style boost and applies the configured Soul Elytra cooldown;
- semantic type: discrete supernatural equipment/flight action;
- public baseline state: `BASELINE_PRESENT / CONFIG_CONDITIONAL`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

`soulElytraCooldown == -1` disables this action in the public baseline. The deployed value is not used to overcome the larger physical-JAR mismatch.

## Excluded adjacent surfaces

- `SculkTransmitterItem` and its transmit keybind — remote inventory/block interaction utility;
- `AncientCompassItem` — structure locator;
- `SoulElytraItem.inventoryTick` — presentation/cooldown feedback;
- `WardenArmorItem.inventoryTick` — passive effect suppression;
- boat/flower interactions — ordinary item placement.

## Accounting

- public supernatural roots: **3**;
- exact-current physical roots proven: **0**;
- strict contribution: **+0**;
- provider state: **⚠️ partial / physical denominator open**.
