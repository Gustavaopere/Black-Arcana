# Arcana Core — preparatory implementation checkpoint

Branch: `prep/02-arcana-core`
Base: Foundation HEAD `e843d35789a7a30be16da8348e7daf06f604cdea`.
Status: PREPARATORY ONLY. Stage 00 is not canonical; no Stage 02 task receives ✅ and this branch must not merge before the causal gates are restored.

## Implemented pure-Java infrastructure

### Cast identity and execution
- `ArcanaCastId` UUID identity on each request.
- `CastRequestValidator` seam for canonical identity/loadout/policy checks.
- `ReplayGuard` seam and bounded in-memory implementation.
- Engine order begins with identity and replay validation before progression/cooldown/target/cost/world mutation.
- Duplicate cast ids and replay-guard saturation have explicit denial codes.

### Costs
- Foundation `check -> reserve -> effect -> commit/refund` transaction is preserved.
- `CompositeCostProvider` reserves providers sequentially and refunds already-reserved components in reverse order if a later component fails.
- Composite reservation commit uses deterministic provider order; explicit refund uses reverse order.
- Provider contract assumes `commit()` is infallible after a successful reservation. A provider that can still fail irreversibly at commit is not compatible with the contract and must use a compensating/escrow adapter designed explicitly in Stage 03.

### Cooldowns
- `ArcanaCooldownSpec` supports shared group id, bounded duration and session/persistent mode.
- `PersistentCooldownService` stores caster/group entries, produces persistent snapshots and restores them.
- A later config decrease can shorten an existing cooldown; a later increase does not extend an already-started cooldown.
- Cooldown time currently consumes `ArcanaCastContext.serverTick`; the canonical Minecraft bridge must supply a persistent monotonic gameplay tick suitable for restart-safe SavedData semantics.

### Targeting and bounded effects
- `ArcanaTargetSpec` defines target kind, hard maximum range, target count, LOS, player and friendly-fire policy.
- `BoundedTargeting` filters server-computed candidates only: loaded/alive/range/LOS/player/friendly state, then sorts deterministically and applies the target cap.
- `BoundedWorkScheduler` enforces a fixed per-tick work budget, bounded queue and at-most-once-per-item processing each tick.
- No client-provided coordinates become authoritative through these primitives.

### Canonical registries and data
- `ArcanaSpellRegistry` atomically replaces compiled server definitions and rejects unknown/spoofed definitions.
- `SpellDataCatalog` atomically reloads validated schema-v1 metadata and produces deterministic presentation snapshots.
- Failed duplicate/malformed reloads leave the previous registry snapshot intact.

### Network contracts, not transport
- Protocol version 1 and hard collection/string bounds.
- Cast intent carries only `castId`, `spellId`, bounded `loadoutSlot` and bounded target hint.
- Cast result, cooldown snapshot and presentation snapshot records are versioned and bounded.
- `IngressRateLimiter` provides bounded per-caster sliding-window request control before expensive cast execution.
- No payload contains authoritative damage, cost, cooldown, range or world-destruction values.

## Test contracts written

JUnit coverage has been added for:
- identity-before-replay ordering;
- deterministic cast pipeline;
- effect failure/exception refund;
- replay duplicate/saturation/expiry;
- composite cost partial-reservation rollback and terminal order;
- cooldown expiry, persistence, session-only mode and config-change clamping;
- target validity/range/LOS/player/friendly filtering and hard target cap;
- work-budget enforcement and queue capacity;
- canonical spell definition anti-spoofing and atomic registry reload;
- protocol/version/collection bounds;
- ingress rate limiting;
- atomic spell-data reload and deterministic presentation ordering.

These tests are source-level preparatory evidence only until Gradle/NeoForge executes them in a real verification environment.

## Remaining work by Stage 02 task

### 02.01 Cast Request & Execution
Still required:
- actual loadout ownership validator and slot-to-spell resolution;
- charge/channel lifecycle without duplicate execution semantics;
- request creation path from server-validated network intent;
- dedicated-server replay/duplicate tests.

### 02.02 Resource & Cost Providers
Still required:
- explicit flat vs percent-of-max cost representation;
- creative/admin payment policy;
- zero-cost provider and reusable reservation utilities;
- composite provider contract tests executed by Gradle;
- later host adapters must run the same transaction suite.

### 02.03 Targeting & Effect Runtime
Still required:
- Minecraft/NeoForge candidate collection for self/entity/ray/block/cone/sphere/cylinder/projectile/linked targets;
- actual chunk-loaded, LOS, entity-liveness and friendly-team facts from server state;
- effect enqueue integration with the work scheduler;
- GameTests for chunk edges and real entities.

### 02.04 Cooldowns & Persistence
Still required:
- SavedData or equivalent server persistence bridge;
- canonical persistent tick/time source;
- charge pools;
- death/logout/dimension/restart GameTests;
- migration/pruning of obsolete cooldown groups.

### 02.05 Networking & Data-driven Content
Still required:
- NeoForge 1.21.1 payload registration and codecs;
- server handler that rate-limits, resolves the canonical spell, validates loadout and builds `ArcanaCastRequest`;
- minimal result/cooldown/presentation synchronization;
- reload listener/datapack codec bridge for `SpellDataCatalog`;
- malformed/spam packet dedicated-server tests.

## Promotion rule

This branch may continue implementing pure Black Arcana infrastructure while Foundation verification is externally blocked, but canonical promotion remains:

`Stage 00 green + main -> Stage 01 canonical review/merge -> Stage 02 rebase/review/test -> main`.

No preparatory checkpoint changes that causal order.