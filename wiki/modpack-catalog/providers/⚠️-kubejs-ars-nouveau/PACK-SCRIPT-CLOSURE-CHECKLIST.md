# KubeJS Ars Nouveau 1.3.2 — pack-script closure checklist

Status: `CURRENT PHYSICAL FRAMEWORK IDENTIFIED / SIX RECIPE SCHEMAS BOUNDED / CURRENT SERVER-SCRIPT MUTATIONS REQUIRED`

## Purpose

Close the current pack's concrete Ars Nouveau recipe mutations without confusing recipe customization with new spell/glyph identity.

## Already closed — do not redo

- JAR `kubejsarsnouveau-1.3.2.jar`;
- mod id `kubejsarsnouveau`;
- runtime `1.3.2`;
- physical SHA-1 `f39f4f409e628731be551fd961fac2964768d358`;
- current KubeJS `2101.7.2-build.377`;
- current Ars Nouveau `5.13.1`;
- official CurseForge file `7181937`;
- public source is only versioned through 1.3.1 at inspected HEAD `18278a05d27def7200158a6d08516d5f22318e44`;
- framework exposes six Ars recipe schemas rather than a new glyph/spell registry.

## Required current pack inputs

Capture from the exact current assembled instance:

1. `kubejs/server_scripts/**`;
2. any generated/imported JS loaded into those server scripts;
3. `kubejs/data/**` when scripts write or ship Ars recipes there;
4. current KubeJS startup log only as corroboration of script load state.

Preserve file paths and hashes when possible.

## Recipe audit

Search for Ars recipe mutation through:

- `ServerEvents.recipes`;
- `event.remove` / `event.replaceInput` targeting Ars recipes;
- `ars_nouveau:enchanting_apparatus`;
- `ars_nouveau:enchantment`;
- `ars_nouveau:crush`;
- `ars_nouveau:imbuement`;
- `ars_nouveau:glyph`;
- `ars_nouveau:caster_tome`;
- equivalent builder syntax exposed by the installed KubeJS version.

For every concrete mutation, record:

- recipe ID;
- script file and line/range;
- target/output ID;
- ingredients/reagent/pedestal list;
- Source/XP cost when present;
- conditions and replacement/removal behavior;
- whether it changes survival reachability of an already cataloged glyph/spell/item.

## Glyph rule

Do not count a scripted glyph recipe as a new glyph.

The framework's documented glyph schema changes the recipe for an **existing valid Ars glyph**. If a script references an unknown glyph ID, treat it as invalid/stale until Ars itself proves a registered glyph object.

## Caster Tome rule

A scripted Caster Tome packages a list of spell-part IDs into a tome/item recipe. Record the configured spell recipe when useful for gameplay documentation, but do not create a second semantic identity for each tome unless some other provider actually registers a distinct spell object.

## Reachability / economy

Recipe scripts can still alter strict eligibility of existing Ars content. For affected objects, re-evaluate:

- survival acquisition;
- Source cost;
- XP cost;
- removed/replaced recipes;
- tome-only or item-only availability;
- reload/data-pack conditions.

## Zero-semantic closure

The framework contribution remains **+0 semantic identities** even when current scripts exist, as long as the installed addon surface remains recipe-only.

What remains open is the exact **recipe/reachability configuration**, not an unknown count of new spells.

If an exact 1.3.2 JAR audit later exposes a registration API beyond the documented recipe schemas, reopen this conclusion and catalog that surface separately.

## Current result

- provider-owned spell/glyph semantic contribution: **+0**;
- current recipe/tome mutation inventory: **UNVERIFIED**;
- state: **⚠️ partial / conditioned**.
