# Black Arcana — Status

Last updated: 2026-09-01

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge `33171003791` both passed the full pipeline.

Stage 04 World Safety is ✅ complete, verified and merged at `b5a515335544cee5273ff67d033c68bacf98b05a`. Canonical branch run `33171942536` and post-merge main run `33172216821` both passed the full pipeline.

Stage 05 Casting & UX implementation is merged on `main` at `630db8d57a0703a1231075d68353447b8ce37add`. Branch run `33182063857` and post-merge main run `33182458511` both passed the automated pipeline. The stage remains 🟨 active because its required real-client visual/input matrix has not yet been manually executed.

Inserted Stage 05A Arcane Danger is 🟨 active and materially implemented on `main`. The danger model, Arcane/Corruption Resistance, strain/recovery, persistent hazard state and the dedicated Arcane Backlash pipeline are present. Backlash was verified at `583286d1dd28c35da8a64261b6c6eceb22242522` by workflow `33222848359`, including exact zero-resistance 1:1 multi-hit settlement and non-recursive accounting.

Since that checkpoint, Stage 05A has also gained production contracts for equipment-derived hazard resistance and emergency protection, optional Curios equipment/resistance snapshots and bootstrap, authoritative danger-profile runtime, RPG Skill Tree hazard/progression/mastery integration, data-driven equipment set bonuses, causal damage-family attribution, numeric resistance hardening, bounded concurrent/delayed ledger stress coverage and server-authored selected-spell hazard preflight presentation. The preflight now combines the fail-closed Arcane Resistance forecast with a deliberately partial read-only projection of identity/loadout, progression, cooldown and resource-cost gates, and the loadout editor exposes synchronized static hazard metadata as a hover tooltip. Client input never supplies resistance, danger tier, gate state or loadout slot. The 05A.12 automated hardening matrix has explicit coverage for every required row, including terminal Backlash offensive-credit/mastery exclusions.

The read-only gate/runtime/networking path passed the full pipeline on workflow `33422931351` at `44dda0c3586cb17d5461c18ccbb75432d9ac1626`. The HUD gate presentation and loadout tooltip then followed an explicit RED (`33471498889`) and GREEN (`33471722454`) cycle; the GREEN head `7c617983a266e084cacb98682e669cce561e333f` passed unit tests, diff sanity, NeoForge build, JAR inspection, Foundation GameTest server and dedicated-server smoke.

No Corruption/strain client value is added to this 05A.11 closure because the current client networking surface has no bounded synchronized Corruption/strain snapshot contract. A future presentation for those values requires an explicit server-authored sync contract rather than a client-side estimate or an unreviewed new state channel.

Stage 06 Rituals has a current promotion PR (#21) with verified functional work but is intentionally not canonicalized ahead of the unresolved Stage 05 real-client gate. Stage 07 Spell Domains is stacked downstream in PR #22 and remains non-canonical until its dependency chain is cleared.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch + post-merge CI green |
| 04 World Safety | ✅ Complete | merged at `b5a51533...`; branch + post-merge CI green |
| 05 Casting & UX | 🟨 Active / code merged | automated gates green; manual client QA remains in `docs/qa/casting-ux-manual-matrix.md` |
| 05A Arcane Danger | 🟨 Active / automated presentation advanced | 05A.12 automated hardening covered; 05A.11 resistance + predictable gate preflight + loadout tooltip implemented/verified; real-client validation and formal closeout remain |
| 06 Rituals | 🟦 Promotion prepared | PR #21 is downstream of the Stage 05 manual gate |
| 07 Spell Domains | 🟦 Stacked preparatory | PR #22 remains downstream/non-canonical |
| 08 Progression & Balance | 🟦 Preparatory | final quantitative progression/balance closure remains downstream |
| 09 Hardening & Release | ⬜ Not started | final compatibility, migration, provenance and release closure |

## Canonical active stage

`05-casting-ux` remains the formal active stage until its manual client matrix is closed. `05a-arcane-danger` may continue deterministic server-side/automated closure in parallel, but cannot be declared complete ahead of the required Stage 05 presentation gate.

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

## Stage 05 remaining closure work

Execute the real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md`. Do not rename Stage 05 task files to ✅ until applicable rows are actually exercised. Future-only presentation flags may be carried explicitly to Stage 09 only when the corresponding effect is genuinely deferred.

## Stage 05A verified/implemented capabilities

The current codebase contains:

- deterministic danger-profile and root-cast attribution contracts;
- Arcane and Corruption Resistance provider/snapshot semantics;
- persistent strain/corruption/recovery state;
- confirmed-damage/backlash settlement with recursion and offensive-credit exclusions;
- equipment-derived hazard resistance and transactional emergency-protection state/coordinator paths;
- optional Curios snapshot/resistance integration under `integration/curios`, including `CuriosServerIntegrationBootstrap`;
- RPG Skill Tree provider/progression/mastery integration under `integration/rpg`;
- authoritative danger-profile runtime/registry;
- data-driven equipment set bonuses;
- selected-spell Arcane Resistance forecast networking/presentation with a complete-provider read-only mirror, bounded request rate, stale-response rejection and fail-closed diagnostics;
- selected-spell predictable gate projection owned by the canonical `ArcanaCastEngine`, restricted to identity/loadout, progression, cooldown and resource-cost query-only gates;
- server-derived loadout-slot context for gate preview; no client loadout-slot authority;
- bounded gate transport (`CLEAR`, `IDENTITY`, `PROGRESSION`, `COOLDOWN`, `COST`, `UNAVAILABLE`) without arbitrary forecast detail;
- static loadout hover tooltip derived only from synchronized `HazardPreflightPayload` metadata;
- explicit 05A.12 evidence for persistence/death, Stage 04 protection semantics, malformed data/migration, provider snapshots, dedupe/capacity, damage-family attribution, numeric boundaries, concurrent/delayed stress and terminal Backlash exclusions.

The presence of these contracts does not by itself mark their numbered planning files ✅; that rename remains subject to the stage's complete acceptance and documentation closeout rules.

## Stage 05A still open

- real-client validation of the 05A.11 resistance/gate forecast, loadout tooltip and stale/reconnect/accessibility behavior in `docs/qa/casting-ux-manual-matrix.md`;
- reconciliation of numbered Stage 05A task status/closeout after the remaining presentation gate is proven;
- Stage 05 manual client gate, which still blocks declaring Stage 05A complete or downstream stages canonical.

05A.11's deterministic automated presentation scope is implemented, but its manual acceptance remains open. Corruption/strain client values are intentionally not retained without a separate bounded synchronization contract. 05A.12's automated acceptance matrix is covered, but neither fact overrides the stage-level exit rule or substitutes for real-client presentation evidence.

## Stage 06 / 07 preservation rule

Do not discard the verified Stage 06/07 work, but do not bypass the causal gate. Stage 06 PR #21 and stacked Stage 07 PR #22 remain downstream until Stage 05 manual closure and any required Stage 05A freeze/acceptance gates are complete.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 05A owns forbidden-magic hazard computation; downstream stages consume it rather than implementing parallel backlash systems.
- Stage 06/07 content is not canonicalized ahead of unresolved Stage 05 closure and required Stage 05A freeze/acceptance gates.
