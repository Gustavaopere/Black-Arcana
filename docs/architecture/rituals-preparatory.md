# Stage 06 — Rituals architecture

Status: implementation promoted on the current-main line; applicable automated validation is green. Final real-modpack/manual acceptance remains deferred under D031 and must not be inferred as PASS.

Current-main promotion baseline: `d8fb667cc5954d5811dacbbef4da1053fa296581`.
Historical reviewed source: PR #21 / `9b2fd70a60a487ffe17eb90cbc870e24af7e2a80`.
TDD RED: workflow `33555023989` on test-only commit `63fc59a1ddee145c5d3a14de9897b997ab52c4d2` failed at test compilation because the Stage 06 production contracts were deliberately absent.
Core GREEN: workflow `33556263487` on `0f8e6bd90837d182f3add9ad047303115d7145f0` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.
Integrated GREEN: workflow `33556878810` on `90c3a4b4f4be4570b4e45e51edcec90df47a4377` passed the same full pipeline after server lifecycle persistence, Malum grand-ritual wiring and Eidolon anchor-attunement registration were restored against the current-main contracts. The run executed Java 21 / NeoForge 21.1.248 and all 21 required GameTests passed.

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

The current-main transplant preserves the newer Stage 05A persistence for corruption, strain, emergency protection and contextual pending backlash. Ritual session persistence is additive to those contracts.

The runtime indexes active ritual sessions rather than scanning the world every tick. Ritual definitions and anchors do not create chunk tickets; unloaded/chunk-lifecycle behavior remains explicit and bounded.

## Eidolon bridge

`EidolonAnchorAttunementRitual` extends the existing public-API-only Eidolon integration. Its recipe is data-driven under `data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json` and is guarded by the `eidolon_repraised` mod-loaded condition.

Registration retains the existing Black Arcana probe ritual and adds the anchor-attunement ritual with ownership checks so an unexpected third-party collision fails instead of silently replacing a ritual.

Eidolon supplies the ritual host/presentation where supported; Black Arcana remains authoritative for its own completion state, progression and downstream world-safety requirements.

## Malum spirit components

`MalumRitualSpiritComponentProvider` binds selected rituals to Malum's typed spirit economy. Spirit requirements are discrete, typed and transactional. Reservations are exact-count, cancellation/refund safe and fail closed when Malum is absent or incompatible.

The representative `veil_anchor_consecration` grand ritual requires four `arcane` and two `wicked` spirits. Server-side admission additionally requires the caster to remain online, the anchor dimension and chunk to already be loaded, and the caster-scoped completion ledger to be clear. Completion is recorded exactly once through `RitualCompletionSavedData`.

## Grand ritual engine

`BlackArcanaGrandRituals` provides the bespoke path for mechanics that should not be forced through another mod's ritual API. It composes requirements, components and outcomes on the same bounded `RitualEngine` and remains subject to frozen Stage 04 world-safety contracts for later world mutation.

No arbitrary global structure scan or permanent chunk loading is introduced.

## Automated evidence

The Stage 06 test suite covers core transaction/session/completion registries, composite components, persistence round-trips, runtime ownership/ticking, Malum component behavior and representative grand-ritual binding. The current-main promotion also runs the repository-wide JUnit, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke gates.

The integrated current-main candidate is automated-green at `90c3a4b4f4be4570b4e45e51edcec90df47a4377` / workflow `33556878810`. No real-modpack/manual host acceptance is claimed from that run.

## Final validation status

Stage 06 is eligible to be canonicalized as `IMPLEMENTED / FINAL VALIDATION DEFERRED` under D031 because its current-main implementation and applicable automated gates are green. This does not convert any Stage 05/05A real-client row to PASS and does not claim representative real-modpack/manual validation that has not been executed.

Do not rename Stage 06 task files to `✅-*` solely from automated evidence. Stage 07 may begin only after Stage 06 is canonical on the latest `main`, and Stage 09 remains release-blocked until the accumulated deferred validation campaign is closed.
