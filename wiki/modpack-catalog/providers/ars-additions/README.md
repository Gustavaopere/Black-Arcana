# Ars Additions — Ars Nouveau Extension Provider

Status: `PHASE 2Q / SOURCE-PINNED 21.3.0 CATALOG IN PROGRESS / RUNTIME+PACK QA PENDING`

## Exact installed identity

- JAR: `ars_additions-1.21.1-21.3.0.jar`
- Mod id: `ars_additions`
- Runtime/version metadata: `1.21.1-21.3.0`
- Physical SHA-1: `ce2440b606acb20b79a42bf7c6c24d163c93241f`
- CurseForge project/file: `974408` / `7646325`
- Loader/game: NeoForge 1.21.1

Physical identity comes from the current 612-entry modlist. The publisher release is the 1.21.1 NeoForge `21.3.0` file published on 2026-02-18.

## Exact source checkpoint used by Phase 2Q

Read-only factual cataloging is pinned to `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

At that commit:

- the repository `version` file is exactly `21.3.0`;
- the commit is the publisher's `ci: bump version` revision dated 2026-02-18;
- root `LICENSE` is GNU LGPL v3;
- `gradle.properties` targets Minecraft 1.21.1 / NeoForge 21.1.x and declares `mod_license=LGPLv3`;
- the source build baseline references Ars Nouveau `5.11.2.1298`, while the physical pack currently runs Ars Nouveau `5.13.1`; source semantics may be cataloged, but runtime compatibility with the newer installed Ars base remains a separate QA gate.

The matching version label/date is strong release-line evidence but is not treated as a cryptographic proof that the physical CurseForge JAR was built from this exact commit.

## Provider relationship and authority

Ars Additions extends Ars Nouveau rather than replacing it.

Ars Nouveau remains authority for:

- player mana and spell cost settlement;
- Source as the canonical Ars world/automation resource;
- spell grammar, `SpellContext`, resolver execution and glyph learning;
- Ritual framework and base Ars infrastructure such as Storage Lecterns and Imbuement/Enchanting systems.

Ars Additions owns its added glyphs, rituals, items, charms, blocks, persisted reference/warp state and addon-specific recipes. Black Arcana must not create parallel Source/mana/inventory/reference stores, replay provider effects or convert provider child execution into independent Black Arcana casts.

## Exact core Ars-facing registry surface

`ArsNouveauRegistry` registers exactly:

- **3 glyphs:** Retaliate, Mark, Recall;
- **2 rituals:** Arcane Permanence / chunk loading, Locate Structure;
- **1 perk:** Reach;
- Recall also installs provider-native Spell Turret behavior.

The addon additionally registers one `marked` mob effect. Its broader block/item/recipe/component/attachment registries are being normalized separately in this Phase 2Q tree.

## High-value overlap findings

- Mark + Recall already occupy persistent stored-target / remote-resolution territory. A Black Arcana mark/remote-cast mechanic must prove a materially distinct contract.
- Retaliate occupies event-context reactive targeting, but its executable 21.3.0 class does not itself enforce the five-second window stated in its description; this is preserved as a runtime QA divergence.
- Arcane Permanence is an actual force-loading ritual. Its existence does not weaken Black Arcana's no-force-load safety policy; Black Arcana must never infer force-load permission from another provider.
- Ender Source / remote Ars infrastructure must remain one Ars Source economy, not become a Black Arcana resource mirror.

## Current source-catalog progress

- Glyphs: **3/3 source-pinned**.
- Rituals: **2/2 source-pinned**.
- Perks: **1/1 source-pinned**.
- Mob effects: **1/1 registry identity source-pinned**.
- Charms: registry identity/count confirmed; granular event semantics in progress.
- Blocks/items/recipes/components/attachments/warp/storage/Source systems: inventory normalization in progress.

## Validation boundary

Phase 2Q is documentation/provenance/deduplication work. It does not implement an Ars Additions adapter, does not promote a Black Arcana runtime Stage and does not infer runtime/config/client/full-modpack acceptance from source inspection.
