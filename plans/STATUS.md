# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation is implemented on `round-1-foundation` but is **not complete or frozen** because the required NeoForge CI/dedicated-server verification has still not executed. Pure Java 21 validation passes for the domain/config contracts, including transactional cost reservation/refund and transitive ID migration. Earlier GitHub-hosted Actions attempts terminated before runner assignment with zero repository steps executed.

Stage 01 Reference Catalog has advanced only in the isolated `prep/01-reference-catalog` branch. Its preparatory completeness audit reconciles all 53 observable reference rows and its safety/risk contracts are ready for canonical rebase/review after Foundation lands. It is not canonical or frozen.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | Implementation HEAD includes transactional contracts and pinned build bootstrap; waiting for real CI/GameTest/dedicated-server execution |
| 01 Reference Catalog | 🟨 Preparatory | Isolated clean-room catalog ready for canonical rebase/review |
| 02 Arcana Core | ⬜ Not started canonically | Preparatory implementation exists outside `main` |
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
- Gradle 9.2.1 bootstrap with a fixed distribution SHA-256 in Unix, Windows and wrapper metadata.
- GitHub Actions workflow for unit tests, build, JAR inspection, GameTest server and dedicated-server smoke.
- Clean-room provenance rules and reference ledger.
- Black Arcana-owned cast/cooldown/progression/target/world-policy/effect/integration contracts.
- Transactional cost contract: affordability check → atomic reservation → effect → commit, with refund on failed/exceptional effect execution.
- Server/common/client configuration authority contract and schema v1 validation.
- Transitive spell-ID migration with explicit removal, cycle/conflict rejection and deterministic diagnostics.
- Dedicated GameTest fixture `foundation_empty`.
- Pure Java 21 compile validation: PASS.
- Pure transactional cast/migration smoke validation: PASS.

## External verification blocker

Earlier workflow attempts terminated before a hosted runner executed any step (`runner_id=0`, empty step list). GitHub's public status page now reports Actions operational after the Aug 26–27 incidents, so this commit intentionally triggers a completely fresh workflow run rather than reusing a failed run attempt. Do not interpret a runnerless failure as a Gradle/Java/GameTest failure. Do not merge or add ✅ until a runner actually executes the required workflow successfully, or an explicitly approved equivalent verification environment proves the same acceptance gates.

## Immediate next actions

1. Inspect the fresh post-incident Foundation workflow triggered by this commit.
2. Fix any real Gradle/NeoForge/GameTest failure exposed by an actual execution.
3. After green verification: mark the four Stage 00 task files complete and merge/fast-forward `round-1-foundation` into `main`.
4. Recreate/rebase the Reference Catalog from latest `main`, carry forward only reviewed clean-room specification commits, run canonical completeness/host-version review, then merge Stage 01.
5. Keep Stage 02 work preparatory until the canonical dependency chain is restored.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation, tests, CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
