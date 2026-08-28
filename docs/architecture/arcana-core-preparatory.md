# Arcana Core — preparatory implementation checkpoint

Branch: `prep/02-arcana-core`.
Original code base: Foundation HEAD `e843d35789a7a30be16da8348e7daf06f604cdea`.
Current Foundation branch: `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00` (verification-trigger/documentation delta; still not canonical).
Status: PREPARATORY ONLY. No Stage 02 task receives ✅ and this branch must not merge before the causal gates are restored.

## Implemented infrastructure

### 02.01 — Cast identity, ingress and execution
- `ArcanaCastId` UUID identity on every cast intent.
- Canonical server-side spell resolution before request construction.
- Server-owned loadout registry and slot-to-spell validation.
- Composite identity validator.
- Bounded replay protection with duplicate, expiry and saturation semantics.
- Structured denial statuses/codes, including channel-specific denial.
- Channel lifecycle is integrated into `ArcanaServerRuntime`: begin/cancel/timeout do not execute a cast; a valid release consumes the server-owned session and enters the same `ArcanaCastEngine` used by immediate casts exactly once.
- Channel sessions preserve cast id, canonical spell id and loadout slot. Release recomputes elapsed channel time from server ticks and exposes it as bounded `ArcanaCastRequest.channelTicks`; the client cannot author charge duration.
- Release re-resolves the current spell runtime and revalidates the current server-owned loadout through the normal engine, so changing a loadout during charge cannot bypass identity checks.
- Expired abandoned channel sessions are pruned from the live server tick rather than only when another channel begins.
- `ArcanaCastIngressService` rate-limits immediate casts first, resolves canonical definitions/engines and builds the immutable server request.

### 02.02 — Transactional costs
- `check -> reserve -> effect -> commit/refund` transaction.
- `CompositeCostProvider` reserves all components atomically and rolls partial reservation back in reverse order.
- Flat and percent-of-max cost representation.
- Explicit SURVIVAL/CREATIVE/ADMIN payment policy instead of adapter-local bypasses.
- Host resource systems remain adapters; Black Arcana still has no mandatory mana pool.

### 02.03 — Targeting and bounded work
- `ArcanaTargetSpec` with hard range/count/LOS/player/friendly-fire policy.
- `TargetResolution` supports a bounded target set while retaining a primary-target convenience for single-target effects.
- `ArcanaTargetReference` provides canonical typed entity/block references instead of ad-hoc client-authored coordinates.
- `BoundedTargeting` accepts server-computed candidate facts only and applies deterministic filtering/caps.
- Minecraft `ServerEntityTargetSelector` re-resolves caster/target from live server state, refuses unloaded/missing/dead targets and never deliberately force-loads chunks.
- Minecraft routes now exist for SELF, ENTITY, PROJECTILE, BLOCK, RAY, SPHERE, CONE, CYLINDER and LINKED target kinds.
- BLOCK/RAY perform loaded-chunk preflight before clipping; ENTITY/PROJECTILE only resolve entities naturally loaded in the caster dimension.
- CONE/CYLINDER use explicit bounded `ArcanaTargetGeometry` contracts and shared pure geometry predicates; no hidden default angle/height is embedded in the adapter.
- LINKED targets come only from a server-owned `LinkedTargetResolver`; candidate sets are bounded, null-safe and stably deduplicated before entity resolution.
- `BoundedWorkScheduler` provides bounded queue/work budget and at-most-once processing per item per tick, isolates failing work items and is driven by the real server tick.
- `ScheduledArcanaEffect` enqueues bounded follow-up work through that scheduler and fails the effect before cost commit when capacity is exhausted.

### 02.04 — Cooldowns, charges and persistence
- Per-spell/shared group cooldown specs with session/persistent policy.
- Restart-capable snapshots and config-decrease clamping.
- Reusable charge pools with continuous recharge semantics and persistence snapshots.
- Composite cooldown service for spells that combine cooldown and charge policy.
- Server-owned loadout snapshot/restore.
- Cooldown keys are caster + canonical group, so dimension changes do not reset cooldown state.
- NeoForge/Minecraft `SavedData` adapter is stored globally in the Overworld.
- Saved state is captured periodically and during server stopping, then restored on server start.
- `RuntimeGroupMigrations` supports validated chained cooldown/charge group renames with cycle detection.
- Startup order is `initializers/policies -> SavedData restore -> group migrations -> orphan pruning`, so renamed state is not discarded before migration.
- Collision during cooldown rename preserves the later ready boundary; charge collisions preserve the lower charge count and later recharge boundary, preventing migrations from granting power.
- Restored orphan cooldown/charge groups are pruned only after runtime initializers register canonical active policies and migrations run.
- Defensive restore ceilings bound cooldown, charge-pool and loadout collection counts.
- Bounded cooldown UI snapshot prunes expired state for that caster.

### 02.05 — Networking and data-driven content
- Protocol v1 with centralized hard string/list bounds shared by domain payloads and NeoForge codecs.
- Cast ids, resource ids, result status/code/detail, target hints, translation keys and icon ids have one canonical bound source.
- Cooldown snapshots reject duplicate group ids and presentation snapshots reject duplicate spell ids at the protocol boundary.
- Serverbound intent contains only protocol version, cast id, spell id, loadout slot and bounded advisory target hint.
- No client packet carries authoritative damage, cost, cooldown, range, channel duration or world-destruction permission.
- NeoForge 1.21.1 payload registration is implemented with `RegisterPayloadHandlersEvent` / `PayloadRegistrar`.
- S2C cast-result, cooldown-snapshot and spell-presentation packets are registered.
- Presentation/cooldown sync happens at bounded lifecycle points only: login, metadata reload and successful cast; no per-tick full-state synchronization.
- Pure ingress tests prove unknown-spell rejection and rate limiting happen before gameplay execution.
- Real `StreamCodec<ByteBuf, ...>` round-trip tests exist for cast intent, cast result, cooldown snapshot and spell presentation packets.
- `SpellDataCatalog` atomically replaces validated metadata.
- Strict server datapack listener uses the NeoForge 1.21.1 `AddReloadListenerEvent` surface.
- Datapack spell metadata lives under `data/<namespace>/black_arcana/spells/*.json`.
- File resource id and JSON `id` must match; unknown fields are rejected.
- Datapack ids and presentation fields obey the same bounds as the wire protocol, preventing a server-valid/client-invalid metadata snapshot.
- Current data schema is intentionally presentation-only (`schemaVersion`, `id`, `translationKey`, `iconId`). Gameplay implementation/cost/damage/world mutation cannot be injected by JSON.

## Verification source written

JUnit coverage now includes:
- cast pipeline order, denial and transactional refund;
- replay duplicate/saturation/expiry;
- loadout ownership and snapshot/restore;
- channel begin/release/cancel/timeout semantics;
- channel release execution exactly once through the canonical engine, server-owned duration propagation and loadout revalidation;
- composite costs and payment-mode policy;
- cooldown persistence/config clamping/pruning/UI snapshots, dimension invariance, expired restore filtering and long-overflow saturation;
- cooldown/charge group rename chains, cycle rejection, conservative collision merge and migrate-before-prune runtime behavior;
- charge depletion/recharge/persistence/pruning;
- bounded target filtering, target-reference round-trip, cone/cylinder geometry boundaries and linked candidate normalization;
- work scheduler budget/capacity/failure isolation and scheduled-effect admission behavior;
- canonical spell anti-spoofing;
- atomic spell catalog reload;
- protocol/packet collection and identifier bounds, duplicate snapshot rejection, ingress rate limiting and real NeoForge packet codec round-trips;
- strict datapack parser schema/unknown-field/resource-id checks.

Dedicated GameTest source includes:
- a synthetic Arcana Core cast through ingress, canonical registry, loadout, replay, cooldown, target, cost reservation, world policy and effect without any optional magic mod; a second immediate cast must be denied by the server-owned cooldown;
- an NBT round-trip for persistent cooldown and loadout state using the real GameTest server registry access.

These are implementation/test sources, not a green verification claim. GitHub-hosted jobs are still terminating before runner assignment, with zero repository steps executed. Foundation run `33126490920` was retried again after this work began and the new job also completed with `steps=null`.

## Remaining work before Stage 02 can close

### 02.01
- Prove channel/replay/loadout behavior under Gradle and dedicated GameTest.
- Add any invocation-specific channel network messages only if Stage 05 UX requires them; they must terminate in the existing coordinator/engine rather than creating a second execution path.

### 02.02
- Execute the full transaction test suite in Gradle.
- Stage 03 host adapters must satisfy the same reservation contract; providers whose commit can fail irreversibly require explicit escrow/compensation design.

### 02.03
- Add dedicated GameTests for chunk borders, LOS and real entity/friendly-fire behavior.
- Bind each future expensive world/content effect to `ScheduledArcanaEffect`/`BoundedWorkScheduler`; the infrastructure is already live but content producers do not exist yet.

### 02.04
- Execute NBT save/load and actual server-restart persistence tests.
- Verify death/logout invariants in GameTests; dimension invariance is now covered at the service-contract level.

### 02.05
- Execute packet codec tests and real C2S/S2C flow in a working CI/dedicated environment.
- Add malformed/spam transport-level GameTests where the harness permits packet injection; pure protocol/ingress bounds are already covered.
- Extend the data schema with bounded authoritative balance parameters only after Stage 08 defines their canonical model; do not invent an early universal spell DSL.

## Promotion rule

Canonical order remains:

`Stage 00 green + main -> Stage 01 canonical review/merge -> Stage 02 rebase/review/test -> main`.

Preparatory progress does not change that order and no task receives ✅ until its acceptance evidence exists.
