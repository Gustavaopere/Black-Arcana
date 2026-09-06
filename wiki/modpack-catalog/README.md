# Modpack Magic Catalog — Phase 2

Status: `IN PROGRESS`

This directory is the canonical Phase 2 inventory for every magic-relevant top-level component in the current Black Arcana modpack.

## Canonical checkpoints

- Phase 1 — architecture/plans/Wiki structure — merged through PR #61 at `main@edcc9f8cf1d582681d4b7d2aa1facbcb39b99ae9`.
- Phase 2 baseline — provider inventory + first granular catalogs + capability matrix — merged through PR #62 at `main@17f87619bc8ed71023bc80d0adb752c13dc8c6c4`.
- Subsequent Phase 2 documentation is merged incrementally when coherent and CI-green; an incremental merge does not mean the complete catalog is finished.

The Phase 2 baseline established the magic-relevant registry and a first set of provider pages, while multiple exact spell/glyph/ritual/power inventories remain explicitly incomplete.

## Single canonical provider tree

All provider-owned catalog data lives under:

`wiki/modpack-catalog/providers/`

The old `wiki/providers/` tree was consolidated into this catalog and must not be recreated. Unique technical/source-audit material from that tree is preserved inside the appropriate provider under `audits/` or `TECHNICAL-AUDIT.md`.

Global catalog metadata lives under:

`wiki/modpack-catalog/meta/`

including the current provider inventory, deduplication policy and audit queue.

## Authority order

1. `modlist.txt` snapshot from 2026-09-06 is authoritative for **presence, JAR identity, mod id, runtime name and runtime version**. The snapshot contains 607 top-level entries.
2. Current Notion pages and project guides provide ecosystem classification, gameplay context and known compatibility notes.
3. Official/public documentation, public APIs, changelogs and clean-room observable behavior provide granular spell/glyph/ritual/power facts.
4. External source code may only inform an implementable specification when the exact license permits that use and the provenance ledger requirement has already been satisfied.

Old guide versions never override the current JAR/runtime identity.

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
- Ars Nouveau: `providers/ars-nouveau/glyphs/forms|effects|augments/<glyph>.md`, plus `rituals/` and `systems/`;
- Goety: Focuses / rituals / brews / servants / systems;
- Malum: Spirit Rites / Geas-Pacts / spirits / systems;
- Hexalia: brews / rituals / infusions;
- Toxony: effects / oils / mutagens.

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

## Known Phase 2 work still open

Examples include:

- finish Iron's base catalog: Ice, Lightning and Nature currently remain after the first 75/110 individual fichas;
- exact current inventories/numbers for providers such as Apprentice's Codex, Cataclysm: Spellbooks, Dreamless, Leyline and Somake;
- exact installed capability reconciliation for Goety 3.1.4, Malum 1.8.2, Eidolon, Hexalia, Toxony, Vampirism/Bloodlines/Werewolves, Mobstein and related addons;
- remaining Ars addon primitives not yet normalized to the same confidence level;
- provider-specific acquisition, IDs, costs and formulas wherever public evidence is still incomplete;
- final semantic disposition of every row in `CAPABILITY-MATRIX.md`.

## Output

The final Phase 2 product is:

`capability → provider(s) → current coverage → semantic overlap → real gap`

That matrix is the gate for Phase 3. No new Black Arcana spell is approved merely because its presentation differs from an existing provider capability.
