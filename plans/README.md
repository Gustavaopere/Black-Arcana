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

## Completion convention

A task starts as `NN-name.md`. Only after all acceptance criteria are verified, tests/CI are green and its implementation branch is merged into `main` may it be renamed to `✅-NN-name.md`. Update `STATUS.md` in the same merge. Planning files are not marked complete merely because they exist.

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

## Branch policy

Planning is canonical on `main`. Implementation branches are created from the latest `main` only when their causal predecessor has merged.

Planned sequence:

1. `round-1-foundation`
2. `feat/01-reference-catalog`
3. `feat/02-arcana-core`
4. `feat/03-integration-layer`
5. `feat/04-world-safety`
6. `feat/05-casting-ux`
7. `feat/06-rituals`
8. `feat/07-spell-domains` (may be split by domain)
9. `feat/08-progression-balance`
10. `feat/09-hardening-release`

Later stages may prepare isolated work in parallel only when the required contracts are already frozen. They must not invent upstream contracts.

## Architecture order

`00-foundation` establishes build, CI, provenance and domain boundaries. `01-reference-catalog` inventories reference mechanics and converts them into original Black Arcana specifications. `02-arcana-core` builds the server-authoritative execution model. `03-integration-layer` freezes adapters for the existing magic/RPG mods. `04-world-safety` provides destruction/rollback/budget controls consumed by all dangerous content. `05-casting-ux` builds direct casting and contextual UI. `06-rituals` implements occult/grand ritual orchestration on top of real integration contracts. `07-spell-domains` delivers the actual magic families. `08-progression-balance` closes progression, mastery and anti-OP tuning. `09-hardening-release` validates compatibility, persistence, performance and release provenance.

## Stages

- [00 — Foundation](00-foundation/README.md)
- [01 — Reference Catalog](01-reference-catalog/README.md)
- [02 — Arcana Core](02-arcana-core/README.md)
- [03 — Integration Layer](03-integration-layer/README.md)
- [04 — World Safety](04-world-safety/README.md)
- [05 — Casting & UX](05-casting-ux/README.md)
- [06 — Rituals](06-rituals/README.md)
- [07 — Spell Domains](07-spell-domains/README.md)
- [08 — Progression & Balance](08-progression-balance/README.md)
- [09 — Hardening & Release](09-hardening-release/README.md)
