# Black Arcana — Architectural Decisions

This file records decisions that must survive across sessions. Amend deliberately; do not silently reinterpret them.

## D001 — Target platform
Black Arcana targets Minecraft 1.21.1 on NeoForge with Java 21.

## D002 — Clean-room implementation
Mahou Tsukai is a behavioral/design reference only. Black Arcana will not copy/decompile its code or reuse protected assets. Mechanics are specified from observable/public behavior and then implemented independently with original code, naming, presentation and balancing.

## D003 — Original identity
Black Arcana is not "Mahou Tsukai 2". Strongly derivative names, fiction-specific terminology and presentation should be replaced with original Black Arcana terminology unless a term is generic.

## D004 — No mandatory second mana pool
Black Arcana core must support pluggable cost providers. Spells may consume Iron's mana, Ars resources, Malum spirits, items, health, cooldown budget or composite costs. A permanent Black Arcana mana pool/UI is not the default architecture.

## D005 — Casting is not staff-locked
Core casting must support direct keybind/loadout invocation. Books, weapons, staves and rituals can be optional invocation surfaces, not universal requirements.

## D006 — Server authority
The server validates cast legality, resource costs, cooldowns, progression gates, targets and world effects. Client UI is predictive/presentational only.

## D007 — World destruction is policy-controlled
Every Black Arcana mechanic capable of altering blocks, fluids, explosions, fire or persistent entities must route through a configurable `WorldEffectPolicy`. Default presets favor temporary/limited effects over permanent destruction.

## D008 — Bounded power
No mechanic may scale without an explicit upper bound or diminishing-return function. Resurrection charges, stored damage, weapon strengthening, summoned arsenal size, domain radius/duration and area destruction all require caps/budgets.

## D009 — Integration architecture
External-mod integrations live behind Black Arcana-owned interfaces. Core code must not scatter direct optional-mod references. Adapters activate only when the target mod and compatible API are present.

## D010 — Content taxonomy
Initial content families are: Blood & Curses, Souls & Death, Projection & Arsenal, Space & Displacement, Black Flame, Forbidden Domains, Familiars & Divination. Stage 01 may merge/drop concepts before implementation.

## D011 — Ritual philosophy
Routine combat spells should not require ritual busywork. Rituals are reserved for permanent unlocks, high-impact bargains, grand effects, soul contracts, domain creation/upgrades and other actions that benefit from preparation and world interaction.

## D012 — Progression philosophy
Power should come from knowledge, RPG attributes/mastery, equipment and meaningful ritual milestones—not repetitive resource-spending loops that inflate a mana cap indefinitely.

## D013 — License
Project license is intentionally undecided until the clean-room/provenance stage. Do not add a repository license without an explicit decision. `All Rights Reserved` in mandatory NeoForge mod metadata is a conservative packaging placeholder and is not a decision to publish under a particular license.

## D014 — Foundation toolchain pins
The initial 1.21.1 foundation follows the current official NeoForge MDK baseline observed on 2026-08-27: ModDevGradle `2.0.144`, NeoForge `21.1.248`, Parchment `2024.11.17` for Minecraft `1.21.1`, Java 21, and Gradle `9.2.1`.

## D015 — Reproducible text Gradle bootstrap
Until a standard binary `gradle-wrapper.jar` can be introduced and verified cleanly, the repository uses text `gradlew`/`gradlew.bat` bootstraps pinned to Gradle 9.2.1. The launcher downloads the official binary distribution and verifies it against Gradle's published SHA-256 before executing. This is an implementation detail, not an API contract; replacing it later with the official wrapper is allowed without changing gameplay architecture.

## D016 — Cast identity and replay [PREPARATORY Stage 02]
Every server cast request has a unique `ArcanaCastId`. Canonical identity/loadout validation happens before progression and gameplay execution, and a bounded replay guard claims the cast id before expensive work. Duplicate request replay is a structured denial, not an idempotent second execution.

## D017 — Composite resource transactions [PREPARATORY Stage 02]
Multi-resource costs reserve every component before the effect executes. If any later reservation fails, earlier reservations refund in reverse order. After a reservation reports success, `commit()` is required to be an infallible terminal operation; adapters that cannot guarantee that contract require explicit escrow/compensation design rather than pretending to be atomic.

## D018 — Cooldown time semantics [PREPARATORY Stage 02]
Cooldowns are keyed by caster + canonical group, not by client UI state. Persistent cooldown storage uses a monotonic gameplay tick supplied by the server persistence bridge. A config decrease may shorten an existing cooldown; a config increase does not retroactively extend one already started.

## D019 — Bounded targeting and follow-up work [PREPARATORY Stage 02]
Client targeting is only intent. Server-computed facts determine loaded/alive/range/LOS/player/friendly eligibility. Area selection has absolute range/target ceilings and deterministic ordering. Expensive multi-tick effects use a bounded scheduler rather than unbounded per-tick loops.

## D020 — Minimal network authority [PREPARATORY Stage 02]
Cast-intent payloads carry only bounded identity/intention fields such as cast id, spell id, loadout slot and target hint. Authoritative cost, damage, cooldown, range, progression and world mutation values are resolved from server registries/config. Protocol payloads are versioned, bounded and rate-limited at ingress.

## D021 — Datapacks are declarative, not executable [PREPARATORY Stage 02]
The initial spell datapack schema is intentionally limited to identity/presentation metadata. Unknown fields are rejected and a resource's path-derived id must match its declared id. Data-driven authoritative balance may be added only through a bounded schema designed by Stage 08; datapacks never provide Java class names, commands, script bodies or arbitrary execution hooks.

## D022 — Global player runtime state uses Overworld SavedData [PREPARATORY Stage 02]
Cooldowns, charge pools and loadouts are player/global runtime state rather than dimension-local state, so their Minecraft persistence adapter is attached to the Overworld `DimensionDataStorage`. Restore is bounded and tolerant of malformed individual entries. Removed cooldown/charge groups are pruned only after server initializers install the current canonical policies, preventing early startup from deleting valid state.

## D023 — Client synchronization is event-driven [PREPARATORY Stage 02]
Black Arcana does not send full runtime state every tick. Spell presentation is synchronized on login and successful metadata reload; cooldown snapshots are synchronized on login and after a successful cast. Future UI-specific incremental packets must preserve this event-driven model and hard payload limits.

## D024 — Channeling converges on the canonical cast engine [PREPARATORY Stage 02]
Beginning a charge/channel creates bounded server-owned session state but does not execute gameplay effects or spend resources. Releasing a valid session consumes it and then enters the same `ArcanaCastEngine` used by immediate casts exactly once. The server computes channel duration from gameplay ticks, preserves the original loadout slot, and revalidates the current spell/loadout/runtime at release. Client-reported charge duration is never authoritative, and Stage 05 input packets must terminate in this coordinator rather than introducing a parallel execution pipeline.

## D025 — Target kinds require explicit server geometry [PREPARATORY Stage 02]
Every `ArcanaTargetSpec.Kind` has a server-owned resolution route. Entity/projectile hints are advisory ids only; block/ray results come from server raycasts with loaded-chunk preflight; cone/cylinder require bounded `ArcanaTargetGeometry` rather than hidden default angles or heights; linked targets come from a server-owned resolver and never from a client-authored entity list. Target references crossing core/effect boundaries use canonical typed entity/block encodings.

## D026 — Expensive effects are admitted before cost commit [PREPARATORY Stage 02]
Multi-tick or high-cardinality effects use `ScheduledArcanaEffect` and the runtime-owned `BoundedWorkScheduler`. Queue saturation fails the effect before resource commit so the normal cast transaction can refund. Accepted work is processed under a fixed per-tick budget, a pending item runs at most once per tick, and a failing work item is isolated/dropped instead of corrupting the remaining queue.

## D027 — Runtime group renames precede orphan pruning [PREPARATORY Stage 02]
Cooldown and charge group identifiers may be renamed through a validated, cycle-free migration graph. Startup order is `initializers/policies -> SavedData restore -> runtime group migrations -> orphan pruning`. Rename collisions merge conservatively: cooldowns preserve the later ready boundary; charge pools preserve the lower available charge count and later recharge boundary. Removed groups remain the responsibility of the active-policy pruning pass.

## D028 — Arcane Danger is inserted as Stage 05A
Arcane Danger, Resistance, Corruption & Backlash is a causal prerequisite for canonical high-power Rituals and Spell Domains. It is inserted as Stage `05A` between Casting & UX and Rituals rather than renumbering established Stages 06–09 or invalidating already-verified branch history. Existing ritual preparatory code is preserved as a downstream prototype and must be synchronized/retested after Stage 05A freezes its hazard APIs. Black Arcana owns hazard computation; downstream content consumes these contracts rather than implementing parallel backlash/corruption systems.

## D029 — Arcane Danger extends the canonical cast transaction
Stage 05A does not introduce a parallel cast engine. Hazard handling is an optional server-side transaction hook inside the existing `ArcanaCastEngine`: after ordinary identity/replay/progression/cooldown/target/cost-check/world-policy validation, the engine obtains a side-effect-free hazard preflight; only an allowed preflight permits normal resource reservation. After reservation succeeds, hazard activation occurs before spell effects. Any denial or effect failure before commit cancels the prepared hazard state and preserves the existing resource-refund path. A successful effect commits the resource transaction, starts cooldown state, then commits the prepared hazard transaction before optional success observers. Existing non-hazardous engines retain identical behavior through the no-op hazard gate. Hazard `commit()` is a terminal/infallible contract; adapters that cannot guarantee it require explicit compensation design rather than silently weakening cast atomicity.
