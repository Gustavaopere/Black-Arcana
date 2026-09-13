# SnackPirate's Aeromancy Additions 1.2.8 — upstream tests and current-host runtime QA

Status: `SOURCE TEST SURFACE INVENTORIED / CURRENT PHYSICAL HOST QA NOT EXECUTED`

## Upstream source test surface

The exact recursive source tree `fcee08e613fbfa030f034268a0240c8693ab7f45` contains no `src/test` subtree. No upstream automated test PASS is inferred from build/run configuration alone.

## Current physical-host gates

The following remain direct runtime QA rather than catalog facts:

- client boot with the current full provider set;
- dedicated-server boot;
- successful application of both required mixins;
- current Iron's 3.16.3 interoperability versus source build dependency 3.16.1;
- current NeoForge 21.1.248 behavior versus source build target 21.1.228;
- Scroll Forge recognition of Breeze Rod as the Wind focus in the assembled datapack/tag stack;
- acquisition visibility/reachability for all ten registered spells under physical server configs;
- representative execution of all ten spells;
- Updraft Tome and Wind Sword embedded-spell behavior;
- Airstep C2S movement handling and provider-owned state synchronization;
- Dash/player-data S2C synchronization;
- persistence/reload behavior for Aeromancy spell data where applicable;
- multiplayer causal ownership and duplicate-processing checks;
- compatibility with other Iron's addons, Sable-aware content and overlapping movement/combat systems in the pack.

## Dependency-range fact

Provider metadata requires Iron's `[1.21.1-3.15.0,1.21.1-4.0.0)` and ExpandAbility `[12.0.0,13.0.0)`. The physical Iron's 3.16.3 and embedded ExpandAbility 12.0.0 are within those ranges. This is contract compatibility evidence only, not runtime PASS evidence.

## Fail-closed rule

The exact source-pinned registry/acquisition audit is sufficient for catalog identity and semantic counting after normal evidence promotion. It is not sufficient to certify the assembled provider runtime.

If current-host behavior contradicts source-line assumptions, a required mixin fails, host tags/config disable acquisition, or payload behavior is incompatible, Black Arcana must withhold/disable the affected optional integration. It must not fabricate provider state, duplicate spell effects, create replacement Wind resources, or introduce a second casting/mana/cooldown pipeline.
