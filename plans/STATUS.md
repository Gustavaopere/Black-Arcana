# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation is implemented on `round-1-foundation` but is **not complete or frozen** because the required NeoForge CI/dedicated-server verification has not yet executed successfully. Pure Java domain contracts compile on Java 21 and their local smoke path passes. A fresh rerun of the hosted workflow was requested on 2026-08-27 and remains the gate for promotion.

Stage 01 Reference Catalog is being developed only as an isolated preparatory branch (`prep/01-reference-catalog`). Its clean-room inventory, host-capability map, classification, original identity, candidate contracts and risk guardrails may advance while Stage 00 is blocked, but Stage 01 is not canonical and cannot be marked complete before Foundation lands on `main` and the catalog is rebased/reviewed against that canonical base.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | Branch HEAD `78210ef35e87e1f4357e03a2543930cd0816a5ca`; waiting for real CI/GameTest/dedicated-server execution |
| 01 Reference Catalog | 🟨 Preparatory | Isolated clean-room specification work; no canonical merge yet |
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
- Pinned Gradle bootstrap with published-checksum verification.
- GitHub Actions workflow for unit tests, build, JAR inspection, GameTest server and dedicated-server smoke.
- Clean-room provenance rules and reference ledger.
- Black Arcana-owned cast/cost/cooldown/progression/target/world-policy/effect/integration contracts.
- Server/common/client configuration authority contract, schema v1 validation and ID migration seam.
- Dedicated GameTest fixture `foundation_empty`.
- Pure Java 21 compile validation: PASS.
- Pure cast pipeline smoke validation: PASS.

## Stage 01 preparatory checkpoint

- Public/observable reference feature inventory without reference implementation code/assets.
- Host-capability map for Iron's Spellbooks, Ars Nouveau, Malum and Eidolon.
- `KEEP / REIMAGINE / MERGE / DROP / DEFER` matrix.
- Original Black Arcana identity/naming vocabulary.
- Candidate implementation contracts with costs, tiers, host intent and acceptance-test obligations.
- Balance/abuse risk register.
- Numeric server safety ceilings and absolute runtime guardrails.

## Promotion gates

1. Foundation CI must actually execute on a hosted runner and pass unit tests, build, JAR inspection, GameTest server and dedicated-server smoke.
2. Fix any real Gradle/NeoForge/GameTest failure exposed by that execution.
3. Only after green CI: mark the four Stage 00 task files complete and merge/fast-forward `round-1-foundation` into `main`.
4. Rebase/recreate the Reference Catalog branch from the new `main`, carry forward only reviewed clean-room specification commits, then perform its canonical review.
5. No Stage 02/07 gameplay implementation begins from the preparatory catalog branch.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation, tests, CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
