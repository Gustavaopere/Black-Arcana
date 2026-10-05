# Iron's Spellbooks KubeJS 4.0.3 — deployed-instance parity checklist

Status: `✅ CATALOG CLOSED +0 / OWNER-ATTESTED ZERO AUTHORED SPELL-SCHOOL CONTENT / PHYSICAL SCRIPT-TREE PARITY CHECK PENDING`

## Purpose

Verify that the deployed current modpack instance still matches the cataloged authored-content state for Iron's Spellbooks KubeJS.

The catalog itself is already closed at **✅ / +0** based on the exact 4.0.3 source audit plus the project owner's 2026-10-05 attestation that no custom Iron's spells or schools were authored through KubeJS. This checklist is therefore a **deployment-parity/reopen trigger**, not a prerequisite for the current ✅ catalog state.

If physical inspection finds a relevant registration script, the provider must be reopened and the exact objects cataloged before further semantic accounting.

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

- historical Black Arcana main at the original evidence-branch creation: `e614dea1be34936b095af2a3d7c8d65c69f7e34d`;
- Black Arcana main reconciled for the current host-377 collector hardening in PR #624: `3b386df50d3db3a8e5606529f97c7413dbf6ab32`;
- Black Arcana main reconciled for the Iron's-3.16.3 same-instance host hardening in PR #627: `969771099e8e04758f29b8aa09835b467967d3c7`;
- Black Arcana main reconciled again before final PR #627 validation after concurrent Deeper audit #629: `3c8f5163ea7985bdf5ed667b804d0f663c676798`;
- Black Arcana main reconciled again before final PR #627 validation after concurrent Traveloptics #628: `d1cffe8068d16fcf6c61876e14133bf966c8d387`;
- Black Arcana main reconciled again before final PR #627 validation after concurrent Deeper summary #630: `59fc2ead8443ecdb2cb652047fa948952baa7fec`;
- Black Arcana main reconciled again before final PR #627 validation after concurrent Traveloptics runtime evidence #631: `285499cb762173a1b1079cc4a72bbd6d02d0274e`;
- sibling modlist authority: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`;
- current physical row remains `irons_spells_js-4.0.3.jar` / mod id `irons_spells_js` / runtime `4.0.3`;
- current host stack remains Iron's `1.21.1-3.16.3` + KubeJS `2101.7.2-build.377`;
- current sibling default-branch searches did not expose a committed `kubejs/startup_scripts` or `kubejs/server_scripts` tree;
- available Project/Library retrieval did not expose an authoritative current script tree; only historical 2026-09-08 KubeJS build-374 boot evidence and later physical modlist metadata were found;
- on 2026-10-05 the project owner attested that no custom Iron's spells/schools were authored through KubeJS and that this addon was added as future creation infrastructure;
- catalog contribution is therefore closed at **+0** at the accepted authored-content evidence ceiling; exact deployed-instance script parity remains unverified.

This is documented in [`CURRENT-EVIDENCE-2026-10-04.md`](CURRENT-EVIDENCE-2026-10-04.md). Do not promote from this checkpoint alone.
## Collector-assisted evidence

Run the current deployed-evidence collector on the authoritative instance first. Require all four evidence components from the same assembled instance:

1. `mods.irons_spells_js[*].current_physical_4_0_3_equality == true`;
2. `mods.irons_spellbooks[*].current_physical_3_16_3_equality == true`;
3. `mods.kubejs[*].current_physical_build_377_equality == true`;
4. the resulting `kubejs_script_inventory`.

The inventory records the exact bounded `startup_scripts`, `server_scripts`, `client_scripts` and `data` files by relative path, SHA-256 and byte size without copying bodies.

Read `irons_spellbooks_kubejs_closure.status` as a routing aid only:

- `ARTIFACT_NOT_OBSERVED` / `ARTIFACT_HASH_MISMATCH` -> stop; provider identity is not current-certified;
- `IRONS_HOST_NOT_OBSERVED` / `IRONS_HOST_HASH_MISMATCH` -> stop; the same-instance Iron's host is not certified 3.16.3;
- `KUBEJS_HOST_NOT_OBSERVED` / `KUBEJS_HOST_HASH_MISMATCH` -> stop; the same-instance KubeJS host is not current build 377;
- `ZERO_CONTENT_REVIEW_CANDIDATE` -> provider + both hosts are current-certified and the bounded tree is empty; review provenance/current-instance scope before closure;
- `SCRIPT_REVIEW_REQUIRED` -> provider + both hosts are current-certified and bounded files exist; inspect the exact hashes/files regardless of marker count.

These values are deployment-parity routing states, not catalog statuses. Row #98 is already catalog-closed at `✅ / +0`; a `SCRIPT_REVIEW_REQUIRED` result that reveals an actual Iron's spell/school registration is a mandatory **catalog reopen trigger**.

- If `current_physical_4_0_3_equality` is not `true`, stop: the collector is not observing the certified physical 4.0.3 artifact.
- If `current_physical_3_16_3_equality` is not `true`, stop: the collector is not observing the certified current Iron's host.
- If `current_physical_build_377_equality` is not `true`, stop: the collector is not observing the certified current KubeJS host.
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

## Zero-content parity confirmation

An authoritative current-instance inventory with no relevant Iron's spell/school registration corroborates the owner-attested catalog state and closes deployed-instance parity.

A repository search returning no scripts is insufficient for physical parity.

If relevant scripts are found, do not preserve the `+0` catalog result by assumption: reopen the provider, enumerate the exact registered objects, deduplicate ownership, evaluate effective host config/acquisition/reachability, and then recompute the semantic contribution.

## Current result

- base framework semantic contribution: **+0**;
- project-authored custom Iron's spell/school contribution: **+0, owner-attested 2026-10-05**;
- provider catalog state: **✅ cataloged**;
- exact deployed-instance script parity: **PENDING QA**;
- any contradictory physical registration: **REOPEN CATALOG**.
