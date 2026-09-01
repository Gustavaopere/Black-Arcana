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

The canonical CI delivery path is merged through PR #41. Current `main` is `e573a0edfcb69d09e423b60ad75ab71b9d8e70c5`; post-merge workflow `33532564420` passed the full automated gate and published `black-arcana-e573a0edfcb69d09e423b60ad75ab71b9d8e70c5` only after those gates. Artifact publication is support infrastructure for later real-client execution, not manual acceptance.

Stage 06 Rituals is authorized for latest-`main` resynchronization and promotion under D031. Historical PR #21 remains useful reviewed source material, but its stale ancestry is not merged wholesale. Shared runtime/persistence must be reconciled against current Stage 05A contracts, the full automated gate rerun, and any host/client-only evidence that CI cannot provide must be recorded as `FINAL VALIDATION DEFERRED` rather than blocking implementation merge.

Stage 07 Spell Domains remains downstream/non-canonical until Stage 06 implementation is canonical on `main`. Historical stacked PR #22 preserves substantial reviewed work but must be resynchronized to the resulting latest `main`. Stage 07.06 Forbidden Domains follows D032: bounded localized in-world fields/arenas are the default; dynamic dimensions require a new explicit architectural decision.

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
| 06 Rituals | 🟦 IMPLEMENTATION AUTHORIZED | resynchronize reviewed #21 behavior onto latest main; automated gates required before merge |
| 07 Spell Domains | 🟦 DOWNSTREAM / NON-CANONICAL | resynchronize after Stage 06 merge; finish 07.04–07.07 |
| 08 Progression & Balance | ⬜ WAITING FOR 07 IMPLEMENTATION | implement after 07 becomes canonical |
| 09 Hardening & Release | ⬜ WAITING FOR 08 IMPLEMENTATION | infrastructure first; final campaign remains release-blocking |

## Canonical implementation sequence

The sequence is now governed by D031:

`05/05A frozen runtime contracts -> 06 Rituals -> 07 Spell Domains -> 08 Progression & Balance -> 09 Hardening/Release infrastructure -> accumulated final validation`

Missing manual/final evidence blocks validation and release claims, not downstream implementation, when the downstream stage's causal runtime contracts are frozen and applicable automated gates are green.

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 are complete and may change only through explicit follow-up decisions. Stage 05A server/gameplay contracts are frozen for downstream consumers; changing their authority, transaction, hazard, resistance or persistence semantics requires explicit reviewed follow-up work.

## Stage 05 / 05A deferred validation ledger

The real-client visual/input matrix remains in `docs/qa/casting-ux-manual-matrix.md`. Execute it later using `docs/qa/casting-ux-real-client-runbook.md`, the exact-SHA `main` CI artifact and the removable fixture under `docs/qa/fixtures/stage05-real-client/` where applicable.

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

## Stage 06 promotion rule

Use historical PR #21 only as reviewed Stage 06 source/evidence. Create a fresh Stage 06 branch from the latest canonical `main`, restore the ritual core and tests, manually reconcile shared runtime/persistence/provider bootstrap files, rerun the complete automated pipeline and open a replacement PR. Close #21 as superseded rather than merging stale ancestry.

Stage 06 may merge as `IMPLEMENTED / FINAL VALIDATION DEFERRED` if optional host/runtime client evidence is unavailable. It may only become `VALIDATED / COMPLETE` when its own documented acceptance criteria are directly evidenced. Stage 05's separate manual presentation debt no longer blocks Stage 06 implementation canonicalization.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 05A owns forbidden-magic hazard computation; downstream stages consume it rather than implementing parallel backlash systems.
- Deferred validation is recorded, never inferred as PASS.
- Stages 06→09 integrate sequentially through the latest `main`; stale preparatory branches are not merged wholesale.
