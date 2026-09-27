# Reliquified L_Ender's Cataclysm — 0.1.1

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 0.1.1 / RELEASE-BOUNDED LOWER BOUND 7 / COMPLETE 0.1.1 ABILITY DENOMINATOR OPEN / +0 STRICT / RUNTIME QA SEPARATE`

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

The compatibility companion adapts the old Relics API to the current Relics 0.12.x stack. It does not create a second semantic identity for any provider ability.

## Publisher release boundary

CurseForge project `1232116` exposes two public NeoForge 1.21.1 release files:

1. File `6415478` — `reliquified_lenders_cataclysm-1.21.1-0.1.jar`, uploaded 2025-04-12, changelog: initial release;
2. File `6882649` — `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`, uploaded 2025-08-13, changelog: compatibility fix for OctoLib 0.6.

Official project page:
`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm`

Exact 0.1.1 file page:
`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm/files/6882649`

Exact initial 0.1 file page:
`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm/files/6415478`

The 0.1.1 changelog is compatibility-only, but a changelog is **not** accepted as proof that no unlisted content/root exists. Installed-JAR ↔ publisher-JAR byte equality is also not established, and an exact public 0.1.1 source revision is unavailable. Therefore 0.1.1 is not promoted to a closed semantic denominator.

## Public initial-release source checkpoint

Official repository:
`Octo-Studios/reliquified-lenders-cataclysm`.

Release-day source checkpoint:
`291f066c0471e44f50fe78ea8e7d786f6775446e` on branch `1.21.1`, dated 2025-04-12.

At that checkpoint:

- `minecraft_version=1.21.1`;
- `mod_id=reliquified_lenders_cataclysm`;
- `mod_version=0.1`;
- license metadata is All Rights Reserved;
- `ItemRegistry` registers five provider relic items;
- localization and relic definitions expose seven provider-owned ability roots.

This public initial-release source is valid evidence for a **release-line lower bound**, not for exact-current 0.1.1 completeness.

## Confirmed lower-bound ability inventory

| # | Relic owner | Ability ID | Localized ability name | State |
|---:|---|---|---|---|
| 1 | Scouring Eye | `glowing_scour` | Pursuit | confirmed baseline |
| 2 | Void Vortex in Bottle | `spawn_vortex` | Void Tornado | confirmed baseline |
| 3 | Void Cloak | `void_invulnerability` | Invulnerability | confirmed baseline |
| 4 | Void Cloak | `void_rune` | Call of the Void | confirmed baseline |
| 5 | Void Cloak | `seismic_zone` | Final Cry | confirmed baseline |
| 6 | Vacuum Glove | `vacuum_slowdown` | The Edge | confirmed baseline |
| 7 | Void Bubble | `protective_bubble` | Protective Bubble | confirmed baseline |

The five known owners therefore establish **at least seven** provider-owned Relics ability roots.

Semantic disposition: **`LOWER_BOUND 7 / +0 STRICT`**.

## Current-pack runtime corroboration

Project Library runtime log `latest(20260908-134522).log` records the compatibility coremod remapping legacy Relics references for exactly these five loaded relic item classes:

- `items/relics/back/VoidCloakItem`;
- `items/relics/charm/ScouringEyeItem`;
- `items/relics/charm/VoidVortexInBottleItem`;
- `items/relics/hands/VacuumGloveItem`;
- `items/relics/head/VoidBubbleItem`.

The same log contains ten matching transformation lines across early/main and modloading-worker phases and no additional `reliquified_lenders_cataclysm/items/relics/` class name.

This is strong current-pack corroboration that the known five relic classes are active in the assembled stack. It is **not** promoted to a complete semantic denominator because the compatibility transform log is not itself a formal registry enumeration: an additional ability/root could exist outside the transformer's covered/logged surface.

## Later-development exclusion

The public source branch continued development after the initial release and later introduced additional relics while the development property temporarily still read `0.1`, followed by commit `d7df82b857158a68d2c3430605d2a15137dc31ad` (`Version Bump [0.1 -> 0.2]`).

Those later WIP relics are not backfilled into the current lower bound. They prove that the moving branch cannot be treated as exact 0.1.1 authority.

## Baseline acquisition evidence

At the initial-release source checkpoint all five baseline owners have Relics `LootData` routes:

- Scouring Eye — Cursed Pyramid / The End;
- Void Vortex in Bottle — Frosted Prison / The End;
- Void Cloak — Cursed Pyramid / Frosted Prison / The End;
- Vacuum Glove — Cursed Pyramid / The End;
- Void Bubble — The End.

`RECLootEntries` defines Cataclysm-specific Cursed Pyramid and Frosted Prison loot targets. This closes source-level acquisition for the seven baseline roots only; it does not close a complete current 0.1.1 denominator or assembled-world loot behavior.

## Ownership boundary

- L_Ender's Cataclysm owns bosses, structures, drops and source mechanics.
- Relics owns generic relic progression, levels/ranks, ability framework state and cooldown/XP machinery.
- Reliquified L_Ender's Cataclysm owns its provider relic/ability identities.
- New Relics Fix 1.0.2 owns compatibility adaptation from the old Relics API to the current Relics 0.12.x stack and does not mint duplicate semantic identities.
- Black Arcana must not duplicate relic progression, cooldowns, provider ability execution or Cataclysm causal ownership.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates exposed through real contracts.

## Closure gate

Promote this provider from ⚠️ only when the **complete current 0.1.1 semantic action surface** is closed by one of:

1. exact 0.1.1 source matching the published/current artifact;
2. bounded exact 0.1.1 artifact evidence that enumerates the complete provider ability registry without violating clean-room constraints;
3. deterministic current-pack registry/runtime evidence that proves all provider-owned relic ability roots and excludes hidden/additional roots.

A publisher changelog and a compatibility-fix target list are corroboration, not completeness proofs.

## Runtime and compatibility QA remains separate

Even after catalog closure, runtime validation remains separate for:

- dedicated-server startup with physical 0.1.1 + fix 1.0.2 + Relics 0.12.8 + Cataclysm 3.33 + OctoLib 0.6.2;
- Curios equip/unequip and stale-modifier behavior;
- XP/rank/level persistence across relog/restart;
- cooldown persistence and exactly-once expiry;
- active abilities in remote multiplayer;
- motion/network behavior restored by the compatibility fix;
- boss kill/loot causal deduplication;
- live assembled loot injection and survival acquisition.

## Result

**⚠️ Partial / conditioned.**

Current evidence establishes **at least 7 provider-owned Relics ability roots across 5 baseline relic owners**.

Strict semantic contribution remains **+0** until exact-current completeness is proven.
