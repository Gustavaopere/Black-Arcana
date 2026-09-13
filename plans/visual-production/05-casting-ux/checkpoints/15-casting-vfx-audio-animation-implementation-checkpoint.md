# Stage 05.15 — Casting VFX / Audio / Animation Presentation — Implementation Checkpoint

Status: **APPROVED STAGE 05 HARDENING / IMPLEMENTED PROVIDER-FREE TRANCHE / PHYSICAL-CLIENT QA PENDING**

Canonical implementation branch checkpoint base: `main@0bd1c04460e63a03b6b484b785247e75f6e44178`.

## Scope delivered

### Phase A — evidence and authority boundary

Delivered in `docs/architecture/casting-audiovisual-provider-boundary.md`.

The generic Stage 05.15 tranche requires no external animation, camera, particle, or spell-provider API. Cast admission, targeting, world mutation, costs, cooldowns and settlement remain server-authoritative. Borrowed Sight keeps its dedicated Stage 07 camera/channel lifecycle and is not folded into this generic presentation layer.

### Phase B — pure presentation lifecycle

Delivered as a bounded, provider/renderer-independent model keyed by canonical `ArcanaCastId`.

The model distinguishes local anticipation from authoritative server result. Local intent cannot promote itself to success. Unmatched results remain generic and do not infer spell/target/impact context. Duplicate settled results are idempotent. State has deterministic size, stale-age and clear semantics. Accessibility policy (`particleDensity`, reduced motion, reduced flashes) is presentation-only.

### Phase C — generic result/denial audiovisual presentation

Delivered as a physical-client sink driven only by correlated local intent and authoritative generic cast results.

Presentation consists of:

- bounded anticipation/result pulse in screen space;
- UI-local project-owned sound when the corresponding resource exists;
- success / denial / effect-failure outcomes with the latest authoritative result replacing older authoritative pulses;
- local anticipation never visually overwriting an active authoritative result;
- no world-space impact marker, hit-result lookup, target inference, range claim or gameplay telegraph.

### Phase D — project-owned resources, fallback and provenance

Delivered:

- `black_arcana:cast.intent`;
- `black_arcana:cast.success`;
- `black_arcana:cast.denied`;
- `black_arcana:cast.failed`;
- four original Black Arcana OGG assets;
- `sounds.json` bindings;
- positive/negative resource resolution cache;
- fail-closed missing/malformed-resource handling;
- resource-reload invalidation and transient-effect teardown;
- clean-room provenance and SHA-256 inventory in `docs/architecture/casting-audiovisual-asset-provenance.md`.

Resource availability never changes cast legality or server result semantics.

## Deferred by evidence gates

### Phase E — animation-provider adapter

**DEFERRED / NOT REQUIRED FOR THE CURRENT GENERIC TRANCHE.**

There is no concrete Stage 05.15 behavior that currently requires an external animation-provider API. The plan's exact-version provider gate therefore remains closed rather than inventing an adapter. If a later content requirement needs provider animation, exact physical-version API evidence must be captured before implementation.

### Phase F — gameplay-relevant telegraph geometry

**DEFERRED / NO GENERIC AUTHORITY AVAILABLE.**

The current generic cast result contract does not carry authoritative world/impact geometry or lifecycle geometry. Stage 05.15 therefore does not infer telegraph positions from client aim, `hitResult`, selection, camera, or provider state. Content-specific Stage 07 presentation may consume its own server-owned lifecycle facts where separately specified.

### Phase G — real-client/full-pack audiovisual QA

**PENDING PHYSICAL-CLIENT QA.**

CI, GameTests and dedicated-server smoke do not substitute for a physical assembled-pack client. Do not mark visual/audio timing, GUI-scale behavior, live sound playback, resource reload, reduced-motion/reduced-flash perception, or coexistence with Iron's / Spell Actionbar / Epic Fight / EFIS as PASS until executed on the physical client.

## Phase H — teardown / cleanup contract

Implemented cleanup boundaries include:

- bounded pulse expiry;
- stale cast-correlation eviction;
- logout/disconnect/session loss;
- player UUID/session replacement;
- player death;
- dimension transition;
- screen transition suppression/clear for transient pulse presentation;
- resource reload;
- provider absence (no provider adapter is installed or required).

Generic result settlement cancels/replaces anticipation for the same correlated cast. The single transient pulse is bounded to one entry. No temporary presentation state is persisted as gameplay state.

## Protocol and authority non-expansion

This tranche adds:

- no new network payload;
- no protocol version change;
- no client-authored gameplay admission;
- no target/impact geometry authority;
- no provider-owned gameplay mutation;
- no generic camera ownership;
- no shader requirement;
- no world-space particle/impact engine.

`CastIntentPayload.castId` and `CastResultPayload.castId` are reused for correlation. The client-created ID is recorded before transport and the exact canonical ID is sent to the server.

## TDD / CI evidence

Key evidence from the implementation sequence:

- Phase C candidate `0a9bc454…` — workflow `34739694016` GREEN;
- reconciled Phase C `731589f5…` — workflow `34740088968` GREEN;
- Phase D resource RED — workflow `34740228124`, expected missing `CastPresentationResources`;
- project-owned resource candidate `f72877bc…` — workflow `34740536325` GREEN;
- effects-layer RED `6a8576ce…` — workflow `34740738323`, expected missing `CastPresentationPulseState`;
- reload/teardown fix `f113e483…` — workflow `34740994253` GREEN;
- authoritative-pulse ordering RED `e25c750d…` — workflow `34741549287`, one expected regression failure (`RESULT_SUCCESS` blocked by older `RESULT_DENIED`);
- ordering fix `e8ac64ee…` — workflow `34741686833`: attempt 1 reached GameTests and failed only unrelated Rift Blades UUID-index fixture visibility; the exact same SHA rerun as attempt 2 passed unit tests, diff sanity, build, JAR verification, all GameTests and dedicated-server smoke;
- Phase H teardown RED `ba7358fe…` — workflow `34741979741`, one expected missing death/dimension/screen teardown contract;
- Phase H production `ff622ac0…` — workflow `34742086866` GREEN across unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke;
- reconciliation with current main completed as real two-parent merge `5686c96322773b3cf5de321423c4a613f817af2f`, preserving Phase 2BS catalog work and leaving the effective diff restricted to Stage 05.15.

## Remaining gate

Before durable merge, require a final GREEN CI run on the latest reconciled/checkpoint HEAD and re-check `main` for additional concurrent drift. After merge, require the canonical `main` workflow including canonical QA JAR publication.

Physical-client/full-pack validation remains separate and **PENDING** after merge until actually executed.
