# 07.07 — Astral Severance runtime checkpoint

## State

`PARTIAL RUNTIME IMPLEMENTATION / SERVER-OWNED PROJECTION + MOVEMENT SUBSTRATE + C2S CONTROL TRANSPORT + S2C CAMERA PRESENTATION / NOT END-TO-END`

The control tranche is canonical on `main` via PR #235 at merge SHA `29454a7dd604ba0ea0200724d53bd9526b09cb10`, built from the earlier lifecycle merged by PR #138 at `3469b454de2b65d0c15e89e7d689fe760dd30994`. The server-authored Astral camera-presentation tranche is canonical via PR #240 at merge SHA `834c3f7e2c236161e04e21c1e690ca9e0503a39b`.

This checkpoint closes additional bounded Stage 07.07 runtime gaps. It does **not** complete Astral Severance, promote 07.07, freeze Stage 08 balance values, or authorize a parallel cast path.

## Implemented boundary

`AstralSeveranceRuntime` owns bounded ephemeral projection state keyed by the physical caster. The runtime provides:

- one active projection per caster;
- a bounded global active-projection ceiling;
- server-generated projection UUID identity;
- immutable active snapshots retaining the physical caster as the canonical body identity;
- exact projection-id matching for control and explicit return;
- monotonic movement/control sequence tracking;
- stale, foreign, replayed and wrong-session movement intent failing closed;
- finite movement axes bounded to `[-1, 1]`;
- finite look-delta validation;
- server-selected `ControlLimits` for movement step/look clamping;
- range enforcement from the server-owned origin;
- loaded-only destination admission;
- duration and range admission constrained by existing `NoeticSafetyCeilings` hard ceilings;
- expiry and server-stop cleanup.

`AstralProjectionEntity` is the dedicated non-owning server-side world representation. It mirrors only the server-owned logical projection pose. It does not become a player clone, second caster, inventory owner, combat attribution root or persistence authority.

`MinecraftNoeticRuntime` composes this lifecycle with Minecraft/NeoForge server state:

- activation requires an already-loaded living `ServerPlayer` physical body and remains explicitly downstream of upstream canonical cast authorization;
- projection materialization uses the server-authored projection UUID;
- movement updates resolve only the authenticated caster's loaded representation;
- destination checks use `getChunkNow`, never chunk acquisition/tickets;
- accepted logical movement is mirrored to the representation;
- representation loss is revalidated every server tick from only the bounded active Astral session set and terminates the session without waiting for a MOVE packet;
- positive post-mitigation body damage terminates projection;
- player dimension change terminates it;
- logout terminates it;
- final-death settlement terminates it through the existing deferred death cleanup, preserving Soul Anchor/death-prevention authority;
- server stop clears it;
- `activeStateCount()` includes active Astral projections.

The generic observed-entity Noetic route remains unable to stand in for Astral Severance identity.

## C2S control transport

The canonical runtime contains dedicated C2S `MOVE` and `RETURN` transport.

### Authority contract

Caster identity is **never** supplied by the client. NeoForge handlers derive the authenticated caster only from `IPayloadContext.player()`.

The client payloads carry only bounded intent:

- exact server-authored `projectionId`;
- positive monotonic `sequence`;
- MOVE: strafe/vertical/forward axes plus yaw/pitch deltas;
- RETURN: exact projection identity plus sequence.

They do **not** carry:

- caster UUID;
- authoritative world coordinates;
- authoritative velocity;
- duration/range extensions;
- cost/cooldown settlement;
- a target entity to borrow as projection identity.

`AstralMoveIntentPayload` validates protocol version, exact projection identity, positive sequence, finite unit axes and finite look deltas before the domain `ControlIntent` is constructed.

`AstralReturnIntentPayload` validates protocol version, exact projection identity and positive sequence. The production RETURN handler additionally requires the return sequence to be newer than the active projection's `lastProcessedControlSequence` before closing the exact authenticated caster session. After close, replay naturally fails because no active projection remains.

### Wire compatibility

Minecraft/NeoForge 1.21.1 compatibility is preserved by composing the MOVE codec from bounded nested records rather than relying on later-version high-arity `StreamCodec.composite` overloads. Projection identity uses Minecraft's `UUIDUtil.STREAM_CODEC`.

Unit coverage round-trips both MOVE and RETURN codecs back to the validated domain payloads and asserts that no trailing bytes remain.

### Ingress bounds

MOVE and RETURN use independent ingress windows:

- at most one MOVE intent per authenticated caster per server tick;
- at most one RETURN intent per authenticated caster per server tick;
- bounded tracked-caster capacity reuses `ArcanaServerRuntime.DEFAULT_MAX_TRACKED_CASTERS`;
- limiter histories are scoped to the concrete `MinecraftServer`, so an integrated-server restart/world-server replacement cannot inherit a larger tick history and fail valid packets as `clock_regression`;
- server ingress state uses weak server keys so stopped server instances are not retained solely for transport-abuse accounting.

These are protocol abuse/safety bounds, **not** Stage 08 spell balance values. Separate MOVE/RETURN windows ensure a valid cancellation attempt is not consumed merely because the same caster sent a movement intent in that tick.

## S2C camera presentation

The canonical runtime now contains a bounded, server-authored Astral camera presentation path. It does not add gameplay authority to the client.

- `AstralViewPayload` / `AstralViewPacket` carry only protocol version, `BEGIN`/`END`, the exact server-authored projection UUID and the transient loaded entity id.
- `AstralViewTransitionTracker` is bounded by the existing Noetic active-session ceiling and emits no duplicate transition for unchanged state.
- Replacing a tracked projection emits `END` for the old exact identity before `BEGIN` for the new identity.
- `MinecraftNoeticRuntime` derives desired Astral presentation only from canonical `AstralSeveranceRuntime.ActiveProjection` snapshots and resolves the representation by exact UUID in the already-loaded caster level.
- Missing/unloaded representation produces no camera claim and never acquires a chunk.
- The physical client changes camera only when the received entity id resolves to a loaded `AstralProjectionEntity` whose UUID exactly matches the server-authored projection UUID.
- A `BEGIN` that arrives before vanilla entity spawn remains pending while the physical body keeps the camera; later client ticks may claim the camera only after the exact representation becomes available.
- A stale `END` cannot clear a newer desired projection because client presentation state closes only the matching projection UUID.
- Concurrent Borrowed Sight and Astral camera claims for the same viewer fail closed: both presentations are suppressed rather than inventing a priority rule.
- Astral and Borrowed Sight camera restoration is ownership-safe: a controller restores the physical body only if the current camera is still the exact entity that controller previously claimed.

This tranche does **not** capture movement/look input, call `sendMove`, settle gameplay, or make the client authoritative for projection pose.

## Deliberate fail-closed boundary: MOVE execution policy

The C2S MOVE packet is registered, decoded, validated and rate-limited, and the bridge exposes a server handler seam. Production `BlackArcanaMod` does **not** install a MOVE gameplay handler yet.

This is intentional. `MinecraftNoeticRuntime.applyAuthorizedAstralControl(...)` requires server-selected `AstralSeveranceRuntime.ControlLimits`, but the current canonical config/specification does not freeze a production `maxStepBlocks` or `maxLookDeltaDegrees` authority/value. Existing test fixture values must not become accidental gameplay defaults, and `NoeticSafetyCeilings` are absolute implementation ceilings rather than balance defaults.

Therefore MOVE remains fail-closed at the transport-to-gameplay seam until a reviewed canonical server-side control-limit/config authority exists. RETURN can be connected now because it does not require inventing missing balance values.

## Authority and non-goals

This checkpoint does not add a second casting route. It does not choose or settle resource cost, cooldown, progression, hazard, channel state or final gameplay tuning. Activation remains downstream runtime work after the canonical cast/channel transaction authorizes the spell.

It also does **not** yet implement:

- client input capture/redirect from the physical body to the projection;
- a production MOVE gameplay policy with frozen server-side control limits;
- projection interaction with blocks, containers, items or entities;
- casting or combat from the astral position;
- chunk tickets or force-loading;
- terrain mutation;
- persistence/resume across logout or restart;
- final resource authority/cost;
- cooldown identity/value;
- scaling equation;
- final RPG Skill Tree progression/mastery gate;
- final bounded gameplay config surface;
- per-spell provenance closure.

Those omissions are intentional fail-closed boundaries, not implicit permission for later code to invent them.

## Test evidence boundary

Existing earlier Astral lifecycle/movement tests cover server-owned identity, movement sequencing, range, loaded-only application, representation wiring and cleanup behavior.

For the C2S tranche, test commit `123c60d08600d2e3dc18442876dbc3ad44df5117` introduced the payload contract before implementation. Its GitHub Actions run did not obtain a runner before later branch pushes superseded it, so it is **not** recorded as executed RED CI evidence.

A later review found that representation loss was only observed from MOVE handling. Test-only commit `6b36734dee4d1c324714a5147799cd9c7da9d983` added `missingProjectionRepresentationClosesServerSession`, but its workflow also did not receive a runner and was cancelled when the fix was pushed. It is therefore retained as TDD history, **not** claimed as executed RED evidence.

Implementation/review history for the control tranche includes:

- `385f2ab00994474251cdeacb819617e5d5688298` — bounded C2S MOVE/RETURN transport;
- `774c2e0d22cc62cbb5df20ee4bceae9fcdc19ac5` — Minecraft 1.21.1-compatible stream-codec composition;
- `30711187c63440e6cfedf947499edc94dc665f55` — MOVE/RETURN codec round-trip coverage;
- `b8ec5f8915ae64d4f8bcf14e6e68a34b987446c7` — isolated MOVE/RETURN ingress limits and canonical tracked-caster capacity;
- `1cf6e16144bf11977dc45fc88cbd4e56edf3bdc4` — bounded tick revalidation so representation loss closes the server session without MOVE input;
- `bf3945c068d136f55151417dca27325eb9d12cc7` — per-`MinecraftServer` ingress state, preventing cross-server tick-history contamination.

Final control branch head `8b9fd3ce0bb2347dc672b85db058eeb891d850d9` passed push workflow `34778875762` and PR workflow `34778877787` through JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke. PR #235 was then squash-merged at `main@29454a7dd604ba0ea0200724d53bd9526b09cb10`; exact-SHA post-merge workflow `34779849669` passed the complete pipeline and published canonical QA artifact `black-arcana-29454a7dd604ba0ea0200724d53bd9526b09cb10`, artifact ID `10325066285`, SHA-256 `8c5d47037661e2b697196e15ef0ca272dce5e4d496b11aef99edc323b54e69b4`.

For the S2C camera tranche, test-only head `f01dcc0db5c3e5cd48fe3dca396c5336a0f830ec` produced executed RED evidence in workflow `34793604024`: `compileTestJava` failed because `AstralViewPayload` and `AstralViewTransitionTracker` did not yet exist. The implemented branch head `9080f01763a13696471965c40142671215c02cec` passed push workflow `34794636221`, and PR #240 workflow `34796582786` passed JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke against the then-current `main`. PR #240 merged at `main@834c3f7e2c236161e04e21c1e690ca9e0503a39b`; exact-SHA post-merge workflow `34796772128` passed the complete pipeline and published canonical QA artifact `black-arcana-834c3f7e2c236161e04e21c1e690ca9e0503a39b`, artifact ID `10330321029`, SHA-256 `45cd7777f67fd8ccba127a1091a7cd9f43226f65c9172642d9c507c75b4e11a5`.

## Remaining 07.07 gate

Astral Severance remains **NOT IMPLEMENTED end-to-end** until at minimum:

- a reviewed canonical server-side control-limit/config authority exists and MOVE execution is connected without inventing Stage 08 values;
- client movement/look input capture and redirect is implemented without transferring gameplay authority to the client;
- activation/channel lifecycle is connected through the canonical Stage 02 cast/channel transaction without introducing a parallel authority path;
- the complete per-spell specification gate closes the remaining resource/cooldown/scaling/progression/config/provenance fields;
- required automated tests are GREEN on the exact reconciled merge head;
- real-client acceptance is directly observed where required by D031.

Therefore:

- Stage 07.07 remains `IN PROGRESS`;
- Borrowed Sight real-client acceptance remains deferred under D031;
- automated Astral camera presentation is canonical, but no real-client Astral Severance acceptance exists yet;
- Stage 08 must not consume 07.07 as canonical balance input yet.