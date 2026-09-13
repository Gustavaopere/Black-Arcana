# Phase 2BP — SnackPirate's Aeromancy Additions 1.2.8 checkpoint

Status: `EXACT SOURCE CATALOG COMPLETE / +10 SEMANTIC SPELLS / COMPONENT PROMOTION PENDING SHARED-QUEUE RECONCILIATION / CURRENT-HOST RUNTIME QA OPEN`

Execution branch: `docs/magic-catalog-phase2bp-aeromancy`
Base main at phase start: `a3b01c124ec0e9cc852e9945121795a1bfb19273`
Physical modlist: 595 entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
Physical JAR: `aero_additions-1.2.8.jar`
Physical mod id/version: `aero_additions` / `1.2.8`
Physical SHA-1: `dee32c9fa84d6e39846608f8f77591ea56f`
Physical CurseForge hash: `3079423735`
Physical NeoForge: `21.1.248`
Physical Iron's host: `irons_spellbooks-1.21.1-3.16.3.jar`
Exact public source: `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`
Exact source tree: `fcee08e613fbfa030f034268a0240c8693ab7f45` (`truncated=false`)

## Evidence closed in this tranche

- current physical provider identity/hash from the canonical 595-entry modlist;
- exact public 1.2.8 source pin and complete recursive tree;
- source Minecraft 1.21.1, NeoForge build target 21.1.228 and Java 21 mixin compatibility;
- source build dependency on Iron's 3.16.1 plus generated required range `[1.21.1-3.15.0,1.21.1-4.0.0)`;
- provider classification as a mixed Iron's spell/content provider, not UI/library/compat-only;
- exactly ten active unconditional provider spell registrations;
- five source spell candidates explicitly excluded because their registry lines are commented out;
- Wind school focus/reachability contract through Breeze Rod + Iron's Scroll Forge;
- provider survival support for Breeze Rod through Trial Chamber vault data;
- independent embedded-spell routes for Updraft Tome and Wind Sword;
- exactly two required mixins;
- exactly three provider-owned payload registrations observed, including Airstep C2S handling;
- no `src/test` tree in the exact source tree;
- metadata license declaration and source-license ambiguity recorded conservatively;
- Black Arcana authority, deduplication and fail-closed runtime boundaries.

## Semantic disposition

The source-pinned registry contributes **10 independent semantic spell objects** as promotion candidates:

- `aero_additions:wind_charge`
- `aero_additions:updraft`
- `aero_additions:airstep`
- `aero_additions:asphyxiate`
- `aero_additions:feather_fall`
- `aero_additions:wind_shield`
- `aero_additions:airblast`
- `aero_additions:wind_blade`
- `aero_additions:flush`
- `aero_additions:dash`

The Wind school, armor/items, effects, projectiles/entities, recipes, focus tags and acquisition/support content are not added as separate spell objects under the current strict metric.

The current canonical shared ledgers remain **1322 strict semantic objects / 63 of 100 technical components** until this evidence tranche is merged and a separate shared-ledger reconciliation is completed. Candidate post-reconciliation state: **1332 / component #64 / 64 of 100**.

## Acquisition / reachability disposition

Wind's seven-argument `SchoolType` uses Iron's 3.16.3 defaults `requiresLearning=false` and `allowLooting=true`. Provider/host data marks Breeze Rod as the Wind/School Focus. Iron's Scroll Forge enumerates spells for the matched school and applies enabled/crafting/player gates. Host `DefaultConfig` defaults enabled/craftable, and no Aeromancy override of the relevant gates was found for the ten active classes.

This closes a source-pinned provider/host-native acquisition route without inventing a Black Arcana path. Physical server config/tag composition and actual acquisition/execution remain assembled-pack QA.

## Current-host QA kept open

1. Source targets NeoForge 21.1.228; physical pack uses 21.1.248.
2. Source build uses Iron's 3.16.1; physical pack uses 3.16.3, although 3.16.3 is inside the declared required range.
3. Two required mixins must apply successfully in the full pack.
4. Three provider payloads, including Airstep C2S movement, require multiplayer/runtime QA.
5. Scroll Forge focus resolution, physical config gates and acquisition of all ten spells require direct validation.
6. Client/dedicated-server boot and representative casts remain unexecuted here.
7. No source/binary cryptographic equivalence is claimed between upstream source output and the physical JAR.

## Clean-room boundary

The exact source was inspected only for factual provider identity, registry IDs/counts, dependency declarations, narrow host/acquisition relationships, mixin/network footprint, authority boundaries and compatibility risks. No provider code, assets, prose, models, sounds or balance implementation is copied into Black Arcana.
