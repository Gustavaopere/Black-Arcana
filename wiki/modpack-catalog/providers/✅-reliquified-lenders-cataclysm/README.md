# Reliquified L_Ender's Cataclysm — 0.1.1

Status: `✅ CATALOGED / CURRENT PHYSICAL 0.1.1 / COUNTED_RELEASE_BOUNDED / 9 RELIC OWNERS / 11 PROVIDER-OWNED ABILITY ROOTS / +11 STRICT / REQUIRED RELICS-0.12 FIX SEPARATE / ASSEMBLED QA SEPARATE`

## Current physical identity

Current physical Project Library modlist authority records:

- JAR: `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`;
- mod id: `reliquified_lenders_cataclysm`;
- runtime: `0.1.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- mixin config: `reliquified_lenders_cataclysm.mixins.json`;
- physical SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`.

The same physical pack also contains the separate compatibility provider `reliquified_lenders_cataclysm_new_relics_fix` 1.0.2 / SHA-1 `9d4710e665ec74af917bb9f5f819154ca9f74ca0`. The fix is not the semantic owner of these relic abilities; it adapts the original addon to the newer Relics API.

## Exact publisher release boundary

Official CurseForge project: `Reliquified L_Ender's Cataclysm` / project `1232116`.

Current release:

- File ID `6882649`;
- filename `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`;
- Release / NeoForge 1.21.1;
- uploaded 2025-08-13;
- published changelog: `Fixed Compatibility with OctoLib 0.6`;
- Curse Maven coordinate `curse.maven:reliquified-l-ender-s-cataclysm-1232116:6882649`;
- publisher license: All Rights Reserved.

The publisher release page does not announce new relic identities or a semantic content expansion for 0.1.1. It describes the mod as a Relics × L_Ender's Cataclysm compatibility/content addon whose relics provide unique abilities.

## Public source boundary

Official repository: `Octo-Studios/reliquified-lenders-cataclysm`.

The public 1.21.1 history does **not** contain an exact source checkpoint labeled 0.1.1. The last located checkpoint whose `gradle.properties` still declares `mod_version=0.1` is:

`29a3b80febeac6e1fb5726d8b5883cdff4e775da` — `Added leveling`.

Its immediate successor `d7df82b857158a68d2c3430605d2a15137dc31ad` changes only `gradle.properties` from `mod_version=0.1` to `0.2`.

Therefore the installed 0.1.1 semantic inventory is treated as **release-bounded** by the last public 0.1 source inventory plus the exact publisher 0.1.1 compatibility-only release boundary. Reproducible physical-JAR↔source equality is not claimed.

## Registry and semantic inventory

The last public 0.1 source checkpoint registers exactly **9 provider-owned relic items** in `ItemRegistry`:

1. `scouring_eye`;
2. `void_vortex_in_bottle`;
3. `void_cloak`;
4. `vacuum_glove`;
5. `void_bubble`;
6. `ring_of_the_flame_kindler`;
7. `mask_of_rage`;
8. `fire_plate`;
9. `volcano`.

Across those nine owner classes, the provider defines exactly **11 owner-scoped ability roots**. `Void Cloak` owns three; each other relic owns one.

See [`ABILITY-INVENTORY-0.1.1-RELEASE-BOUNDED.md`](ABILITY-INVENTORY-0.1.1-RELEASE-BOUNDED.md).

Rank/stat modifiers, XP sources, cooldown values, packets, spawned projectiles/entities, status effects and downstream consequences are not counted as additional semantic identities.

## Provider-native reachability

Every one of the nine relic owner classes constructs a provider loot definition in the public 0.1 source line:

- `Mask of Rage`, `Volcano`, `Fire Plate`, `Ring of the Flame Kindler` → Relics `THE_NETHER` entry;
- `Void Bubble` → `THE_END`;
- `Void Vortex in Bottle` → provider `FROSTED_PRISON` + `THE_END`;
- `Vacuum Glove`, `Scouring Eye` → provider `CURSED_PYRAMID` + `THE_END`;
- `Void Cloak` → provider `CURSED_PYRAMID` + `FROSTED_PRISON` + `THE_END`.

The provider-specific entries are source-defined against Cataclysm cursed-pyramid archaeology tables and the Frosted Prison treasure table. This closes a source-level acquisition route for all nine owners. Final assembled loot mutation/frequency remains runtime QA.

## Semantic disposition

The Black Arcana semantic metric counts discrete provider-owned supernatural actions while excluding the relic item container and downstream effects.

The **11 owner-scoped ability roots** are distinct provider actions and are therefore **`COUNTED_RELEASE_BOUNDED`** for the installed 0.1.1 line.

Semantic contribution: **+11 strict objects**.

## Relationship with New Relics Fix 1.0.2

The separate current fix provider exists because the original addon targets an older Relics API. Publisher documentation for the fix states that it:

- converts legacy relic definitions to the RelicTemplate system;
- restores Curios integration/modifiers;
- adapts stats, levels, ranks, cooldowns and experience;
- restores legacy active-ability behavior;
- replaces the removed player-motion packet;
- preserves ability order and progression values.

It explicitly names five relics as compatibility targets: Void Cloak, Scouring Eye, Void Vortex in Bottle, Vacuum Glove and Void Bubble.

The fix remains a **+0 semantic bridge**. It must not be counted as a second owner of the original addon abilities.

## Authority boundaries

- L_Ender's Cataclysm owns its bosses/mobs/structures/base content.
- Reliquified L_Ender's Cataclysm owns these nine relic identities and eleven ability roots.
- Relics owns the generic progression/rank/ability framework.
- New Relics Fix 1.0.2 owns only the compatibility translation into current Relics 0.12.x.
- Black Arcana must not duplicate relic XP, rank, cooldown, loot, motion or ability settlement.
- RPG Skill Tree remains sibling authority only for its own progression/contracts and receives no Relics/Cataclysm runtime authority.

## Runtime QA remains separate

Catalog closure is not an assembled-pack PASS. Regression gates include:

- physical 0.1.1 + fix 1.0.2 + Relics 0.12.8 + Cataclysm + OctoLib boot;
- all nine relic owners instantiate and acquire correctly;
- the five explicitly transformed relics preserve their original provider-owned ability identities without duplicate processing;
- equip/unequip, XP/rank/cooldown persistence and death/relog/restart;
- active/motion abilities in dedicated multiplayer;
- no duplicate legacy + fixed ability settlement;
- boss/structure loot and provider acquisition routes.

## Result

**✅ Cataloged — `COUNTED_RELEASE_BOUNDED`.**

Current semantic inventory: **11 provider-owned relic ability roots**. Strict semantic delta: **+11**.
