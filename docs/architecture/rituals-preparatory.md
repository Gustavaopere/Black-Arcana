# Stage 06 — Rituals preparatory architecture

Status: preparatory implementation complete; canonical promotion is blocked only by the still-open Stage 05 manual client QA.

Verified source checkpoint: `78bab54207965d906c607322417f92b10f6c86a3`.
Verification branch: `feat/verify-rituals-v8`.
Workflow run: `33189742674`.
Result: full GREEN — JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke all passed.

## Core ritual model

Black Arcana owns ritual identity and lifecycle through bounded server-side contracts:

- `ArcanaRitualId` — canonical ritual identity.
- `RitualActivationId` — unique activation/replay identity.
- `RitualAnchor` — dimension + anchor identity without implicit chunk tickets.
- `RitualContext` — server-owned activation facts.
- `RitualDefinition` / `RitualDefinitionRegistry` — bounded canonical definitions.
- `RitualActivationGuard` — duplicate/concurrent activation protection.
- `RitualSessionRegistry` — bounded active-session state.
- `RitualCompletionLedger` — exactly-once completion/reward accounting.
- `RitualComponentProvider` / `CompositeRitualComponentProvider` — transactional component reservation.
- `RitualRequirementEvaluator` — deterministic pre-consumption validation.
- `RitualOutcomeExecutor` — result boundary after successful transactional validation.
- `RitualEngine` — single activation/interruption/completion pipeline.

The engine validates requirements before consumption where possible, reserves components transactionally, commits only at the defined completion phase and refunds on cancellation/failure according to the session state. Duplicate activation and completion are guarded independently so a replay cannot double-consume or double-reward.

## Persistence and lifecycle

Active ritual sessions are included in `BlackArcanaSavedData` and restored with bounded defensive parsing. Completed ritual outcomes use `RitualCompletionSavedData` / `RitualCompletionLedger` so reward semantics survive reload/restart without replay.

The runtime indexes active ritual sessions rather than scanning the world every tick. Ritual definitions and anchors do not create chunk tickets; unloaded/chunk-lifecycle behavior remains explicit and bounded.

## Eidolon bridge

`EidolonAnchorAttunementRitual` is the production bridge demonstrating supported Eidolon ritual registration. Its recipe is data-driven under `data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json` and uses the public Eidolon 1.21.1 ritual API established in Stage 03.

Eidolon supplies the ritual host/presentation where supported; Black Arcana remains authoritative for its own completion state, progression and downstream world-safety requirements.

## Malum spirit components

`MalumRitualSpiritComponentProvider` binds selected rituals to Malum's typed spirit economy. Spirit requirements are discrete, typed and transactional. Reservations are exact-count, cancellation/refund safe and fail closed when Malum is absent or incompatible.

The Stage 06 v8 checkpoint specifically verifies that the representative grand ritual is actually bound to the Malum component provider rather than merely having an unused adapter available.

## Grand ritual engine

`BlackArcanaGrandRituals` demonstrates the bespoke fallback for mechanics that should not be forced through another mod's ritual API. It composes requirements/components/outcomes on the same bounded `RitualEngine` and remains subject to frozen Stage 04 world-safety contracts for any later world mutation.

No arbitrary global structure scan or permanent chunk loading is introduced.

## Automated evidence

The Stage 06 test suite covers the core transaction/session/completion registries, composite components, persistence round-trips, runtime installation, Malum component behavior and representative grand-ritual binding. `feat/verify-rituals-v8` passed the repository's full CI pipeline.

## Promotion gate

Do not rename Stage 06 task files to `✅-*` and do not merge Stage 06 ahead of Stage 05. The implementation itself is preparatory-complete and fully automated-green; the remaining block is ordering: Stage 05 requires the real-client visual/input matrix before it can be frozen, after which Stage 06 can be canonicalized from this verified checkpoint (or its conflict-resolved descendant) and re-run before merge.
