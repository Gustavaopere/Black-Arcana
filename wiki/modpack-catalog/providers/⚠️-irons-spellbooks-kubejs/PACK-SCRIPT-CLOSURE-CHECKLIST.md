# Iron's Spellbooks KubeJS 4.0.3 — pack-script closure checklist

Status: `CURRENT PHYSICAL FRAMEWORK IDENTIFIED / EXACT 4.0.3 SOURCE PINNED / PACK STARTUP SCRIPT INVENTORY REQUIRED`

## Purpose

Close the only semantic question that the base-addon audit cannot answer: whether the exact current modpack uses Iron's Spellbooks KubeJS to register additional spells, schools or other semantic magic objects, and which ones.

## Already closed — do not redo

- JAR `irons_spells_js-4.0.3.jar`;
- mod id `irons_spells_js`;
- runtime `4.0.3`;
- physical SHA-1 `0481395c5847e2920d1425e77833bef87df63139`;
- current Iron's `1.21.1-3.16.3`;
- current KubeJS `2101.7.2-build.377`;
- exact official source pin `sentwayfarer/irons_spells_js@f3c05a102707a87ac3b8f0d2df5d2ffa5ae5b6c7`;
- base framework exposes spell/school builders rather than a fixed provider spell roster.

## Required physical script inputs

Collect from the same current assembled instance used as pack authority:

1. `kubejs/startup_scripts/**`;
2. `kubejs/server_scripts/**` when they mutate spell runtime/config/acquisition or define related progression/recipes;
3. `kubejs/client_scripts/**` only when needed to distinguish presentation-only behavior;
4. any generated or indirectly loaded KubeJS script source.

Preserve file paths and hashes when possible. Do not infer absence merely because scripts are absent from GitHub or Project search.

## Registration audit

Inspect the exact scripts for use of Iron's/KubeJS builder surfaces. For every concrete custom spell, record:

- exact `ResourceLocation`;
- script file and line/range;
- registration condition/branch;
- school ID;
- active vs disabled/commented state;
- explicit acquisition/progression route when present;
- whether it duplicates a spell owned by another provider.

Do not infer display name, mechanics or ownership from the ID alone.

## Namespace rule

Do not search only namespace `irons_spells_js`. Scripts may create spell IDs under arbitrary namespaces. Closure must use registration provenance or a bounded assembled-registry comparison.

## Assembled registry corroboration

When practical, compare the exact assembled Iron's spell registry against already cataloged provider ownership. Any unexplained registry row must be traced to its actual registration authority before counting.

Registry presence alone does not prove survival eligibility.

## Config and reachability

For each surviving script-defined spell, close:

- effective Iron's `enabled`;
- effective `allow_crafting` or script/provider crafting predicate;
- school/focus acquisition;
- loot/equipment/script grant path;
- script-side learning/progression gates;
- normal survival reachability.

Registered debug/admin-only or normally unreachable objects remain outside the strict numerator.

## Zero-content closure

Promote this provider to a closed zero-semantic framework only if authoritative current-instance evidence establishes that no relevant script registration exists.

Acceptable evidence includes an exact current `kubejs/` tree audited with no Iron's spell/school registrations, or a bounded assembled-registry provenance audit paired with the current script inventory.

A repository search returning no scripts is insufficient.

## Current result

- base framework semantic contribution: **+0**;
- current pack script-defined semantic contribution: **UNKNOWN / NOT ADDITIVE**;
- provider state: **⚠️ partial / conditioned**.
