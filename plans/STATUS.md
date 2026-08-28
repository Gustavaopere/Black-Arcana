# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is **complete, verified and merged into `main`** at `9743064b34cadd26ae767677c773856ebcd3677c`.

Verification evidence:
- branch CI run `33165948006`, job `98831312937`: all steps green;
- post-merge `main` CI run `33166155632`, job `98831943918`: all steps green;
- gates passed: JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is now the canonical active stage. Its previously prepared clean-room catalog is being reapplied onto the verified `main` through `feat/01-reference-catalog`, without importing the stale/divergent Foundation history from `prep/01-reference-catalog`.

Later stages have preparatory implementations but remain non-canonical until their causal predecessors merge in order. Stage 04's integrated preparatory checkpoint additionally achieved a full green verification in run `33166278505`, job `98832347653`; this evidence is retained for later canonicalization but does not bypass Stages 01–03.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | merged at `9743064b...`; branch and post-merge CI fully green |
| 01 Reference Catalog | 🟨 Active | canonical branch `feat/01-reference-catalog`; clean-room catalog awaiting review/CI/merge |
| 02 Arcana Core | 🟦 Preparatory | implementation exists downstream; canonicalization waits for Stage 01 |
| 03 Integration Layer | 🟦 Preparatory | Iron's, Ars, Eidolon, Malum and RPG adapters exist downstream |
| 04 World Safety | 🟦 Preparatory verified | integrated v9 run `33166278505` fully green; canonicalization still waits for Stages 01–03 |
| 05 Casting & UX | ⬜ Not started canonically | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`01-reference-catalog`

## Stage 00 freeze

The Foundation contracts are now frozen unless an explicit follow-up decision is recorded in `DECISIONS.md`.

Frozen baseline includes:
- Minecraft 1.21.1 / NeoForge / Java 21 / ModDevGradle build;
- reproducible Gradle bootstrap with fixed distribution SHA-256;
- CI gates for JUnit, build, artifact inspection, GameTests and dedicated server;
- clean-room provenance rules;
- Black Arcana-owned cast/cost/cooldown/progression/target/world-policy/effect/integration boundaries;
- transactional cost reservation/commit/refund;
- server/common/client configuration authority contract;
- transitive spell-ID migration and explicit removal semantics.

## Immediate next actions

1. Reapply the reviewed Stage 01 catalog onto latest `main` in `feat/01-reference-catalog`.
2. Reconcile all 53 observable reference rows and 32 candidate specifications against the canonical branch.
3. Run the full CI on the canonical Stage 01 branch.
4. If green, merge Stage 01 to `main`, mark its four tasks ✅ and make Stage 02 canonical active.
5. Recut/reapply Stage 02 from the new `main`; do not merge preparatory downstream branches out of order.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation/specification acceptance, tests/CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
