# Stage 07.07 Familiars & Divination Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the Stage 07.07 Noetic/Familiar runtime as bounded server-authoritative observation, gaze, nullification and familiar-aura contracts without force-loading chunks, leaking arbitrary player/NBT data, duplicating host familiar systems or depending on unverified provider internals.

**Architecture:** Black Arcana owns provider-neutral Noetic session/privacy/safety contracts. Minecraft adapters resolve only already-loaded entities and expose whitelisted perception data. Ars Nouveau contributes familiar ownership only through its exact public `api.familiar.IFamiliar` surface; Alshanex/FamiliarsLib remains fail-closed until a stable build-time/public adapter surface can be consumed without private/reflection coupling. Client camera/presentation acceptance remains part of the deferred real-client campaign and is never inferred from server CI.

**Tech Stack:** Java 21, NeoForge 1.21.1 / 21.1.248, JUnit 5, NeoForge GameTests, Ars Nouveau 5.13.1 public API.

**Spec:** `plans/07-spell-domains/07-familiars-divination.md`, `docs/design/candidate-specifications.md`, `docs/reference/classification-matrix.md`, `docs/reference/candidate-host-viability.md`.

## Global Constraints

- Current modpack authority is the uploaded 607-mod snapshot; exact relevant versions are Ars Nouveau `5.13.1`, Iron's Spells `1.21.1-3.16.3`, Eidolon: Repraised `0.5.0.2`, Alshanex's Familiars `1.21.1_v4.0.3`, FamiliarsLib jar `1.21.1-1.7.1` / metadata `1.21.1-1.7`.
- Update the stale Ars compile baseline from 5.13.0/file `8517890` to exact installed 5.13.1/file `8721482` before compiling provider code.
- Never force-load/generate a chunk for scrying, remote perception, familiar resolution or sanctuary operation.
- Never expose arbitrary NBT, capabilities, inventories, container contents, private integration state or hidden entities through Noetic APIs.
- Player Namescry defaults fail-closed unless explicit server/covenant/consent authority is supplied for that request.
- Borrowed Sight accepts only an owned familiar or an explicitly consenting bonded target. Foreign familiar/player targeting fails closed.
- Generic familiar summoning/recall stays host-owned. Black Arcana must not create a duplicate generic familiar framework.
- Ars familiar ownership may use only `com.hollingsworth.arsnouveau.api.familiar.IFamiliar#getOwnerID()` from exact 5.13.1.
- Alshanex/FamiliarsLib source demonstrates ownership methods, but the current published dependency path does not provide a stable consumable API artifact for this repository. No private class reflection/NBT inference is allowed; unsupported provider mode fails closed and is documented.
- Gaze of Stillness uses bounded CONTROL semantics with reciprocal LOS/facing and no permanent movement/faction mutation.
- Nullifying Gaze affects only explicitly registered/tagged nullifiable effects; unknown mod state is never mutated reflectively.
- Pact Sanctuary may suppress an eligible mob's current hostile target only while its owned-familiar-centered aura is live; bosses/event-excluded entities remain unaffected and the runtime may not permanently rewrite teams/factions/AI.
- Real-client camera/HUD/input behavior is `FINAL VALIDATION DEFERRED` unless directly observed on the exact artifact.
- Stage 08 may tune ordinary values below hard ceilings but may not raise safety ceilings silently.

---

### Task 1: Exact provider baseline and Noetic core contracts

**Files:**
- Modify: `gradle.properties`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticSafetyCeilings.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticObservationKind.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticObservationFacts.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticObservationPolicy.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticObservationSession.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticObservationRuntime.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/content/noetic/NoeticObservationContractTest.java`

**Interfaces:**
- `NoeticObservationPolicy.authorize(NoeticObservationKind, NoeticObservationFacts) -> ArcanaDecision`.
- `NoeticObservationRuntime.start(UUID viewer, UUID target, NoeticObservationKind kind, long nowTick, int durationTicks) -> StartResult`.
- One active observation session per viewer; global active-session ceiling.
- Close reasons: `EXPLICIT`, `EXPIRED`, `VIEWER_LOGOUT`, `VIEWER_DEATH`, `TARGET_UNAVAILABLE`, `SERVER_STOP`.

- [ ] Write RED tests proving hard duration/range/session ceilings, player Namescry consent, Borrowed Sight ownership/consent, loaded/same-dimension/range requirements, one-session-per-viewer, expiry and exactly-once cleanup.
- [ ] Push test-only commit and verify CI fails because the Noetic production contracts do not exist.
- [ ] Implement the minimal core classes and sync Ars compile baseline to 5.13.1 / Curse file `8721482`.
- [ ] Verify full CI GREEN before continuing.

### Task 2: Familiar ownership provider registry and exact Ars 5.13.1 adapter

**Files:**
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/FamiliarOwnershipProvider.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/FamiliarOwnershipRegistry.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/integration/ars/ArsFamiliarOwnershipProvider.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/integration/ars/ArsIntegrationBridge.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/api/ArcanaIntegrationCapability.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/content/noetic/FamiliarOwnershipRegistryTest.java`

**Interfaces:**
- Provider result is tri-state: `OWNED`, `NOT_OWNED`, `UNSUPPORTED`; provider exceptions become `UNSUPPORTED` and never grant ownership.
- Registry deduplicates provider IDs, evaluates bounded provider count and grants ownership only on explicit `OWNED`.
- Ars adapter performs a public API type check and compares `IFamiliar#getOwnerID()` against the requested owner UUID.

- [ ] Write RED tests for provider dedupe, exception fail-closed, foreign familiar denial and no-provider denial.
- [ ] Implement registry and Ars public-API adapter.
- [ ] Add `FAMILIAR_OWNERSHIP` capability to the Ars bridge only when the exact public API is available.
- [ ] Verify GREEN.

### Task 3: Minecraft observation admission and whitelisted perception payload

**Files:**
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticPerceptionSnapshot.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticObservationRuntime.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticObservationRuntimeContractTest.java`

**Interfaces:**
- `start(server, viewerId, targetId, kind, durationTicks, explicitConsent) -> ArcanaDecision`.
- Target resolution iterates only currently loaded `ServerLevel` entity maps; it never calls a chunk acquisition API.
- Snapshot whitelist: target UUID/type id, bounded display-name text, health fraction for living targets, bounded active-effect IDs and main-hand item ID. No NBT/capability/inventory serialization.
- `snapshot(server, viewerId) -> Optional<NoeticPerceptionSnapshot>` revalidates loaded target/session before exposing data.

- [ ] Write RED tests for payload bounds/privacy and no arbitrary data fields.
- [ ] Implement loaded-target/same-dimension/range/LOS/consent/familiar admission.
- [ ] Wire lifecycle pruning for viewer logout/death, target unavailable/death, expiry and server stop.
- [ ] Verify GREEN.

### Task 4: Gaze of Stillness and Nullifying Gaze bounded policies

**Files:**
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticGazePolicy.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/NullificationRegistry.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticGazeRuntime.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/content/noetic/NoeticGazeContractTest.java`

**Interfaces:**
- Stillness requires living/loaded/same-dimension target, reciprocal LOS/facing facts, range ceiling and canonical hostile CONTROL authorization before applying a bounded temporary suppression state.
- Nullification accepts only registered/tag-authorized `ResourceLocation` effect IDs, caps removals per action and revalidates target/authorization at settlement.
- Unknown effects/adapters fail closed; no private host state reflection.

- [ ] RED tests for broken LOS/facing, boss/player limits, unknown-effect denial, removal budget and expiry cleanup.
- [ ] Implement policy/runtime using canonical CONTROL admission where applicable.
- [ ] Verify GREEN.

### Task 5: Pact Sanctuary bounded familiar aura

**Files:**
- Create: `src/main/java/dev/gustavopere/blackarcana/content/noetic/PactSanctuarySpec.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftPactSanctuaryRuntime.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/content/noetic/PactSanctuaryContractTest.java`

**Interfaces:**
- Activation requires confirmed familiar ownership through `FamiliarOwnershipRegistry` and all aura-covering chunks already loaded.
- Hard ceilings: bounded radius/duration/member count/concurrent auras and per-tick mob scan budget.
- Only clears an eligible ordinary mob's current hostile target when that target is an explicitly supplied sanctuary member. No permanent team/faction/brain rewrite.
- Familiar unload/death, owner logout/death, expiry and server stop close the aura.

- [ ] RED tests for owner mismatch, radius/duration/member ceilings, candidate budget, deduplication and exactly-once cleanup.
- [ ] Implement bounded runtime and lifecycle.
- [ ] Verify GREEN.

### Task 6: Composition root and live NeoForge GameTests

**Files:**
- Modify: `src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/BlackArcanaNoeticGameTests.java`
- Modify as required: `src/main/java/dev/gustavopere/blackarcana/integration/ars/ArsServerIntegrationBootstrap.java`

**Interfaces:**
- Register Noetic observation/gaze/sanctuary lifecycle exactly once on the NeoForge game bus.
- Install Ars familiar provider only from the optional Ars server entrypoint after NeoForge confirms `ars_nouveau` is loaded.
- Live GameTests prove already-loaded target admission, foreign familiar/player privacy denial, whitelisted snapshot bounds, cleanup and no orphan server state.

- [ ] Add RED wiring/GameTest contract if composition-root registration is absent.
- [ ] Wire runtimes/provider registration.
- [ ] Run full repository gate: JUnit, diff sanity, NeoForge build, built-JAR verification, all required GameTests and dedicated-server smoke.

### Task 7: PR review, merge, canonical promotion and Notion persistence

**Files:**
- Runtime PR first.
- After exact runtime-merge main CI is GREEN, update `plans/07-spell-domains/07-familiars-divination.md`, `plans/07-spell-domains/README.md`, `plans/STATUS.md` in a separate promotion PR.

- [ ] Open runtime PR from exact latest-main ancestry; inspect complete diff and review threads.
- [ ] Require exact final PR head full GREEN; resolve all review threads before squash merge.
- [ ] Confirm exact runtime merge SHA, exact main CI and canonical artifact.
- [ ] Promote docs with only observed evidence; preserve client/provider/manual rows as deferred.
- [ ] Merge promotion PR only after its exact head CI is GREEN, then verify final main CI/artifact.
- [ ] Update the canonical Black Arcana Notion dossier to final main SHA and re-fetch to prove persistence.
- [ ] Stop. Do not start Stage 08 automatically.

## Self-review

- Spec coverage: Astral Severance/Namescry/Borrowed Sight/Occult Appraisal share the observation authority; Gaze of Stillness/Nullifying Gaze have dedicated bounded policies; Pact Sanctuary has its own owned-familiar aura runtime. Generic summon/recall remains host-owned by design.
- Provider coverage: exact Ars 5.13.1 public familiar ownership is implementable; Alshanex/FamiliarsLib is explicitly recorded but not guessed through internals.
- Safety coverage: no-force-load, player privacy, bounded metadata, lifecycle cleanup, no arbitrary NBT/inventory, no permanent faction mutation and fail-closed unknown provider state are each tied to tests.
- No placeholders are used; deferred items are validation/provider boundaries rather than missing implementation instructions.
