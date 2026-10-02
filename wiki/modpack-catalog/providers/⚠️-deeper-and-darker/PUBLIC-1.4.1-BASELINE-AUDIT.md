# Deeper and Darker 1.4.1 — public baseline artifact audit

Status: `PUBLIC 1.4.1 BASELINE ENUMERATED / PHYSICAL RELATION OTHER_VERIFIED / NOT EXACT-CURRENT`

## Physical authority

- physical JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

## Official publisher artifacts tested

NON-MERGE PR #517 tested GitHub release `v1.4.1`, Modrinth `TuD0Zvi3`, and CurseForge project/file `659011 / 8201775`. All three produce the same bytes:

- SHA-1 `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256 `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- size `3,906,057` bytes.

Therefore `publisher_sha1 != physical_sha1`. Relation: **`OTHER_VERIFIED_PUBLISHER_DIFFERS_FROM_PHYSICAL`**.

## Successful baseline audit

- branch/head: `audit/deeper-and-darker-1.4.1-exact-artifact-2026-10-02@8b4cd6b1f60805397f29af9d9d660abf508a7df6`;
- workflow run: `36959073485` — SUCCESS;
- evidence artifact: `11206937200`;
- evidence digest: `sha256:b103afe2dd4b52780acf54682ddcca4b6df484df9ad9cf7accd218e443fb8b1f`.

Public artifact inventory:

- archive entries: **2,900**;
- classes: **207**;
- resources: **2,693**;
- `data/deeperdarker/**` paths: **1,126**.

## Exhaustive top-level item activation index

The public binary audit found only these item classes with ordinary Java activation/tick surfaces:

- `AncientCompassItem` — `inventoryTick`;
- `DDBoatItem` — `use`;
- `LilyFlowerItem` — `useOn`;
- `SculkTransmitterItem` — `use`, `useOn`;
- `SonorousStaffItem` — `use`, `releaseUsing`, `inventoryTick`;
- `SoulElytraItem` — `inventoryTick`;
- `WardenArmorItem` — `inventoryTick`;
- `WardenHeartItem` — `useOn`, `inventoryTick`.

The audit additionally identified network/input surfaces outside item overrides. `SoulElytraBoostPacket` is the important semantic one: the client BOOST keybind sends this payload to the server, which validates fall-flying, equipped Soul Elytra, cooldown/config, then creates the provider boost and cooldown.

## Semantic baseline disposition

Public-release supernatural actions: **3**.

1. Heart of the Deep / Otherside Portal Activation — supernatural traversal setup/portal creation.
2. Sonorous Staff Sonic Boom — deliberate charged sonic attack.
3. Soul Elytra Boost — deliberate keybound supernatural equipment action.

Explicit exclusions:

- Ancient Compass locator;
- Sculk Transmitter remote interaction;
- ordinary boat/flower placement;
- Warden Armor passive state;
- Soul Elytra presentation tick;
- portal traversal/exit generation downstream of portal creation;
- enchantment modifiers of Sonorous Staff.

## Public acquisition evidence

The exact public-release data/source closes:

- Warden loot modifier -> `deeperdarker:heart_of_the_deep`;
- shaped recipe -> `deeperdarker:sonorous_staff`;
- advancement progression around Warden/entering Otherside.

These routes describe the **public publisher baseline only**. They are not promoted as exact physical pack reachability while the installed JAR remains byte-different.

## Strict disposition

`PUBLIC_BASELINE_3 / PHYSICAL_DENOMINATOR_OPEN / +0 STRICT`.

The public release is useful for identifying likely action families and for clean-room comparison, but Black Arcana must not claim `3/3 exact-current` until the physical `83f7...` artifact is directly inspected or matched to a publisher artifact.
