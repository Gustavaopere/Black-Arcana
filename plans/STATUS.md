# Black Arcana — Status

Last updated: 2026-09-01

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge `33171003791` both passed the full pipeline.

Stage 04 World Safety is ✅ complete, verified and merged at `b5a515335544cee5273ff67d033c68bacf98b05a`. Canonical branch run `33171942536` and post-merge main run `33172216821` both passed the full pipeline.

Stage 05 Casting & UX is `IMPLEMENTED / FINAL VALIDATION DEFERRED`. Its implementation is merged and its deterministic automated gates are green, but the required real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md` remains genuinely unexecuted. Every applicable manual row remains `PENDING` until directly observed.

Stage 05A Arcane Danger is `IMPLEMENTED / FINAL VALIDATION DEFERRED`. Its server/gameplay contracts are frozen and materially implemented: danger profiles, Arcane/Corruption Resistance, corruption/strain persistence and recovery, causal confirmed-damage/backlash settlement, equipment/Curios/RPG providers, emergency protection, read-only server-authored resistance/gate forecast, loadout tooltip and the 05A.12 automated hardening matrix are present. Remaining presentation acceptance is part of the same deferred real-client campaign; no manual acceptance is inferred from automated evidence.

The deterministic Stage 05/05A fixture is merged at `06f0a9a495b6fe6576da75f673800a94af14dab0`, with post-merge workflow `33501635945` green. It supplies reproducible hazard/resistance/gate/reload states without production debug hooks or client authority, but fixture availability is not PASS evidence.

Stage 06 Rituals is canonical on `main` as `IMPLEMENTED / FINAL VALIDATION DEFERRED` via PR #43 at merge SHA `4a79d440a4bba3920002eb8fc49a520e15744c48`. Historical PR #21 was used only as reviewed source material and was closed unmerged as superseded. The replacement implementation was rebuilt from baseline `d8fb667cc5954d5811dacbbef4da1053fa296581`, preserved current Stage 05A runtime/persistence contracts, and followed an explicit TDD RED→GREEN sequence: workflow `33555023989` on test-only `63fc59a1...` failed because production Rituals contracts were absent; core workflow `33556263487` on `0f8e6bd9...` passed the complete pipeline; integrated workflow `33556878810` on `90c3a4b4...` passed after runtime-manager, Malum and Eidolon wiring; final branch workflow `33560762231` and PR workflow `33561144294` were green on final head `f5c2249...`; post-merge workflow `33561613644` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 21 required GameTests, dedicated-server smoke and canonical artifact publication on exact `main` SHA `4a79d440...`.

The current canonical QA artifact for that Stage 06 merge is `black-arcana-4a79d440a4bba3920002eb8fc49a520e15744c48`, produced by workflow `33561613644`. Its publication confirms the automated mainline delivery gate only; real-modpack/manual host acceptance remains deferred under D031 and is not inferred as PASS.

Stage 07 Spell Domains is now eligible for a fresh latest-`main` resynchronization because Stage 06 is canonical. Historical stacked PR #22 preserves substantial reviewed work but is still non-canonical/stale relative to the new `main` and must be resynchronized before any promotion. Stage 07.06 Forbidden Domains follows D032: bounded localized in-world fields/arenas are the default; dynamic dimensions require a new explicit architectural decision. No Stage 07 implementation is started by this Stage 06 closeout.

Stage 08 Progression & Balance starts only after Stage 07 implementation is canonical. Stage 09 Hardening & Release infrastructure starts only after Stage 08 implementation is canonical. Stage 09 cannot leave `RELEASE BLOCKED` until the accumulated final validation campaign is executed on the exact release candidate.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch + post-merge CI green |
| 04 World Safety | ✅ Complete | merged at `b5a51533...`; branch + post-merge CI green |
| 05 Casting & UX | 🟨 IMPLEMENTED / FINAL VALIDATION DEFERRED | automated gates green; exact-SHA QA artifact + fixture available; real-client matrix remains PENDING |
| 05A Arcane Danger | 🟨 IMPLEMENTED / FINAL VALIDATION DEFERRED | server contracts frozen; automated presentation/hardening advanced; real-client presentation acceptance remains |
| 06 Rituals | 🟨 IMPLEMENTED / FINAL VALIDATION DEFERRED | canonical on `main` at `4a79d440...`; post-merge full CI green; real-modpack/manual host acceptance deferred |
| 07 Spell Domains | 🟦 READY FOR LATEST-MAIN RESYNC / NOT STARTED | historical #22 is non-canonical; resync only on explicit continuation |
| 08 Progression & Balance | ⬜ WAITING FOR 07 IMPLEMENTATION | implement after 07 becomes canonical |
| 09 Hardening & Release | ⬜ WAITING FOR 08 IMPLEMENTATION | infrastructure first; final campaign remains release-blocking |

## Canonical implementation sequence

The sequence is governed by D031:

`05/05A frozen runtime contracts -> 06 Rituals -> 07 Spell Domains -> 08 Progression & Balance -> 09 Hardening/Release infrastructure -> accumulated final validation`

Missing manual/final evidence blocks validation and release claims, not downstream implementation, when the downstream stage's causal runtime contracts are frozen and applicable automated gates are green.

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 are complete and may change only through explicit follow-up decisions. Stage 05A server/gameplay contracts are frozen for downstream consumers; changing their authority, transaction, hazard, resistance or persistence semantics requires explicit reviewed follow-up work. Stage 06 is now canonical as an implemented downstream consumer; any change to its ritual identity, transaction, persistence or provider semantics requires explicit reviewed follow-up work.

## Stage 05 / 05A deferred validation ledger

The real-client visual/input matrix remains in `docs/qa/casting-ux-manual-matrix.md`. Execute it later using `docs/qa/casting-ux-real-client-runbook.md`, an exact-SHA `main` CI artifact and the removable fixture under `docs/qa/fixtures/stage05-real-client/` where applicable.

Do not rename Stage 05/05A task files to ✅ merely because downstream implementation advances. Direct client evidence is still required for rows that explicitly require it. Corruption/strain client values remain intentionally absent until a bounded server-authored synchronization contract is separately approved.

## Stage 05A verified/implemented capabilities

The current codebase contains:

- deterministic danger-profile and root-cast attribution contracts;
- Arcane and Corruption Resistance provider/snapshot semantics;
- persistent strain/corruption/recovery state;
- confirmed-damage/backlash settlement with recursion and offensive-credit exclusions;
- equipment-derived hazard resistance and transactional emergency-protection paths;
- optional Curios snapshot/resistance integration;
- RPG Skill Tree provider/progression/mastery integration;
- authoritative danger-profile runtime/registry;
- data-driven equipment set bonuses;
- selected-spell Arcane Resistance forecast with bounded request rate, stale-response rejection and fail-closed diagnostics;
- predictable gate projection owned by the canonical `ArcanaCastEngine`, restricted to identity/loadout, progression, cooldown and resource-cost query-only gates;
- server-derived loadout-slot context; no client loadout-slot authority;
- bounded gate transport (`CLEAR`, `IDENTITY`, `PROGRESSION`, `COOLDOWN`, `COST`, `UNAVAILABLE`);
- static loadout hazard tooltip from synchronized metadata;
- 05A.12 automated persistence/death/protection/malformed-data/provider/dedupe/numeric/stress/backlash exclusion coverage;
- removable real-client datapack fixture validated by strict loaders;
- main-only exact-SHA QA JAR publication after the complete automated CI gate.

These contracts do not convert deferred real-client acceptance to PASS.

## Stage 06 implementation and validation state

The canonical Stage 06 implementation provides the bounded ritual core, session persistence, exactly-once completion ledger, server lifecycle wiring, Eidolon anchor-attunement bridge and Malum typed-spirit grand-ritual path while retaining current 05A state.

Canonical merge: PR #43 / `4a79d440a4bba3920002eb8fc49a520e15744c48`.
Post-merge automated evidence: workflow `33561613644` full GREEN with canonical artifact `black-arcana-4a79d440a4bba3920002eb8fc49a520e15744c48`.
Optional host/runtime evidence that requires the real modpack remains `FINAL VALIDATION DEFERRED`; no manual PASS is claimed. Historical PR #21 is closed unmerged and superseded as an integration vehicle.

Stage 07 is eligible for a new latest-main resynchronization, but it is not started automatically by this closeout.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 05A owns forbidden-magic hazard computation; downstream stages consume it rather than implementing parallel backlash systems.
- Deferred validation is recorded, never inferred as PASS.
- Stages 06→09 integrate sequentially through the latest `main`; stale preparatory branches are not merged wholesale.
