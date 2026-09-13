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

Implementation evidence and direct physical validation are separate facts. CI/GameTests do not fabricate a real-client/full-pack PASS. A completed runtime stage may proceed downstream when its required runtime contracts are frozen even if non-blocking presentation polish is deferred.

## Runtime implementation sequence

1. `00-foundation`
2. `01-reference-catalog`
3. `02-arcana-core`
4. `03-integration-layer`
5. `04-world-safety`
6. `05-casting-ux`
7. `05a-arcane-danger`
8. `06-rituals`
9. `07-spell-domains`
10. `07a-arcane-polarity-fusion-metamagic`
11. `08-progression-balance`
12. `09-hardening-release`
13. accumulated final validation/release closeout

Stages integrate sequentially through current `main`; stale feature ancestry is not merged wholesale.

## Visual production is a separate planning lane

UI, HUD, textures, iconography, models, animations, VFX/particles/shaders, sound/audio and visual accessibility are planned under [`visual-production/`](visual-production/README.md).

That directory is intentionally **not** a numbered runtime stage. It owns Black Arcana-specific presentation requirements while `Gustavaopere/minecraft-mod-factory` owns reusable mod/asset production infrastructure, source-art pipeline rules, validators, templates and tooling.

The numbered engineering plans retain only presentation-adjacent facts required for runtime correctness, such as bounded synchronized presentation data, cosmetic fallback modes, render-safe identities and server/client authority boundaries. Final look/layout/art/audio belongs to visual production.

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
