# Phase 2V — Ars Technica 2.7.6 checkpoint

Status: `SOURCE CATALOG COMPLETE / FINAL MAIN SYNC COMPLETE / CI PENDING / INSTALLED CONFIG + RUNTIME QA DEFERRED`

Execution branch: `docs/magic-catalog-phase2v-ars-technica`
Base main at phase start: `310c280419b49e5a57077e3460d956ac3dcd27e1`
Pre-CI reconciliation: branch confirmed **0 commits behind** `main@310c280419b49e5a57077e3460d956ac3dcd27e1`; exact diff remains confined to `wiki/modpack-catalog/**`.
Provider source pin: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`
Provider build dependencies: Ars Nouveau `5.11.0.1267`, Create `6.0.8`
Inherited Ars source checkpoint where required: `baileyholl/Ars-Nouveau@f89dacc5d7467aae8497d98e95dad8347a8d7d21`
Physical JAR: `ars_technica-1.21.1-2.7.6.jar`
Physical SHA-1: `adb2641d538375f6eff6a22f0196bb330ab0b171`

## Closed source catalog

- exact installed mod id/JAR/runtime version/file SHA-1;
- exact public provider source version/checkpoint;
- 11/11 production spell-part registrations;
- 11/11 generated glyph-learning recipes;
- 11/11 source defaults normalized for tier, mana, school, compatible augments and provider-specific limits/processing semantics;
- exact inherited Ars Tier-I behavior pinned for Insert;
- major provider acquisition/apparatus recipes;
- 3/3 blocks;
- 3/3 block entities;
- 8/8 misc entity types;
- current item/equipment surface plus old Runic Spanner alias/migration semantics;
- 12/12 armor pieces across Technomancer, Artificer and Machinaguard;
- Ars perk-provider registration for all 12 pieces;
- 1/1 provider perk, `thread_pressure`;
- Pressure Thread persistent `air` reserve and Create backtank seam;
- 3/3 provider persistent data components;
- Transmutation Focus Ars/Fortune and processing effects;
- Source Motor Ars Source → Create kinetic conversion, exact cost formula and source-default multiplier;
- Precise Relay / Ars Rune cadence customization;
- Transmutation Turret Source/caster/resolver transaction;
- Fuse/Arcane Fusion item/fluid processing, output bounds and world-placement controls;
- Whirl/Create processing-family mapping;
- Apply/Insert/Telefeast inventory/fluid/world mutation boundaries;
- 18/18 declared mixins classified: 12 common + 6 client;
- 5/5 registered payload types classified across two network registration paths;
- COMMON source-default interoperability config surface;
- provider-native authority/deduplication consequences;
- semantic overlap mapped into a capability-matrix delta;
- clean-room provenance and LGPL-vs-GPL metadata discrepancy documented.

## High-value factual consequences

1. Ars Technica already occupies broad magic→Create processing. Darker naming/VFX do not create a Black Arcana gameplay gap.
2. Source Motor settles Ars Source and Create kinetics once; no second Source/SU economy is permitted.
3. Transmutation Turret converts the spell's Ars cost to provider Source cost using source-default multiplier 2.0 before Ars turret execution.
4. Pressure Thread is a real provider air reserve exposed to Create BacktankUtil, not a conceptual buff that Black Arcana should duplicate.
5. Transmutation Focus modifies the same provider cast/processing settlement and can double eligible sub-100%-chance Ars Crush outputs; external duplicate yield procs would violate causal deduplication.
6. Provider Fuse can place bounded result-fluid blocks under config; provider behavior does not weaken Black Arcana `WorldEffectPolicy` for BA-owned effects.
7. Normal Rune/Relay UIs are bounded, while the exact client→server cooldown handlers do not show their own range/distance/ownership validation. This remains a provider runtime/security QA item and is not copied into Black Arcana's client-intent model.

## Version-drift gate

The exact 2.7.6 source was built against Ars Nouveau 5.11.0.1267 and Create 6.0.8. The physical pack uses Ars Nouveau 5.13.1 and Create 6.0.10. Several Ars Technica mixins target implementation classes from those hosts. Dependency ranges permit newer versions but do not prove semantic or binary compatibility.

No current-host runtime behavior is promoted to PASS without installed validation.

## Deferred installed-runtime/config validation

- compare installed/generated COMMON config against source defaults;
- validate all 11 glyph registrations and acquisition recipes in the installed runtime/datapack;
- validate mixin application against Ars 5.13.1/Create 6.0.10;
- Source Motor transactional/resource/save-reload/network behavior;
- Pressure/backtank lifecycle behavior;
- Transmutation Focus yield behavior under current addons;
- Transmutation Turret exactly-once Source/cast settlement;
- Create processing/item-fluid conservation for the processing glyph family;
- cooldown/config packets in multiplayer;
- Schematicannon performance/material conservation;
- dedicated-server/client/full-pack interoperability;
- resolve license metadata discrepancy before any source/asset reuse.

These are runtime/config/provenance gates, not missing source-catalog entries.

## Final merge gate

- pre-CI current-main reconciliation: complete against `main@310c280419b49e5a57077e3460d956ac3dcd27e1`;
- exact catalog-only diff review: complete before this checkpoint commit;
- fresh CI must pass on the exact final execution HEAD after this commit;
- immediately before merge, fetch `main` again and reconcile/revalidate if it advanced;
- review threads must remain clear;
- merge only after those gates pass;
- confirm final `main` SHA after merge.

Phase 2V is documentation/catalog state only and does not promote any Black Arcana runtime Stage.