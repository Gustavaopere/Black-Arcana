# 07.06 — Forbidden Domains

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

Canonical runtime integration: PR #59, squash merge `836623d39d3060de1b8830000c43d493305cd740`.

The deterministic server/runtime boundary is implemented and exact-SHA automated validation is GREEN. Real-modpack/provider/manual host acceptance remains deferred under D031 and is not inferred as PASS.

## Objective

Represent reality/domain-style endgame magic as bounded, server-authoritative localized battle fields without introducing a second casting authority, arbitrary world destruction or unbounded instance lifecycle.

## Frozen architecture — D032

D032 resolves the earlier architecture question in favor of **localized in-world fields/arenas in an already-loaded dimension**. Stage 07.06 does not create temporary dimensions or isolated dynamic instances. A future dynamic-dimension design requires a new explicit architectural decision and cannot be silently added under this stage.

The Stage 07.06 runtime therefore:

- creates no dynamic dimension and no orphan dimension lifecycle;
- acquires no chunk ticket and never force-loads/generates chunks for a domain;
- clones no inventory, capability or persistent player state;
- owns no parallel teleport/casting/world-mutation pipeline;
- performs no arbitrary terrain mutation in the base domain runtime;
- reuses the canonical Stage 04 loaded-chunk, world-border, protection and world-effect authorities;
- reuses the Stage 07.04 safe-destination boundary for recovery admission;
- keeps domain state bounded, ephemeral and server-owned.

## Hard safety ceilings

The implementation freezes these absolute ceilings:

- radius: `24` blocks maximum;
- duration: `1,200` ticks maximum;
- tracked participants/entities: `64` per domain maximum;
- active domains: `8` server-wide maximum;
- active domains per owner: `1`;
- restoration/work metadata budget: `512` recorded positions maximum.

A `ForbiddenDomainSpec` outside these bounds is rejected. `TEMPORARY_DIMENSION` exists only as an explicit mode marker and is rejected by the current spec under D032.

## Admission and authority

A localized field starts only when the live Minecraft adapter can prove all required facts. Unknown state fails closed.

Admission requires:

1. every covered chunk is already loaded, checked without chunk acquisition;
2. the entire bounded field is inside the live world border;
3. canonical protected-destination authorization succeeds;
4. canonical Stage 04 world-effect admission succeeds for the registered cosmetic field profile;
5. a safe recovery position is valid through the shared Stage 07.04 destination policy.

Participant capture additionally requires same-dimension/radius membership, an already-loaded position, canonical `EntityInteractionType.DOMAIN_CAPTURE` authorization and a valid safe-recovery boundary.

The current implementation is intentionally provider-neutral. Stage 01 did not establish concrete provider-native Arsenal/Soul/Blood Forbidden Domain gameplay semantics, so Stage 07.06 does **not** invent damage, resource, soul, blood or spell effects. Those semantics remain fail-closed until separately approved and backed by verified provider/API authority.

## Lifecycle and anti-orphan behavior

Server-owned lifecycle cleanup covers explicit close, expiry, owner logout, owner death, owner-unavailable state and server stop. Close is exactly-once/idempotent.

Participant UUIDs are deduplicated and bounded. Logout/death removes a participant globally without permanently consuming the participant budget. Tick pruning removes participants that are dead, unavailable, outside the field, in another dimension or no longer in an already-loaded chunk. Owner-unavailable state closes the owner's field instead of leaving an orphan session.

Server stop clears all ephemeral sessions and field metadata. No inventory/state duplication path is owned by this system.

## TDD and automated evidence

The implementation was developed through explicit RED→GREEN contracts:

- initial RED: test-only head `730b29d76a625f764ca8cf9722cbfd518aeffdcd`, workflow #1176 / run `34031175395`, failed exactly because the Forbidden Domain contracts did not yet exist;
- participant-cleanup RED: workflow #1180 / run `34034771331`, reproduced the missing participant logout cleanup;
- intermediate hardened head `b042b1592b071b93d5d99640cce7c0bfc3df30b2`: workflow #1186 / run `34036053266` passed the complete gate;
- final PR head `b560a1a0e4d2679d101008526d87de6a8a3b4325`: push workflow #1187 / run `34036461398` and PR workflow #1188 / run `34036463695` both GREEN;
- runtime merge `836623d39d3060de1b8830000c43d493305cd740`: exact-SHA post-merge workflow #1189 / run `34036992474` GREEN.

The exact post-merge workflow passed JUnit, diff sanity, NeoForge build, built-JAR verification, **95/95 required GameTests**, dedicated-server smoke and main-only canonical QA artifact publication.

Canonical runtime artifact:

- name: `black-arcana-836623d39d3060de1b8830000c43d493305cd740`;
- artifact ID: `9990520844`;
- SHA-256: `e77666b5768a51193597c65f1f0be4547c5e5723fa51a1a36d41c5354e8b1ebe`.

`BlackArcanaForbiddenDomainGameTests` exercises the live NeoForge GameTest-server boundary for canonical runtime lookup, loaded-world admission, world-border/protection/world-effect/safe-recovery checks, bounded session creation, active-count ownership and exactly-once cleanup.

## Acceptance boundary

The deterministic acceptance target is satisfied: the implementation does not create temporary dimensions, does not force-load chunks, does not clone inventories, does not own arbitrary terrain destruction and closes bounded runtime state across validated lifecycle paths.

Real-modpack/provider/manual host behavior remains part of the deferred final validation campaign under D031. No manual or provider-native effect PASS is claimed from automated CI.
