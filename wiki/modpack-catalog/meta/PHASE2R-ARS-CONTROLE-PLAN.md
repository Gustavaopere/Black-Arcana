# Phase 2R — Ars Controle 1.6.15 audit plan

Status: `PLANNING / NO RUNTIME IMPLEMENTATION`

Baseline Black Arcana: `main@4053c060bb7e4c3f57ca06f49295868277a6eb57`.

This document plans the next unclaimed Phase 2 provider audit after the current Ars Nouveau checkpoint while preserving the concurrent Ars Additions work in PR #94. It is a catalog/provenance/deduplication plan only. It does not promote a Black Arcana runtime Stage, does not modify Stage 07.07, and does not authorize Phase 3 implementation.

## 1. Why this provider is next

Ars Controle is physically present in the current 2026-09-07 modlist and remains granular-catalog pending in the canonical provider queue. No Ars Controle-specific branch was found during the pre-work reconciliation. Ars Additions is already owned by concurrent draft PR #94, so this plan intentionally avoids that provider and its paths.

Current physical identity:

- JAR: `ars_controle-1.21.1-1.6.15.jar`;
- mod id: `ars_controle`;
- runtime version: `1.21.1-1.6.15`;
- physical SHA-1: `fdf381d5733698abe336354c7541299ab495ecae`;
- target: Minecraft 1.21.1 / NeoForge 21.1.248 / Java 21.

Current provider context:

- Ars Nouveau: `ars_nouveau-1.21.1-5.13.1.jar` / `5.13.1`;
- Curios: `curios-neoforge-9.5.1+1.21.1.jar` / `9.5.1+1.21.1`;
- CC:Tweaked / ComputerCraft was not located as a top-level JAR in the current physical modlist, so its Ars Controle path is currently optional/absent until a later modlist proves otherwise.

## 2. Source and provenance baseline

Exact public source checkpoint selected for factual audit:

- repository: `Vonr/Ars-Controle`;
- commit: `ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`;
- commit message: `ver: 1.6.15`;
- `gradle.properties`: `mc_version=1.21.1`, `mod_id=ars_controle`, `mod_version=1.6.15`, `mod_license=LGPLv3`;
- root `LICENSE`: GNU Lesser General Public License v3.

The source checkpoint is suitable for read-only factual cataloging and contract discovery. It is not cryptographic proof that the installed JAR was built from this exact commit. JAR↔source equivalence remains a separate evidence question.

Before any source-derived implementation seam is approved, update the Black Arcana provenance surfaces (`SOURCES.md`, `THIRD_PARTY_NOTICES.md`, `docs/provenance/REFERENCE_LEDGER.md`) and preserve clean-room/provider-native boundaries.

## 3. Version-drift gate

The exact 1.6.15 source checkpoint declares build dependencies older than the current pack:

- NeoForge source baseline: `21.1.217` vs pack `21.1.248`;
- Ars Nouveau source baseline: `5.10.6.1245` vs pack `5.13.1`;
- Curios source baseline: `9.0.12` vs pack `9.5.1+1.21.1`;
- CC:Tweaked source baseline: `1.112.0`, while no top-level CC:Tweaked JAR is currently present in the pack.

Consequences:

1. static registry/content facts may be cataloged from the exact source checkpoint;
2. API signatures, optional integration activation, event order, capability behavior, networking and runtime compatibility must not be inferred from source-version eligibility;
3. any future Ars Controle adapter remains `FAIL-CLOSED` until its intended seam is verified against the actual loaded versions;
4. no Black Arcana fallback may emulate a missing Ars Controle/Ars Nouveau provider contract if doing so changes resource, targeting, world-state or ownership semantics.

## 4. Source-observed inventory that defines the audit scope

The exact source registry currently exposes the following static scope to close during Phase 2R:

- 4 registered blocks;
- 6 registered items, including the block items plus two standalone utility items;
- 3 registered block-entity types;
- 2 persistent/network-synchronized data-component types;
- 4 attachment types used for provider-owned references/association state;
- 9 Ars spell parts total:
  - 1 effect glyph;
  - 8 filter glyphs;
- 1 creative tab.

These counts are planning baselines, not yet the Phase 2R acceptance claim. Execution must enumerate the exact registry IDs and prove that no additional registration surface is omitted elsewhere in the exact source revision.

## 5. Public player-facing systems to catalog

The exact provider README and source baseline identify these player-facing families:

### 5.1 Warping Spell Prism

Catalog:

- projectile redirection/warping semantics;
- cross-dimensional behavior and destination representation;
- loaded-state/chunk behavior;
- Ars projectile/resource authority;
- optional CC:Tweaked configuration surface and its current pack absence;
- recipe/acquisition, block entity state, persistence and cleanup.

Critical dedup gate: thematic similarity to Black Arcana Space & Displacement does not transfer authority. Provider projectile routing remains Ars/Ars Controle-owned. Black Arcana must not replay the spell, duplicate its Source/mana settlement or treat provider cross-dimensional capability as permission to force-load chunks for Black Arcana effects.

### 5.2 Scryer's Linkage

Catalog:

- remote block linkage identity;
- item/fluid/energy/redstone and other exposed resource routes;
- provider capability delegation;
- target persistence and cross-level behavior if any;
- invalid/unloaded target semantics;
- recipe/acquisition and protection interaction.

Important semantic guard: despite the name, this is not automatically a divination/remote-vision capability. Do not mark overlap with Borrowed Sight or other Noetic observation mechanics unless the exact behavior proves an observation surface.

### 5.3 Temporal Stability Sensor

Catalog:

- measured server/world instability signal;
- redstone/comparator projection;
- sampling cadence and performance behavior;
- recipe/acquisition.

Dedup guard: this is operational/performance observability unless exact evidence proves otherwise. Its temporal naming does not create a time-magic or Arcane Danger contract.

### 5.4 Warp Scroll Holder

Catalog:

- relationship to Ars Nouveau Warp Scroll/portal authority;
- Source requirement and source-search semantics;
- opening/closing lifecycle;
- destination persistence;
- loaded-chunk and cross-dimensional behavior;
- recipe/acquisition and failure modes.

Do not convert this into a Black Arcana portal provider. Stage 07.04 keeps its own canonical safe-destination, ownership, consent and no-force-load contracts.

### 5.5 Remote

Catalog:

- provider-owned remote configuration state;
- single/multiple selection semantics;
- first/second endpoint locking;
- block/entity target types;
- persistence/network synchronization;
- invalid target cleanup;
- acquisition.

Black Arcana targeting remains server-authoritative and separate. The Remote is not a generic authorization token for Black Arcana targets or world effects.

### 5.6 Portable Brazier Relay

Catalog:

- carried ritual-effect semantics;
- identity of the originating Ars ritual/brazier;
- requirement for the brazier to remain loaded;
- Source consumption/provider ownership;
- persistence, logout/death/dimension behavior;
- effect cleanup/revocation;
- acquisition.

Critical ritual boundary: Ars Nouveau remains authority for its ritual effect and Source economy. Black Arcana Rituals must not mirror, re-settle or convert an Ars ritual merely because the relay can carry its result.

## 6. Glyph catalog closure

Create one canonical page per registered spell part under a provider-native hierarchy. The source registry baseline requires nine pages:

- effect: Precise Delay;
- Y-level filters: Above, Level, Below;
- adaptive/logical filters: NOT, OR, XOR, XNOR;
- probability filter: Random.

For each glyph record, where evidence exists:

- exact registry ID;
- native Ars category/tier;
- effect/filter semantics;
- augment interactions;
- mana cost or cost contribution;
- limits/bounds;
- acquisition/learning recipe;
- server/client authority;
- child-spell or continuation behavior;
- persistence/scheduling implications;
- VFX/audio only when verified;
- provenance/confidence;
- semantic overlap/disposition in the capability matrix.

Provider formulas may be recorded factually when source/public docs agree. Do not transplant the implementation into Black Arcana.

## 7. Registry and data audit

Close the exact provider-owned registry surface, not only the README-visible content:

1. enumerate exact block IDs and block entity IDs;
2. enumerate exact item IDs;
3. enumerate exact glyph IDs;
4. enumerate data-component IDs and their persistence/network role;
5. enumerate attachment IDs and ownership/scope;
6. inspect recipes, advancements, loot, tags, data generation and localization for acquisition/reachability;
7. inspect config files and defaults;
8. inspect payload/network registrations and validate which state is client-synchronized;
9. inspect optional-mod gates, especially CC:Tweaked;
10. search the exact source tree for additional registrations outside the central registry before declaring counts complete.

No internal class/method name becomes a supported integration API merely because it is public in source. Candidate integration seams require a separate supported-contract determination.

## 8. Authority and deduplication matrix

Phase 2R must produce explicit dispositions rather than only descriptions.

### Ars Nouveau authority that must remain intact

- Source and player Ars mana;
- base spell grammar/execution;
- base glyph/augment semantics;
- Warp Scroll/portal infrastructure;
- ritual execution and ritual effects;
- Dominion Wand/configuration concepts that Ars Controle extends.

### Ars Controle authority

- its registered spell parts;
- its registered blocks/items and provider-owned reference state;
- remote linkage/configuration semantics;
- portable relay state;
- provider-specific cross-dimensional projectile/warp behavior;
- provider-specific integration/config behavior.

### Black Arcana authority that must remain intact

- canonical Black Arcana cast pipeline;
- Black Arcana cost transaction/replay/cooldowns;
- Black Arcana targeting admission;
- `WorldEffectPolicy` and protection decisions for Black Arcana mutations;
- Arcane Danger, Corruption and Strain;
- Stage 06 Black Arcana ritual orchestration;
- Stage 07.04 safe-destination/teleport contracts;
- Stage 07.07 Noetic observation/privacy contracts.

### Mandatory semantic dispositions

At minimum classify these overlaps:

- projectile relocation/remote routing;
- warp/portal infrastructure;
- remote endpoint/reference storage;
- logical/conditional spell filters;
- probabilistic spell control;
- delayed continuation/scheduling;
- portable ritual effects;
- remote resource interaction;
- performance/lag sensing.

Every row must end as one of: `PROVIDER-OWNED / DO NOT DUPLICATE`, `COMPLEMENTARY`, `BLACK ARCANA GAP`, `PRESENTATION-ONLY`, `UNKNOWN / FAIL-CLOSED`, or another already-canonical catalog disposition. Similar names are insufficient evidence.

## 9. Safety and performance review

Give special scrutiny to features that can cross distance or dimensions:

- no assumption that a provider-loaded target is safe for Black Arcana;
- no Black Arcana chunk forcing inherited from provider behavior;
- no global scans introduced for linkage, ritual relay or target discovery;
- bounded lookup/iteration must be demonstrated where a future integration depends on it;
- provider target invalidation must not produce stale Black Arcana authorization;
- provider resource transfer must not be double-processed by Black Arcana;
- player/entity/block references must remain provider-owned unless a real public boundary exposes them safely;
- optional integration failure must degrade locally and never grant free effects/resources/access.

## 10. Planned canonical deliverables

Provider tree:

`wiki/modpack-catalog/providers/ars-controle/`

Planned files:

- `README.md` — identity, authority, coverage status;
- `REGISTRY-INVENTORY.md` — exact registries/IDs/counts;
- `ACQUISITION-RECIPES.md` — recipes/learning/reachability;
- `CONFIG-COMPAT.md` — configs and optional integrations;
- `TECHNICAL-AUDIT.md` — persistence/network/capability/version-drift evidence;
- `INTEGRATION-RULES.md` — provider-native and Black Arcana boundaries;
- `glyphs/effects/precise-delay.md`;
- `glyphs/filters/above.md`;
- `glyphs/filters/level.md`;
- `glyphs/filters/below.md`;
- `glyphs/filters/not.md`;
- `glyphs/filters/or.md`;
- `glyphs/filters/xor.md`;
- `glyphs/filters/xnor.md`;
- `glyphs/filters/random.md`;
- system sheets for Warping Spell Prism, Scryer's Linkage, Temporal Stability Sensor, Warp Scroll Holder, Remote and Portable Brazier Relay.

Global overlays to update only after the provider audit is internally coherent:

- `wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE-DELTA-PHASE2R.md`;
- `wiki/modpack-catalog/meta/CAPABILITY-MATRIX-DELTA-ARS-CONTROLE.md`;
- `wiki/modpack-catalog/README.md` checkpoint/status;
- `SOURCES.md`;
- `THIRD_PARTY_NOTICES.md`;
- `docs/provenance/REFERENCE_LEDGER.md`.

Avoid destructive regeneration of the full provider queue while narrow concurrent overlays are active.

## 11. Execution order

1. Re-fetch `origin/main` and active PRs before editing provider files.
2. If PR #94 or another concurrent branch touches Ars Controle/meta files, reconcile ownership before continuing.
3. Pin provenance and source/version evidence.
4. Exhaustively enumerate registrations on the exact 1.6.15 source checkpoint.
5. Close glyph pages and acquisition.
6. Close block/item/system pages.
7. Audit persistence, networking, configs, capabilities and optional compat.
8. Reconcile every capability against Ars Nouveau, Black Arcana and already-cataloged providers.
9. Write narrow queue/capability overlays only after semantic dispositions are decided.
10. Review diff for accidental runtime/Stage changes.
11. Re-fetch `origin/main`; merge current main into the branch if it advanced.
12. Re-run documentation/applicable repository CI on the reconciled exact HEAD.
13. Merge only with exact-head gates green and no unresolved blocking review finding.
14. Confirm final `main` SHA and record the next provider only after a fresh queue/concurrency read.

## 12. Acceptance gates for Phase 2R

Phase 2R is catalog-complete only when all applicable gates are directly evidenced:

- exact physical provider identity recorded;
- exact 1.6.15 source pin and LGPLv3 provenance recorded;
- complete source registration search performed;
- all nine registered spell parts individually cataloged;
- all player-facing blocks/items individually cataloged;
- recipes/learning/acquisition resolved or explicitly `UNVERIFIED`;
- provider persistence/network/config surface classified;
- current-pack version drift recorded;
- CC:Tweaked current absence handled as optional, not assumed active;
- capability matrix dispositions written without semantic duplication;
- no new Black Arcana resource/cast/target/world-effect path introduced;
- no Stage 07.07 runtime file changed;
- no Phase 3 capability declared unblocked solely by this provider audit;
- final branch reconciled with latest `main`;
- applicable CI green on exact reconciled HEAD before merge.

## 13. Explicit non-goals

This Phase 2R plan does not:

- implement or alter Ars Controle;
- implement a Black Arcana adapter;
- add a Chaos/Order/Infernal/Holy/Blood school;
- implement a new Black Arcana spell;
- change Stage 07.07 Borrowed Sight/Astral Severance runtime;
- change Stage 08 progression/balance;
- grant Black Arcana authority over Ars Source, Ars rituals, Warp Scrolls, Ars spell grammar or Ars Controle links;
- claim runtime compatibility from source inspection alone;
- copy Ars Controle code/assets into Black Arcana.

The purpose is to finish the provider evidence and deduplication needed before Phase 3 can safely decide whether any genuine Black Arcana gameplay gap remains.