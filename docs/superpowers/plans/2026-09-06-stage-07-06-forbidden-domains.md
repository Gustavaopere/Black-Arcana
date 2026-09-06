# Stage 07.06 Forbidden Domains Implementation Plan

**Base:** `main@1391084d187e3c4b2fc96a245f2cc97d27f2879c`

## Frozen architecture

Decision D032 is binding: Forbidden Domains are bounded localized fields/arenas in an already loaded dimension. This stage does not create temporary dimensions, force-load chunks, clone inventories, or introduce a second casting/world-mutation authority. Admission and settlement must reuse Stage 02 casting, Stage 04 loaded-chunk/protection/world-effect boundaries, and Stage 07.04 safe-destination recovery.

The Stage 01 catalog does not establish concrete arsenal/soul/blood domain gameplay semantics. Therefore this implementation provides provider-neutral domain infrastructure and explicit extension seams; unverified effect semantics remain fail-closed instead of being invented.

## Safety ceilings

- radius: hard ceiling 24 blocks;
- duration: hard ceiling 1,200 ticks;
- participants/entities tracked per domain: hard ceiling 64;
- active domains per server: hard ceiling 8;
- one active domain per owner;
- restoration/work budget: hard ceiling 512 recorded positions, with no terrain mutation performed by the base runtime;
- loaded chunks only; unknown/unloaded/protected admission fails closed;
- all exits use a validated safe-return contract; failure keeps the participant in the current valid world position rather than teleporting to an unsafe guess.

## Task 1 — Pure domain contracts and budgets

**Files:**
- Add `src/main/java/dev/gustavopere/blackarcana/content/forbidden/ForbiddenDomainSpec.java`
- Add `src/main/java/dev/gustavopere/blackarcana/content/forbidden/ForbiddenDomainSafetyCeilings.java`
- Add `src/main/java/dev/gustavopere/blackarcana/content/forbidden/ForbiddenDomainAdmission.java`
- Add tests under `src/test/java/dev/gustavopere/blackarcana/content/forbidden/`

TDD: first add tests proving invalid/unbounded radius, duration, entity counts, restoration budgets and dynamic-dimension mode are rejected. Commit RED before implementation. Then implement the minimum immutable spec/admission contract and prove GREEN.

## Task 2 — Bounded server-owned lifecycle

**Files:**
- Add `ForbiddenDomainSession.java`
- Add `ForbiddenDomainRuntime.java`
- Add lifecycle tests.

The runtime owns active sessions by owner UUID, enforces global/owner ceilings, expiry, participant deduplication and exactly-once close. Closing never duplicates/copies inventory or persistent player state. Logout/server-stop cleanup clears ephemeral sessions. Tests cover duplicate start, participant budget, expiry, idempotent close and cleanup.

## Task 3 — Minecraft admission and recovery adapter

**Files:**
- Add `MinecraftForbiddenDomainRuntime.java`
- Reuse `LoadedChunkGuard`, protection/world-effect policy and Stage 07.04 `SafeDestinationPolicy`/settlement primitives.
- Add GameTests where an actual server/world boundary is required.

Admission must prove center and bounded field are in loaded chunks and permitted by canonical world policy/protection. No `getChunk`/ticket path may force load. Return/eviction uses a validated destination; unsafe/unknown recovery fails closed. No arbitrary terrain destruction is introduced.

## Task 4 — Composition-root lifecycle wiring

**Files:**
- Update `BlackArcanaMod.java`
- Extend wiring/lifecycle tests.

Register one server-owned Forbidden Domain runtime. Tick/stop/logout hooks must be explicit and bounded. Add a regression contract proving the runtime is wired and cleared on lifecycle teardown.

## Task 5 — Integrated verification and PR

Run/require the complete repository gate: JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke. Review the exact PR head, resolve review threads, squash merge only from the verified head, then verify the exact `main` SHA and canonical artifact.

## Task 6 — Canonical documentation promotion

Only after runtime merge/main CI is green: update `plans/07-spell-domains/06-forbidden-domains.md`, Stage 07 README and `plans/STATUS.md` with exact evidence. Preserve any real-modpack/manual acceptance as deferred. Merge the documentation PR, verify final main CI/artifact, update the Notion Black Arcana dossier, then stop. Do not start 07.07 automatically.
