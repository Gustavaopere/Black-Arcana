# Farmer's Spell 1.0.5.1 — Upstream tests and current-host runtime QA

Status: `SOURCE TEST SURFACE INVENTORIED / CURRENT PHYSICAL HOST QA NOT EXECUTED`

## Upstream source test surface

The exact recursive source tree for `b7cbb40316a9ccbbc2ce2b56b3023647261ce569` contains no `src/test` subtree.

`build.gradle` defines ordinary ModDevGradle run configurations including client, server and `gameTestServer`, but a configured run target is not evidence that any test was executed or passed. No upstream test PASS is inferred.

## Current physical-host gates

The following remain direct runtime QA rather than catalog facts:

- client boot with the current full provider set;
- dedicated-server boot;
- successful application of all seven required mixins;
- current Iron's `3.16.3` interoperability;
- current Farmer's Delight `1.3.4` behavior versus source build dependency `1.3.2`;
- current GeckoLib `4.9.2` behavior despite source/physical version-label agreement;
- Foodgeist spawn/reward lifecycle in the assembled pack;
- Gluttony focus recognition in the physical Scroll Forge;
- representative acquisition and execution of all six spells;
- persistence/reload/chunk-unload behavior for provider entities/effects where applicable;
- multiplayer causal ownership and duplicate-processing checks;
- compatibility with other Iron's addons affecting the same host runtime.

## Fail-closed rule

The exact source-pinned registry audit is sufficient for catalog identity and semantic counting after normal Black Arcana evidence promotion. It is not sufficient to certify the assembled provider runtime.

If current-host behavior contradicts the source-line assumptions or mixin/API bindings fail, Black Arcana must disable/withhold the affected optional integration rather than fabricate provider state, duplicate a spell effect or create a replacement resource/casting pipeline.
