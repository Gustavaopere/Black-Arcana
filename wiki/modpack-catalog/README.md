# Modpack Magic Catalog — Phase 2

Status: `IN PROGRESS`

This directory is the canonical Phase 2 inventory for every magic-relevant top-level component in the current Black Arcana modpack.

## Canonical checkpoints

- Phase 1 — architecture/plans/Wiki structure — merged through PR #61 at `main@edcc9f8cf1d582681d4b7d2aa1facbcb39b99ae9`.
- Phase 2 baseline — provider inventory + first granular catalogs + capability matrix — merged through PR #62 at `main@17f87619bc8ed71023bc80d0adb752c13dc8c6c4`.
- Phase 2 coherent checkpoint through PR #74 — merged at `main@aafea4b7e49dc5571ac006b3202be61862326e63`.
- Phase 2I provider checkpoint through PR #75 — merged at `main@12f752eab7d6fc2861fb2c6e722b70c33bf82cf5`, including Vampirism Integrations, Werewolves, Goety, Goety addons, Malum evidence reconciliation and major Hexalia inventories.
- Phase 2J Toxony checkpoint — merged through PR #78 at `main@15f03291bc1d2955dc7faab8cfa4ef4eb991f4af`; exact 0.10.7 Toxicity/Oil/Mutagen/Affinity factual catalog and provenance boundary are canonical.
- Phase 2K Mobstein checkpoint — merged through PR #79 at `main@3fa87ec0c43b4e57e06b540642f99ef258459358`; exact installed 5.4.4 artifact plus publisher-public resurrection/anatomy/experiment/structure coverage are canonical under the ARR/public-only boundary.
- Phase 2L Apprentice's Codex checkpoint — merged through PR #80 at `main@4f45a0a1a3442d75fc11b2d5e6186848870377a5`; exact installed `0.9.7.1` identity and exact source pin `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, with 83/83 spell pages and provider-wide registry/acquisition/compat coverage complete at source-catalog level; full runtime QA remains separately pending.
- Phase 2M Cataclysm: Spellbooks checkpoint — exact installed `1.1.13-1.21` Beta identity and current publisher 65-spell scale are pinned; the official public repository remains `1.1.11-1.21`, so a 34-registration source baseline is cataloged separately and the exact current 65-entry registry remains fail-closed pending an inspectable 1.1.13 artifact or matching source.
- 25/09 current physical-Magic reconciliation — sibling `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` has **50 current status-prefixed rows whose physical category path contains `Magic`**, all mapped to provider directories after ownership-name normalization. Effective state is **46 ✅ cataloged / 4 ⚠️ partial-conditioned**: Tombstone contributes 10 actions that are now `COUNTED_EXACT` after physical↔publisher SHA-1 equality was closed; it remains partial because additional config-sensitive castables are unresolved. Gaze remains a separate ⚠️ magic provider because its current sibling dossier is categorized under `Addons/`, outside this physical-category count. **Traveloptics is absent from the current sibling modlist/dossier tree and is retained only as historical Phase 2BS evidence; it is not a current provider blocker.** Companions +9, Crystal Chronicles +1, Relics +41 and Tombstone +10 keep the strict reconstructible minimum at **1443**. The technical denominator remains `PENDING REBASE`.
- 27/09 current physical-Magic reconciliation — sibling `neoforge-rpg-skilltree@82d0d551f34d20363201f5b71f0ad91a141cbe56` has **84 rows whose category field contains `Magic`**, all **84/84 mapped** into Black Arcana as **72 ✅ + 12 ⚠️**. The +17 delta from the prior 67-row snapshot contains 11 already-cataloged providers plus six newly mapped providers: Reliquified L_Ender's Cataclysm, ShadowsZ, Simply Swords: Cataclysm, Simply More, Simply Swords and Waystones. Reliquified L_Ender's Cataclysm 0.1.1 is ✅ `COUNTED_EXACT 7`, and Waystones 21.1.45 is ✅ `COUNTED_SOURCE_PINNED 3` after complete exact-version source action-surface reconciliation. ShadowsZ 1.1.9 has an exact 10-root semantic inventory but remains +0 strict until deployed attunement/Fusion state is captured. Simply More Alpha 5 now has an exact hash-matched **24-action current-pack denominator** (10 active API + 13 legacy direct-use + 1 shared Mimicry), but remains +0 strict until deployed Awakening/acquisition/Mimicry/config reachability is closed. The reconstructible strict minimum is now **1687**. Canonical structural tree: **115 = 101 ✅ + 14 ⚠️**. See `meta/PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md`.
- Subsequent Phase 2 documentation is merged incrementally when coherent and CI-green; an incremental merge does not mean the complete catalog is finished.

The Phase 2 baseline established the magic-relevant registry and a first set of provider pages, while multiple exact spell/glyph/ritual/power inventories remain explicitly incomplete.

## Single canonical provider tree

All provider-owned catalog data lives under:

`wiki/modpack-catalog/providers/`

The old `wiki/providers/` tree was consolidated into this catalog and must not be recreated. Unique technical/source-audit material from that tree is preserved inside the appropriate provider under `audits/` or `TECHNICAL-AUDIT.md`.

Global catalog metadata lives under:

`wiki/modpack-catalog/meta/`

including the current provider inventory, deduplication policy and audit queue.

`meta/PROVIDER-AUDIT-QUEUE.md` remains the historical 103-provider queue from the older physical baseline. The 22/09 sibling re-audit has already surfaced magic-relevant components outside that frozen set, so the queue denominator is **PENDING REBASE**. Narrow status overlays may be used during incremental provider work to avoid destructive whole-table rewrites. Current overlays:

- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-GOETY-ADDONS.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-GOETY-ADDONS.md) — prevails only for `goety_cataclysm` and `goetyiron`;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2J.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2J.md) — prevails for base `goety`, `malum`, `hexalia` and `toxony` until integral queue regeneration;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2K.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2K.md) — prevails only for `mobstein` until integral queue regeneration;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2L.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2L.md) — prevails only for `apprenticecodex`, while preserving its explicit runtime-QA flags;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2M.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2M.md) — prevails only for `cataclysm_spellbooks`, advancing the public/source baseline without pretending that the exact 1.1.13 spell table is resolved.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-HAZEN-N-STUFF.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-HAZEN-N-STUFF.md) — prevails for `hazennstuff`, closing the exact release-pinned spell inventory while assembled-pack runtime QA remains fail-closed.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-CREATE-WIZARDRY.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-CREATE-WIZARDRY.md) — prevails for current physical `create_wizardry` 1.21.1-0.5.1-pre1, closing it as source-pinned host-spell automation with zero provider-owned spell identities while assembled-pack runtime QA remains fail-closed.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-IRONS-APOTHIC.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-IRONS-APOTHIC.md) — prevails for `irons_apothic` 2.2.2, closing the exact source-pinned affix/gem bridge surface with zero provider-owned spell registrations while assembled-pack runtime QA remains fail-closed.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-CORAIL-TOMBSTONE.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-CORAIL-TOMBSTONE.md) — prevails for Tombstone 9.5.6; physical Project Library SHA-1 equals exact publisher File `8842741`, so **10 `COUNTED_EXACT` prayer/Ritual-Flute actions** are strict-counted, while 12 config-sensitive castable magic-item action families remain conditional.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-RELICS.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-RELICS.md) — closes Relics 0.12.8 at exact physical/publisher equality with 39 base abilities + 2 distinct synergies = **41 `COUNTED_EXACT` provider powers**; runtime/config QA remains fail-closed.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-FANTASY-ARMOR.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-FANTASY-ARMOR.md) — closes Fantasy Armor 1.2.4 as passive gear/effect magic with +0 semantic actions.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-ENCHANTMENT-DESCRIPTIONS.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-ENCHANTMENT-DESCRIPTIONS.md) — closes Enchantment Descriptions 21.1.11 as client presentation only with +0.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-A-GOOD-PLACE.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-A-GOOD-PLACE.md) — closes A Good Place 1.2.5 as client placement-animation presentation with +0.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-DUNGEONS-DELIGHT.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-DUNGEONS-DELIGHT.md) — closes Dungeon's Delight 1.5.1 as effect/enchantment/food support with +0.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-ACOLYTE.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-ACOLYTE.md) — closes Acolyte 1.0.3 at +0 provider-owned spells while preserving Iron's ownership.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-COMPANIONS.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-COMPANIONS.md) — closes nine source-pinned Companions Magic Book actions.
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-CRYSTAL-CHRONICLES.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-CRYSTAL-CHRONICLES.md) — closes one source-pinned Crystal Chronicles spell while runtime Alpha QA remains fail-closed.

Capability-matrix deltas follow the same narrow-overlay rule:

- [`meta/CAPABILITY-MATRIX-DELTA-GOETY.md`](meta/CAPABILITY-MATRIX-DELTA-GOETY.md) supersedes only Goety-specific evidence clauses, reconciling the public 123-entry 3.1.0/3.1.1 Focus registry with the legacy 110-name Wiki subset while keeping exact 3.1.4 mechanics fail-closed;
- [`meta/CAPABILITY-MATRIX-DELTA-TOXONY.md`](meta/CAPABILITY-MATRIX-DELTA-TOXONY.md) records Toxony's current semantic delta;
- [`meta/CAPABILITY-MATRIX-DELTA-MOBSTEIN.md`](meta/CAPABILITY-MATRIX-DELTA-MOBSTEIN.md) records Mobstein's corporeal-resurrection/anatomy/experiment overlap;
- [`meta/CAPABILITY-MATRIX-DELTA-APPRENTICE-CODEX.md`](meta/CAPABILITY-MATRIX-DELTA-APPRENTICE-CODEX.md) records Apprentice's Codex overlap, especially with Familiars & Divination, sensing, storage, mobility and provider-owned alternative casting surfaces;
- [`meta/CAPABILITY-MATRIX-DELTA-CATACLYSM-SPELLBOOKS.md`](meta/CAPABILITY-MATRIX-DELTA-CATACLYSM-SPELLBOOKS.md) records the current provider-level and old-source-baseline overlaps for Abyssal, Technomancy, Sand, Fire/Ignis, Void/gravity, summons and battlefield control while keeping unknown 1.1.13 content fail-closed.
- [`meta/CAPABILITY-MATRIX-DELTA-IRONS-APOTHIC.md`](meta/CAPABILITY-MATRIX-DELTA-IRONS-APOTHIC.md) records Iron's Apothic school/level/mana/effect/trigger/imbued/loot bridge overlap without reclassifying external Iron's spells as provider-owned identities.
- [`meta/CAPABILITY-MATRIX-DELTA-CORAIL-TOMBSTONE.md`](meta/CAPABILITY-MATRIX-DELTA-CORAIL-TOMBSTONE.md), [`CAPABILITY-MATRIX-DELTA-RELICS.md`](meta/CAPABILITY-MATRIX-DELTA-RELICS.md), [`CAPABILITY-MATRIX-DELTA-FANTASY-ARMOR.md`](meta/CAPABILITY-MATRIX-DELTA-FANTASY-ARMOR.md), [`CAPABILITY-MATRIX-DELTA-ENCHANTMENT-DESCRIPTIONS.md`](meta/CAPABILITY-MATRIX-DELTA-ENCHANTMENT-DESCRIPTIONS.md), [`CAPABILITY-MATRIX-DELTA-A-GOOD-PLACE.md`](meta/CAPABILITY-MATRIX-DELTA-A-GOOD-PLACE.md), [`CAPABILITY-MATRIX-DELTA-DUNGEONS-DELIGHT.md`](meta/CAPABILITY-MATRIX-DELTA-DUNGEONS-DELIGHT.md) and [`CAPABILITY-MATRIX-DELTA-CRYSTAL-CHRONICLES.md`](meta/CAPABILITY-MATRIX-DELTA-CRYSTAL-CHRONICLES.md) preserve the corresponding current ownership/deduplication boundaries.

## Authority order

1. Current physical modlist evidence is authoritative for **presence, JAR identity, mod id, runtime name and runtime version**. The former **595 top-level / NeoForge `21.1.248`** snapshot is now historical. The current sibling authority at `neoforge-rpg-skilltree@82d0d551f34d20363201f5b71f0ad91a141cbe56` contains both status-prefixed current physical dossiers and uncategorized legacy/export Markdown files. Legacy files and their older top-level counts are not silently promoted into the current physical denominator. Until the integral magic-provider queue is regenerated, each newly certified dossier is a provider-specific physical override; internal `jarjar` dependencies do not count as top-level providers.
2. Current Notion pages and project guides provide ecosystem classification, gameplay context and known compatibility notes.
3. Official/public documentation, public APIs, changelogs and clean-room observable behavior provide granular spell/glyph/ritual/power facts.
4. External source code may only inform an implementable specification when the exact license permits that use and the provenance ledger requirement has already been satisfied.

Old guide versions never override the current JAR/runtime identity. A physical version update does not revalidate an old API/hook automatically.

A source/version pin may still be useful for factual cataloging when provenance is explicitly recorded, but a license conflict or current-source mismatch blocks promotion of source internals into Black Arcana implementation authority.

## Catalog unit

A provider is not automatically a spell provider. Every relevant component is classified before granular extraction:

- `ENGINE / PRIMARY PROVIDER`
- `SPELL PROVIDER / CONTENT ADDON`
- `ARS GLYPH / SYSTEM PROVIDER`
- `RITUAL / POWER / SUPERNATURAL PROVIDER`
- `GEAR / ENCHANT / SUPPORT CONTENT`
- `BRIDGE / COMPAT / PROGRESSION`
- `LIBRARY / API / VFX / SCRIPTING`

Only components that expose discrete player-facing capabilities require a spell/glyph/ritual/power catalog. Bridges and libraries are still listed because they can change authority, acquisition, UI, animation, resource routing or deduplication.

When granular verification disproves a baseline classification, `CLASSIFICATION-CORRECTIONS.md` is the canonical correction overlay until the registry table is regenerated.

## Provider-native hierarchy

The first directory dimension is provider ownership. The second uses the strongest stable native classification available for that provider.

Examples:

- Iron's: `providers/irons-spells/<school>/<spell>.md`;
- Asterism/Paladin/Dreamless and other school-based Iron's addons: `providers/<addon>/<school>/<spell>.md`;
- Apprentice's Codex: `providers/apprentice-codex/<school>/<spell>.md` for its 83 Iron's-native spells, plus provider-wide item/block/effect/attribute, School Affinity, acquisition and compatibility inventories;
- Cataclysm: Spellbooks: `providers/cataclysm-spellbooks/` separates exact installed/current publisher evidence from `SOURCE-1.1.11-BASELINE.md`; the exact 1.1.13 material is retained as historical/hash-matched control, while current 1.1.14 revalidation is recorded separately; stale source rows are never promoted across release boundaries;
- Ars Nouveau: `providers/ars-nouveau/glyphs/forms|effects|augments/<glyph>.md`, plus `rituals/` and `systems/`;
- Goety: Focuses / rituals / brews / servants / systems;
- Goety Cataclysm and Goety Iron: separate addon-provider directories; they are not folded into Goety's base Focus count;
- Malum: Spirit Rites / Geas-Pacts / spirits / systems;
- Hexalia: brews / rituals / infusions / mutations / processing / censer / items;
- Toxony: effects / oils / mutagens / processing, with Toxicity/Tolerance/Affinity progression documented as provider systems;
- Mobstein: corporeal resurrection / resurrected mobs / anatomical processing / surgery / subject assembly / failed experiments / structures-bosses-acquisition.

No category is invented merely to make the directory tree look symmetrical.

## Per-capability contract

Where applicable each capability receives:

- real provider + mod id + current JAR/version;
- real registry/content id when publicly verifiable;
- school/domain/category;
- semantic role;
- level/tier/rarity;
- resource and cost;
- cooldown;
- cast/channel time;
- range/area/duration;
- damage/healing/control/summon/world-effect values or formulas;
- acquisition/learning/crafting/loot/progression;
- authority and causal owner;
- relevant VFX/animation/audio;
- compatibility/bridge behavior;
- provenance and confidence.

Unknown data is written as `UNVERIFIED`, `NÃO VERIFICADO` or `TBD`, never inferred.

Existing content remains mandatory even when Black Arcana will not modify it. `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA` is a valid catalog state.

## Ars Nouveau rule

Ars Nouveau is compositional. Phase 2 catalogs forms, effects, augments, rituals and other finite primitives, then maps the capabilities they can compose. It does **not** enumerate every possible player-authored spell recipe.