# Sophisticated Backpacks: Ars Compat — runtime QA gate

Status: `EXACT RELEASE IDENTITY CLOSED / RUNTIME QA REQUIRED / FAIL-CLOSED`

## Why runtime QA remains open

The physical artifact is `arssophisticatedcompat-0.3.0.jar`, and the catalogue now aligns that identity with official CurseForge File ID `8653384` for **Sophisticated Backpacks: Ars Compat 0.3.0 — NeoForge 1.21.1**. The prior comparison against `arssophisticatedstoragecompat-0.3.0.jar` File ID `8655579` was a comparison against a separate Sophisticated Storage sibling project and is no longer used as evidence of a binary mismatch.

Release identity and semantic catalogue scope are therefore closed. Runtime/API internals are not.

The publisher declares Ars Nouveau, Sophisticated Backpacks and Sophisticated Core as required families, but this dossier does not infer exact deployed host versions unless independently established by physical evidence.

## Required internal/API evidence before a Black Arcana adapter

Before any code-level Black Arcana adapter is approved, establish from an allowed exact boundary:

1. exact metadata/dependency ranges;
2. registered item/upgrade/resource IDs relevant to integration;
3. capability/API entry points;
4. config values/defaults;
5. payloads/network direction and server validation, if any;
6. mixins, if any;
7. lifecycle/tick entry points;
8. Source storage/conversion/repair settlement semantics;
9. recipe/acquisition definitions when needed by integration;
10. persistence and migration semantics.

These are runtime/integration requirements, not blockers for the zero spell/glyph/ritual catalogue result.

## Required runtime matrix

On the actual modpack stack, validate at minimum:

- install/remove every supported backpack upgrade;
- Source insert/extract and full-capacity behavior;
- Stack Upgrade increase/decrease while Source or potion duration is stored;
- Sourcelink conversion under player and automated inventory mutation;
- chunk unload/reload and full server restart;
- backpack lifecycle paths supported by the provider;
- Potion Jar effect expiration/removal/reconnect without ghost refresh;
- Enchanter repair with insufficient/exact/excess Source;
- concurrent users/automation actors touching the same backpack state where supported;
- dedicated-server startup/classloading.

## Acceptance rule

Only directly observed or exact-source/API-backed behavior may move from `UNKNOWN` to `CONFIRMED` for integration.

A failed or unavailable provider hook disables the dependent Black Arcana feature. It must not trigger a generic fallback that invents Source, repairs, potion duration or backpack state.
