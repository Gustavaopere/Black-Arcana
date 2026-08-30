# 07.06 — Forbidden Domains

## Objective
Reimagine reality/domain-style endgame magic as bounded, configurable temporary battle spaces or localized fields.

## Candidate variants
Arsenal, soul and blood-oriented domains only after Stage 01 approves them.

## Architecture decision
Stage 07 uses a **localized in-world rulespace**, not a dynamic temporary dimension or cloned instance.

The approved candidate `black_arcana:inner_dominion` is represented by a bounded server-owned session journal. Opening captures immutable server-derived origin and fallback routes for the selected participants. The implementation deliberately does not create dimensions, force-load chunks, create domain-holder entities, clone player inventory or duplicate player state.

This decision makes restart/recovery safety primary and removes the orphan-dimension/chunk cleanup class of failure by construction.

## Runtime contract

`Inner Dominion` is server-authoritative and bounded by the frozen forbidden-domain safety ceilings:

- radius `<= 32` blocks;
- duration `<= 2400` ticks;
- participants `<= 16`;
- active sessions `<= 4` per server runtime;
- owner must be part of the participant set;
- every participant must be loaded, alive, in the owner's dimension and within the requested radius when the session opens;
- nested-domain participation is denied;
- opening captures a participant-local origin plus a distinct loaded/protected/collision-safe fallback;
- return destinations are revalidated immediately before movement through the shared Stage 04 safe-destination resolver;
- no route validation force-loads a chunk;
- a failed/unavailable return leaves the recovery obligation journaled rather than discarding it.

## Persistence and lifecycle recovery

Recovery obligations are mirrored into `InnerDominionSavedData` after every journal mutation. Rehydration restores bounded non-overlapping sessions, including already-overdue obligations.

Lifecycle settlement is fail-closed:

- normal close returns all currently required loaded participants before removing the session;
- a participant can be settled independently while other obligations remain persisted;
- logout attempts settlement before vanilla removes/saves the `ServerPlayer`;
- login retries any persisted pending obligation;
- respawn retries against the replacement `ServerPlayer`;
- `ServerTickEvent.Post` discovers expired sessions with the non-destructive `due(now)` view and retries only their currently loaded/alive participants;
- offline, dead, blocked or otherwise unsafe participants are not released from the journal merely because the duration elapsed.

## Safety
Hard radius/duration/participant/session budgets; no arbitrary terrain destruction; no dynamic dimensions; no implicit chunk force-loading; robust origin-plus-fallback return path.

The localized runtime does not mutate inventory or clone player state, so duplicated inventory/state is outside the implementation path rather than being cleaned up after an instance transfer.

## Verification

TDD and lifecycle evidence on `feat/stage-07-spell-domains-resync`:

- baseline lifecycle checkpoint `4dc5a78f2ad27e8cdbd8245a01c741d1d6441263`: full CI GREEN in run #671;
- automatic-expiry RED `7657a5f9a74fa7af80de56a398008fcbc87b1bc1`: 85 GameTests ran and exactly `expiredsessionautomaticallyreturnsloadedparticipant` failed because the loaded participant had not been returned automatically;
- automatic-expiry implementation `7f6b320c21cbec58ea4e714a02506dc927f9b4bb`: full CI GREEN in run #673, including 85/85 GameTests and dedicated-server smoke.

Covered behaviors include bounded opening, nested denial, radius denial, normal multi-participant return, alternate fallback when origin becomes invalid, persistence rehydration, partial participant recovery, logout/login/respawn recovery and automatic loaded-participant expiry recovery. Unit coverage additionally verifies that overdue obligations survive expiry discovery and restore until explicitly settled.

## Acceptance

For the localized Stage 07 implementation, the acceptance contract is satisfied at the preparatory branch level:

- loaded participants have validated normal/expiry return paths;
- unavailable obligations remain durable for later lifecycle recovery rather than being dropped;
- no dynamic dimension, forced chunk, domain entity, inventory clone or parallel player-state copy is created;
- return movement remains under the shared Stage 04 displacement/protection/collision policy.

This is a **verified preparatory Stage 07 checkpoint**, not a canonical promotion. PR #22 remains stacked on Stage 06 and cannot merge ahead of the unresolved Stage 05 manual client QA/promotion order.
