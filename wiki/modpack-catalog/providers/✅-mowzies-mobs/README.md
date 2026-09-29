# Mowzie's Mobs — 1.8.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / COMPLETE 11-POWER CATALOG / 10 STRICT DISCRETE PLAYER POWERS + 1 CONFIG-CONDITIONAL POWER / 13 ACTIVE PLAYER-ABILITY SLOTS / RUNTIME QA SEPARATE`

> Folder-prefix rule (2026-09-29): **✅ means the current semantic/action denominator is fully cataloged and materialized.** Deployed config, reachability or runtime QA may still keep individual identities conditional or outside the strict numerator; those conditions remain documented here and do not make the folder structurally partial.

## Current physical authority

- pack JAR: `mowziesmobs-1.21.1-1.8.2.jar`;
- mod id: `mowziesmobs`;
- runtime: `1.8.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `d64475cd77444b056ece6472c79d40293dc63c6c`;
- CurseForge project/file: `250498 / 7760267`.

Exact NON-MERGE audit branch `audit/mowzies-mobs-1.8.2-exact-artifact-2026-09-26` materialized File `7760267` and hard-verified the same SHA-1. Physical↔publisher artifact identity is therefore closed.

## Provider role

Mowzie's Mobs is primarily a creature/boss/encounter provider, but its current 1.8.2 artifact also owns a player-ability framework containing heliomancy, geomancy, ice and weapon-bound powers. Black Arcana must not duplicate those provider-native powers or their acquisition/runtime state.

## Exact player-ability registry

The hash-matched current artifact exposes 17 named player `AbilityType` ids in `AbilityHandler`, but only **13** are members of the current `PLAYER_ABILITIES` array.

Current array members:

- `sunstrike`;
- `solar_beam`;
- `solar_flare`;
- `supernova`;
- `wrought_axe_swing`;
- `wrought_axe_slam`;
- `ice_breath`;
- `spawn_boulder`;
- `spawn_pillar`;
- `tunneling`;
- `hit_boulder`;
- `rock_sling`;
- `backstab`.

Four declared ids are not current array members and are not promoted: `fireball`, `ground_slam`, `boulder_roll`, `fissure`.

See [`EXACT-1.8.2-ARTIFACT-AUDIT.md`](EXACT-1.8.2-ARTIFACT-AUDIT.md).

## Semantic inventory

Under the canonical semantic-magic metric, Mowzie's contributes **11 provider-owned discrete player powers** in the current artifact:

- **4 Heliomancy:** `sunstrike`, `solar_beam`, `solar_flare`, `supernova`;
- **1 Ice power:** `ice_breath`;
- **3 strict Geomancy actions:** `spawn_boulder` (Boulder Lift), `spawn_pillar` (Pillar Rise), `rock_sling`;
- **1 config-conditional Geomancy action:** `tunneling`;
- **2 active Axe powers:** `wrought_axe_swing`, `wrought_axe_slam`.

`hit_boulder` is not counted separately because exact binary causality ties it to the boulder-projectile interaction and the provider presents that hit/launch step as part of the Boulder Lift action. `backstab` is not counted because exact binary causality ties the ability slot to the dagger critical/backstab proc path rather than to an independent player-invoked power.

See [`PLAYER-MAGIC-INVENTORY.md`](PLAYER-MAGIC-INVENTORY.md).

Object-level catalog: [ACTION-CARDS-1.8.2.md](ACTION-CARDS-1.8.2.md).

## Exact acquisition/reachability evidence

The exact artifact packages or references current provider-native routes for the counted families:

- Sun's Blessing: `MessageUmvuthiTrade` references `SUNS_BLESSING`; the `suns_blessing` advancement is packaged;
- Earthrend Gauntlet: `GuiSculptorTrade` references `EARTHREND_GAUNTLET`; the `sculptor_challenge` advancement is packaged;
- Geomancer Staff: exact `sculptor` loot table is packaged and `ItemSculptorStaff` references `ROCK_SLING`;
- Ice Crystal: exact `frostmaw` loot table and `steal_ice_crystal` advancement are packaged; `ItemIceCrystal` references `ICE_BREATH_ABILITY`;
- Axe powers: `ItemWroughtAxe` references both active axe ability slots.

These facts close catalog-level identity and acquisition surfaces. Live encounter/worldgen/drop/trade behavior remains runtime QA.

## Conditional boundary — Tunneling

The exact `TunnelingAbility.canUse()` bytecode references `ConfigHandler$EarthrendGauntlet.enableTunneling` directly. The deployed pack COMMON value is not captured in current authority.

Therefore:

- `tunneling` exists in the exact current player-ability array;
- its provider-native action identity is cataloged;
- it remains **`CONDITIONAL`** and contributes **+0 strict** until the deployed value is evidenced;
- the other counted actions are not blocked by this specific boolean.

Source default values are not substituted for the deployed pack config.

Canonical closure procedure: [`DEPLOYED-CONFIG-CHECKLIST.md`](DEPLOYED-CONFIG-CHECKLIST.md). The read-only deployed-evidence collector now captures both the exact 1.8.2 physical fingerprint comparison and bounded `enable_tunneling` observations.

## Strict semantic disposition

- strict counted actions: **10**;
- conditional actions: **1** (`tunneling`);
- technical/subaction exclusions: **2** (`hit_boulder`, `backstab`);
- inactive declared player-ability ids excluded: **4** (`fireball`, `ground_slam`, `boulder_roll`, `fissure`).

**Strict semantic delta: +10 `COUNTED_EXACT`.**

Provider catalog status is **✅ Cataloged** because all 11 semantic roots are materialized. Tunneling remains deployment-conditioned and outside the strict numerator until its deployed config is evidenced.

## Runtime QA remains separate

Still fail-closed:

- deployed `mowziesmobs-common.toml`, especially `enable_tunneling`;
- exact full-pack boss/structure/worldgen reachability;
- trade/loot settlement and competition with datapack overrides;
- power persistence, interruption, reconnect and multiplayer behavior;
- interaction with Integrated Mowzie's Mobs, Mowzie's Cataclysm, GTBC's Geomancy Plus and Black Arcana;
- balance, damage, cooldown/durability and animation/network settlement.

## Result

**✅ Catalog complete; Tunneling remains deployment-conditioned.**

Current strict semantic contribution: **10 provider-owned discrete player powers**, plus **1 config-conditional Tunneling power**.