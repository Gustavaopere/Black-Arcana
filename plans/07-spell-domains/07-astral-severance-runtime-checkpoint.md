# 07.07 — Astral Severance runtime checkpoint

## State

`PARTIAL RUNTIME IMPLEMENTATION / SERVER-OWNED PROJECTION LIFECYCLE / NOT END-TO-END`

PR #138 is the implementation vehicle for this checkpoint. Its implementation baseline is `main@2de722272814d2d5664266f5fc8ad05ba25d2940`.

This checkpoint closes one specific Stage 07.07 gap: Astral Severance now has a dedicated bounded server-owned projection/session identity lifecycle. It does **not** complete the spell, promote 07.07, or unlock Stage 08 balance input.

## Implemented boundary

`AstralSeveranceRuntime` owns bounded ephemeral projection state keyed by the physical caster. The runtime provides:

- one active projection per caster;
- a bounded global active-projection ceiling;
- server-generated projection UUID identity;
- exact caster + projection-id matching for explicit return;
- stale, foreign and replayed return handles failing closed;
- duration and range admission constrained by the existing `NoeticSafetyCeilings` hard ceilings;
- identity-collision denial;
- expiry and server-stop cleanup;
- immutable active-projection snapshots that retain the physical caster as the canonical body identity.

The generic observed-entity Noetic route no longer authorizes `ASTRAL_SEVERANCE`. `NoeticObservationPolicy` returns `noetic_astral_requires_projection_lifecycle` before arbitrary target facts can confer identity. Existing observation/snapshot coverage now uses an actual observation kind rather than Astral Severance as a placeholder.

`MinecraftNoeticRuntime` composes the dedicated lifecycle with already-existing Stage 07.07 server lifecycle handling:

- activation requires an already-loaded living `ServerPlayer` physical body and is explicitly documented as callable only after an upstream canonical cast transaction has authorized the spell;
- positive post-mitigation body damage terminates the active projection;
- player dimension change terminates it;
- logout cleanup terminates it;
- final-death settlement terminates it through the existing deferred death cleanup, preserving Soul Anchor/death-prevention authority;
- server stop clears it;
- `activeStateCount()` includes active Astral projections.

No client packet or avatar/entity identity is inferred from this state.

## Authority and non-goals

This checkpoint does **not** add a second casting route. It does not choose or settle resource cost, cooldown, progression, hazard, or channel state. The activation seam is deliberately named `activateAuthorizedAstralProjection(...)` to express that it is downstream runtime activation, not player-facing cast admission.

It also does **not** implement:

- an astral avatar/entity/anchor representation in the world;
- authoritative astral position or movement;
- client-to-server projection movement/look intent;
- a client camera/viewpoint adapter for Astral Severance;
- interaction from the astral position;
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

## TDD evidence

RED:

- head `d8020c853ba49a414c4b8a13fbe2abf1fe005533`;
- Black Arcana CI #2142 / run `34299774715`;
- 572 tests executed with exactly one expected failure: `NoeticAstralSeveranceAdmissionTest.genericObservedEntityAdmissionCannotStandInForAstralProjection()`;
- the failure demonstrated that the pre-existing generic Noetic policy still allowed an arbitrary observed `LivingEntity` to stand in for Astral Severance.

GREEN code checkpoint before this documentation commit:

- head `a642f7988292be7f979f3a00cc058751c95e9173`;
- Black Arcana CI #2152 / run `34300303579`;
- unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke all succeeded;
- main-only artifact publication was correctly skipped on the PR run.

A later documentation or synchronization commit invalidates #2152 as the **final merge-head** CI gate. The exact reconciled PR HEAD must pass again immediately before merge.

## Remaining 07.07 gate

Astral Severance remains **NOT IMPLEMENTED end-to-end** until the reviewed server-owned avatar/viewpoint and movement/control representation exists and the spell is connected to the canonical Stage 02 cast/channel transaction without introducing a parallel authority path.

Separately, `07-familiars-divination-specification-gate.md` remains open for the seven-spell resource/cooldown/scaling/progression/config/provenance and related authority fields. Safety ceilings remain implementation caps rather than Stage 08 balance defaults.

Therefore:

- Stage 07.07 remains `IN PROGRESS`;
- Borrowed Sight real-client acceptance remains deferred under D031;
- no real-client Astral Severance acceptance exists yet;
- Stage 08 must not consume 07.07 as canonical balance input yet.
