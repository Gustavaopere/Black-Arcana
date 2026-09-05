# 07.04 — Space & Displacement

## State

**CANONICAL ON `main` / IMPLEMENTED / FINAL REAL-MODPACK VALIDATION DEFERRED.**

Stage 07.04 was implemented sequentially from canonical `main@f30999b375d42506127eb4c7570f1b8bfd68262c` in PR #52 and merged at `a567419f1cccd3a33db95402fcb267c0ad79bc67`. Historical stacked PR #22 remained reviewed source material only and was not merged as canonical ancestry.

Final PR-head workflow `33997420003` passed JUnit, diff sanity, NeoForge build, JAR inspection, all required GameTests and dedicated-server smoke on head `f74bf5b15e3178392a2ea52d3f00969ac6288ea2`.

Exact-SHA post-merge workflow `33997767668` passed the full pipeline on `main@a567419f1cccd3a33db95402fcb267c0ad79bc67`, including **77/77 required GameTests**, dedicated-server smoke and canonical QA artifact publication.

Canonical QA artifact:

- name: `black-arcana-a567419f1cccd3a33db95402fcb267c0ad79bc67`;
- artifact ID: `9978600971`;
- SHA-256: `c4343f5764d76d6b5310dc446ff1bfbb9359b17ccf74898e615743010259dc1e`.

No 07.05–07.07 runtime is included in this domain. Real-modpack/provider/manual host acceptance remains deferred under D031 and is not inferred from automated CI.

## Implemented mechanics

### Threshold Gate

Server-authoritative paired-threshold transfer for existing eligible living entities.

- stable gate-pair identity and owner context;
- same permitted loaded dimension only;
- no chunk force-loading;
- shared safe-destination admission before settlement and immediate revalidation;
- explicit consent when another player is moved;
- bounded fixed-window throughput;
- lifecycle cleanup on server stop;
- settlement uses the entity teleport contract so `ServerPlayer` follows its player-specific teleport path.

The host/provider owns threshold presentation and crossing detection. Black Arcana owns pair registration, validation, throughput, player consent and final movement. Blocks and block entities are never transferred by this runtime.

### Veilstep Reflex

Bounded owner-scoped reflex teleport with charge/cooldown semantics and safe-candidate validation.

- bounded safe-position candidate search;
- no unloaded-destination force-load path;
- server-owned charge/cooldown state;
- logout/server-stop cleanup;
- protected, colliding, fluid-unsafe, vehicle-unsafe or otherwise invalid destinations fail closed.

### Anchor Recall

Owner-attributed projectile recall to a previously captured anchor context.

- projectile identity and owner are explicit;
- same permitted loaded dimension by default;
- projectile age and recall range are bounded;
- destination safety is revalidated at settlement;
- logout/server-stop cleanup prevents stale owner state;
- no inferred cross-dimensional recall or forced chunk load.

### Reciprocal Transposition

Transactional exchange of two eligible loaded entity endpoints.

- distinct endpoint identities;
- explicit host/server consent inputs;
- same loaded dimension;
- endpoint fingerprints captured and rechecked before settlement;
- both destinations are validated and revalidated;
- protection admission is server authoritative;
- throughput is owner-scoped and bounded;
- settlement and rollback use the entity teleport contract, including the `ServerPlayer` override when applicable;
- ItemEntity participation preserves the existing stack and does not clone or consume it.

The runtime never transposes blocks or block entities.

### Vector Reversal

Bounded directional displacement/impulse over explicitly supplied living targets.

- finite non-zero direction;
- maximum four distinct targets per application;
- canonical Stage 04 entity-interaction admission and settlement revalidation;
- player and boss semantic multipliers;
- resulting velocity hard-clamped;
- partial authorization is explicit: denied targets do not invalidate already-authorized independent targets.

## Shared destination authority

`SafeDestinationPolicy` and `MinecraftSafeDestinationResolver` preserve one fail-closed destination contract for the domain. Applicable movement checks include:

- destination chunk already loaded;
- live world border;
- full-entity collision/headroom;
- fluid policy;
- dimension rules;
- protected-area/entity interaction authority;
- teleport-support tags;
- passenger/vehicle safety.

Queries are bounded and must not force-load chunks. Unknown/missing protection authority does not become implicit permission.

## Frozen technical ceilings

These values are **hard safety ceilings**, not final Stage 08 balance targets:

- Threshold Gate throughput: at most `32` transfers/second;
- Anchor Recall projectile age: at most `600` ticks;
- Anchor Recall distance: at most `128` blocks;
- Reciprocal Transposition throughput: at most `16` swaps/second;
- resulting Vector Reversal speed: at most `2.5` blocks/tick;
- safe-position candidate search: at most `64` candidates.

Stage 08 may tune ordinary gameplay values below these ceilings but must not silently raise the ceilings or weaken the safety authority.

## Provider and authority boundaries

- Black Arcana core/Stage 04 remains authority for destination/entity-interaction safety.
- Ars Nouveau or other hosts may expose invocation/resource/presentation surfaces, but do not become destination authority merely by hosting a cast.
- Iron's Spells or combat hosts may expose invocation/cost/cooldown context, but do not bypass Black Arcana protection, consent, throughput or safe-destination settlement.
- Optional providers that do not expose a verified causal/authorization hook remain fail-closed for the dependent feature; no generic substitute bonus is introduced.
- Client presentation/input is never accepted as authoritative destination, consent, ownership or protection state.

## TDD and validation evidence

The implementation was rebuilt from latest canonical `main` with RED→GREEN discipline rather than merging stale PR #22 ancestry.

Additional audit hardening during PR #52 identified two live-wiring/settlement issues:

1. stateful 07.04 lifecycle runtimes existed but were not registered by `BlackArcanaMod`; an explicit RED wiring contract reproduced the missing composition-root registration before Threshold Gate, Veilstep Reflex, Anchor Recall and Reciprocal Transposition were registered on `NeoForge.EVENT_BUS`;
2. Threshold Gate and Reciprocal Transposition used raw `setPos(...)` even though player endpoints are supported; a dedicated RED contract failed on both paths before settlement/rollback were moved to `teleportTo(...)`.

The canonical post-merge GameTest server ran 77 tests and reported `All 77 required tests passed`. Coverage includes loaded safe destinations, collision/headroom, fluids, world border, dimension mismatch, vehicles, player consent, throughput, stale endpoint snapshots, atomic/no-partial transposition behavior, ItemEntity non-duplication and Vector Reversal authorization/bounds.

## Deferred acceptance

Real-modpack/provider/manual host acceptance remains `FINAL VALIDATION DEFERRED` under D031. Automated CI proves deterministic Black Arcana contracts only; it does not convert unexecuted real-client/provider rows into PASS.
