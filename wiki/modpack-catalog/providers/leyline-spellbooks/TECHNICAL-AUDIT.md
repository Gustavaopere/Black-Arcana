# Leyline Spellbooks 1.0.3 — technical/provenance audit

## Exact installed identity

- JAR: `leylines-1.0.3.jar`
- mod id/runtime: `leylines` / `1.0.3`
- Minecraft/loader: `1.21.1` / NeoForge
- CurseForge Project ID: `1636676`
- CurseForge File ID: `8565076`
- release: `2026-08-02`, Release channel
- Curse Maven coordinate: `curse.maven:leylines-irons-spells-n-spellbooks-addon-1636676:8565076`
- physical modlist hash: `dfa6908731f432905caaaa1e53b4aedeaa26ed59`
- license: `All Rights Reserved`

The current physical modlist is authoritative for the installed hash. It records SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59` for `leylines-1.0.3.jar`, and an independent public manifest for CurseForge File ID `8565076` corroborates that same artifact/hash pair. The previously recorded SHA-1 `5307a4edc885ab949eed4438d9d7f9cb6176421d` is rejected for Leylines; independent public manifests associate that value with `letsdo-wildernature-neoforge-1.1.5.jar` / CurseForge File ID `8543233`.

## Public source status

No publisher-controlled public source repository matching 1.0.3 was located in the current search pass. GitHub repository/code search produced no attributable Leyline Spellbooks source repository.

Consequences:

- this provider is **not source-pinned**;
- public descriptions/changelogs can establish semantic behavior;
- internal registries/classes/API/hooks cannot be inferred from names or from another Iron's addon;
- ARR prevents treating binary/source inspection as permission to copy implementation or assets.

## Exact binary audit status

The previous environment-specific binary-retrieval blocker is closed by isolated non-merge PR #194. CurseForge File ID `8565076` was materialized through Curse Maven and hard-gated against physical SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59` before every inspection pass.

Evidence runs/artifacts:

- primary exact-artifact audit: `34666436710 / 10289437099`;
- targeted reachability audit: `34666652534 / 10289292617`;
- school/loot-gate audit: `34667641655 / 10289184487`.

Only factual identities, resource paths, member signatures, narrow registry/default-control facts and structured acquisition/progression references were retained. The provider binary itself is not committed or redistributed.

## Exact spell inventory supersedes the public lower bound

The publisher names nine `Signature Spells`, but the exact installed registry closes fourteen current identities. The historic publisher list is:

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

## Fields still outside the exact identity closure

Registry identity and current active/survival eligibility are now closed strongly enough for the semantic ledger. The following remain separate evidence gates unless an exact source/config/runtime observation states otherwise:

- assembled-pack numerical spell balance/config values;
- final loot probabilities after complete datapack/modifier composition;
- exact charge accounting internals;
- pillar/rift persistence/network implementation and multiplayer ownership;
- stable public API/hooks suitable for a Black Arcana adapter;
- complete-modpack runtime QA.

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

`EXACT HASH-MATCHED 1.0.3 ARTIFACT / 14 CURRENT SPELL IDENTITIES / CURRENT ELIGIBILITY CLOSED / RUNTIME + API QA FAIL-CLOSED`
