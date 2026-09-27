# Reliquified L_Ender's Cataclysm — 0.1.1

Status: `✅ CATALOGED / CURRENT PHYSICAL 0.1.1 / COUNTED_RELEASE_BOUNDED / 5 RELIC OWNERS / 7 PROVIDER-OWNED ABILITY ROOTS / +7 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority records:

- sibling checkpoint: `neoforge-rpg-skilltree@ac23fc1c67937deeffe982ae971c21d4f3561bc5`;
- JAR: `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`;
- mod id: `reliquified_lenders_cataclysm`;
- runtime: `0.1.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`;
- current host stack: L_Ender's Cataclysm `3.33`, Relics `0.12.8`, OctoLib `0.6.2`;
- compatibility companion: `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`.

The companion fix is a separate compatibility layer for the current Relics 0.12.x stack. It does not own a second copy of the addon ability identities.

## Publisher release boundary

CurseForge project `1232116` exposes only two NeoForge 1.21.1 release files:

1. File `6415478` — `reliquified_lenders_cataclysm-1.21.1-0.1.jar`, uploaded 2025-04-12, changelog: initial release;
2. File `6882649` — `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`, uploaded 2025-08-13, changelog: compatibility fix for OctoLib 0.6.

Official project page:
`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm`

Exact 0.1.1 file page:
`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm/files/6882649`

Exact initial 0.1 file page:
`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm/files/6415478`

No content addition is announced for 0.1.1; the publisher delta is compatibility-only. Because installed-JAR ↔ publisher-JAR byte equality has not been independently established and the exact 0.1.1 source revision is not public, the correct evidence class is `COUNTED_RELEASE_BOUNDED`, not `COUNTED_EXACT`.

## Public initial-release source checkpoint

Official public repository:
`Octo-Studios/reliquified-lenders-cataclysm`.

Release-day source checkpoint:
`291f066c0471e44f50fe78ea8e7d786f6775446e` on branch `1.21.1`, dated 2025-04-12.

At that checkpoint:

- `minecraft_version=1.21.1`;
- `mod_id=reliquified_lenders_cataclysm`;
- `mod_version=0.1`;
- license metadata is All Rights Reserved;
- `ItemRegistry` registers exactly five provider relic items;
- localization and relic definitions close exactly seven provider-owned ability roots.

This audit uses public factual registry/localization structure only. It does not copy provider implementation.

## Semantic ability inventory

The Black Arcana metric counts discrete provider-owned supernatural Relics ability roots while excluding the relic item container, stats, leveling sources, spawned entities/projectiles and downstream effects.

| # | Relic owner | Ability ID | Localized ability name | Disposition |
|---:|---|---|---|---|
| 1 | Scouring Eye | `glowing_scour` | Pursuit | counted |
| 2 | Void Vortex in Bottle | `spawn_vortex` | Void Tornado | counted |
| 3 | Void Cloak | `void_invulnerability` | Invulnerability | counted |
| 4 | Void Cloak | `void_rune` | Call of the Void | counted |
| 5 | Void Cloak | `seismic_zone` | Final Cry | counted |
| 6 | Vacuum Glove | `vacuum_slowdown` | The Edge | counted |
| 7 | Void Bubble | `protective_bubble` | Protective Bubble | counted |

The five registered relic owners therefore contain **seven** distinct provider-owned ability roots. Void Cloak owns three roots; each of the other four owners owns one.

Semantic contribution: **+7 strict objects**.

## Why 0.1.1 inherits the seven-root inventory

The release-bounded closure uses three converging facts:

1. the public initial-release source on 2025-04-12 contains exactly five registered relic owners and seven ability roots;
2. the only publisher-listed 0.1.1 change is compatibility with OctoLib 0.6;
3. the current Relics-compatibility companion documents the same five legacy relic owners as the surfaces requiring adaptation: Void Cloak, Scouring Eye, Void Vortex in Bottle, Vacuum Glove and Void Bubble.

Later public branch development added additional relics under a `0.1`/then `0.2` development line, but those later WIP additions are **not** backfilled into the published 0.1.1 inventory. This prevents the source branch from inflating the current pack denominator.

## Provider-native acquisition evidence

The same initial-release source checkpoint assigns provider-native Relics loot routes to all five owners:

- Scouring Eye — Cursed Pyramid / The End;
- Void Vortex in Bottle — Frosted Prison / The End;
- Void Cloak — Cursed Pyramid / Frosted Prison / The End;
- Vacuum Glove — Cursed Pyramid / The End;
- Void Bubble — The End.

`RECLootEntries` defines the Cataclysm-specific Cursed Pyramid and Frosted Prison loot targets. This is sufficient for catalog-level source reachability of all seven owner-scoped ability roots. It does not prove final assembled loot injection, drop frequency or survival acquisition in a particular world.

## Ownership boundary

- L_Ender's Cataclysm owns bosses, structures, drops and source mechanics.
- Relics owns generic relic progression, levels/ranks, ability framework state and cooldown/XP machinery.
- Reliquified L_Ender's Cataclysm owns the seven provider ability identities above and their Cataclysm-themed relic content.
- New Relics Fix 1.0.2 owns compatibility adaptation from the old Relics API to the current Relics 0.12.x stack; it does not mint duplicate semantic identities.
- Black Arcana must not duplicate relic progression, cooldowns, provider ability execution or Cataclysm causal ownership.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates exposed through real contracts.

## Runtime and compatibility QA remains separate

Catalog closure does **not** assert assembled-pack PASS. Current runtime validation remains fail-closed for:

- dedicated-server startup with physical 0.1.1 + fix 1.0.2 + Relics 0.12.8 + Cataclysm 3.33 + OctoLib 0.6.2;
- all five relics instantiating without linkage errors;
- Curios equip/unequip and stale-modifier behavior;
- XP/rank/level persistence across relog/restart;
- cooldown persistence and exactly-once expiry;
- active abilities in remote multiplayer;
- motion/network behavior restored by the compatibility fix;
- boss kill/loot causal deduplication;
- live assembled loot injection and survival acquisition.

## Result

**✅ Cataloged — `COUNTED_RELEASE_BOUNDED`.**

Current semantic inventory: **7 provider-owned Relics ability roots across 5 relic owners**.

Strict global semantic delta: **+7**.
