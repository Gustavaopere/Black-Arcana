# Stage 07.05 Black Flame Implementation Plan

> **For agent:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

## Goal

Implement canonical Stage 07.05 Black Flame / `black_arcana:black_pyre` on top of `main@0e508b646b602beefd136bf9602945e247b2a524`, including the approved additive Stage 04 requested-mutation-class and block/world-mutation protection authorities, bounded temporary/permanent terrain settlement, bounded Black Pyre propagation, NeoForge runtime/GameTests, exact-head CI, merge, exact-main CI and post-merge documentation promotion.

## Architecture

Preserve all existing Stage 04 entity/displacement/world-effect APIs for predecessor callers. Add a separate provider-neutral mutation-protection query/registry and an operation-specific requested `WorldMutationClass` admission path under the existing static worst-case `WorldEffectProfile`. Terrain settlement remains server-authoritative, loaded-chunk-only, budgeted, CAS-based and protection-aware. Black Pyre owns its finite frontier and never delegates spread to vanilla fire/random ticks. Entity damage remains an independent `EntityInteractionType.DAMAGE` plane.

## Tech Stack

- Java 21
- NeoForge 1.21.1
- JUnit 5
- Minecraft/NeoForge GameTest
- GitHub Actions `Black Arcana CI`
- Existing Black Arcana Stage 02 cast authority, Stage 04 world-safety services and Stage 05A hazard/provenance contracts

## Task 1 — RED: freeze requested-class and mutation-protection contracts

**Files:**
- Modify: `src/test/java/dev/gustavopere/blackarcana/core/world/ConfigurableWorldEffectPolicyTest.java`
- Modify: `src/test/java/dev/gustavopere/blackarcana/core/world/WorldEffectAdmissionServiceTest.java`
- Create: `src/test/java/dev/gustavopere/blackarcana/core/world/WorldMutationProtectionAdapterRegistryTest.java`
- Create: `src/test/java/dev/gustavopere/blackarcana/core/world/PermanentBlockMutationGatewayTest.java`

**Test requirements:**
1. A `PERMANENT` worst-case profile permits a requested `TEMPORARY` operation when effective mode is `TEMPORARY`.
2. Requested class above the profile maximum fails closed with a stable machine-readable code.
3. Existing two-argument `ConfigurableWorldEffectPolicy#authorize` retains its current worst-case behavior.
4. Existing `WorldEffectAdmissionService#authorize` retains its current behavior.
5. New mutation-protection registry: empty registry allows; all installed adapters must allow; denial propagates; exception/linkage/null decision fails closed; capacity/duplicate IDs remain bounded.
6. New query preserves caster, cast, spell, exact block key, mutation type and requested class.
7. Permanent gateway rejects invalid classes and stale CAS; protection denial occurs before budget consumption.

**RED gate:** commit only tests and run the branch CI. Expected failure must be caused by missing requested-class/mutation-protection/permanent-gateway production APIs, not unrelated regressions.

**Verification command:** `./gradlew --no-daemon test`

**Commit:** `test(stage-07.05): freeze world mutation authority contracts`

## Task 2 — GREEN: implement additive Stage 04 mutation authority

**Files:**
- Create: `src/main/java/dev/gustavopere/blackarcana/core/world/WorldMutationProtectionQuery.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/core/world/WorldMutationProtectionAdapterRegistry.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/core/world/PermanentBlockMutationGateway.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/core/world/ConfigurableWorldEffectPolicy.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/core/world/WorldEffectAdmissionService.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/core/world/TemporaryBlockMutationGateway.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntime.java`
- Tests from Task 1

**Implementation requirements:**
1. Keep `WorldEffectProfile` as the static maximum/worst-case declaration.
2. Add requested-class policy admission without changing the old `authorize(request,target)` semantics.
3. Split actual world-effect admission internally into a non-consuming preflight plus canonical budget consumption so protection can be checked/rechecked before budget is burned; old `authorize(...)` composes the same sequence as before.
4. Requested class must be `<= profile.mutationClass()` and allowed by effective `WorldEffectMode`.
5. Mutation-protection query is separate from entity `ProtectionQuery` and uses provider-neutral core identities only.
6. Registry maximum remains bounded to 32 adapters; empty registry is neutral allow; installed adapter failure is fail-closed.
7. Add a protected temporary mutation path that requests `TEMPORARY`, performs protection before budget, then uses the existing tracker/CAS restoration semantics. Keep the legacy temporary gateway method behavior-compatible.
8. Add `PermanentBlockMutationGateway` for `LIMITED` and `PERMANENT` only: loaded state read, protection, world preflight, protection recheck, budget consume once, CAS; no restoration record and no force-load surface.
9. Install/expose the mutation authority and permanent gateway in `ArcanaServerRuntime` without weakening existing entity protection or protected-destination routes.

**Verification command:** `./gradlew --no-daemon test`

**Commit:** `feat(stage-04): add protected requested-class world mutation authority`

## Task 3 — RED/GREEN: bounded Black Pyre core

**Files:**
- Create: `src/main/java/dev/gustavopere/blackarcana/content/cinder/BlackPyreCell.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/cinder/BlackPyreSafetyCeilings.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/cinder/BlackPyreFrontierScheduler.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/content/cinder/BlackPyreDomainSpecifications.java`
- Create: `src/test/java/dev/gustavopere/blackarcana/content/cinder/BlackPyreFrontierSchedulerTest.java`
- Create: `src/test/java/dev/gustavopere/blackarcana/content/cinder/BlackPyreDomainSpecificationsTest.java`

**RED requirements:** add tests first for constructor ceilings, duplicate/frontier capacity, cell cap, radius, per-tick work, unloaded-cell drop, lifetime expiry/finish and default TEMPORARY domain specification.

**GREEN requirements:**
- ceiling values: radius 12, 256 cells/frontier, 16 processed/tick/frontier, 8 frontiers, 1200 ticks;
- scheduler owns seed/origin and lifecycle timing;
- different dimension/out-of-radius candidates are rejected;
- unloaded candidates are dropped permanently;
- no vanilla fire or chunk-loading API exists in the scheduler;
- duplicate IDs/cells are idempotently rejected;
- expired frontiers are removed.

Historical PR #22 may be used as reviewed source material, but the scheduler must be extended beyond its historical implementation to cover the now-approved radius/lifetime invariants.

**Verification command:** `./gradlew --no-daemon test`

**Commits:**
- `test(stage-07.05): define bounded Black Pyre frontier`
- `feat(stage-07.05): implement bounded Black Pyre core`

## Task 4 — RED/GREEN: NeoForge Black Pyre terrain/runtime authority

**Files:**
- Create/extend: `src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftBlackPyreRuntime.java`
- Create: `src/main/java/dev/gustavopere/blackarcana/integration/neoforge/BlackPyreGameTests.java`
- Modify as required: `src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java`
- Modify as required: NeoForge world-backend/bootstrap wiring that installs `ArcanaServerRuntime#installWorldBackend`
- Add only necessary Black Pyre data/resource registrations under `src/main/resources/`

**RED GameTests first:**
1. COSMETIC does not mutate terrain.
2. Entity-only Black Pyre damages an eligible target while terrain is absent/denied.
3. Allied/protected entity target is not damaged.
4. TEMPORARY can settle even when Black Pyre profile maximum is PERMANENT.
5. Temporary cell restores at expiry; a later player/world edit is not overwritten.
6. Unloaded/chunk-edge candidate does not force-load.
7. Mutation-protection denial prevents mutation and does not burn mutation budget.
8. LIMITED commits one bounded permanent CAS only under allowed mode/protection.
9. PERMANENT path is denied below FULL.
10. Stale state blocks overwrite.
11. No vanilla fire cascade/random-tick propagation.
12. Max legal frontier stress remains bounded.

**GREEN implementation:**
- register `black_arcana:black_pyre` world-effect profile using `WorldMutationType.FIRE_SPREAD` and worst-case `WorldMutationClass.PERMANENT`, bounded to the frontier cell ceiling;
- reuse historical entity DAMAGE boundary semantics: live caster/targets, target dedup, same level, canonical DAMAGE admission, settlement-time reauthorization, finite raw damage <=100, policy multiplier cap never used as an amplifier, actual health loss returned;
- route terrain exclusively through runtime mutation gateways;
- map COSMETIC/TEMPORARY/LIMITED/FULL to no mutation/TEMPORARY/LIMITED/PERMANENT respectively;
- keep terrain result independent from already-authorized entity damage;
- return stable terrain denial/degradation codes;
- do not invent Malum amplification without a verified causal numeric hook; keep it fail-closed/deferred if unsupported;
- do not add a second cast/resource authority for Iron's.

**Verification commands:**
- `./gradlew --no-daemon test`
- `./gradlew --no-daemon runGameTestServer`

**Commits:**
- `test(stage-07.05): add Black Pyre world-mode GameTests`
- `feat(stage-07.05): implement protected Black Pyre runtime`

## Task 5 — integrate lifecycle, hardening and documentation

**Files:**
- Modify runtime/bootstrap lifecycle only where needed to finish/clear Black Pyre frontiers on server stop and ensure restart does not revive spread jobs.
- Modify: `plans/07-spell-domains/05-black-flame.md`
- Modify: `plans/07-spell-domains/README.md`
- Modify: `plans/STATUS.md`
- Update this implementation plan with exact RED/GREEN workflow evidence.

**Requirements:**
- restoration state remains Stage 04 persistent state; frontier jobs are ephemeral and not rehydrated;
- lifecycle cleanup is bounded;
- provider/manual validation remains explicitly deferred under D031;
- stage status becomes implemented/pending merge, never canonical before merge + exact-main GREEN;
- 07.06 remains untouched.

**Verification commands:**
- `./gradlew --no-daemon test`
- `./gradlew --no-daemon build`
- `./gradlew --no-daemon runGameTestServer`
- dedicated-server smoke through the repository workflow.

**Commit:** `docs(stage-07.05): record Black Pyre implementation evidence`

## Task 6 — review, exact-head CI and runtime merge

1. Audit PR changed files against this plan and `plans/07-spell-domains/05-black-flame.md`.
2. Run the Superpowers code-review workflow and resolve findings that do not require redesign; architectural redesign must fail closed and return to design.
3. Confirm branch is not behind canonical main or reconcile intentionally without importing unrelated stale ancestry.
4. Require exact PR head full GREEN:
   - JUnit;
   - diff sanity;
   - NeoForge build;
   - built-JAR verification;
   - all required GameTests;
   - dedicated-server smoke.
5. Merge with `expected_head_sha` protection only after review and exact-head GREEN.

**Commit/merge:** PR title `Stage 07.05: implement protected Black Flame domain`.

## Task 7 — exact-main verification and canonical documentation follow-up

1. Fetch runtime merge SHA from `main`.
2. Require the exact runtime merge SHA workflow to pass the full pipeline and publish the canonical QA JAR.
3. Record artifact name, artifact ID and SHA-256.
4. Create a fresh docs-only branch from that exact runtime main SHA.
5. Rename `plans/07-spell-domains/05-black-flame.md` to `plans/07-spell-domains/✅-05-black-flame.md` only now.
6. Update Stage 07 README and `plans/STATUS.md` with exact runtime PR/head/merge/workflow/artifact evidence.
7. Open docs-only PR, require exact-head GREEN, merge with expected-head protection.
8. Require exact final-main workflow GREEN and canonical artifact publication.
9. Synchronize the Black Arcana Notion dossier and re-fetch it to verify persistence.
10. Confirm final `main` SHA and stop. Do not start 07.06 automatically.

## Non-goals / fail-closed boundaries

- No dynamic dimensions or 07.06 work.
- No vanilla fire spread/random-tick cascade.
- No force-loading.
- No entity `ProtectionQuery` abuse for block claims.
- No direct spell-level arbitrary `ServerLevel#setBlock` bypass.
- No inferred Malum spirit amplification.
- No duplicate Iron's/Black Arcana cast or cost engine.
- No manual/provider PASS without real pack evidence.
- No Stage 08 balance promotion; safety ceilings are not final balance values.
