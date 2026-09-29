# Somake Spells 1.0.9 — exact release resource-only audit

Status: `EXACT CURSEFORGE RELEASE / RESOURCE-ONLY CLEAN-ROOM / RELEASE SHA-1 CAPTURED / PHYSICAL PACK BYTE-EQUALITY NOT YET PROVEN / REGISTRY NOT CLOSED`

## Evidence checkpoint

Temporary audit branch/HEAD:

- branch: `audit/somake-1.0.9-resource-audit-2026-09-17`;
- exact HEAD: `ed37ab8ffb0fba23ab68c3810d94fdf0c1da579c`;
- workflow: **Somake 1.0.9 Clean-room Resource Audit**;
- run: `35298734758`;
- audit job: `105456630521`;
- text-only artifact: `10529435038`;
- artifact digest: `sha256:6c21e00982ac5a5c91fb15089dffc6c4b904414cc4b7957346fb71d3a0727955`.

The workflow downloaded exact CurseForge project/file `1461634 / 8867079` through Curse Maven and retained metadata/resource evidence only. It did not use `javap`, decompile bytecode, reconstruct implementation bodies, or copy protected asset contents.

## Exact release identity

- filename: `somakespells-1.0.9-1.21.1.jar`;
- mod id: `somakespells`;
- runtime metadata: `1.0.9`;
- license: All Rights Reserved;
- exact release SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- current Black Arcana physical-pack SHA-1: **not yet available**.

Therefore this audit is exact for the publisher release artifact, but it is **not yet a cryptographic physical-pack equality proof**. The sibling modlist independently identifies the same installed filename/runtime.

## Exact metadata dependencies

The release metadata declares these required dependencies:

- NeoForge `[21.1.222,)`;
- Minecraft `[1.21.1]`;
- Iron's Spells 'n Spellbooks `[1.21.1-3.16.2,)`;
- GeckoLib `[4.6.6,)`;
- Curios `[9.2.2+1.21.1,)`;
- Placebo `[9.9.0,)`;
- Apothic Attributes `[2.9.0,)`;
- Cataclysm `[3.33,)`.

The release metadata also declares these optional dependencies:

- `legendary_monsters`;
- `gtbcs_geomancy_plus`;
- `born_in_chaos_v1`;
- `iss_magicfromtheeast`;
- `familiarslib`;
- `alshanex_familiars`;
- `mowziesmobs`;
- `tunes_n_tomes`;
- client-side `jei`.

This metadata proves dependency declarations, not which spell registrations are gated by each optional mod.

## Resource inventory

The exact release contains:

- `651` class files counted only as an aggregate;
- `613` localization keys total;
- `166` localization keys under the `spell` prefix;
- exactly `83` base `spell.somakespells.<id>` keys;
- exactly `83` matching `.guide` keys;
- `196` JSON resources under `data/somakespells/`.

JSON resource buckets:

- `damage_type=3`;
- `irons_spellbooks=17`;
- `loot_modifiers=6`;
- `loot_table=5`;
- `neoforge=2`;
- `recipe=119`;
- `tags=2`;
- `weapon_attributes=42`.

The exact resource tree still contains `data/somakespells/tags/item/school_focus/aqua.json`. That proves the tag resource exists in the release; this audit did not retain its protected membership as a reachability claim.

## 1.0.8-fix → 1.0.9 localization-surface delta

Compared with the historical 67 exact 1.0.8-fix registry IDs, the 1.0.9 localization base-key surface has 17 candidate additions and one missing historical root.

Candidate-added localization roots:

- `bloodbound_blade`;
- `comforting_lullaby`;
- `crimson_reflection`;
- `funeral_bloom`;
- `grave_sigil`;
- `procession_of_souls`;
- `sacred_phoenix_blessing`;
- `soul_bastion`;
- `soul_latch`;
- `soul_reprisal`;
- `soulfall_judgment`;
- `sovereign_armory`;
- `spectral_rondo`;
- `spiral_of_ruin`;
- `summon_drowned`;
- `winged_ruin`;
- `withered_rose_vortex`.

Historical root absent from the 1.0.9 localization surface:

- `summon_zombie`.

The official 1.0.9 changelog independently states that `Summon Zombie` was replaced by `Summon Drowned` and explicitly names **16 spells** in the 1.21.1 File `8867079` **New Spells** section. Those public names/school labels are materialized in [`CURRENT-1.0.9-PUBLIC-NAMED-SPELLS.md`](CURRENT-1.0.9-PUBLIC-NAMED-SPELLS.md) and corroborate a material content delta.

However **localization keys and publisher display names are not registry proof**. The 83 base-key surface and the 16-name public tranche must not be promoted to a current registry count until an authoritative current-line registry source exists.

## Red Soul / progression resource evidence

Resource/localization paths independently corroborate the public 1.0.9 Red Soul feature surface, including:

- `data/somakespells/recipe/red_soul_lantern.json`;
- `data/somakespells/recipe/alchemist_cauldron/corrupted_red_soul.json`;
- `effect.somakespells.red_soul`;
- `hud.somakespells.red_soul`;
- `item.somakespells.red_soul_lantern`;
- `item.somakespells.corrupted_red_soul`;
- multiple `message.somakespells.crimson_reflection.*` and Red Soul progression keys.

These are content/progression surfaces. They do not by themselves add independent semantic magic objects beyond any discrete spells/actions separately proven.

## Current closure consequence

This audit materially narrows the 1.0.9 revalidation:

- exact publisher release identity/hash: **closed**;
- release metadata/dependency surface: **closed**;
- resource/localization surface: **closed at path/key level**;
- current physical byte equality: **open**;
- current spell registry: **open**;
- exact optional registration predicates: **open**;
- deployed config: **open**;
- survival acquisition/reachability: **open**.

Somake remains **⚠️ Parcial / condicionado** and contributes **+0** to the strict semantic count until the current-line registry/reachability gates are closed.
