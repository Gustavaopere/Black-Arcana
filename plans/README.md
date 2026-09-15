# Black Arcana — Master Plan

This directory is the canonical planning memory for Black Arcana. Implementation sessions read this file, `STATUS.md`, `DECISIONS.md`, then the README/task files for the active numbered engineering stage.

## Goal

Build an original, server-authoritative forbidden-magic system for Minecraft 1.21.1 / NeoForge / Java 21, integrating safely with the modpack's existing magic/RPG providers without cloning Mahou Tsukai code/assets/presentation.

## Engineering method

- TDD for deterministic behavior: RED -> minimal GREEN -> refactor.
- GameTests/integration tests for world, entity, network and provider bridges.
- Server-authoritative casting, costs, cooldowns, progression, Arcane Danger and destructive effects.
- No unbounded scans or chunk forcing.
- Optional integrations are isolated and fail closed/safely.
- Data-driven definitions are declarative and bounded.
- Destructive mechanics pass through canonical world-effect policy.
- High-power mechanics have explicit caps/budgets.

## Completion/validation rule

Implementation evidence and direct physical validation are separate facts. CI/GameTests never fabricate a real-client, real-modpack, provider-native or manual PASS.

For numbered-stage progression, D034 is authoritative and supersedes D031. The active stage is the earliest incomplete stage. A stage may advance only after every requirement defined by its plans is complete, including required implementation, integration, automated tests, manual/physical validation, real-client or real-modpack observation, provider-native acceptance, persistence/lifecycle/multiplayer/world-safety checks and acceptance criteria where applicable.

Statuses such as `IMPLEMENTED`, `FINAL VALIDATION DEFERRED`, `PHYSICAL VALIDATION PENDING`, `PARTIAL` or `CANONICAL RUNTIME` do not authorize promotion. A plan file receives the `✅-` prefix only after its own full completion contract is proven. Existing downstream code remains reusable historical implementation, but it does not override the stage gate and must not become the current work target while an earlier stage is incomplete.

## Runtime implementation sequence

Completed historical stages:

1. `00-foundation`
2. `01-reference-catalog`
3. `02-arcana-core`
4. `03-integration-layer`
5. `04-world-safety`

Strict current promotion order:

`05-casting-ux -> 05a-arcane-danger -> 06-rituals -> 07-spell-domains -> 07a-arcane-polarity-fusion-metamagic -> 08-progression-balance -> 09-hardening-release`

For each numbered stage use:

`AUDIT -> IDENTIFY GAPS -> IMPLEMENT -> TEST -> VALIDATE -> MARK ✅ -> AUDIT AGAIN -> ONLY THEN ADVANCE`

Stages integrate through current `main`; stale feature ancestry is not merged wholesale. Later stages are not a place to defer functional or validation work required by an earlier stage.

## Visual production is a separate planning lane

UI, HUD, textures, iconography, models, animations, VFX/particles/shaders, sound/audio and visual accessibility are planned under [`visual-production/`](visual-production/README.md).

That directory is intentionally **not** a numbered runtime stage. It owns Black Arcana-specific presentation requirements while `Gustavaopere/minecraft-mod-factory` owns reusable mod/asset production infrastructure, source-art pipeline rules, validators, templates and tooling.

The numbered engineering plans retain only presentation-adjacent facts required for runtime correctness, such as bounded synchronized presentation data, cosmetic fallback modes, render-safe identities and server/client authority boundaries. Final look/layout/art/audio belongs to visual production unless a numbered plan explicitly makes a presentation/physical observation an acceptance requirement; in that case the required evidence still blocks that numbered plan under D034.

See [`visual-production/MIGRATION-MAP.md`](visual-production/MIGRATION-MAP.md) for the extraction audit.

## Non-goals

- no full Mahou Tsukai clone;
- no copied/decompiled Mahou code, assets, models, sounds, animations or protected presentation;
- no mandatory second mana bar/pool by default;
- no universal staff requirement;
- no unbounded power growth or mass permanent destruction by default;
- no client UI or asset failure becoming gameplay authority.

## Engineering stages

- [00 — Foundation](00-foundation/README.md)
- [01 — Reference Catalog](01-reference-catalog/README.md)
- [02 — Arcana Core](02-arcana-core/README.md)
- [03 — Integration Layer](03-integration-layer/README.md)
- [04 — World Safety](04-world-safety/README.md)
- [05 — Casting Runtime & Client Contracts](05-casting-ux/README.md)
- [05A — Arcane Danger](05a-arcane-danger/README.md)
- [06 — Rituals](06-rituals/README.md)
- [07 — Spell Domains](07-spell-domains/README.md)
- [07A — Arcane Polarity, Fusion & Metamagic](07a-arcane-polarity-fusion-metamagic/README.md)
- [08 — Progression & Balance](08-progression-balance/README.md)
- [09 — Hardening & Release](09-hardening-release/README.md)

## Presentation lane

- [Visual Production](visual-production/README.md)
