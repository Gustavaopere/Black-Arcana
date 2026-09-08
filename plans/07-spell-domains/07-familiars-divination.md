# 07.07 — Familiars & Divination

## State

`IN PROGRESS — SERVER SUBSTRATE MERGED / BORROWED SIGHT CODE PATH IMPLEMENTED / ASTRAL SEVERANCE + SPECIFICATION GATE PENDING`

Planning reconciliation baseline: `main@8af81c925a6d6d725e1663de516fc20b393ec207`.

PR #72 merged the bounded server-side Noetic/familiar/gaze/sanctuary substrate at `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`. PR #77 merged the bounded server-authored Borrowed Sight BEGIN/END presentation channel and physical-client camera adapter at `4053c060bb7e4c3f57ca06f49295868277a6eb57` on top of that canonical substrate.

This does **not** promote Stage 07.07 as a completed domain. Astral Severance still lacks its canonical astral avatar/viewpoint implementation, the complete per-spell specification gate remains open, and real-client Borrowed Sight acceptance has not been executed. Stage 08 must therefore not treat 07.07 as canonical balance input yet.

The detailed per-spell completeness matrix is `07-familiars-divination-specification-gate.md`.

## 1. Implemented server substrate

The merged runtime provides:

- bounded Noetic observation sessions;
- loaded-only same-dimension target resolution with no force-loading;
- whitelisted `NoeticPerceptionSnapshot` output instead of arbitrary NBT/capability/inventory exposure;
- familiar ownership through bounded explicit providers (`OWNED`, `NOT_OWNED`, `UNSUPPORTED`);
- verified Ars familiar ownership adapter;
- server-side observation privacy/admission policy;
- Gaze of Stillness / Nullifying Gaze runtime and safety ceilings;
- Pact Sanctuary bounded aura/eligibility/target-change enforcement;
- expiry/logout/death/server-stop cleanup, including Soul Anchor-compatible final-death settlement.

These are reusable prerequisites, not proof that every approved spell is invocable end-to-end.

`NoeticSafetyCeilings` defines absolute implementation ceilings. In particular, the generic observation layer currently caps maximum range at 128 blocks and maximum duration at 600 ticks, and the class explicitly states Stage 08 may tune below these values. They are **not** final Astral Severance, Namescry, Borrowed Sight or Occult Appraisal balance values.

## 2. Borrowed Sight — production code path implemented

Canonical design requires channeling the viewpoint of an owned familiar or explicitly consenting bonded target, with range/channel cost and return on interruption/unload.

PR #77 preserves the existing server-owned admission/ownership/session authority and adds only presentation derived from those canonical sessions:

- `NoeticObservationRuntime.activeSessions()` exposes immutable bounded value snapshots for projection; it does not create a second session authority;
- `NoeticViewSyncPlanner` projects only `BORROWED_SIGHT`; `ASTRAL_SEVERANCE`, `NAMESCRY` and `OCCULT_APPRAISAL` cannot enter this camera channel;
- `NoeticViewTransitionTracker` is bounded by the canonical active-session ceiling and emits idempotent BEGIN/END transitions only when desired presentation changes;
- `MinecraftNoeticRuntime` resolves only the transition viewer and that viewer's already-loaded `ServerLevel` target by UUID, without global-player iteration or chunk forcing;
- `MinecraftNoeticObservationRuntime.tick()` revalidates the same canonical `NoeticObservationPolicy` used at admission for every bounded active session before presentation sync; target unload keeps the existing `TARGET_UNAVAILABLE` lifecycle reason, while loss of range/dimension/ownership/privacy authorization closes the server-owned session as `AUTHORIZATION_REVOKED`;
- `NoeticViewNetworkBridge` registers a play-to-client payload and sends only to the authoritative viewer when the channel is present;
- `BorrowedSightClientController`, loaded only from the `Dist.CLIENT` entrypoint, resolves only the server-authored runtime entity id from the already-loaded client level, moves only the physical camera, and restores it to the local player's body on END or target loss;
- the client adapter creates no client-to-server gameplay packet path and cannot choose target, admission, duration, ownership or privacy state.

NeoForge 1.21–1.21.1 documentation confirms payload handlers registered without `PayloadRegistrar#executesOn(HandlerThread.NETWORK)` execute on the main thread by default. PR #77 does not switch handler thread.

### 2.1 Borrowed Sight evidence boundary

TDD for the continuous-authorization regression was executed after PR #77 had been reconciled with `main@f9c3854bc7e5b2f1bd051434080f13ae3c7d5e5d` through synchronization PR #95:

- RED head `5eec2e7818dae68c75fcccc7e80600e7c43a290d`, Black Arcana CI #2005 / `34185866007`: **571 tests, exactly one failure**, `activeObservationTickRevalidatesCanonicalAuthorizationPolicy()`, proving active-session policy revalidation was absent;
- GREEN code head `45f970edd10e20d41315cd1471471fadbef731fd`, Black Arcana CI #2010 / `34186494393`: GREEN in JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke;
- canonical runtime merge: PR #77 / `4053c060bb7e4c3f57ca06f49295868277a6eb57`.

Earlier Borrowed Sight transport/client checkpoints remain useful TDD history, including `d221408400ecec4a4430df510823cfc6efc4be41` / CI #1994, but they are not the final evidence after the authorization fix and merge.

Automated evidence proves compilation, deterministic server/domain contracts and dedicated-server safety for the implemented code path. It does **not** prove actual first-person camera feel, rendering compatibility, input behavior or restoration in the user's full physical-client modpack. Those remain direct real-client validation work under D031.

## 3. Astral Severance — NOT IMPLEMENTED end-to-end

Canonical candidate design requires a controllable non-combat viewpoint/avatar while the physical body remains vulnerable, with hard range, timeout/interruption return, no unauthorized projection interaction, and logout/death restoration.

The current server observation API accepts an already-loaded `LivingEntity` target and owns session/snapshot state only. Borrowed Sight's camera channel deliberately refuses `ASTRAL_SEVERANCE`. Reusing an arbitrary observed entity as the astral body would violate the required identity, authority and interaction model.

A future Astral Severance implementation must therefore define and implement a canonical bounded astral viewpoint/avatar lifecycle before any client camera/input path is enabled for that observation kind. Until then it remains fail-closed.

## 4. Astral Severance lifecycle plan

Everything in this section is `PLANNED / NOT IMPLEMENTED` unless explicitly identified as an existing reused contract.

### 4.1 Authority model

Black Arcana server runtime must own:

- whether the projection can start;
- the projection/session identity;
- the authoritative physical-body identity;
- the authoritative astral viewpoint/avatar identity if a distinct runtime representation is used;
- allowed dimension and loaded-region boundary;
- range and duration admission;
- interruption and termination causes;
- whether any requested movement is accepted;
- restoration/cleanup;
- resource/cooldown settlement through the canonical casting/channel pipeline.

The client may own only presentation and bounded intent for an already-authorized projection. It must never be able to declare itself projected, choose an arbitrary astral position, extend duration, bypass range, suppress interruption or select another entity as its astral body.

### 4.2 Conceptual lifecycle states

The implementation may use different names, but the design must preserve these conceptual transitions:

1. **inactive** — no astral projection exists;
2. **admission pending/validated** — the normal canonical cast/channel pipeline validates identity, progression, resource, cooldown, hazard and projection preconditions;
3. **projected** — server owns one bounded projection tied to one physical body;
4. **terminating** — a terminal condition has been accepted and further projection intent is rejected;
5. **restored/closed** — camera/input presentation returns to the body and all ephemeral projection state is gone.

This is a planning state model, not a claim that a production enum/class already exists.

Exactly one active Astral Severance projection per viewer/caster should be permitted unless a later reviewed design proves a safe reason for more. Repeated activation must not create stacked viewpoints, duplicate avatars, extra resource settlement or replayable session handles.

### 4.3 Physical body contract

The physical player entity remains the real gameplay body throughout projection.

Planned invariants:

- health, death, effects, hazards, inventory, equipment, progression and world ownership remain attached to the physical body;
- projection does not make the body invulnerable, untargetable, unloaded or replaced;
- body damage is an interruption condition per the approved candidate specification;
- body death terminates the projection before/with normal death settlement and cannot be hidden by camera state;
- Soul Anchor or other canonical death-prevention semantics remain owned by their existing pipeline; Astral Severance must not create a parallel death path;
- ordinary server/player position authority remains the body position; an astral viewpoint is not a silent teleport of the physical body.

### 4.4 Astral identity contract

The astral representation must have its own bounded, server-authored identity if implementation requires a runtime avatar/entity/anchor.

It must **not** be implemented by borrowing identity from an arbitrary observed `LivingEntity`.

Default planning rule:

- astral representation is non-combat and non-owning;
- it grants no inventory, equipment, container, loot, damage-credit, projectile, proc, pickup or entity-ownership identity;
- it cannot be persisted as an ordinary player clone;
- it cannot become a second caster or second root-cast authority;
- it cannot receive hidden target data beyond an explicitly approved perception contract.

The concrete representation type is intentionally not invented in this plan. Runtime implementation must choose a NeoForge/Minecraft-safe representation after code/API review and test it directly.

### 4.5 Movement and input contract

Astral control may require a future client→server movement-intent seam, but that seam does not exist merely because Borrowed Sight has a camera payload.

If introduced later:

- client sends bounded movement/look **intent**, never authoritative coordinates or settlement;
- server validates the projection/session identity before applying intent;
- server clamps movement to the approved movement model and hard range from the physical body/approved origin;
- wrong-session, stale, replayed, out-of-order or post-termination intents fail closed;
- the implementation must rate-limit/bound input and avoid per-intent world scans;
- no movement intent may force-load a chunk;
- no client prediction may become server gameplay authority;
- physical-player movement/input must not be accidentally applied to the body while the projection is intended to control only the astral viewpoint, except for explicit cancellation/return controls.

Exact packet shape, sequence field and movement rate are intentionally not frozen here because no implementation/API evidence has yet justified them.

### 4.6 Loaded-only spatial boundary

Astral Severance inherits the existing Noetic principle of bounded loaded-only observation.

Planned rules:

- same-dimension by default;
- never create chunk tickets or force-load destination/adjacent chunks;
- entering an unavailable/unloaded region terminates or refuses the movement rather than loading it;
- range is server-calculated against the canonical physical-body/approved-origin position;
- existing `NoeticSafetyCeilings.MAX_RANGE_BLOCKS` is an absolute ceiling, not the final spell range;
- existing `MAX_DURATION_TICKS` is an absolute ceiling, not the final spell duration;
- Stage 08 may tune below those ceilings only after the rest of the specification gate is closed.

### 4.7 Interaction boundary

Astral Severance is non-combat by default.

Without a separate approved contract, projection must not:

- attack or damage entities;
- cast another spell from the astral position;
- create projectile/kill/proc attribution;
- use, break or place blocks;
- open or mutate containers;
- pick up/drop/move items;
- interact with block entities;
- mount/possess entities;
- bypass doors, protection, claims or server permissions to perform a remote action;
- expose arbitrary inventory, capability, attachment, NBT or hidden-player state.

If a future design wants any projection interaction, that capability must be specified independently with target/protection/privacy/WorldEffectPolicy authority and must still terminate in canonical server pipelines. It is not implicitly authorized by this plan.

### 4.8 Privacy and player policy

Astral camera freedom must not become a generic player-surveillance bypass.

Planned rules:

- projection does not weaken `NoeticObservationPolicy` for explicit player-targeted observation;
- any remote player metadata still requires the appropriate observation/privacy contract;
- server-hidden or provider-hidden player state remains hidden;
- the projection cannot use unloaded-chunk traversal to locate players;
- PvP servers may restrict/disable or tune the projection through the eventual bounded config surface, but exact defaults are Stage 08 work.

### 4.9 Termination triggers

The authoritative server projection must terminate safely on at least:

- explicit cancel/return;
- channel end where applicable;
- hard duration expiry;
- hard range violation;
- body damage, per candidate specification;
- body death/final death settlement;
- logout/disconnect;
- server stop;
- dimension change;
- projection representation loss/unload if one exists;
- required chunk becoming unavailable;
- authorization/session invalidation;
- invalid/stale/replayed session state;
- provider/resource/channel failure where the eventual cost contract requires continued upkeep.

The exact close-reason enum is implementation work; the required behavioral causes above are the plan contract.

### 4.10 Restoration and recovery

The safest planned recovery rule is **fail closed to the physical body**.

Unless a later persistence design explicitly proves safe resumability:

- active astral projection is ephemeral and must not resume automatically after logout/reconnect or server restart;
- the server does not restore a stale remote projection position as player location;
- the client camera/input adapter returns to the physical body when an authoritative END/close is received or when its server-authored projection representation disappears;
- reconnect/session reset clears stale projection presentation before accepting a new BEGIN;
- server restart cleanup leaves the physical body's ordinary persisted state authoritative;
- no duplicate astral representation may survive cleanup.

This section defines the planned recovery contract; it does not claim that Astral Severance persistence code exists today.

### 4.11 Resource, cooldown and progression boundary

No exact Astral Severance cost/cooldown/scaling value is frozen in Stage 07.

Current supported design says only:

- cost class: channel/resource drain;
- progression class: T3;
- hard implementation safety ceilings exist above final balance values.

Before implementation/promotion:

- resource authority must be explicitly selected without creating a second mana system;
- if an external provider owns the resource, exact provider transaction/query support must be verified;
- cooldown identity/group must be explicit and server-owned;
- scaling equation or explicit `NO SCALING` decision must be written;
- final RPG Skill Tree gate must use a real contract and must not transfer projection runtime authority to RPG Skill Tree;
- eventual client presentation follows Stage 05 `07-presentation-data-contracts.md`, not client recomputation.

These remain specification blockers, not permission for Stage 07 to invent Stage 08 numbers.

### 4.12 WorldEffectPolicy relationship

The default Astral Severance plan performs no terrain mutation, so it should not manufacture a world-mutation path merely to satisfy an abstraction.

If future approved projection interaction mutates world state, it must use the canonical Stage 04 `WorldEffectPolicy`/protection/budget path applicable to that operation. Camera/viewpoint motion itself is not permission for block mutation.

### 4.13 Performance budgets

Astral Severance must remain bounded by construction:

- no global entity/player/chunk scans;
- no force-loading;
- no per-tick full-state network snapshots;
- movement/input handling bounded to active authorized projections;
- lifecycle lookup indexed by server-owned session/viewer identity;
- interaction remains disabled by default, avoiding remote raycast/action spam;
- camera BEGIN/END remains event/lifecycle driven;
- any required server position update is bounded and rate-controlled rather than broadcast as an unbounded stream;
- cleanup is proportional to bounded active projection state.

No numeric networking rate is frozen without implementation evidence.

## 5. Astral Severance test plan

### 5.1 Pure/state tests

Required deterministic coverage should include:

- inactive → admitted → projected → terminating → closed transition legality;
- duplicate activation denied/idempotent;
- stale/replayed session intent rejected;
- post-close movement/input ignored;
- range and duration safety-ceiling enforcement;
- exact-once cleanup semantics;
- no arbitrary observed-entity identity accepted as the astral body;
- restoration target remains the physical body.

### 5.2 Server/runtime tests

Required tests should include:

- activation still passes through the canonical cast/channel admission path;
- body damage terminates projection;
- death terminates projection without bypassing Soul Anchor/final-death authority;
- logout terminates and cleans projection;
- dimension change terminates/fails closed;
- server stop cleans all active projections within the global bound;
- unloaded/unknown spatial state never force-loads;
- crossing hard range terminates/refuses movement;
- no interaction path can attack/cast/use/break/place/open/pick up from the projection by default;
- wrong player/session cannot control another projection;
- no duplicate root-cast/damage/proc attribution exists;
- provider absence/failure remains fail-closed where a future resource/gate adapter is optional.

### 5.3 Network/client tests

If a movement/view payload is later implemented:

- malformed/bounded codec cases;
- stale and wrong-session rejection;
- server wins over client position/prediction;
- END restores camera/control idempotently;
- target/avatar loss restores camera safely;
- reconnect clears stale client projection state;
- physical-client-only classes remain absent from dedicated-server classloading.

### 5.4 Real-client acceptance

Astral Severance cannot be declared client-validated from automated CI alone.

The final campaign must directly observe, on an exact QA build in the real modpack:

- start transition and visual clarity;
- camera/control feel;
- body vulnerability during projection;
- body-damage interruption;
- range/timeout return;
- logout/reconnect restoration;
- death/Soul Anchor interaction;
- F1/GUI behavior;
- first-person/camera mod coexistence;
- Epic Fight/combat-camera coexistence where applicable;
- no stuck camera after failure/END;
- no remote interaction exploit;
- no visible duplicate player/avatar state inconsistent with the chosen implementation.

Until that evidence exists, client acceptance remains deferred under D031.

## 6. Other 07.07 spells — specification status

The current approved/preparatory family contains:

- Astral Severance;
- Namescry;
- Gaze of Stillness;
- Nullifying Gaze;
- Occult Appraisal;
- Borrowed Sight;
- Pact Sanctuary.

The canonical completeness audit is `07-familiars-divination-specification-gate.md`.

Key conclusion: current runtime implementation does not remove the need to specify missing balance/authority fields. In particular, exact resource cost, cooldown semantics, scaling equation, final progression gate, config surface and per-spell provenance are not frozen across the family.

## 7. Familiar-provider boundary

Familiar ownership remains provider-native first.

Current rules:

- ownership must be proven by an explicit bounded provider/adapter;
- `OWNED`, `NOT_OWNED` and `UNSUPPORTED` remain distinct outcomes;
- unknown/provider-error state fails closed;
- physical mod presence or thematic similarity does not establish ownership;
- the verified Ars familiar adapter does not automatically authorize Alshanex's Familiars, Ars Elemental familiars or any other companion system;
- each additional provider requires exact-version/API/source verification before its entities can satisfy Black Arcana ownership gates;
- RPG Skill Tree may gate progression/mastery through a real contract but does not own familiar identity or Noetic runtime.

## 8. Specification gate

`plans/07-spell-domains/README.md` requires every spell to define fantasy, host integration, invocation, target rules, resource cost, cooldown, scaling equation, progression gate, world-effect mode, boss/PvP behavior, config surface, tests and provenance.

The candidate entries in `docs/design/candidate-specifications.md` intentionally do not freeze exact numeric balance. They are preparatory design input, not Stage 08-ready specifications.

Therefore:

- no safety ceiling becomes a balance default;
- no qualitative `mana/channel`, `upkeep`, `cooldown` or `range` phrase becomes an invented number;
- no provider resource/host is assumed without a verified transaction/presentation seam;
- every spell needs an explicit scaling equation or explicit `NO SCALING` decision;
- every cooldown needs canonical identity/group semantics if present;
- progression must be frozen through the actual RPG Skill Tree contract only when that boundary is real;
- provenance must be linked per final spell/specification;
- final config surfaces must be bounded and validated.

Until `07-familiars-divination-specification-gate.md` is closed and Astral Severance mechanics are implemented/reviewed, 07.07 remains `IN PROGRESS` and Stage 08 remains blocked from consuming this domain as canonical balance input.

## 9. Existing automated evidence — merged server substrate

- final PR #72 runtime head: `673aff57e15ec29a6fc0d6a94f0034726b99a4c1`;
- Black Arcana CI #1562 / `34069825298`: GREEN;
- 103/103 Foundation GameTests and dedicated-server smoke;
- runtime merge: `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`;
- exact-SHA post-merge CI #1563 / `34070253755`: GREEN;
- artifact `black-arcana-5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, ID `10000268004`, SHA-256 `35c8436ab3cbd2f75e8cc6f7ae5554edb7a330205f5166265f96979b6fa65b16`;
- Borrowed Sight final GREEN code head: `45f970edd10e20d41315cd1471471fadbef731fd`, CI #2010 / `34186494393`;
- Borrowed Sight canonical merge: PR #77 / `4053c060bb7e4c3f57ca06f49295868277a6eb57`.

This evidence remains authoritative for the code it actually exercises; it is not reclassified as real-client acceptance or as proof that the specification gate is closed.

## 10. 07.07 completion rule

07.07 may become canonical only when all of the following are true:

- existing Noetic/familiar/gaze/sanctuary substrate remains intact;
- Borrowed Sight production path remains server-authoritative and real-client acceptance is correctly recorded/deferred under D031;
- Astral Severance has a reviewed bounded server-authoritative avatar/viewpoint lifecycle and implemented canonical path;
- Astral Severance does not create client-authoritative movement, duplicate caster identity, force-loading or remote interaction bypass;
- all seven candidate spells satisfy the per-spell specification gate;
- exact provider bridges used by any final spell are verified against the installed version/API/source;
- required automated tests are green on the reconciled exact HEAD;
- any mandatory real-client rows are directly observed or explicitly deferred only where D031 permits;
- `plans/STATUS.md` and this directory README match the real `main` state.

Creating this plan does not itself satisfy those gates and does not promote Stage 07 or Stage 08.
