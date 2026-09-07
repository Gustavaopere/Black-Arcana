# 07.07 — Familiars & Divination

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

Canonical runtime integration: PR #72, squash merge `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`.

The deterministic server/runtime boundary is implemented and exact-SHA automated validation is GREEN. Real-modpack/provider/manual host acceptance, including real-client camera/HUD/input behavior, remains deferred under D031 and is not inferred as PASS.

## Objective

Provide bounded server-authoritative familiar ownership, divination/occult perception, gaze control and Pact Sanctuary behavior without creating a second casting engine, exposing arbitrary private player state or force-loading remote chunks.

## Implemented runtime

Stage 07.07 implements:

- bounded Noetic observation sessions for the approved divination family;
- whitelisted perception snapshots instead of arbitrary NBT/capability/inventory exposure;
- loaded-only target resolution with no force-load/generation path;
- familiar ownership through a bounded provider registry with explicit `OWNED`, `NOT_OWNED` and `UNSUPPORTED` semantics;
- a verified Ars Nouveau 5.13.1 familiar ownership adapter based on the provider's public ownership contract;
- Gaze of Stillness and Nullifying Gaze policies/runtime;
- player privacy admission across observation modes;
- Pact Sanctuary as an owned-familiar, server-authoritative bounded aura;
- lifecycle cleanup for expiry, logout, death and server stop;
- canonical NeoForge game-bus integration and live GameTests.

Provider-native summon/recall behavior remains owned by the host mods. Black Arcana does not introduce a duplicate generic familiar summoning framework.

## Hard safety ceilings

`NoeticSafetyCeilings` freezes the Stage 07.07 upper bounds used by the runtime. Stage 08 may tune below these values but must not silently exceed them:

- observation range: `128` blocks;
- observation/session duration: `600` ticks;
- active observation sessions: `64`;
- effect IDs exposed in one bounded snapshot: `16`;
- display-name payload length: `96` characters;
- familiar ownership providers: `16`;
- nullifications per action: `8`;
- active gazes: `64`;
- gaze range: `24` blocks;
- generic gaze duration: `160` ticks maximum;
- player gaze duration: `40` ticks maximum;
- player gaze reapplication immunity: `80` ticks, with a hard minimum policy floor of `40` ticks;
- nullifiable effect types: `128`;
- gaze diminishing-return stacks: `3`;
- gaze DR tracked targets: `256`;
- gaze DR reset: `600` ticks;
- Sanctuary radius: `16` blocks;
- Sanctuary duration: `600` ticks;
- Sanctuary members: `8`;
- active Sanctuaries: `32`;
- Sanctuary hostile candidates processed per refresh: `32`;
- Sanctuary refresh cadence: `20` ticks, never below the canonical hard floor of `5` ticks;
- pending deferred death cleanups: `256`.

## Privacy, targeting and authority

Observation of another player is admitted only through server-owned privacy/permission facts. A caller cannot bypass player privacy by choosing another observation kind. Perception output is intentionally whitelisted and bounded.

Gaze admission uses canonical entity-interaction authority and keeps PvP control conservative. Stillness enforces horizontal control at entity-tick boundaries rather than relying only on a late server-tick velocity reset. Player applications are capped and followed by an explicit reapplication-immunity window. Diminishing-return state is bounded and expires.

Unknown or unsupported nullification state is not mutated reflectively. Failure to prove a supported nullification path fails closed.

## Familiar ownership

Familiar ownership is provider-driven and fail-closed. Unknown provider state is not interpreted as ownership, and foreign familiars are rejected. Provider count is bounded and provider registration remains explicit.

The Ars Nouveau integration uses the installed `5.13.1` provider boundary. This does not authorize Black Arcana to replace Ars summon/recall, familiar persistence or progression with synthetic equivalents.

## Pact Sanctuary

Pact Sanctuary requires an owned familiar and explicit protected-member membership. Its runtime is bounded by radius, duration, member count, active-aura count and per-refresh candidate budgets.

The spatial query is throttled to the configured bounded refresh cadence and filters for relevant hostile target/member candidates before consuming the hard candidate budget. Target acquisition is also intercepted through the NeoForge target-change event so an eligible hostile mob cannot simply reacquire a protected member before the next settlement pass.

Entity eligibility is fail-closed. `black_arcana:pact_sanctuary_eligible` is the positive eligibility surface; explicit exclusions win. Raiders, Warden and non-allowlisted encounter entities such as Breeze are not pacified merely because they are vanilla mobs. The runtime does not permanently rewrite faction/team/brain state.

## Lifecycle and Soul Anchor interaction

Death cleanup is deferred until the final death outcome is known so a death cancelled by the canonical Soul Anchor runtime does not destroy valid Noetic/Gaze/Sanctuary state for a player who survived. Pending cleanup state is bounded.

Ordinary expiry, logout, confirmed death, familiar removal and server stop clear owned ephemeral state without creating orphan sessions or auras. Cleanup operations are designed to be idempotent where repeated lifecycle signals can occur.

## Automated evidence

Final runtime PR head: `673aff57e15ec29a6fc0d6a94f0034726b99a4c1`.

Authoritative PR workflow: Black Arcana CI #1562 / run `34069825298` — GREEN on that exact head. It passed:

- unit tests;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTest server with **103/103 GameTests**;
- dedicated-server smoke.

All 12 blocking review threads were resolved with evidence before merge.

Canonical runtime merge: PR #72 / `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`.

Exact-SHA post-merge workflow: Black Arcana CI #1563 / run `34070253755` — GREEN on `main@5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, including unit tests, diff sanity, NeoForge build, built-JAR verification, **103/103 GameTests**, dedicated-server smoke and main-only QA artifact publication.

Canonical artifact:

- name: `black-arcana-5c818c12bb6f580893e44f31fd0e17b9c1fe5840`;
- artifact ID: `10000268004`;
- SHA-256: `35c8436ab3cbd2f75e8cc6f7ae5554edb7a330205f5166265f96979b6fa65b16`.

## Acceptance boundary

The deterministic server/runtime acceptance target is satisfied by the automated evidence above: bounded ownership and observation, privacy gates, no-force-load behavior, bounded gaze control, Sanctuary eligibility/budgeting, target-acquisition suppression and lifecycle cleanup are covered by the canonical runtime and validation suite.

This does **not** claim real-client camera/HUD/input acceptance, real-modpack provider behavior or optional-host acceptance. Those remain part of the deferred final validation campaign under D031. No deferred row is converted to PASS from automated CI alone.
