# Modpack Magic Catalog — Phase 2

Status: `IN PROGRESS`

This directory is the canonical Phase 2 inventory for every magic-relevant top-level component in the current Black Arcana modpack.

## Canonical checkpoints

- Phase 1 — architecture/plans/Wiki structure — merged through PR #61 at `main@edcc9f8cf1d582681d4b7d2aa1facbcb39b99ae9`.
- Phase 2 baseline — provider inventory + first granular catalogs + capability matrix — merged through PR #62 at `main@17f87619bc8ed71023bc80d0adb752c13dc8c6c4`.
- Exact post-merge CI for the PR #62 baseline: Black Arcana CI run `34056029588` / #1477 — `SUCCESS`.

The PR #62 checkpoint is not the end of Phase 2. It establishes the 101-component magic-relevant registry and a first set of provider pages, while multiple exact spell/glyph/ritual/power inventories remain explicitly incomplete.

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

Unknown data is written as `UNVERIFIED` or `TBD`, never inferred.

## Ars Nouveau rule

Ars Nouveau is compositional. Phase 2 catalogs forms, glyphs, augments, rituals and other finite primitives, then maps the capabilities they can compose. It does **not** enumerate every possible player-authored spell recipe.

### Ars ecosystem normalization — current pass

The second Ars pass adds/normalizes dedicated pages for:

- Ars Additions 21.3.0;
- Ars Zero 2.0.2;
- Ars Technica 2.7.6;
- Ars Creo 5.4.0;
- Ars Elemancy 1.18.3;
- Not Enough Glyphs 4.6.1;
- Ars 'n' Spells 3.2.4;
- Ars Polymorphia 1.0.3.

It also corrects four baseline classification errors without changing their current modlist identities:

- Ars Creo → bridge/compat, not a proven glyph provider;
- Ars Elemancy → gear/support, not a proven glyph provider;
- Ars 'n' Spells → cross-engine Ars↔Iron's bridge with discrete bridge rituals;
- Ars Polymorphia → Storage Lectern/Polymorph compatibility, not a spell provider.

The new evidence expands the deduplication matrix for event-triggered casting, stored-reference targeting, cross-engine spellbooks/mana, Create-integrated magic automation, geometry, gravity and randomization.

## Known Phase 2 work still open

Examples explicitly still incomplete after the baseline and this pass include:

- exact current inventories/numbers for providers such as Apprentice's Codex, Cataclysm: Spellbooks, Dreamless, Leyline and Somake;
- exact installed capability reconciliation for Goety 3.1.4, Malum 1.8.2, Eidolon, Hexalia, Toxony, Vampirism/Bloodlines/Werewolves, Mobstein and related addons;
- remaining Ars addon primitives not yet normalized to the same confidence level;
- provider-specific acquisition, IDs, costs and formulas wherever public evidence is still incomplete;
- final semantic disposition of every row in `CAPABILITY-MATRIX.md`.

## Output

The final Phase 2 product is:

`capability → provider(s) → current coverage → semantic overlap → real gap`

That matrix is the gate for Phase 3. No new Black Arcana spell is approved merely because its presentation differs from an existing provider capability.
