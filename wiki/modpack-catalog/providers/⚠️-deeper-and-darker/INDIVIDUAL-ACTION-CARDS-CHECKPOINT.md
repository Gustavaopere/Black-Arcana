# Deeper and Darker 1.4.1 — individual action-card materialization checkpoint

Status: `3/3 PUBLIC+SOURCE BASELINE ROOTS MATERIALIZED / +0 STRICT / PHYSICAL DENOMINATOR STILL OPEN`

## Authority

- Black Arcana base before this tranche: `4d6ff1f63bda925836af0b1b1c0a2702c7cbdf3a`;
- physical provider: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- current physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- official publisher SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- exact upstream tag/source pin: `KyaniteMods/DeeperAndDarker@f7ba235d078411a1165a8cac184adfe0ccc8cebe`.

The physical JAR remains byte-different from all official 1.4.1 publisher artifacts and from the clean exact-source build. This tranche therefore **does not promote** any action into the current strict numerator.

## Materialized cards

The already-audited three-root public/source baseline is now split into one file per semantic action:

1. [Otherside Portal Activation](actions/otherside-portal-activation.md)
2. [Sonorous Staff Sonic Boom](actions/sonorous-staff-sonic-boom.md)
3. [Soul Elytra Boost](actions/soul-elytra-boost.md)

The aggregate [PUBLIC-BASELINE-ACTIONS.md](actions/PUBLIC-BASELINE-ACTIONS.md) remains the compact three-root overview.

## Exact source surfaces rechecked

The individual cards are grounded in exact 1.4.1 source/data surfaces:

- `WardenHeartItem.useOn(...)`;
- `OthersidePortalBlock.spawnPortal(...)` / `OthersidePortalShape`;
- `SonorousStaffItem.use(...)` / `releaseUsing(...)`;
- `SoulElytraBoostPacket.handle(...)`;
- `DeeperDarkerClientEvents.keyInput(...)`;
- `Keybinds.BOOST`;
- `DeeperDarkerConfig.soulElytraCooldown`;
- exact generated recipes for Sonorous Staff and Soul Elytra;
- exact generated Warden Heart loot modifier.

No current-physical formula, registration or config value was inferred from those public/source files.

## Accounting

- baseline supernatural roots: **3/3 individually materialized**;
- current exact-physical roots proven: **0**;
- strict semantic delta: **+0**;
- strict global minimum: **1849 unchanged**;
- provider folder state: **⚠️ partial/conditioned**.

## Remaining closure gates

No existing blocker is removed:

- raw-byte inspection or an exact SHA-1 bridge for physical `83f7edd0...`;
- deployed effective `soulElytraCooldown` for Soul Elytra Boost.

These cards improve object-level catalog detail only.
