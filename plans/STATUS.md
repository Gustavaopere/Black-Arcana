# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation is implemented on `round-1-foundation` but is **not complete or frozen** because the required NeoForge CI/dedicated-server verification has still not executed. Pure Java 21 validation passes for the domain/config contracts, including transactional cost reservation/refund and transitive ID migration. GitHub-hosted Actions continues to terminate before runner assignment with zero repository steps executed.

Stage 01 Reference Catalog has advanced only in the isolated `prep/01-reference-catalog` branch. Its preparatory completeness audit reconciles all 53 observable reference rows and its safety/risk contracts are ready for canonical rebase/review after Foundation lands. It is not canonical or frozen.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | Transactional implementation checkpoint `a81ff8049ff1bbe175d457dc1e04894a0beb09bf`; waiting for real CI/GameTest/dedicated-server execution |
| 01 Reference Catalog | 🟨 Preparatory | Prep HEAD `60fa4e4a936d59fbdb0bfa198c47868a4e2241ca`; 53/53 inventory rows classified, awaiting canonical rebase/review |
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

The latest workflow for implementation checkpoint `a81ff8049ff1bbe175d457dc1e04894a0beb09bf` (run `33122757379`) again terminated before a hosted runner executed any step. Earlier retries showed the same signature. Do not interpret these as Gradle/Java/GameTest failures: no checkout or repository command ran. Do not merge or add ✅ until a runner actually executes the required workflow successfully, or an explicitly approved equivalent verification environment proves the same acceptance gates.

## Immediate next actions

1. Re-run/check Foundation CI when GitHub allocates hosted runners normally.
2. Fix any real Gradle/NeoForge/GameTest failure exposed by an actual execution.
3. After green verification: mark the four Stage 00 task files complete and merge/fast-forward `round-1-foundation` into `main`.
4. Recreate/rebase Stage 01 from that latest `main`, carry forward the reviewed preparatory catalog, run the canonical completeness/host-version review, then merge Stage 01.
5. Do not begin Stage 02/07 gameplay implementation from the preparatory catalog branch.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation, tests, CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
