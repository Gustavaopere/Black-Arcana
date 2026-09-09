# Phase 2AH — Monsters & Spellbooks 0.0.16.3 checkpoint

Status: `PARTIAL CHECKPOINT / DOES NOT INCREMENT GLOBAL COVERAGE`

## Baseline

- Black Arcana base main: `2de722272814d2d5664266f5fc8ad05ba25d2940`
- Branch: `docs/magic-catalog-phase2ah-monsters-spellbooks`
- Physical modlist: 595 top-level entries
- NeoForge: `21.1.248`
- Physical provider: `monstersspellbooks-0.0.16.3.jar`
- Physical SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`
- Physical Iron's host: `1.21.1-3.16.3`

## Exact release evidence

- CurseForge project `1428928`
- File ID `8788560`
- exact filename/version: `monstersspellbooks-0.0.16.3.jar`
- NeoForge / Minecraft 1.21.1 / Release
- uploaded 2026-09-01
- current publisher scale: `90+ spells`, `2 new spell schools`

## Official source baseline

- repository: `RedReaper28/Monsters-Spellbooks-1.21.1`
- inspected head: `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`
- source head date: 2026-09-01
- source build metadata: mod `0.0.14`, NeoForge `21.1.216`, Iron's `1.21.1-3.15.4`
- source-baseline spell registrations: **98** across 11 families
- source-baseline provider school registrations: `necro`, `aero`

## Why this phase is partial

The official source tree does not declare the installed version and no `0.0.16.3` tag/commit declaration was located. The exact installed JAR binary was not available for inspection. In addition, the exact 0.0.16.3 release notes say some Aero remnants were removed while the current public source head still registers an Aero school.

Therefore this pass cannot prove exact current:

- spell registry count/IDs;
- class/API/signature parity;
- Aero school state;
- configs/network/save formats;
- full-modpack runtime compatibility.

## Provenance gate

CurseForge currently labels the project MIT, while source `gradle.properties` says All Rights Reserved. `TEMPLATE_LICENSE.txt` licenses the MDK template, not the addon's implementation. This is recorded as a license-metadata divergence; source use remains read-only factual reference only.

## Architecture outcome

- Iron's retains host casting/mana authority.
- Monsters & Spellbooks retains authority for its actual provider spell/school/content behavior.
- Black Arcana does not duplicate provider mana, effects, summons, projectiles, progression or school settlement.
- Provider Necro does not become BA Corruption/Strain/Arcane Danger/Souls & Death or RPG Mastery by naming similarity.
- exact-internal adapters stay fail-closed.

## Coverage outcome

Canonical coverage entering this phase: **36/100**.

Phase 2AH contributes **0 additional closed-component points** because an unresolved current-version delta remains. Coverage after this checkpoint therefore remains **36/100**.

The next provider selection may seek a component whose exact/current evidence can actually close point #37. Phase 3 remains blocked.