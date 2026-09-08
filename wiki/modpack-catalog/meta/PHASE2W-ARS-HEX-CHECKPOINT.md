# Phase 2W — Ars Hex 5.0.4b checkpoint

Status: `SOURCE CATALOG COMPLETE / PRE-CI MAIN SYNC COMPLETE / CI PENDING / INSTALLED JAR+CONFIG+RUNTIME QA DEFERRED`

Execution branch: `docs/magic-catalog-phase2w-ars-hex`
Base main at phase start: `f2169e77d2030f76be5bd555c99bf8b616c93b45`
Pre-CI reconciliation: branch confirmed **0 commits behind** `main@f2169e77d2030f76be5bd555c99bf8b616c93b45`; exact diff remains confined to 11 files under `wiki/modpack-catalog/**`.
Provider source checkpoint: `Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227` (`RELEASE-ALIGNED`, not claimed byte-identical)
Physical JAR: `ars_hex-1.21.1-5.0.4b.jar`
Physical SHA-1: `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`

## Closed source catalog

- physical mod id/JAR/runtime version/SHA-1;
- release-aligned source checkpoint and later-Notion-pin divergence;
- build host pins and current physical host-version drift;
- provider bootstrap/gating for Malum, Iron's and Hexerei;
- Malum-present/source-selected path:
  - 1/1 production glyph registration in source;
  - 3/3 production Ars thread perk registrations in source;
  - Enchanter's Scythe;
  - scythe-boomerang/Reactive seam;
  - LightManager bridge;
  - 5/5 committed Malum-conditioned acquisition recipes;
- Iron's-present/source-selected path:
  - Ars→Iron school map;
  - exact school damage/resistance multiplier event path;
  - optional general SPELL_POWER merge path;
  - Ars Elemental armor→Iron school-power modifiers;
  - 5/5 particle wrappers;
  - COMMON config fields and duplicate config-path risk;
- Hexerei source-only path:
  - 3 items;
  - 1 broom entity;
  - 12 particle wrappers;
  - render/client/docs/recipe-page bridge;
  - 3 Hexerei-conditioned manual recipes;
- one Hex Casting-conditioned `archwood_staff` resource classified dormant/orphan because provider is absent and Java registration was not located;
- 0/0 declared mixins;
- 0 provider-owned custom payload registrations identified;
- datagen intent for cross-provider tags separated from committed generated-resource/package evidence;
- code LGPLv3 + assets ARR clean-room boundary;
- capability/deduplication consequences.

## High-value factual consequences

1. Ars Hex is a compatibility provider, not a new independent spell school.
2. The physical pack contains Malum and Iron's, so their source bootstrap conditions are eligible; successful installed-runtime execution remains deferred QA. Hexerei/Hex Casting are absent and their conditions are not current-pack eligible.
3. Soul Shatter's selected source path performs Ars spell damage with Malum Voodoo authority; BA must not replay that provider damage/spirit settlement if confirmed active.
4. Enchanter's Scythe source is a provider-owned Malum weapon→Ars resolver bridge with its own on-hit/boomerang/Reactive lifecycle.
5. The selected Iron's source path applies Iron school power/resistance to eligible Ars damage; a second BA/RPG bridge around the same confirmed provider event would double-process the hit.
6. The exact Ars Elemental source for the installed version line implements the Sauce interface consumed by Ars Hex's Iron bridge; installed interoperability remains QA.
7. Two conceptual Iron scaling fields share one persisted config path in source; they cannot be documented as independently configured without installed config evidence.
8. The optional general Iron merge source path reads general SPELL_POWER from the target. This is preserved as a source-risk observation rather than silently corrected.
9. Source datagen intent is not equivalent to packaged JAR data when generated tag outputs are absent from the committed generated-resource tree.

## Version-drift gate

Release-aligned source build pins:

- NeoForge 21.1.210;
- Ars Nouveau 5.11.0.1267;
- Ars Elemental 0.7.6.12.117;
- Iron's 3.14.8;
- Lodestone 1.8.3.549;
- Malum 1.8.2.150;
- Sauce preferred 0.0.16.46.

Physical pack:

- NeoForge 21.1.248;
- Ars Nouveau 5.13.1;
- Ars Elemental 0.7.10.1;
- Iron's 3.16.3;
- Lodestone 1.8.2;
- Malum 1.8.2;
- nested Sauce 0.0.16.46 visible inside the Ars Hex physical artifact listing.

No Ars Hex mixin targets exist, but event/API/attribute/library compatibility is not inferred from version ranges.

## Deferred installed JAR/config/runtime validation

- physical JAR extraction/resource enumeration;
- installed COMMON config inspection/shared-key behavior;
- Soul Shatter + Malum spirit outcome causal validation;
- thread modifiers across installed Ars armor/thread layouts;
- Enchanter's Scythe melee/boomerang/Reactive/Repairing/discount lifecycle;
- Iron school and optional general damage bridge under current Iron's;
- Ars Elemental armor bridge under 0.7.10.1;
- optional-provider classloading with Hexerei absent;
- physical presence/absence of intended datagen tags;
- Sauce jarjar resolution in the complete pack;
- dedicated-server/client/full-pack interoperability.

These are runtime/config/package gates, not missing source-catalog entries.

## Final merge gate

- pre-CI current-main reconciliation: complete against `main@f2169e77d2030f76be5bd555c99bf8b616c93b45`;
- exact catalog-only diff review: complete before this checkpoint update;
- fresh CI must pass on the exact final execution HEAD after this checkpoint commit;
- immediately before merge, fetch `main` again and reconcile/revalidate if it advanced;
- review threads must remain clear;
- merge only after those gates pass;
- confirm final `main` SHA after merge.

Phase 2W is documentation/catalog state only and does not promote any Black Arcana runtime Stage.
