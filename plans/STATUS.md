# Black Arcana — Status

Last updated: 2026-09-05

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

Stage 07 Spell Domains is **IN PROGRESS** through fresh latest-`main` domain-scoped promotion. Stage 07.01 Blood & Curses is canonical via PR #45 at merge SHA `0f6d70bf6ccfbb0b8da4700f88aa84ab63f34791`. Stage 07.02 Souls & Death is canonical via PR #47 at merge SHA `998186beed3522a0821a7dbb911f5e31cd6a9e1d`; final PR head `8d3e2ce9fa7c9c760257294ae3d805f55b9a8901` passed workflow `33981212999`, and post-merge workflow `33981437469` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 40 required GameTests, dedicated-server smoke and canonical QA artifact publication. The exact-SHA artifact is `black-arcana-998186beed3522a0821a7dbb911f5e31cd6a9e1d`. 07.02 keeps automatic Malum death-to-spirit harvesting and player-specific Eidolon unlock fail-closed because the verified provider hooks do not expose the required causal/value or caster-identity contracts; no synthetic soul economy or inferred player ownership was introduced. Stage 07.03 Projection & Arsenal is canonical via PR #50 at merge SHA `8631c614e7e319a46ab6b29fe7ab33b3903fc2ef`. Final PR-head workflow `33991180861` (#992) and exact-SHA post-merge workflow `33991393657` (#993) both passed JUnit, diff sanity, NeoForge build, JAR inspection, all 58 required GameTests and dedicated-server smoke; #993 also published canonical QA artifact `black-arcana-8631c614e7e319a46ab6b29fe7ab33b3903fc2ef` (artifact `9976772186`, SHA-256 `81688a5db8ab9e3d1dc37d63ff4153d3d80fe2739941235af0a81c831d59d2bc`). Stage 07.04 Space & Displacement is canonical via PR #52 at merge SHA `a567419f1cccd3a33db95402fcb267c0ad79bc67`; final PR-head workflow `33997420003` passed the complete pre-merge gate and exact-SHA post-merge workflow `33997767668` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 77 required GameTests, dedicated-server smoke and canonical QA artifact publication. The exact-SHA artifact is `black-arcana-a567419f1cccd3a33db95402fcb267c0ad79bc67` (artifact `9978600971`, SHA-256 `c4343f5764d76d6b5310dc446ff1bfbb9359b17ccf74898e615743010259dc1e`). 07.05–07.07 remain pending. Historical stacked PR #22 remains non-canonical/stale reviewed source material and is not merged wholesale. Stage 07.06 Forbidden Domains continues to follow D032: bounded localized in-world fields/arenas are the default; dynamic dimensions require a new explicit architectural decision. Real-modpack/manual host acceptance remains deferred and is not inferred from automated evidence.

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
| 07 Spell Domains | 🟦 IN PROGRESS — 07.01 + 07.02 + 07.03 + 07.04 CANONICAL | 07.04 merged at `a567419f...` with exact-SHA post-merge full CI + 77 GameTests + QA artifact; 07.05–07.07 pending; real-modpack/manual acceptance deferred |
| 08 Progression & Balance | ⬜ WAITING FOR 07 IMPLEMENTATION | implement after 07 becomes canonical |
| 09 Hardening & Release | ⬜ WAITING FOR 08 IMPLEMENTATION | infrastructure first; final campaign remains release-blocking |

## Canonical implementation sequence

The sequence is governed by D031:

`05/05A frozen runtime contracts -> 06 Rituals -> 07 Spell Domains -> 08 Progression & Balance -> 09 Hardening/Release infrastructure -> accumulated final validation`

Missing manual/final evidence blocks validation and release claims, not downstream implementation, when the downstream stage's causal runtime contracts are frozen and applicable automated gates are green.

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 are complete and may change only through explicit follow-up decisions. Stage 05A server/gameplay contracts are frozen for downstream consumers; changing their authority, transaction, hazard, resistance or persistence semantics requires explicit reviewed follow-up work. Stage 06 is canonical as an implemented downstream consumer; any change to its ritual identity, transaction, persistence or provider semantics requires explicit reviewed follow-up work. Stage 07.01 is a canonical Stage 07 subdomain; changes to its Blood Price authority, target-admission rules, damage-provenance/recursion semantics or bounded state contracts require explicit reviewed follow-up work rather than silent drift in later domains. Stage 07.02 is also canonical: changes to Mortal Ledger credit identity, Soul Anchor cap/lockout/persistence/exactly-once death settlement, Spirit Sight privacy/provider bounds, or the documented Malum/Eidolon fail-closed authority boundaries require an explicit reviewed follow-up. Stage 07.03 is canonical: changes to projected-item/profile non-duplication semantics, owner-scoped projection budgets, Oathforged allocation/ledger identity, Echo/Tempering/Arsenal lifecycle authority, Rift projectile cleanup/range accounting, marked-strike admission, or its Stage 04-backed destination safety boundary require an explicit reviewed follow-up rather than silent drift in 07.04+. Stage 07.04 is canonical: changes to its shared safe-destination fail-closed authority, no-force-load boundary, Gate owner/consent/throughput contracts, Recall age/range bounds, Transposition endpoint identity/atomicity/player-safe teleport settlement, Vector Reversal admission/velocity ceilings, or lifecycle cleanup require an explicit reviewed follow-up rather than silent weakening in 07.05+.

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

## Stage 07 implementation and validation state

07.01 Blood & Curses was rebuilt on fresh latest-`main` ancestry in PR #45 using explicit RED→GREEN cycles for Blood Price, Equilibrium Rite, Sanguine Harvest, damage-family classification, Law of Recurrence and Sympathetic Wound. Final branch workflow `33655485829` passed on head `3936f1a8468bf71c470e9108e3b531fda211bfda`. Canonical merge: PR #45 / `0f6d70bf6ccfbb0b8da4700f88aa84ab63f34791`. Post-merge workflow `33655891843` passed the full pipeline with 34 required GameTests, dedicated-server smoke and canonical artifact `black-arcana-0f6d70bf6ccfbb0b8da4700f88aa84ab63f34791`.

07.02 Souls & Death was rebuilt sequentially from the latest canonical `main` in PR #47. The implementation includes bounded Mortal Ledger/Soul Anchor contracts, deterministic death-transaction identity, SavedData persistence, server-authoritative exactly-once death prevention, Spirit Sight privacy/provider contracts and runtime, and a stable-registry Malum Spirit Sight adapter. TDD runs covered ledger, specs, policy/provider/runtime and persistence; Soul Anchor RED workflow `33978656892` failed only because the new runtime was absent, and GREEN workflow `33980621225` passed all 40 GameTests. Final PR head `8d3e2ce9fa7c9c760257294ae3d805f55b9a8901` passed workflow `33981212999`. Canonical merge: PR #47 / `998186beed3522a0821a7dbb911f5e31cd6a9e1d`. Post-merge workflow `33981437469` passed the full pipeline and published `black-arcana-998186beed3522a0821a7dbb911f5e31cd6a9e1d`.

Provider-native safety remains explicit in 07.02. `MinecraftSoulAnchorRuntime.creditDeath(...)` is a seam for validated provider-backed or deliberately configured fallback credit; Black Arcana does not infer Malum spirit yield from generic deaths. Malum 1.8.2 exposes real spirit inventory operations and supported Spirit Sight traces but no verified per-death spirit-yield callback/value used by this stage, so automatic harvesting remains fail-closed. Eidolon: Repraised 0.5.0.2 custom ritual callbacks do not expose caster identity, so the existing anchor-bound attunement is not treated as a player-specific Soul Anchor unlock. Neither boundary is replaced by a generic bonus or synthetic resource.

07.03 Projection & Arsenal was rebuilt sequentially from `main@d1388127435e9da902f4baf4814bd52550265a40` in PR #50. The implementation contains pure projected-weapon/profile registries, owner-scoped projection budgets, bounded Oathforged Ascension allocation/ledger seams, and server-authoritative Echo Armament, Ephemeral Tempering, Spectral Arsenal and Rift Blades runtimes. Projected equipment is represented by ephemeral profiles/handles rather than duplicated persistent items or arbitrary copied NBT. Rift Blades projectile handles are bounded by active count, lifetime and range and release budget on expiry, collision, range termination, owner logout or server stop. Marked-strike damage uses canonical entity-interaction admission; optional gap-close independently revalidates loaded destination, border, collision/headroom, fluids, protection, teleport support and vehicle state without force-loading. The historical dependency on the later 07.04 `SafeDestinationPolicy` was deliberately not imported: equivalent pure destination checks are local to the Rift adapter over Stage 04 primitives so 07.03 remains domain-isolated. RED→GREEN evidence includes Spectral Arsenal RED #974/GREEN workflow `33989714645`, Rift Blades RED workflow `33989972103` and GREEN workflow `33990282195`; integrated runtime registration workflow `33990511277` (#986) passed JUnit, diff sanity, NeoForge build, JAR inspection, all 58 required GameTests and dedicated-server smoke. Final PR head `134ced971549480ed8690233f9986793800d3d37` passed workflow `33991180861` (#992). Canonical merge: PR #50 / `8631c614e7e319a46ab6b29fe7ab33b3903fc2ef`. Exact-SHA post-merge workflow `33991393657` (#993) passed the full pipeline, including all 58 GameTests, dedicated-server smoke and main-only artifact publication. Canonical artifact: `black-arcana-8631c614e7e319a46ab6b29fe7ab33b3903fc2ef`, artifact ID `9976772186`, SHA-256 `81688a5db8ab9e3d1dc37d63ff4153d3d80fe2739941235af0a81c831d59d2bc`.

07.04 Space & Displacement was rebuilt sequentially from `main@f30999b375d42506127eb4c7570f1b8bfd68262c` in PR #52. The implementation contains Threshold Gate, Veilstep Reflex, Anchor Recall, Reciprocal Transposition, Vector Reversal and one shared bounded safe-destination authority. Hard ceilings cap Gate throughput at 32 transfers/s, Recall age at 600 ticks and range at 128 blocks, Transposition at 16 swaps/s, resulting reversal speed at 2.5 blocks/tick and safe-position search at 64 candidates. Runtime state is owner/server scoped and lifecycle cleanup is wired into the live NeoForge game bus. A wiring audit exposed missing composition-root registration for four stateful runtimes and reproduced it with an explicit RED contract before fixing `BlackArcanaMod`. A second RED contract reproduced raw `setPos(...)` settlement in player-capable Gate/Transposition paths before both settlement and rollback were moved to `teleportTo(...)`. Destination admission remains loaded-chunk/no-force-load, live-world-border, collision/headroom, fluid, dimension, protection and vehicle aware. Final PR head `f74bf5b15e3178392a2ea52d3f00969ac6288ea2` passed workflow `33997420003`. Canonical merge: PR #52 / `a567419f1cccd3a33db95402fcb267c0ad79bc67`. Exact-SHA post-merge workflow `33997767668` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 77 required GameTests, dedicated-server smoke and main-only artifact publication. Canonical artifact: `black-arcana-a567419f1cccd3a33db95402fcb267c0ad79bc67`, artifact ID `9978600971`, SHA-256 `c4343f5764d76d6b5310dc446ff1bfbb9359b17ccf74898e615743010259dc1e`. Real-modpack/provider/manual host acceptance remains deferred under D031 and is not inferred as PASS.

07.05 Black Flame through 07.07 Familiars & Divination remain pending and must continue sequentially from the latest canonical `main`. They are not pulled in through stale PR #22 ancestry. Optional provider/host behavior that requires the real modpack remains part of the deferred final validation campaign.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 05A owns forbidden-magic hazard computation; downstream stages consume it rather than implementing parallel backlash systems.
- Deferred validation is recorded, never inferred as PASS.
- Stages 06→09 integrate sequentially through the latest `main`; stale preparatory branches are not merged wholesale.
