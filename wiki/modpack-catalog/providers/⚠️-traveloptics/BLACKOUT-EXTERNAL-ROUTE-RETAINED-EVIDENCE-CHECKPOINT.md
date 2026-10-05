# Traveloptics Blackout — retained external-route evidence checkpoint

Status: `NO PRESERVED LITERAL / OBJECT-SPECIFIC EXTERNAL ROUTE FOUND / GENERIC EXTERNAL FILTERS UNRESOLVED / CURRENT PACK ABSENCE NOT PROVEN / FAIL-CLOSED`

## Purpose

This checkpoint narrows the remaining external-acquisition exception space for `traveloptics:blackout`.

The exact publisher File `6342780` provider-owned direct and built-in generic loot surfaces are already excluded by `BLACKOUT-GENERIC-LOOT-EXCLUSION.md`.

The unresolved question is whether the assembled pack adds an external route through KubeJS, datapacks, progression/reward logic or another versioned project-owned surface.

This checkpoint records only what is preserved and auditable now. It does **not** convert missing retained evidence into proof that no current-pack route exists.

## Versioned repository search — 2026-10-05

Current repositories checked:

- `Gustavaopere/Black-Arcana`;
- `Gustavaopere/neoforge-rpg-skilltree`.

The bounded search looked for literal/object-specific references to `blackout` and `traveloptics` in versioned code/script/data surfaces.

Black Arcana does contain Traveloptics references in `src/catalogQaProbe/java/dev/gustavopere/blackarcana/qa/catalog/CatalogRuntimeEvidence.java`. That source is a read-only runtime evidence probe: it observes mod presence and the two bounded Traveloptics loot-modifier serializer registry IDs. It does not grant spells, build loot tables, inject recipes or implement acquisition.

After excluding that observational QA surface, no **literal/object-specific acquisition route** for `traveloptics:blackout` was identified in the versioned Black Arcana or sibling project surfaces checked.

A follow-up current-tree audit now closes that exception for the **versioned project-owned repositories**. At Black Arcana `4749aac3...` and sibling `de80b186...`, no `SpellFilter`, `RandomizeSpellFunction`, `spell_filter` or `randomize_spell` route is versioned. The sibling's only runtime GLM is `rpgskilltree:reward_risk`, which scales already-generated loot and does not create spell/scroll identities; its Iron's progression adapter gates casting/inscription and awards mastery but does not grant spells. The sibling has no `server_scripts` tree and only two duplicated Volcanoes integration-template `.js` files; Black Arcana has zero versioned `.js` files and zero server/startup-script paths. This excludes the **current versioned project-owned generic route**, while the actual assembled external KubeJS/datapack/mod route remains unresolved because those physical surfaces are not captured. See [`BLACKOUT-VERSIONED-GENERIC-ROUTE-AUDIT.md`](BLACKOUT-VERSIONED-GENERIC-ROUTE-AUDIT.md).

## Project / Library retained-source search

The retained Project/Library corpus was searched for:

- exact `traveloptics:blackout`;
- `blackout` + `traveloptics`;
- Traveloptics references associated with `server_scripts`;
- Traveloptics references associated with `global_loot_modifiers`;
- Traveloptics references associated with datapack surfaces.

Matches are runtime/debug logs, physical modlists or catalog/project documentation. No retained source artifact was found that establishes an external Blackout grant.

A direct Library file inventory for `.js`, `.json` and `.toml` artifacts dated 2026-08-15 through 2026-10-05, filtered for KubeJS/server/startup script, datapack/data, loot, Traveloptics or Blackout path/name markers, returned **0 retained source files**.

This is a preservation result, not an assembled-pack absence result. The current KubeJS/datapack tree has not been authoritatively captured.

## Runtime logs are not acquisition evidence

Historical runtime logs do prove that `traveloptics:blackout` registered in multiple August assembled boots, including the 2026-08-19 modified-runtime observation.

Registry/attribute presence does not establish:

- a survival acquisition source;
- a scroll/item reward;
- a progression grant;
- a recipe;
- a loot injection;
- a KubeJS grant;
- a current-world checkpoint demonstrating acquisition.

Those logs therefore remain identity/runtime-presence evidence only.

## Current Gate 3 disposition

Retained evidence now supports the following bounded statement:

- exact File `6342780` provider direct route: **EXCLUDED**;
- exact File `6342780` provider built-in generic random-spell route: **EXCLUDED**;
- Black Arcana literal/object-specific external route: **NOT FOUND AFTER EXCLUDING THE OBSERVATIONAL QA PROBE**;
- sibling literal/object-specific external route: **NOT FOUND IN THE SEARCHED VERSIONED SURFACES**;
- current versioned project-owned generic school/global filter route: **EXCLUDED IN AUDITED REPOSITORY SURFACES**;
- assembled-pack external school/global filter route: **UNRESOLVED — physical KubeJS/datapack/other-mod surfaces are not captured**;
- retained Library KubeJS/datapack source route: **NOT PRESERVED / NOT FOUND**;
- actual assembled current-pack external route: **UNVERIFIED**;
- current physical Traveloptics-only delta route: **UNVERIFIED**.

Therefore Blackout remains:

`REGISTERED / UNIQUE / NON-CRAFTABLE / NON-LOOTABLE IN EXACT ALPHA / NO PRESERVED LITERAL ROUTE FOUND / GENERIC EXTERNAL FILTERS UNRESOLVED / CURRENT-PACK SURVIVAL REACHABILITY UNVERIFIED`.

## What can close the gate

Gate 3 requires one of these current authoritative packets:

1. **positive route evidence**
   - current assembled script/datapack/progression source identifies a route resolving specifically to `traveloptics:blackout`; or
   - runtime/world evidence demonstrates the concrete survival mechanism and prerequisite object/entity/config.

2. **negative complete-pack evidence**
   - authoritative capture of the current KubeJS/datapack/progression surfaces plus exact-current Traveloptics content/runtime evidence sufficient to exclude every supported survival route.

A search of retained evidence alone is not enough for negative complete-pack closure.

## Catalog consequence

No semantic count changes.

No spell status is promoted.

Traveloptics remains **⚠️ partial/conditioned** and Blackout remains the unresolved object-level acquisition exception.

Black Arcana must not create, synthesize or repair a Blackout acquisition route merely to close the catalog.
