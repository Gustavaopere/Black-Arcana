# Leyline Spellbooks 1.0.3 — technical/provenance audit

## Exact installed identity

- JAR: `leylines-1.0.3.jar`
- mod id/runtime: `leylines` / `1.0.3`
- Minecraft/loader: `1.21.1` / NeoForge
- CurseForge Project ID: `1636676`
- CurseForge File ID: `8565076`
- release: `2026-08-02`, Release channel
- Curse Maven coordinate: `curse.maven:leylines-irons-spells-n-spellbooks-addon-1636676:8565076`
- physical modlist hash: `5307a4edc885ab949eed4438d9d7f9cb6176421d`
- license: `All Rights Reserved`

The current physical modlist is authoritative for the installed hash. Previous catalog material recorded `dfa6908731f432905caaaa1e53b4aedeaa26ed59` from a third-party index as the artifact SHA-1. That external value conflicts with the current physical row and is retired from installed-artifact provenance.

## Public source status

No publisher-controlled public source repository matching 1.0.3 was located in the current search pass. GitHub repository/code search produced no attributable Leyline Spellbooks source repository.

Consequences:

- this provider is **not source-pinned**;
- public descriptions/changelogs can establish semantic behavior;
- internal registries/classes/API/hooks cannot be inferred from names or from another Iron's addon;
- ARR prevents treating binary/source inspection as permission to copy implementation or assets.

## Binary retrieval status

The official CurseForge file page and manual download flow were reached and confirm File ID 8565076. The file page publishes the Curse Maven coordinate. The browser exposed only the download countdown page rather than the binary redirect, and the local shell environment had no external DNS resolution for Curse Maven/ForgeCDN.

Therefore, during this checkpoint:

- exact JAR identity: `VERIFIED`;
- inspectable binary bytes: `NOT OBTAINED`;
- hash recomputation in this environment: `NOT PERFORMED`;
- bytecode/resource extraction: `NOT PERFORMED`;
- decompilation: `NOT PERFORMED`.

This is an environment/evidence limit, not evidence that the binary is unavailable publicly.

## Public spell inventory ceiling

The publisher names nine `Signature Spells`:

1. Blink Step
2. Rift Gate
3. Chrono Tether
4. Temporal Stutter
5. Fissure
6. Anchor Recall
7. Beam
8. Ley Blast
9. Eclipse

The same publisher text says `and more`, so these nine names are a lower bound, not an inventory total.

Six receive explicit individual semantic descriptions. Beam, Ley Blast and Eclipse are named together under a general charge/power sentence; no individual mechanic is attributable to any one of those three from that text alone.

## Fields blocked pending exact-artifact inspection

For every Leyline spell unless a publisher source explicitly states otherwise:

- registry ID/class: `UNVERIFIED`
- actual registered school per spell: `UNVERIFIED`
- rarity/levels: `UNVERIFIED`
- mana/cooldown/cast time/recast: `UNVERIFIED`
- damage/healing/power formulas: `UNVERIFIED`
- range/area/duration: `UNVERIFIED`
- exact targeting/PvP/boss rules: `UNVERIFIED`
- charge storage/generation/spend: `UNVERIFIED`
- particles/sounds/animations: `UNVERIFIED`
- item/scroll/codex acquisition: `UNVERIFIED`
- networking/persistence/API hooks: `UNVERIFIED`

## Publisher-confirmed 1.0.3 rift rules

The 1.0.3 changelog establishes these semantic contracts:

- player death during an active encounter fails the fight and denies completion loot/crystal;
- wave boss bar cleanup occurs on death, respawn, logout and dimension change;
- leaving more than 60 blocks from an active rift collapses it;
- wave mobs more than 40 blocks away are returned to the arena;
- encounter mobs persist across brief fighter death to prevent false success;
- `/leylines spawnpillar` requires permission level 2 and is explicitly admin/debug tooling.

The implementation points, storage structures and event hooks remain unknown.

## Authority boundary

Provider-native first:

- Iron's: generic casting/mana/school infrastructure where used through its addon model;
- Leyline Spellbooks: Leyline school content, spell semantics, pillar/rift/progression state and rewards;
- Black Arcana: its own forbidden-magic casting/domains/hazards/corruption/strain/world-safety runtime only.

A future adapter must fail closed unless a stable exact-version hook is proven. It must not create a second rift state machine, portal pair, recall anchor, charge ledger or reward listener.

## Canonical tree correction

Before Phase 2N, the catalog accidentally contained two directories for the same mod id:

- `providers/leyline-spellbooks/` — short summary;
- `providers/leylines/` — richer progression/rift/spell audit.

Phase 2N consolidates them into `providers/leyline-spellbooks/` and removes the duplicate provider tree. This is an editorial normalization only; no runtime behavior changes.

## State

`EXACT INSTALLED IDENTITY / PUBLIC SEMANTIC SURFACE ADVANCED / 9 SIGNATURE NAMES LOWER BOUND / COMPLETE REGISTRY UNKNOWN / BINARY + API QA PENDING / FAIL-CLOSED`
