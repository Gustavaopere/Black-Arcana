# Stage 05 — Casting Runtime & Client Contracts — Execution Status

## Current state

`ACTIVE / IMPLEMENTATION PRESENT / REQUIRED PHYSICAL VALIDATION PENDING`

Stage 05 is the current blocking numbered stage under D034. Deterministic runtime/client-contract implementation is substantially present, but required physical/runtime-input acceptance remains incomplete. Until every applicable Stage 05 plan requirement is proven, Stage 05A and all later numbered stages are blocked from active implementation/audit promotion.

Presentation work that is purely visual remains tracked in `plans/visual-production/05-casting-ux/`. However, any real-client/input/coexistence observation explicitly required by a numbered Stage 05 plan remains part of that plan's completion gate and cannot be moved out of the stage merely because related visual production exists.

## Engineering ledger

| Item | State | Runtime truth | Remaining engineering gate |
|---|---|---|---|
| 05.01 Input & Loadouts | 🟡 | bounded server-owned loadout, persistence, rebindable intent and canonical cast convergence implemented; PR #271 closes immediate-cast forged-slot bypass on `main@1d0e221440506005fd4cd16220436f3573c0adec` | physical input/loadout/session rows, 16-slot reachability, provider/controller coexistence |
| 05.02 Radial Selection | 🟡 | bounded paging/selection semantics implemented; selection is not casting | physical toggle/hold/input-lock authority rows |
| 05.03 Contextual Feedback Data | 🟡 | server-authored result/hazard/gate data and stale-state rules implemented | physical stale/correlation/state-authority rows |
| 05.04 Client Config Authority | 🟡 | client-only config/persistence/input semantics implemented | required real-client proof that client settings cannot affect gameplay authority |
| 05.05 Physical Validation | 🟡 | runtime/input/provider client handoff retained | execute and record all applicable authority/input/integration rows in the real-client matrix |
| 05.06 Modpack Coexistence | 🟡 | Iron's-hosted BA path hard-disables provider mana/cooldown settlement, retains one-root convergence and optional-provider isolation with regression coverage | observe required runtime/provider coexistence in the real modpack/client environment |
| 05.07 Presentation Data Contracts | ✅ | data-authority audit/gates complete | none inside this plan; new fields remain evidence-gated |

## Latest canonical 05.01 authority hardening

PR #271 (`fix(stage05-01): enforce server-owned loadout on immediate casts`) closed a deterministic authority gap where an immediate cast could submit a registered/executable spell for a slot whose server-owned loadout contained another spell.

Canonical evidence:

- RED workflow `35034535110` reproduced the bypass;
- final branch workflow `35035822174` GREEN;
- PR-head workflow `35036140396` GREEN;
- merge SHA `1d0e221440506005fd4cd16220436f3573c0adec`;
- post-merge workflow `35036436151` GREEN for unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke and canonical QA artifact publication;
- artifact `black-arcana-1d0e221440506005fd4cd16220436f3573c0adec`, ID `10423705741`, SHA-256 `f61d7f3f533e220e1f81e72ee75e98dacd7358367e5def88ce6a6df173a73629`.

This evidence closes that deterministic implementation gap only. It does not convert any manual matrix row to PASS and does not complete 05.01.

## Extracted presentation work

05.01–05.06 presentation halves and the former 05.08–05.16 presentation plans are tracked under `plans/visual-production/05-casting-ux/`. Historical checkpoints/evidence retain their factual meaning.

See `plans/visual-production/MIGRATION-MAP.md` for the exact move/split ledger.

## Completion rule

Stage 05 completion requires every numbered Stage 05 plan to satisfy its own implementation, integration, automated test and required physical/manual acceptance criteria. Automated evidence cannot substitute for direct client observation where the plan requires it. Only fully proven files receive `✅-`.

No promotion to Stage 05A is allowed while any Stage 05 file remains pending, deferred, partially validated or otherwise unproven.
