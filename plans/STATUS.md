# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation is implemented on `round-1-foundation` but is **not complete or frozen** because the required NeoForge CI/dedicated-server verification has not executed on a hosted runner. The latest hosted jobs terminate with `runner_id=0`, empty runner name and zero steps. Pure Java 21 contract compilation and local smoke validation pass, but these do not replace NeoForge/GameTest/dedicated-server execution.

Current Foundation branch HEAD: `e843d35789a7a30be16da8348e7daf06f604cdea`. It remains a clean fast-forward candidate over `main` (0 commits behind when last compared).

Stage 01 Reference Catalog is developed only as isolated preparatory work (`prep/01-reference-catalog`). The specification is now preparatory-complete: clean-room inventory, full classification, original identity, candidate contracts, safety ceilings, runtime host baselines and per-candidate host viability/probe requirements are all documented. It is not canonical and receives no ✅ before Foundation lands on `main` and Stage 01 is rebased/reviewed.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | Branch HEAD `e843d35789a7a30be16da8348e7daf06f604cdea`; hosted jobs still receive no runner/steps |
| 01 Reference Catalog | 🟦 Preparatory complete | 53/53 reference items classified; 32 candidates specified; host viability/probe matrix complete; awaiting canonical rebase/review |
| 02 Arcana Core | ⬜ Not started | Server-authoritative execution kernel |
| 03 Integration Layer | ⬜ Not started | Iron's, Ars, Eidolon, Malum, RPG adapters |
| 04 World Safety | ⬜ Not started | Destruction policy, rollback, budgets |
| 05 Casting & UX | ⬜ Not started | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`00-foundation`

## Foundation implemented checkpoint

- NeoForge 1.21.1 / Java 21 / ModDevGradle scaffold.
- Gradle 9.2.1 bootstrap and wrapper metadata pinned to an explicit SHA-256.
- GitHub Actions workflow for unit tests, build, JAR inspection, GameTest server and dedicated-server smoke.
- Clean-room provenance rules and reference ledger.
- Black Arcana-owned cast/cooldown/progression/target/world-policy/effect/integration contracts.
- Transactional cost seam: `check -> reserve -> effect -> commit/refund`, suitable for future composite host costs.
- Server/common/client configuration authority contract, schema v1 validation and transitive/cycle-safe spell ID migrations.
- Dedicated GameTest fixture `foundation_empty`.
- Pure Java 21 compile validation: PASS.
- Transaction/cast/migration smoke validation outside NeoForge: PASS.

## Hosted verification blocker

Repeated Linux and macOS hosted attempts have ended without executing repository commands. The latest observed Linux job reports `runner_id=0`, empty runner metadata and `steps=[]`. This is treated as an external verification blocker, not as a Gradle/NeoForge test failure.

## Stage 01 preparatory checkpoint

- 53 public/observable reference rows reconciled 53/53 into `KEEP / REIMAGINE / MERGE / DROP / DEFER`.
- 32 implementation-facing Black Arcana candidates with behavior, costs, tiers, safety and tests.
- Original naming/domain vocabulary independent from reference names/assets.
- Risk register for PvP, bosses, duplication, immortality loops, privacy, world grief and server load.
- Numeric server safety ceilings/hard runtime guardrails.
- Runtime host baseline: Iron's `3.16.3`, Ars `5.13.0`, Eidolon `0.5.0.2`, Malum `1.8.2` as the installed acceptance targets recorded for Stage 03.
- Per-candidate `CORE / PUBLIC_API / PROBE` matrix with explicit fallback behavior.
- Stage 03 probe queue for exact installed host versions; thematic overlap alone never authorizes private/internal API use.

## Promotion gates

1. Foundation verification must actually execute unit tests, build, JAR inspection, GameTest server and dedicated-server smoke on a real environment.
2. Fix any real Gradle/NeoForge/GameTest failure exposed by that execution.
3. Only after green verification: mark the four Stage 00 task files complete and fast-forward `round-1-foundation` into `main`.
4. Recreate/rebase Stage 01 from the new `main`, carry forward the reviewed specification commits, reconcile 53/53 again and re-check exact host baselines.
5. Only after canonical Stage 01 review/merge may Stage 02 gameplay infrastructure begin from `main`.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation, tests, verification and merge are complete.
- Preparatory branches may reduce future uncertainty but may not silently redefine canonical frozen contracts.