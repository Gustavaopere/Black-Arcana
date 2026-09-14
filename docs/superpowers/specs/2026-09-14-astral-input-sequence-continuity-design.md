# Astral Severance input sequence continuity — design

Date: 2026-09-14
Stage: 07.07 Familiars & Divination / Astral Severance
Target PR: #248 (`feat/stage07-astral-input-redirect`)
Baseline: `main@62c4b5b1b7e02b082557ef74d58d3eb7acd4f36b`

## Purpose

Close the sequence-continuity defect in the pending Astral Severance client movement/look redirect without widening gameplay authority, enabling production MOVE values, or creating a parallel cast/control pipeline.

PR #248 introduces client-side input redirection behind server-authored `MOVE_ARM` / `MOVE_END` state. The server already owns Astral projection identity and monotonic control admission through `AstralSeveranceRuntime.applyControl(...)`. The client therefore must preserve sequence monotonicity for the lifetime of one exact server-authored projection identity.

## Current defect

`AstralSeveranceInputController` currently calls `AstralControlIntentSequencer.clear()` whenever movement control is not armed. `clear()` drops the remembered projection identity and resets the local sequence to zero.

`MOVE_END` may revoke client movement control while leaving the same Astral projection active. The canonical server runtime does not reset `ProjectionSession.lastProcessedControlSequence` merely because client control is disarmed. If the same projection is later re-armed, the client can restart at sequence `1` while the server still requires a value greater than the previously processed sequence. Those packets then fail closed as `STALE_SEQUENCE` until the client counter catches up, which can make control appear frozen.

This is a client sequence-lifecycle mismatch, not a server authority defect.

## Architectural constraints

The correction must preserve these existing contracts:

- caster identity comes from authenticated network context, never from the client payload;
- the client sends bounded movement/look intent, not authoritative coordinates or pose;
- one server-authored `projectionId` scopes control sequencing;
- `AstralSeveranceRuntime` remains authoritative for `lastProcessedControlSequence` and stale/replay rejection;
- camera `BEGIN`/`END` remains distinct from movement authorization `MOVE_ARM`/`MOVE_END`;
- no production `ControlLimits` values are introduced;
- production MOVE remains fail-closed until the separate reviewed server-owned value contract exists;
- PR #247's canonical cast/channel binding remains untouched and continues to satisfy D024/D025;
- no new protocol field, server reset command, Mixin, second cast path, or second gameplay authority is introduced.

## Considered approaches

### 1. Preserve the client sequence for the lifetime of the exact projection — selected

Disarming movement clears only transient pending input/look state. The monotonic sequence counter and exact `projectionId` remain retained while that projection is still the active Astral presentation identity. Re-arming the same projection therefore continues with `N+1`.

A true projection end, explicit client-state reset, or switch to a different `projectionId` resets the sequencer for the new session.

This matches the server's existing lifecycle with the smallest authority surface.

### 2. Reset the server sequence on `MOVE_END` — rejected

This would add server lifecycle semantics solely to compensate for client state loss. It would weaken the current monotonic replay boundary, require exact transition synchronization, and create additional server mutation not required by the Astral runtime design.

### 3. Send last accepted sequence in S2C control messages — rejected

This would add protocol state and synchronization complexity without a demonstrated need. The client already owns its locally emitted sequence for the exact projection identity, while the server remains authoritative in accepting or rejecting it.

## Selected design

### Sequencer lifecycle

`AstralControlIntentSequencer` distinguishes three operations:

1. **Disarm / clear pending input** — preserve `projectionId` and `sequence`; clear only accumulated look deltas or other transient unsent input.
2. **End/reset** — clear `projectionId`, reset sequence to zero, and clear pending input. This is used only when the projection identity is no longer valid on the client.
3. **Projection switch** — when a new exact `projectionId` is observed, reset sequence to zero for that new server-authored session before emitting its first payload.

The implementation may choose precise method names, but these semantics are required.

### Controller behavior

`AstralSeveranceInputController` must not fully reset the sequencer merely because `movementControl()` is absent.

When control is temporarily disarmed for an otherwise still-active projection, the controller must suppress no input and send no MOVE packet, while preserving the sequence state that belongs to that projection.

A full sequencer reset must follow the Astral presentation/session lifecycle, not the transient arm state. Existing client state already distinguishes camera/presentation `desired` identity from `movementControl`, so implementation should reuse that distinction rather than inventing another authority source.

### Projection end and identity switch

When authoritative client state no longer has the old projection presentation (`END`, state clear, disconnect/reset, or replacement with another projection identity), future control for a new projection begins from sequence `1` as a new session.

No old projection's pending look delta may leak into a newly armed projection.

## Data flow after the fix

1. Server sends `BEGIN` for projection P.
2. Client presentation records P; sequence state is either initialized lazily or associated with P.
3. Server may send `MOVE_ARM` for P.
4. Client coalesces movement/look samples and sends monotonically increasing MOVE intents for P.
5. Server may send `MOVE_END` for P without ending P.
6. Client stops redirecting/sending MOVE but retains P's last local sequence and discards transient unsent look input.
7. If server later sends `MOVE_ARM` for the same P, the next emitted MOVE uses the next monotonic sequence.
8. If server sends `END` for P, or a different projection Q replaces P, P's sequence state is discarded. Q starts a fresh sequence domain.

## Failure behavior

- Missing movement arm: no client MOVE gameplay intent is sent.
- Stale/foreign projection identity: existing exact-session state checks continue to fail closed.
- Non-finite input: existing sequencer validation continues to drop it.
- Sequence exhaustion at `Long.MAX_VALUE`: existing fail-closed behavior remains; this design does not introduce wraparound.
- Projection end during pending input: pending input is discarded and cannot be transferred to a future projection.
- Server/client disagreement: server monotonic validation remains the final authority.

## Test design

Use TDD and add a deterministic regression before production changes.

Required regression:

- establish projection P;
- arm P;
- emit one or more payloads through sequence N;
- disarm P without ending the projection;
- re-arm the same P;
- assert the next emitted payload is sequence `N+1`, not `1`.

Required companion coverage:

- transient pending look state is discarded across disarm so stale mouse input is not replayed after re-arm;
- authoritative `END` resets sequence ownership;
- switching from P to Q resets sequencing for Q;
- existing no-arm/no-send and camera-ownership gating behavior remains unchanged;
- existing protocol payload bounds and server stale/replay rejection remain unchanged.

The test-only commit should produce RED evidence against the current reconciled implementation before the minimal fix is added. Final verification requires JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke, and fresh CI on the exact reconciled PR head.

## Integration with PR #247

PR #247 is canonical on the branch ancestry after merge synchronization. Its `ChannelGate` and typed self-target changes are server-side cast admission and target-boundary work; PR #248 remains client control/presentation work.

The sequence-continuity correction must not modify `ArcanaCastEngine`, `ArcanaServices`, `AstralSeveranceCastBinding`, channel duration authority, resource settlement, target encoding, or projection activation semantics.

## Non-goals

This tranche does not:

- enable production MOVE execution;
- bundle or infer `ControlLimits` values;
- emit `MOVE_ARM` from production server code;
- select resource, cooldown, scaling, progression, mastery, or final tuning values;
- add projection interaction, combat, block/container use, remote casting, or world mutation;
- complete Stage 07.07;
- claim real-client/modpack coexistence acceptance under D031.

## Delivery boundary

After implementation, PR #248 may be considered mergeable only after:

- the sequence-continuity regression is GREEN;
- the existing P2 review thread is resolved with code/test evidence;
- the branch is still reconciled with the latest `main`;
- the final diff is reviewed for scope;
- fresh exact-head CI passes all required automated gates.

Stage 07.07 remains partial after this tranche.
