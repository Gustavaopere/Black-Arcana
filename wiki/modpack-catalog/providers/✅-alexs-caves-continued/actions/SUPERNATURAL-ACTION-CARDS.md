# Alex's Caves Continued 1.0.10 — supernatural action cards

Status: `8/8 COUNTED_EXACT ROOTS MATERIALIZED`

These cards retain only the player-owned causal identity. Numerical tuning, enchantment modifiers, entity AI, particles, sounds, cooldowns and world settlement remain Alex's Caves Continued authority.

## 1. Sea Staff — Water Bolt

- owner: `alexscaves:sea_staff`;
- trigger: direct item use;
- semantic root: provider creates and launches its Water Bolt action from the player;
- acquisition: exact Deep One Mage barter loot;
- state: `COUNTED_EXACT`.

Individual Water Bolt entity ticks, targeting, impact and enchantment modifiers are downstream consequences.

## 2. Sugar Staff — Peppermint Cast

- owner: `alexscaves:sugar_staff`;
- trigger: normal direct item use;
- semantic root: provider creates the Peppermint cast pattern around/from the player;
- acquisition: exact Licowitch loot;
- state: `COUNTED_EXACT`.

Number of peppermints, seeking/straight modifiers, lifespan and spin behavior are parameters/consequences.

## 3. Sugar Staff — Hex Cast

- owner: `alexscaves:sugar_staff`;
- trigger: sneaking direct item use;
- semantic root: provider creates one Sugar Staff Hex action at the provider-resolved ground position;
- acquisition: exact Licowitch loot;
- state: `COUNTED_EXACT`.

Hex scale/lifespan enchantment modifiers are not extra identities.

## 4. Magic Conch — Summon Deep Ones

- owner: `alexscaves:magic_conch`;
- trigger: charged use/release;
- semantic root: provider summons a temporary allied Deep One group for the user;
- acquisition: exact Deep One Knight barter loot;
- state: `COUNTED_EXACT`.

Deep One, Deep One Knight and Deep One Mage are participants/variants of the same summon action, not three spells.

## 5. Totem of Possession — Possession / Remote Control

- owner: `alexscaves:totem_of_possession`;
- trigger: use of a valid bound totem while the controlled entity remains eligible;
- semantic root: provider transfers player intent into ongoing remote control of the bound entity;
- acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

Binding, unbinding, repeated path/movement updates, target attacks, enchantment-assisted transfer and detonation-on-death branches are setup/management/consequences of the one possession root. Player-possession compatibility is separately config-sensitive but is not required for the mob-control identity to exist.

## 6. Occult Gem + Beholder — Remote Observation

- owner surface: `alexscaves:occult_gem` + `alexscaves:beholder`;
- trigger: use of an Occult Gem previously bound to a valid Beholder;
- semantic root: provider starts a remote Beholder observation session and creates the Beholder Eye viewpoint tied to the player;
- acquisition: Occult Gem has exact Forlorn/Watcher loot; Beholder has exact crafting relation;
- state: `COUNTED_EXACT`.

Binding the gem to a Beholder is preparation. Forced-chunk/view state, Beholder Eye entity lifetime and camera synchronization are downstream lifecycle.

## 7. Cloak of Darkness — Darkness Incarnate

- owner: `alexscaves:cloak_of_darkness`, requiring the provider Darkness armor condition;
- trigger: provider armor key after charge/eligibility is satisfied;
- semantic root: consumes provider cloak charge and applies the Darkness Incarnate active state, including its provider flight behavior;
- acquisition: exact Cloak/Hood recipes;
- state: `COUNTED_EXACT`.

Charge time, flight duration, light checks and HUD meter are parameters/gates rather than additional abilities.

## 8. Conversion Crucible — Biome Conversion

- owner surface: `alexscaves:conversion_crucible` + `alexscaves:biome_treat`;
- trigger: player selects a target cave biome with a bound Biome Treat and completes the provider-requested offering sequence;
- semantic root: one provider-owned ritual-like lifecycle that converts the local biome/world surface to the selected target;
- acquisition: exact Conversion Crucible and Biome Treat recipes;
- state: `COUNTED_EXACT`.

Target biome choice is a parameter. Individual requested offerings, final-sacrifice variants, conversion ticks, block placements and visual/audio feedback are not separate ritual identities.

## Accounting

- exact supernatural/magical roots: **8**;
- `COUNTED_EXACT`: **8**;
- `CONDITIONAL`: **0** at identity level;
- strict semantic contribution: **+8**.

Full interaction-class exclusions are recorded in [`../ITEM-ACTION-DISPOSITION-1.0.10.md`](../ITEM-ACTION-DISPOSITION-1.0.10.md).
