# 07.07 — Astral Severance runtime checkpoint

## State

`PARTIAL RUNTIME IMPLEMENTATION / SERVER-OWNED PROJECTION + MOVEMENT SUBSTRATE + C2S CONTROL TRANSPORT / NOT END-TO-END`

The current implementation branch is `feat/stage07-astral-severance-control`, reconciled non-destructively with `main@c321063f41c34525cebd5e6936a560253c677442` through merge commit `3123f007a65a8ac03e701d90b8c8b968c8062425`.

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
- representation loss fails closed and terminates the server session;
- positive post-mitigation body damage terminates projection;
- player dimension change terminates it;
- logout terminates it;
- final-death settlement terminates it through the existing deferred death cleanup, preserving Soul Anchor/death-prevention authority;
- server stop clears it;
- `activeStateCount()` includes active Astral projections.

The generic observed-entity Noetic route remains unable to stand in for Astral Severance identity.

## C2S control transport

The branch now contains dedicated C2S `MOVE` and `RETURN` transport.

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

MOVE and RETURN use separate `IngressRateLimiter` instances:

- at most one MOVE intent per authenticated caster per server tick;
- at most one RETURN intent per authenticated caster per server tick;
- bounded tracked-caster capacity reuses `ArcanaServerRuntime.DEFAULT_MAX_TRACKED_CASTERS`.

These are protocol abuse/safety bounds, **not** Stage 08 spell balance values. Separate MOVE/RETURN windows ensure a valid cancellation attempt is not consumed merely because the same caster sent a movement intent in that tick.

## Deliberate fail-closed boundary: MOVE execution policy

The C2S MOVE packet is registered, decoded, validated and rate-limited, and the bridge exposes a server handler seam. Production `BlackArcanaMod` does **not** install a MOVE gameplay handler yet.

This is intentional. `MinecraftNoeticRuntime.applyAuthorizedAstralControl(...)` requires server-selected `AstralSeveranceRuntime.ControlLimits`, but the current canonical config/specification does not freeze a production `maxStepBlocks` or `maxLookDeltaDegrees` authority/value. Existing test fixture values must not become accidental gameplay defaults, and `NoeticSafetyCeilings` are absolute implementation ceilings rather than balance defaults.

Therefore MOVE remains fail-closed at the transport-to-gameplay seam until a reviewed canonical server-side control-limit/config authority exists. RETURN can be connected now because it does not require inventing missing balance values.

## Authority and non-goals

This checkpoint does not add a second casting route. It does not choose or settle resource cost, cooldown, progression, hazard, channel state or final gameplay tuning. Activation remains downstream runtime work after the canonical cast/channel transaction authorizes the spell.

It also does **not** yet implement:

- client-side Astral Severance camera/viewpoint control;
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

Existing earlier Astral lifecycle/movement tests continue to cover server-owned identity, movement sequencing, range, loaded-only application, representation wiring and cleanup behavior.

For the C2S tranche, test commit `123c60d08600d2e3dc18442876dbc3ad44df5117` introduced the payload contract before implementation. Its GitHub Actions run did not obtain a runner before later branch pushes superseded it, so it is **not** recorded as executed RED CI evidence.

Subsequent implementation/review commits include:

- `385f2ab00994474251cdeacb819617e5d5688298` — bounded C2S MOVE/RETURN transport;
- `774c2e0d22cc62cbb5df20ee4bceae9fcdc19ac5` — Minecraft 1.21.1-compatible stream-codec composition;
- `30711187c63440e6cfedf947499edc94dc665f55` — MOVE/RETURN codec round-trip coverage;
- `b8ec5f8915ae64d4f8bcf14e6e68a34b987446c7` — isolated MOVE/RETURN ingress limits and canonical tracked-caster capacity.

These commits are implementation history only. They are **not** GREEN evidence until the exact reconciled PR HEAD passes the complete Black Arcana CI pipeline. Any documentation commit after them also requires a fresh exact-HEAD gate before merge.

## Remaining 07.07 gate

Astral Severance remains **NOT IMPLEMENTED end-to-end** until at minimum:

- a reviewed canonical server-side control-limit/config authority exists and MOVE execution is connected without inventing Stage 08 values;
- client camera/input presentation is implemented without transferring gameplay authority to the client;
- activation/channel lifecycle is connected through the canonical Stage 02 cast/channel transaction without introducing a parallel authority path;
- the complete per-spell specification gate closes the remaining resource/cooldown/scaling/progression/config/provenance fields;
- required automated tests are GREEN on the exact reconciled merge head;
- real-client acceptance is directly observed where required by D031.

Therefore:

- Stage 07.07 remains `IN PROGRESS`;
- Borrowed Sight real-client acceptance remains deferred under D031;
- no real-client Astral Severance acceptance exists yet;
- Stage 08 must not consume 07.07 as canonical balance input yet.
