# Phase 2BR — GTBC's Geomancy Plus 1.1.0-1.21.1 exact checkpoint

## Purpose

Phase 2BR closes the current GTBC's Geomancy Plus provider inventory at the strongest clean-room evidence available for the physically installed 1.21.1 line, without promoting assembled-pack runtime behavior that has not been exercised.

This checkpoint is documentation/catalog evidence only. It adds no Black Arcana runtime adapter, spell implementation, cast path, resource pool or provider hook.

## Base and concurrency

Durable documentation branch was created from:

`main@6397b4b40778cb7867331342c0ce1a22617fc688`

The branch was then reconciled with concurrent Stage 05.14 work after `main` advanced to:

`main@12589c7168163ddd737a0534d6287ce102f97359`

Phase 2BR does not modify the Stage 05.14 files or runtime scope.

## Provider identity

Current physical line:

- mod id `gtbcs_geomancy_plus`;
- version `1.1.0-1.21.1`;
- current pack authority confirms the provider is present.

Exact publisher release inspected:

- CurseForge project/file `1352485 / 7041615`;
- filename `gtbcs_geomancy_plus-1.1.0-1.21.1.jar`;
- exact release SHA-1 `67e9652799f35f1fbd09968da6f400d0229f5599`;
- exact release SHA-256 `b645cf8852b3453f2d7ccc10cd4b4f897edcc6f857f912042dc9f4d96c8e8bf7`.

The repo does not preserve a separate hash of the user's local physical JAR, so Phase 2BR does not label this evidence `hash-matched physical`. The release artifact aligns to the installed mod-id/version/filename line and is inspected exactly as published.

## Exact-artifact evidence

Structural NON-MERGE audit:

- audit HEAD `c9d9bfb86bb036427192c50139f1c9093f5d508e`;
- run `34737230548` GREEN;
- artifact `10310854594`;
- digest `sha256:69d0a4ba925405e6a6f07db79618adea081ca980b73d357c9797001e2f330998`.

Focused registry NON-MERGE reconciliation:

- audit HEAD `bf90b58d15a1c5f1379b562291e8a30b62fc2e92`;
- run `34737352893` GREEN;
- artifact `10311950155`;
- digest `sha256:a948b8ce7d71b43538756cb9a3ef26dc8b3bf02d4e4c4ef04ee16fc00a391dab`.

## Registry closure

The exact `GGSpells` registry closes:

- 12 `Supplier<AbstractSpell>` fields;
- 12 `registerSpell(...)` calls;
- 0 static-initializer branch opcodes;
- 12 exact field -> concrete class -> spell-ID mappings;
- 12 matching root localization spell IDs;
- 0 registry config references;
- 0 registry mod-gate references.

Exact current spell identities:

### Geo — 10

1. `chunker`
2. `dripstone_bolt`
3. `eroding_boulder`
4. `fissure`
5. `geo_conductor`
6. `petrivise`
7. `pillar_of_the_resounding_earth`
8. `seismic_surf`
9. `tremor_spike`
10. `tremor_step`

### Holy — 2

11. `solar_beam`
12. `solar_storm`

## Explicit exclusions

- `EarthshatterSpell` exists in the exact artifact but is not registered by `GGSpells`; exact focused reconciliation records `earthshatter_registered=false` -> **+0**.
- `EarthquakeMixin` and `StormSpellMixin` are not provider registry entries -> **+0** provider identities.
- Geo `SchoolType` is taxonomy/support, not a thirteenth spell.
- generic project-page names from later/project-wide content are not projected backward into exact file `7041615`.
- GTBC SpellLib is shared infrastructure and remains a separate zero-semantic component already closed elsewhere.

## Reachability closure at catalog level

Geo focus path:

`mowziesmobs:bluff_rod -> #gtbcs_geomancy_plus:geo_focus -> irons_spellbooks:school_focus`

This closes the exact provider-defined focus identity path for the Geo family under the already-cataloged Iron's focus/Scroll Forge contract.

Holy acquisition path:

exact Umvuthi loot identifiers reference both `solar_beam` and `solar_storm` together with Iron's scroll/randomization identifiers. The exact publisher 1.1.0 file changelog independently identifies both spells as obtained by defeating Umvuthi.

Catalog reachability is therefore sufficient for the twelve exact registrations. Full assembled-pack acquisition/live drop behavior remains runtime QA.

## Authority

- Iron's owns host casting/mana/cooldown/scroll infrastructure.
- GTBC's Geomancy Plus owns its twelve spell registrations and Geo school/content.
- Mowzie's Mobs owns its base entities/items/state.
- GTBC SpellLib remains shared library infrastructure.
- Black Arcana remains authority for its own magical runtime, world safety, hazards, Corruption, Strain and Arcane Danger.

No authority transfer or duplicate processing path is introduced.

## Runtime fail-closed surfaces

Not promoted to PASS by this checkpoint:

- exact full-pack Iron's host compatibility;
- Geo school UI/runtime settlement;
- Mowzie-linked entity/projectile behavior;
- Umvuthi loot execution and rates;
- terrain mutation/protection interaction;
- multiplayer, restart/reload and duplicate-processing behavior;
- quantitative balance/config behavior.

## Proposed semantic/component result

If and only if this durable evidence is merged and a separate latest-main shared-ledger reconciliation passes all canonical gates:

- strict semantic minimum: `1332 + 12 = 1344`;
- technical component closure: `65/100 -> 66/100`;
- provider state: `COUNTED_EXACT_RELEASE / COMPONENT #66`.

Until then the canonical shared values remain **1332 / 65 of 100**, and this checkpoint records only the evidence candidate.