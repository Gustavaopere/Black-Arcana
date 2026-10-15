# Eidolon: Repraised 0.5.0.2 — physical publisher packaged chants and ritual recipes

**✅ `COUNTED_EXACT` for 42 SHA-equal *packaged recipe identities* (18 chants + 24 rituals) only. ⚠️ Not a loaded RecipeManager, executable spells or Survival PASS.**

## Release and byte-for-byte authority

- Sibling modlist `neoforge-rpg-skilltree@9e6436edb0049a8dcc4e47165db0f6850e5efa68`, physical #246: `eidolon_repraised-1.21.1-0.5.0.2.jar`, mod ID `eidolon_repraised`, NeoForge Minecraft 1.21.1.
- Official CurseForge project **870250**, file **8064602** (May 9, 2026), equivalent official Modrinth version **e82la8yu** of project `eWX2m1eM`. Publisher version 0.5.0.4/0.5.0.5 is **not installed**.
- Exact installed/publisher SHA-1 **`1f05ffd2f9fa672dc2ecff3c32de092cdbcde989`**; size **4,050,310 bytes**; SHA-256 **`8acd575046f7446dcdd4640c83b3022150ab92e5f25878b3b330e98358563bac`**.
- [Independent SHA-gated physical package workflow #38669010587](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38669010587): **SUCCESS**, eight fail-closed fixture tests PASS, exact SHA1 verified, all JSON names and schema types/relationships checked, 0 deviations. The first RED physical run [#38668904094](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38668904094) caught a false negative: single summons omit `count`; the fixed proof permits implicit one and requires explicit three for multi-summons. Source pin `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8` confirmed this representation, but publisher bytes are the final authority.

## Binary packaged identities

| Physical data namespace | Count | Evidence |
|---|---:|---|
| `data/eidolon_repraised/recipe/*.json` type `eidolon_repraised:chant` | **18/18** | Exact recipe filename + internal namespaced spell ID + ordered signs |
| `data/eidolon_repraised/recipe/rituals/*.json` type `ritual_brazier` | **10/10** | Generic ritual prototype `ritual` field matches recipe stem |
| Rituals type `ritual_brazier_summoning` | **11/11** | Exact output entity IDs; 1 by default if omitted, 3 explicitly for Husk/Drowned/Slimy Slug/Raven |
| Rituals type `ritual_brazier_crafting` | **2/2** | Sapping Sword and Sanguine Amulet recipe outputs, with health requirements 20 and 40 |
| Rituals type `ritual_brazier_location` | **1/1** | `ritual_locate_catacombs`, structure identity `eidolon_repraised:catacombs` |
| Additional `chant_conversion` recipes | **4/4** | `convert_inlay_holy`, `convert_inlay_unholy`, `convert_top_hat`, `convert_disc` — *dependent conversion pathways*, not extra spells |
| **Semantic total, excluding dependent conversions** | **42/42** | **18 normal chants + 24 official ritual recipes** |

The spell Java registry was **not** independently decompiled by this workflow. The exact source lists 20 technical spell entries; `undead_lure` lacks a normal chant recipe and has an empty source `cast()` in 0.5.0.2, while `basic_incense` is a technical dummy for the incense subsystem. Neither was counted as an extra normal chant. The 10 generic `RitualRegistry` prototypes are already part of the 24 recipes, not an additional 10 spells. Data-driven summons do not imply player-owned familiars.

## Limits and authority contracts

SHA-matched JSON packaging does not certify corresponding recipe serializers were registered, that recipes entered the server `RecipeManager`, or that datapacks left them enabled. Eidolon retains full authority over SignSequences, Chant/Spell registry, mana, research, Light/Dark devotion, soul systems, ritual health/reagent/focus payments, entity spawning and artifacts. Black Arcana must never replay its resource settlement, recipe output, kill/loot or time mutations.

Manual full-pack validation of spells, mana settlement, the 11 summons, 2 health-cost crafts, Catacombs locator, Curios, multi-client concurrency, progression, server reload and save/restart remain **⚠️ Stage09 PENDING**. Stage 06.05 remains 🟡, and no RPG Skill Tree bridge is implied by static provenance. Inspection was clean-room and read-only: no JAR, source code, assets or resources from Eidolon were committed into Black Arcana.

## Catalog arithmetic

The **same 42 previously counted** `COUNTED_SOURCE_PINNED` semantic objects gain `COUNTED_EXACT` for **packaged static recipe identity only**; **+0 newly discovered roots**. The 39-provider verification campaign advances **31/39 → 32/39 exact** with **7/39** conditioned. Strict magic minima remain **1,856 global / 1,854 in scope**; total denominator unknown.
