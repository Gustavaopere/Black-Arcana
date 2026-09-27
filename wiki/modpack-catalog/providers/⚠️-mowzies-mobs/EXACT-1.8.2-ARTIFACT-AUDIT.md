# Mowzie's Mobs 1.8.2 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER ARTIFACT / CLEAN-ROOM TEXT EVIDENCE / PLAYER-ABILITY REGISTRY CLOSED`

## Audit provenance

- audit branch: `audit/mowzies-mobs-1.8.2-exact-artifact-2026-09-26`;
- final audit HEAD: `3956dcd38238509c7005e3daebce905e0c3e2f8c`;
- final workflow run: `36288758348` — GREEN;
- text-only evidence artifact: `10921622385`;
- evidence-artifact digest: `sha256:7606a1551446363567ddfd7b9d69f95ba16ef7ab6022314eaaf2cb73187363a3`.

The temporary workflow is evidence-only and is intentionally not merged into the canonical branch.

## Exact identity

- CurseForge project/file: `250498 / 7760267`;
- pack filename: `mowziesmobs-1.21.1-1.8.2.jar`;
- physical SHA-1: `d64475cd77444b056ece6472c79d40293dc63c6c`;
- publisher/audit SHA-1: `d64475cd77444b056ece6472c79d40293dc63c6c`;
- audit SHA-256: `b8e7e39fb6430326de7fbb193db56588ee8bd04d0054527924fe588f37131e4f`.

Hash equality closes physical↔publisher artifact identity.

## Exact player-ability structure

The exact artifact contains **19 class files** under the player-ability implementation path.

`AbilityHandler` exposes **17 named player AbilityType ids** plus the `PLAYER_ABILITIES` array. The exact named ids are:

`fireball`, `sunstrike`, `solar_beam`, `solar_flare`, `supernova`, `wrought_axe_swing`, `wrought_axe_slam`, `ice_breath`, `spawn_boulder`, `tunneling`, `hit_boulder`, `spawn_pillar`, `ground_slam`, `boulder_roll`, `fissure`, `backstab`, `rock_sling`.

The exact `PLAYER_ABILITIES` array has **13 members**:

1. `SUNSTRIKE_ABILITY`;
2. `SOLAR_BEAM_ABILITY`;
3. `SOLAR_FLARE_ABILITY`;
4. `SUPERNOVA_ABILITY`;
5. `WROUGHT_AXE_SWING_ABILITY`;
6. `WROUGHT_AXE_SLAM_ABILITY`;
7. `ICE_BREATH_ABILITY`;
8. `SPAWN_BOULDER_ABILITY`;
9. `SPAWN_PILLAR_ABILITY`;
10. `TUNNELING_ABILITY`;
11. `HIT_BOULDER_ABILITY`;
12. `ROCK_SLING`;
13. `BACKSTAB_ABILITY`.

`FIREBALL_ABILITY`, `GROUND_SLAM_ABILITY`, `BOULDER_ROLL_ABILITY` and `FISSURE_ABILITY` are declared but absent from the current array and are not current player-ability inventory.

## Exact causal references

Hash-gated bytecode inspection closes these narrow ownership/trigger facts:

- `ItemWroughtAxe` references both `WROUGHT_AXE_SWING_ABILITY` and `WROUGHT_AXE_SLAM_ABILITY`;
- `ServerEventHandler` references `SUNSTRIKE_ABILITY`, `SOLAR_BEAM_ABILITY` and `BACKSTAB_ABILITY`;
- `EntityBoulderProjectile` references `HIT_BOULDER_ABILITY`;
- `ItemSculptorStaff` references `ROCK_SLING`;
- `ItemIceCrystal` references `ICE_BREATH_ABILITY`;
- `ItemEarthrendGauntlet` references `TUNNELING_ABILITY`;
- `MessageUmvuthiTrade` references `SUNS_BLESSING`;
- `GuiSculptorTrade` references `EARTHREND_GAUNTLET`.

This is sufficient to distinguish active player powers from technical/subaction slots without copying implementation bodies.

## Exact packaged reachability resources

The hash-matched artifact packages:

- `data/mowziesmobs/loot_table/entities/frostmaw.json`;
- `data/mowziesmobs/loot_table/entities/sculptor.json`;
- `data/mowziesmobs/advancement/suns_blessing.json`;
- `data/mowziesmobs/advancement/sculptor_challenge.json`;
- `data/mowziesmobs/advancement/steal_ice_crystal.json`.

These resources corroborate catalog-level routes for Ice Crystal, Sculptor/Geomancer rewards and Sun's Blessing progression. Runtime worldgen/loot/trade settlement remains separate QA.

## Exact config gate

The exact `TunnelingAbility.canUse()` bytecode reads `ConfigHandler$EarthrendGauntlet.enableTunneling`. That boolean is a provider-specific action gate.

The deployed pack value is not available in current authority. The source/default value is therefore not substituted. `tunneling` remains `CONDITIONAL`.

## Release-source corroboration

Public repository `BobMowzie/MowziesMobs-Public` at commit `7aa17309337cbd4102efc418cba12a4983b1540c` declares `mod_version=1.8.2` and corroborates the same ability names, player-facing surfaces and acquisition concepts. This source pin is corroboration only; the exact hash-matched binary above is authority for current inventory.

## Clean-room boundary

The audit retained only hashes, registry/array identities, narrow field references and resource-presence facts. It did not redistribute the JAR, implementation bodies, models, textures, sounds or other protected assets.
