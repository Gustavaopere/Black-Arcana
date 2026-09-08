# Ars Additions — Ars Nouveau Extension Provider

Status: `PHASE 2Q / SOURCE-PINNED 21.3.0 CATALOG COMPLETE / RUNTIME+PACK QA PENDING`

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
- Ritual framework and base Ars infrastructure such as Storage Lecterns, Wixie, Imbuement Chamber and Enchanting Apparatus.

Ars Additions owns its added glyphs, rituals, items, charms, blocks, persisted reference/warp state and addon-specific recipes. Black Arcana must not create parallel Source/mana/inventory/reference stores, replay provider effects or convert provider child execution into independent Black Arcana casts.

## Closed source-catalog surface

- Glyphs: **3/3** — Retaliate, Mark, Recall.
- Rituals: **2/2** — Arcane Permanence and Locate Structure.
- Perks: **1/1** — Reach.
- Mob effects: **1/1** — Marked.
- Charms: **12/12** with executable event semantics, charges, crafting and recharge behavior.
- Direct item registry: **26 direct items**, including **14 non-charm direct items + 12 charms**.
- Blocks/block items: **35 blocks + 35 block items**; total registered item count remains **61**.
- Block entities: **5**; custom EntityTypes: **0**.
- Data components: **11**; attachments: **4**.
- Recipe serializers/types: **5/5**.
- Stateful/provider systems source-audited: Warp Index/Stabilized Warp Index, Warp Nexus, Ender Source Jar, Source Spawner, Handy Haversack, Memory Crystal, Advanced Dominion Wand, XP Jar, Spellweave, Enchanting Wixie, Bulk Scribing and Locate Structure recipes.
- Worldgen/config source-audited: Arcane Library, Nexus Tower and Ruined Warp Portal families.
- Dormant local-weather plumbing is recorded as registered infrastructure but is not promoted as active magic without an executable production path.

Memory Crystal runtime/state semantics are confirmed, but a normal default acquisition path was not proven in the audited generated recipes/loot setup. That gap remains explicit rather than being guessed.

## High-value overlap findings

- Mark + Recall already occupy persistent stored-target / remote-resolution territory. A Black Arcana mark/remote-cast mechanic must prove a materially distinct contract.
- Retaliate occupies event-context reactive targeting, but its executable 21.3.0 class does not itself enforce the five-second window stated in its description; this remains a runtime QA divergence.
- Arcane Permanence is an actual provider force-loading ritual. Its existence does not weaken Black Arcana's no-force-load safety policy.
- Ender Source Jar uses one provider-owned Source economy keyed by owner identity; it must not become a Black Arcana resource mirror.
- Spellweave extends Ars Thread slots onto eligible non-Ars armor; RPG Skill Tree/Black Arcana must not add a second perk-slot interpretation for the same item state.
- Explorer/Nexus warp mechanics, Advanced Dominion linking, Memory Crystal state transfer and Haversack remote inventory all have provider-owned validation/persistence contracts and must not be reproduced by heuristic NBT or client-side inference.

## Validation boundary

Phase 2Q is documentation/provenance/deduplication work. `CATALOG COMPLETE` means the material source surface for this provider has been cataloged at the pinned revision; it does **not** mean the installed 21.3.0 JAR has passed runtime/config/client/full-modpack acceptance against Ars Nouveau 5.13.1.

No Ars Additions adapter is implemented by this phase and no Black Arcana runtime Stage is promoted.
