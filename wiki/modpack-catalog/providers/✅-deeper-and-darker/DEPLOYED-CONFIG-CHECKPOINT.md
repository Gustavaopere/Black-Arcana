# Deeper and Darker 1.4.1 — deployed config checkpoint

Status: `DEPLOYED COMMON CONFIG PATH CONFIRMED / EXACT 1.4.1 CONFIG CONTRACT CONFIRMED / EFFECTIVE SOUL ELYTRA VALUE UNKNOWN / FAIL-CLOSED`

## Scope

This checkpoint is limited to the base provider **Deeper and Darker** / `deeperdarker` and the deployed configuration condition for **Soul Elytra Boost**.

It does not change the physical-JAR provenance boundary and does not cover the separate `darkermagic` / **Deeper and Darker: Spellbooks** addon.

## Exact 1.4.1 source contract

The exact upstream 1.4.1 source authority remains:

- repository: `KyaniteMods/DeeperAndDarker`;
- commit: `f7ba235d078411a1165a8cac184adfe0ccc8cebe`.

Direct Git-tree/blob inspection of that exact commit confirms:

### Common config registration

`src/main/java/com/kyanite/deeperdarker/DeeperDarker.java` registers:

`container.registerConfig(ModConfig.Type.COMMON, DeeperDarkerConfig.CONFIG_SPEC);`

Therefore the relevant 1.4.1 config is a NeoForge **COMMON** config, not the OWO config architecture used by later upstream code.

### Soul Elytra config field

`src/main/java/com/kyanite/deeperdarker/DeeperDarkerConfig.java` defines:

- key: `soulElytraCooldown`;
- default: **600 ticks**;
- valid range: **-1 through 12000**;
- `-1`: explicitly disables Soul Elytra boost.

The default is a source default only. It is not evidence that the deployed pack retained `600`.

### Runtime use of the field

`src/main/java/com/kyanite/deeperdarker/network/SoulElytraBoostPacket.java` reads the same config value at runtime.

The exact handler:

- returns without boosting when `soulElytraCooldown == -1`;
- otherwise requires fall-flying, Soul Elytra equipped and no current item cooldown;
- spawns the provider firework-style boost;
- applies the configured `soulElytraCooldown` value as the item cooldown.

This confirms that deployed config can change both **eligibility** and **cooldown duration** of the public/source Soul Elytra Boost action.

## Deployed runtime config path

Retained runtime logs positively identify the physical config file used by Deeper and Darker 1.4.1:

`C:\Users\gusta\curseforge\minecraft\Instances\Mods\config\deeperdarker-common.toml`

Examples retained in Project Library include:

- `debug(20260817-032729).log`
  - 2026-08-16 23:59:35 local log time: `deeperdarker-common.toml` loaded and watched;
- `debug(20260817-103818).log`
  - 2026-08-17 07:34:14: config file registered for `deeperdarker` tracking;
  - 2026-08-17 07:34:53: the same TOML loaded and watched;
- `debug(20260817-163450).log`
  - 2026-08-17 12:41:37: the same TOML loaded and watched;
- `debug(3).log`
  - 2026-08-18 23:12:47: the same TOML loaded and watched;
- `debug(6).log`
  - 2026-08-19 00:16:03: the same TOML loaded and watched.

This closes the config-**path** question: the deployed 1.4.1 runtime did load `config/deeperdarker-common.toml`.

## Retention boundary

The effective value of `soulElytraCooldown` is still unresolved.

Evidence search found:

- no retained standalone `deeperdarker-common.toml` in the complete Project Library `/Minecraft` file listing;
- no retained log line that explicitly prints the deployed `soulElytraCooldown` value;
- no exact-current configuration artifact from which that value can be recovered.

The absence of a correction warning is **not** used to infer `600`. Any value inside the valid source range, including `-1`, could load without requiring correction.

Likewise, successful loading of `deeperdarker-common.toml` proves only that NeoForge accepted/read the file; it does not prove that the file contained defaults.

## Catalog consequence

This checkpoint narrows but does not remove the Soul Elytra condition:

- exact 1.4.1 config contract: **CONFIRMED**;
- deployed config filename/path: **CONFIRMED**;
- deployed config was loaded in retained boots: **CONFIRMED**;
- effective deployed `soulElytraCooldown`: **UNKNOWN**;
- Soul Elytra Boost exact deployed enablement: **UNKNOWN**;
- public/source Soul Elytra action remains **conditioned**.

The independent physical-JAR blocker also remains:

- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- exact-current physical semantic denominator: **UNKNOWN**.

Therefore:

- public/source supernatural baseline: **3 roots**;
- strict semantic contribution: **+0**;
- provider state: **⚠️ partial / conditioned**.

## Closure requirement

The config condition can close only with direct evidence of the deployed value, for example:

- the actual physical `config/deeperdarker-common.toml` from the pack instance;
- an exact retained copy of that file;
- or a runtime/evidence artifact that explicitly records the effective `soulElytraCooldown` value.

Until then, Black Arcana must not promote Soul Elytra Boost as exact-current enabled solely because the source default is `600`.
