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

## Current freshness checkpoint — 2026-10-04

- Black Arcana main considered at branch creation: `e614dea1be34936b095af2a3d7c8d65c69f7e34d`;
- sibling modlist authority: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`;
- current physical row remains `irons_spells_js-4.0.3.jar` / mod id `irons_spells_js` / runtime `4.0.3`;
- current host stack remains Iron's `1.21.1-3.16.3` + KubeJS `2101.7.2-build.377`;
- current sibling default-branch searches did not expose a committed `kubejs/startup_scripts` or `kubejs/server_scripts` tree;
- available Project/Library retrieval did not expose an authoritative current script tree; only historical 2026-09-08 KubeJS build-374 boot evidence and later physical modlist metadata were found;
- therefore the pack-script semantic contribution remains **UNKNOWN / NOT ADDITIVE**.

This is documented in [`CURRENT-EVIDENCE-2026-10-04.md`](CURRENT-EVIDENCE-2026-10-04.md). Do not promote from this checkpoint alone.
## Collector-assisted evidence

Run the current deployed-evidence collector on the authoritative instance first. Require the exact JAR fingerprint from `mods.irons_spells_js[*].current_physical_4_0_3_equality` **and** the `kubejs_script_inventory` from the same assembled instance. The inventory records the exact bounded `startup_scripts`, `server_scripts`, `client_scripts` and `data` files by relative path, SHA-256 and byte size without copying bodies.

- If `current_physical_4_0_3_equality` is not `true`, stop: the collector is not observing the certified physical 4.0.3 artifact.
- If the authoritative current `kubejs/` root is absent or all four bounded surfaces are empty, that is acceptable zero-content evidence for the script-tree part of this checklist.
- If any relevant files exist, inspect those exact hashed files for Iron's spell/school builder registrations and continue with the provenance rules below.
- Use any `irons_spellbooks_kubejs_markers` only to prioritize that inspection. Marker presence is a candidate, not a registration verdict; marker absence is not zero-content proof because scripts may alias registry keys or construct values dynamically.
- The literal spell/school markers are version-grounded to Iron's 3.11.0 (`216d675627004562bc540b618b77600009cd6ee1`), matching the host baseline declared by exact addon source 4.0.3.
- Do not infer zero content from repository search; the collector must be run against the assembled instance.

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
