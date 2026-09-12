# Phase 2BO — Farmer's Spell 'n Spellbooks 1.0.5.1 checkpoint

Status: `EXACT SOURCE CATALOG COMPLETE / +6 SEMANTIC SPELLS / COMPONENT PROMOTION PENDING SHARED-QUEUE RECONCILIATION / CURRENT-HOST RUNTIME QA OPEN`

Execution branch: `docs/magic-catalog-phase2bo-farmers-spell`
Base main at phase start: `890a3c557b19af07980f752a9b3698e9e4aa56c4`
Physical JAR: `Farmer's Spell 'n Spellbooks-1.0.5.1-1.21.1.jar`
Physical mod id/version: `farmers_spell` / `1.0.5.1-1.21.1`
Physical SHA-1: `f77355e042172e7af3a2bcebbf5d0f87eacb6501`
Physical SHA-256: `a7b9d42d7e4b04ed98778f770ee3a7ecbcf4bd7a73bd3a800838be2af6ae4b87`
Physical Iron's host: `irons_spellbooks-1.21.1-3.16.3.6.jar`
Physical Farmer's Delight host: `FarmersDelight-1.21.1-1.3.2.jar`
Physical GeckoLib host: `geckolib-neoforge-1.21.1-4.7.6.jar`
Exact official source: `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`
Exact source tree: `83f54cd2415b424d1fc209191f6a3f90bd919312` (`truncated=false`)

## Evidence closed in this tranche

- exact current physical provider identity and hashes from the 595-entry physical modlist;
- exact official source commit whose sole version-bump diff changes `1.0.5.0-1.21.1` to `1.0.5.1-1.21.1`;
- source Minecraft `1.21.1`, range `[1.21.1,1.22)`, NeoForge build `21.1.238` / range `[21.1,)`, Java 21;
- required runtime dependencies on Iron's Spells 'n Spellbooks `[3.16.0,)`, Farmer's Delight `[1.2.8,)` and GeckoLib `[4.7.5.1,)`;
- provider class `MIXED`: one own Gluttony spell school, six own Iron's spell registrations plus magical-cooking/food/gear/effect support surfaces;
- exactly six unconditional provider spell identities;
- Gluttony focus and Scroll Forge reachability route separated from the generic random-loot route;
- exactly four required common mixins + three required client mixins = seven direct bindings;
- `NetworkHandler.registerPackets()` has zero provider-owned payload registrations at the source pin;
- no `src/test` tree is present in the exact source tree; source run configuration presence is not treated as executed test evidence;
- All Rights Reserved source/metadata license and clean-room no-reuse posture;
- Black Arcana authority, deduplication and fail-closed runtime boundaries.

## Semantic disposition

The exact registry contributes **6 independent semantic spell objects** under `SEMANTIC-MAGIC-COVERAGE.md`:

- `farmers_spell:goodberry`
- `farmers_spell:phantom_loot`
- `farmers_spell:seal_coat`
- `farmers_spell:bad_apple`
- `farmers_spell:chaos_slash`
- `farmers_spell:preserve_circle`

The Gluttony school itself is provider taxonomy/support for these spells and is not added as a seventh semantic object under the current metric. The current canonical strict minimum remains **1316** on `main` until this evidence tranche is merged and the shared semantic/provider ledgers are reconciled. Candidate strict minimum after promotion is **1322**.

The component is technically auditable as a mixed spell/content provider. Promotion to component **#63 / 63 of 100** is deliberately left for shared-ledger reconciliation after this exact branch has current CI evidence.

## Acquisition / reachability disposition

The provider does not rely on generic random Iron's scroll loot for its school: its `SchoolType` sets `allowLooting=false`.

Instead, the exact provider data defines the Gluttony focus tag with `#minecraft:foods` and `farmers_spell:foodgeist_seasoning`. The public Iron's 3.16.3 source-line Scroll Forge contract uses a matching school focus and enumerates that school's spells subject to the host's enabled/craftable/player gates. No Farmer's Spell override of `allowCrafting`, `isEnabled` or `canBeCraftedBy` was found for the six classes. Foodgeist Seasoning also has provider-owned survival support through Foodgeist spawn/reward/loot surfaces.

This closes a provider/host-native survival acquisition route for the registered spell set without inventing a Black Arcana path. It does not claim final assembled-pack probabilities, numerical economy balance or full runtime PASS.

## Current-host QA kept open

1. Source build targets NeoForge `21.1.238`; the physical pack uses `21.1.248`.
2. Source build depends on GeckoLib `4.9.2`; the physical pack uses `4.7.6`. The metadata minimum `[4.7.5.1,)` is not compatibility proof.
3. Seven direct required mixins bind common and client/render behavior.
4. The physical Iron's package is `3.16.3.6`; the host contract used for Scroll Forge interpretation is the public 3.16.3 source line and is not falsely treated as a cryptographic source match for the `.6` packaging suffix.
5. Client boot, dedicated-server boot, mixin application, Foodgeist progression, Scroll Forge acquisition and representative execution of all six spells remain assembled-pack runtime QA gates.
6. A loader/dependency range being accepted is not a substitute for direct host validation.

## Clean-room boundary

The exact source was inspected only to establish factual provider identity, dependency declarations, registry IDs/types/counts, narrow acquisition relationships, mixin/network footprint, authority boundaries and compatibility risks. No upstream implementation body, assets, localization prose, models, sounds or balance text are copied/adapted into Black Arcana.
