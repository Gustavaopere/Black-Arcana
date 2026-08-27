# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation is implemented on `round-1-foundation` but is **not complete or frozen** because the required NeoForge CI/dedicated-server verification has not executed. Pure Java domain contracts compile on Java 21 and their local smoke path passes. GitHub-hosted Actions is currently failing before runner assignment, with zero workflow steps executed.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | Implementation HEAD `c0ed9789648a03aac7e14699f9b526bd07d7b737`; waiting for real CI/GameTest/dedicated-server execution |
| 01 Reference Catalog | ⬜ Not started | Clean-room mechanic inventory/classification |
| 02 Arcana Core | ⬜ Not started | Server-authoritative execution kernel |
| 03 Integration Layer | ⬜ Not started | Iron's, Ars, Eidolon, Malum, RPG adapters |
| 04 World Safety | ⬜ Not started | Destruction policy, rollback, budgets |
| 05 Casting & UX | ⬜ Not started | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Active stage

`00-foundation`

## Implemented checkpoint

- NeoForge 1.21.1 / Java 21 / ModDevGradle scaffold.
- Pinned Gradle bootstrap with published-checksum verification.
- GitHub Actions workflow for unit tests, build, JAR inspection, GameTest server and dedicated-server smoke.
- Clean-room provenance rules and reference ledger.
- Black Arcana-owned cast/cost/cooldown/progression/target/world-policy/effect/integration contracts.
- Server/common/client configuration authority contract, schema v1 validation and ID migration seam.
- Dedicated GameTest fixture `foundation_empty`.
- Pure Java 21 compile validation: PASS.
- Pure cast pipeline smoke validation: PASS.

## External verification blocker

The Actions runs for the Foundation commits have terminated before runner allocation (`runner_id=0`, no steps/logs). Changing from `ubuntu-latest` to explicit `ubuntu-24.04` produced the same provider-side signature. Do not interpret those runs as code/test failures; they executed no repository command. Do not merge or add ✅ until a hosted runner actually executes the workflow successfully.

## Immediate next actions

1. Re-run Foundation CI when GitHub allocates hosted runners normally.
2. Fix any real Gradle/NeoForge/GameTest failure exposed by that run.
3. Only after green CI: rename all Stage 00 task files with ✅, update this status to complete, and merge/fast-forward `round-1-foundation` into `main`.
4. Create `feat/01-reference-catalog` from the resulting latest `main`.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation, tests, CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
