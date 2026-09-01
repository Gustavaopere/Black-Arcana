# Black Arcana — Master Plan

This directory is the canonical memory for the project. Every implementation session must read this file, `STATUS.md`, `DECISIONS.md`, then the README and task files of the active stage before changing code.

## Goal

Rebuild selected dark/forbidden-magic concepts as original Black Arcana mechanics, integrated with Iron's Spells 'n Spellbooks, Ars Nouveau, Eidolon: Repraised, Malum and the project's RPG skill-tree ecosystem. The result must be less overpowered, less destructive, visually cleaner and more modular than the reference experience.

## Non-goals

- Do not clone Mahou Tsukai as a whole.
- Do not copy or decompile Mahou Tsukai code, assets, models, sounds or implementation details.
- Do not preserve names strongly tied to Mahou Tsukai or third-party fiction when an original identity can replace them.
- Do not create another permanent mana bar when an existing resource provider can be used.
- Do not require a staff for all casting.
- Do not permit unbounded power growth, permanent mass destruction or infinite resurrection loops by default.

## Completion and validation convention

Implementation progress and final validation are separate facts.

Canonical states for active/downstream stages are:

- `IMPLEMENTATION ACTIVE` — design/code work is still incomplete.
- `IMPLEMENTED / AUTOMATED GATES GREEN` — intended implementation is present and applicable deterministic automated checks pass; this does not imply real-client or real-modpack validation.
- `IMPLEMENTED / FINAL VALIDATION DEFERRED` — no known implementation work remains, but one or more acceptance items require the later real-client, real-modpack, representative-performance, migration-fixture, compatibility or exact-release-head campaign.
- `VALIDATED / COMPLETE` — every stage-local acceptance criterion has direct evidence, applicable CI/tests are green and the implementation is merged to `main`.
- `RELEASE BLOCKED` — Stage 09 implementation/harness work may be ready, but release-blocking validation remains open.

A task starts as `NN-name.md`. Only after all of that task's acceptance criteria are genuinely verified, applicable tests/CI are green and its implementation is merged into `main` may it be renamed to `✅-NN-name.md`. A merged implementation may therefore remain non-✅ while final evidence is deferred. Planning files are not marked complete merely because they exist.

Missing manual/final-validation evidence never becomes inferred PASS. CI, GameTests, screenshots, fixtures, artifact availability and static inspection do not substitute for a real-client or real-modpack acceptance criterion that explicitly requires direct observation.

## Engineering method

- Minecraft 1.21.1, NeoForge, Java 21.
- TDD for deterministic behavior: RED → minimal GREEN → refactor.
- GameTests/integration tests for world, entity, networking and mod-bridge behavior.
- Server-authoritative casting, costs, cooldowns, progression and destructive effects.
- No global per-tick scans over loaded chunks/entities.
- Optional integrations must fail closed/safely when their mod is absent or API contracts change.
- Data-driven definitions where practical; hard-coded behavior only where execution semantics require it.
- Every destructive mechanic must pass through the Black Arcana world-effect policy.
- Every high-power mechanic must have explicit resource, cooldown, progression and safety budgets.
- Deferring the final integrated/manual campaign does not defer deterministic engineering tests required to implement safely.

## Branch and promotion policy

Planning is canonical on `main`. Implementation branches are created sequentially from the latest `main` after their causal predecessor's runtime contracts are canonical. Inserted Stage `05A` intentionally preserves the established Stage 06–09 numbering and branch history.

An unresolved manual/final-validation item blocks validation/release claims, but does not block downstream implementation or merge when all runtime contracts required by that downstream stage are frozen, the downstream change is independently reviewable and its applicable automated gates are green.

The implementation sequence remains:

1. `round-1-foundation`
2. `feat/01-reference-catalog`
3. `feat/02-arcana-core`
4. `feat/03-integration-layer`
5. `feat/04-world-safety`
6. `feat/05-casting-ux`
7. `feat/05a-arcane-danger`
8. `feat/06-rituals`
9. `feat/07-spell-domains` (may be split by domain)
10. `feat/08-progression-balance`
11. `feat/09-hardening-release`
12. accumulated final validation and release closeout

For Stages 06→09, each stage is integrated through the then-current `main`; stale preparatory ancestry is not merged wholesale merely to preserve history. Preserve reviewed behavior and evidence while reconciling shared runtime/persistence files against current canonical contracts.

Later stages may prepare isolated work in parallel only when required contracts are already frozen. They must not invent upstream contracts. Stage 09 may reach `RELEASE BLOCKED` with its infrastructure implemented, but public release completion remains impossible until the accumulated final validation campaign is green on the exact release candidate HEAD.

## Architecture order

`00-foundation` establishes build, CI, provenance and domain boundaries. `01-reference-catalog` inventories reference mechanics and converts them into original Black Arcana specifications. `02-arcana-core` builds the server-authoritative execution model. `03-integration-layer` freezes adapters for the existing magic/RPG mods. `04-world-safety` provides destruction/rollback/budget controls consumed by all dangerous content. `05-casting-ux` builds direct casting and contextual UI. Inserted `05A-arcane-danger` defines backlash, resistance, corruption, strain and hazard snapshots before high-power content is canonicalized. `06-rituals` implements occult/grand ritual orchestration against those frozen hazard contracts. `07-spell-domains` delivers the actual magic families. `08-progression-balance` closes progression, mastery and anti-OP tuning. `09-hardening-release` builds and executes compatibility, persistence, performance and release-provenance closure; execution-dependent rows may remain deferred until the final campaign.

## Stages

- [00 — Foundation](00-foundation/README.md)
- [01 — Reference Catalog](01-reference-catalog/README.md)
- [02 — Arcana Core](02-arcana-core/README.md)
- [03 — Integration Layer](03-integration-layer/README.md)
- [04 — World Safety](04-world-safety/README.md)
- [05 — Casting & UX](05-casting-ux/README.md)
- [05A — Arcane Danger, Resistance, Corruption & Backlash](05a-arcane-danger/README.md)
- [06 — Rituals](06-rituals/README.md)
- [07 — Spell Domains](07-spell-domains/README.md)
- [08 — Progression & Balance](08-progression-balance/README.md)
- [09 — Hardening & Release](09-hardening-release/README.md)
