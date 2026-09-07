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
- Phase 2L Apprentice's Codex candidate checkpoint — current branch `docs/magic-catalog-phase2l-apprentice-codex`; exact installed `0.9.7.1` identity and exact source pin `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, with 83/83 spell pages and provider-wide registry/acquisition/compat coverage complete at source-catalog level. It is not canonical until PR/CI/merge complete.
- Subsequent Phase 2 documentation is merged incrementally when coherent and CI-green; an incremental merge does not mean the complete catalog is finished.

The Phase 2 baseline established the magic-relevant registry and a first set of provider pages, while multiple exact spell/glyph/ritual/power inventories remain explicitly incomplete.

## Single canonical provider tree

All provider-owned catalog data lives under:

`wiki/modpack-catalog/providers/`

The old `wiki/providers/` tree was consolidated into this catalog and must not be recreated. Unique technical/source-audit material from that tree is preserved inside the appropriate provider under `audits/` or `TECHNICAL-AUDIT.md`.

Global catalog metadata lives under:

`wiki/modpack-catalog/meta/`

including the current provider inventory, deduplication policy and audit queue.

`meta/PROVIDER-AUDIT-QUEUE.md` remains the full 103-provider queue. Narrow status overlays may be used during incremental provider work to avoid destructive whole-table rewrites. Current overlays:

- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-GOETY-ADDONS.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-GOETY-ADDONS.md) — prevails only for `goety_cataclysm` and `goetyiron`;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2J.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2J.md) — prevails only for `malum`, `hexalia` and `toxony` until integral queue regeneration;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2K.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2K.md) — prevails only for `mobstein` until integral queue regeneration;
- [`meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2L.md`](meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2L.md) — prevails only for `apprenticecodex` after Phase 2L is merged, while preserving its explicit runtime-QA flags.

Capability-matrix deltas follow the same narrow-overlay rule:

- [`meta/CAPABILITY-MATRIX-DELTA-TOXONY.md`](meta/CAPABILITY-MATRIX-DELTA-TOXONY.md) records Toxony's current semantic delta;
- [`meta/CAPABILITY-MATRIX-DELTA-MOBSTEIN.md`](meta/CAPABILITY-MATRIX-DELTA-MOBSTEIN.md) records Mobstein's corporeal-resurrection/anatomy/experiment overlap;
- [`meta/CAPABILITY-MATRIX-DELTA-APPRENTICE-CODEX.md`](meta/CAPABILITY-MATRIX-DELTA-APPRENTICE-CODEX.md) records Apprentice's Codex overlap, especially with Familiars & Divination, sensing, storage, mobility and provider-owned alternative casting surfaces.

## Authority order

1. Current physical modlist snapshot from **2026-09-07** is authoritative for **presence, JAR identity, mod id, runtime name and runtime version**. It contains **612 top-level entries including NeoForge**; internal `jarjar` dependencies do not count as top-level providers.
2. Current Notion pages and project guides provide ecosystem classification, gameplay context and known compatibility notes.
3. Official/public documentation, public APIs, changelogs and clean-room observable behavior provide granular spell/glyph/ritual/power facts.
4. External source code may only inform an implementable specification when the exact license permits that use and the provenance ledger requirement has already been satisfied.

Old guide versions never override the current JAR/runtime identity. A physical version update does not revalidate an old API/hook automatically.

A source/version pin may still be useful for factual cataloging when provenance is explicitly recorded, but a license conflict blocks promotion of source internals into Black Arcana implementation authority.

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

## Current school decisions affecting the catalog

- Celestial/Divine is not a separate school: approved future celestial content belongs to Iron's **Holy** unless another existing provider is the actual authority.
- Blood Binding is not a separate school: the existing Iron's **Blood** school is the target of the planned blood-resource reform.
- Chaos and Order remain candidate Iron's schools pending complete semantic deduplication.
- Infernal remains candidate pending full audit of Fire, Goety, Cataclysm/Ignis, Soul Fire and related providers.

## High-value providers already advanced

The granular queue plus explicit overlays remain authoritative for exact per-row status. Major audits currently include:

- Iron's base spell registry/catalog;
- Ypsilon's Fundamentalism, Asterism Arcanum, Dreamless and other audited Iron's addons;
- Eidolon: Repraised `0.5.0.2` — spells/chants/conversions/ritual recipes/research inventoried in source, runtime QA pending;
- Vampirism `1.10.13` + Bloodlines `3.0.9` + Vampiric Ageing `1.4.21` + Vampire Spells Addon `0.0.9` — provider authority/resources/actions/progression cataloged in source, runtime/inter-addon QA pending;
- Vampirism Integrations `1.10.2` — Cold Sweat eligibility and Jade discovery cataloged without inferring runtime activation;
- Werewolves `2.0.3.3` — faction/forms/actions/skills/effects/leveling/Lord/minions/refinements cataloged in source, runtime/Epic Fight QA pending;
- Goety `3.1.4` — official public inventory normalized to 110 base Focuses, 12 Wands/Staffs, 13 ritual types and 10 Research lines; exact 3.1.4 source/JAR registries/API remain unverified and fail-closed;
- Goety Cataclysm `1.21.1-1.8.2` — exact installed artifact/File ID/hash pinned and public semantic surface audited; matching 1.21.1 source revision not located and project is ARR, so granular internals remain unverified/fail-closed;
- Goety Iron `3.1` — exact installed artifact/File ID/hash and release changelog pinned; eight public servant names cataloged while source/API internals remain unverified/fail-closed;
- Malum `1.8.2` — exact version-line metadata/publisher changelog advanced Spirit Rite/Geas/spirit-resource coverage, but source-internal completion remains blocked by licensing conflict and runtime QA;
- Hexalia — public 1.3.6 source pin with MIT provenance; 8/8 brews, 19/19 player-facing Nature's Ritual recipes, 6/6 Celestial Infusions, 21/21 mutations, 12/12 Mortar recipes, 10/10 Censer combinations and major capability-bearing items audited; installed filename/runtime-version mismatch and API/runtime QA remain;
- Toxony `0.10.7` — exact installed artifact + exact public source-version pin; 5/5 harmful effects, 9/9 Oils, 7/7 Mutagen effect IDs, 11/11 Affinities, threshold selection, major Mutagen mechanics, processing and external compat overlaps audited factually; GPLv3/LGPLv3 provenance conflict, supported-API and runtime gates remain fail-closed;
- Mobstein `5.4.4` — exact installed artifact + exact CurseForge File ID 8040734 and publisher current guide/release lineage; corporeal resurrection, ten resurrected creature families, anatomy/organ extraction, Surgery Stretch + four internal modifiers, Subject Assembly, Igor + seven failed experiments, syringe family, three structures, Dr. Mobstenio and three-stage Witherstein cataloged; ARR means no source/bytecode decompilation, internal registries/API and exact Sable 2.0.5 seam remain fail-closed;
- Apprentice's Codex `0.9.7.1` — exact installed artifact + exact source pin `305ea6a...`; **83/83** spell registry IDs across nine Iron's schools have source-pinned pages, with exact **167/167 item IDs**, **20/20 block IDs**, static/dynamic effect and provider-attribute inventories, 25-slot School Affinity, acquisition surfaces and optional-compat inventory cataloged. Full 612-mod runtime/config QA remains explicit rather than inferred.

Source-pinned means the source catalog is tied to an exact revision. Release/artifact-pinned is weaker and is stated separately. Neither state means runtime validation unless that gate is separately recorded.

## Known Phase 2 work still open

Examples include:

- remaining Malum registry details that cannot be promoted safely under the current provenance conflict;
- exact runtime/API reconciliation for Hexalia, Toxony, Mobstein and Apprentice's Codex after their factual/source catalogs;
- exact current inventories/numbers for providers such as Cataclysm: Spellbooks, Leyline and Somake where exact installed internals remain incomplete;
- remaining Ars base/addon primitives not yet normalized to the same confidence level;
- pending Iron's ecosystem content/gear/compat providers listed in `meta/PROVIDER-AUDIT-QUEUE.md`;
- provider-specific acquisition, IDs, costs and formulas wherever public evidence is still incomplete;
- exact runtime/config/client QA for source-cataloged providers where explicitly recorded;
- final semantic disposition of every row in `CAPABILITY-MATRIX.md` plus its current narrow deltas.

### Next high-value provider checkpoint

Phase 2L does **not** preselect its successor. After Phase 2L is merged, the next provider checkpoint must be chosen only after a fresh read of the then-current `main`, physical modlist, Notion context and provider audit queue, preserving any parallel work already integrated. A stale “next provider” recommendation must never override that reconciliation.

## Output

The final Phase 2 product is:

`capability → provider(s) → current coverage → semantic overlap → real gap`

That matrix is the gate for Phase 3. No new Black Arcana spell is approved merely because its presentation differs from an existing provider capability.