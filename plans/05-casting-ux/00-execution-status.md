# Stage 05 — Casting Runtime & Client Contracts — Execution Status

## Current state

`COMPLETE / ENGINEERING CLOSED / REAL-CLIENT RELEASE VALIDATION CARRIED TO STAGE 09`

Under D035, Stage 05 engineering is closed: its runtime/client contracts, integrations and deterministic gates are complete. Required physical/runtime-input/provider observations remain unresolved evidence, but they are explicitly transferred to the Stage 09 exact-release-candidate campaign and no longer block 05A implementation progression.

Presentation work that is purely visual remains tracked in `plans/visual-production/05-casting-ux/`. Physical/runtime/input/provider observations stay traceable to their originating Stage 05 contracts but execute as Stage 09 release validation under D035.

## Engineering ledger

| Item | State | Runtime truth | Remaining engineering gate |
|---|---|---|---|
| 05.01 Input & Loadouts | ✅ | bounded server-owned loadout, persistence, rebindable intent and canonical cast convergence implemented; PR #271 closes immediate-cast forged-slot bypass on `main@1d0e221440506005fd4cd16220436f3573c0adec` | Stage 09 physical campaign: input/loadout/session, 16-slot reachability, provider/controller coexistence |
| 05.02 Radial Selection | ✅ | bounded paging/selection semantics implemented; selection is not casting | Stage 09 physical toggle/hold/input-lock rows |
| 05.03 Contextual Feedback Data | ✅ | server-authored result/hazard/gate data and stale-state rules implemented | Stage 09 physical stale/correlation/state-authority rows |
| 05.04 Client Config Authority | ✅ | client-only config/persistence/input semantics implemented | Stage 09 real-client authority-isolation proof |
| 05.05 Final Validation Handoff | ✅ | runtime/input/provider client handoff retained | handoff complete; execute rows in Stage 09 exact-release-candidate campaign |
| 05.06 Modpack Coexistence | ✅ | Iron's-hosted BA path hard-disables provider mana/cooldown settlement, retains one-root convergence and optional-provider isolation with regression coverage | Stage 09 provider-real coexistence observation |
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

This evidence closes that deterministic implementation gap. No manual matrix row is converted to PASS; those rows remain PENDING in the Stage 09 campaign.

## Extracted presentation work

05.01–05.06 presentation halves and the former 05.08–05.16 presentation plans are tracked under `plans/visual-production/05-casting-ux/`. Historical checkpoints/evidence retain their factual meaning.

See `plans/visual-production/MIGRATION-MAP.md` for the exact move/split ledger.

## Completion rule

Under D035, Stage 05 completion requires implementation, integration and deterministic acceptance for each numbered engineering plan plus explicit transfer of unresolved manual/physical rows to Stage 09. Automation still cannot substitute for direct client observation, so transferred rows remain PENDING rather than PASS.

All Stage 05 engineering files now satisfy that amended completion contract and receive `✅-`. Stage 05A may proceed. Stage 09 remains release-blocked until the transferred campaign is directly evidenced.
