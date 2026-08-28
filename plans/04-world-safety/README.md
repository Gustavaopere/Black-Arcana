# 04 — World Safety

All dangerous Black Arcana content consumes these contracts before spells are implemented.

## Tasks
- Global/per-spell world-effect policy.
- Temporary block/effect lifecycle and rollback.
- Area budgets, chunk safety and scheduler.
- PvP, bosses, claims/protected-area adapters where appropriate.

## Preparatory implementation state

Implementation is advanced on `prep/04-world-safety`.

Present in source:
- hierarchical `OFF/COSMETIC/TEMPORARY/LIMITED/FULL` policy with mandatory profiles and non-escalating overrides;
- total-per-cast budgets plus bounded global work scheduler;
- loaded-chunk-only admission with no ticket/loading API;
- transactional temporary block gateway, bounded ownership tracker and restart persistence;
- NeoForge/Minecraft backend using loaded chunks, full block-state serialization, CAS and block-entity refusal;
- bounded runtime restoration that preserves external/player edits;
- server-derived PvP/team/boss/invulnerability facts;
- boss-specific caps, claim/protection extension registry and protected-destination guard;
- JUnit, stress and GameTest coverage for the above contracts.

Detailed audit: `docs/architecture/world-safety-preparatory.md`.

## Exit criteria
Synthetic explosions/fire/block mutation cannot bypass policy, exceed configured budgets or leak temporary world state across restart/chunk unload.

## Verification gate

Do not rename tasks to ✅ and do not promote this stage while the runner has not actually executed:
1. JUnit tests;
2. NeoForge build/JAR inspection;
3. GameTest server;
4. dedicated-server smoke.

The current GitHub-hosted runner failure occurs before any executable workflow step (`steps=null`), so implementation remains preparatory rather than falsely marked complete.
