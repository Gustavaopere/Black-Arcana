# 07.07 — Familiars & Divination

## State

`IN PROGRESS — SERVER SUBSTRATE + BORROWED SIGHT + ASTRAL LIFECYCLE CANONICAL / ASTRAL CONTROL PARTIAL / SPECIFICATION GATE OPEN`

Current canonical baseline: `main@29454a7dd604ba0ea0200724d53bd9526b09cb10` after PR #235.

PR #72 merged the bounded server-side Noetic/familiar/gaze/sanctuary substrate at `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`. PR #77 merged the bounded server-authored Borrowed Sight BEGIN/END presentation channel and physical-client camera adapter at `4053c060bb7e4c3f57ca06f49295868277a6eb57`. PR #138 merged the dedicated bounded server-owned Astral Severance projection/session lifecycle at `3469b454de2b65d0c15e89e7d689fe760dd30994`. PR #235 merged the bounded Astral projection representation, server-owned logical pose/movement substrate and C2S MOVE/RETURN control transport at `29454a7dd604ba0ea0200724d53bd9526b09cb10`.

That control tranche does **not** promote Stage 07.07 as complete: Astral client camera/input redirection, canonical cast/channel/upkeep wiring, a production MOVE control-limit authority, the complete per-spell specification gate and real-client acceptance remain open. Stage 08 must not consume 07.07 as canonical balance input yet.

The detailed per-spell completeness matrix is `07-familiars-divination-specification-gate.md`. The implementation checkpoint is `07-astral-severance-runtime-checkpoint.md`.

## 1. Implemented server substrate

The canonical runtime provides:

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

`NoeticSafetyCeilings` defines absolute implementation ceilings. In particular, the generic observation layer caps maximum range at 128 blocks and maximum duration at 600 ticks, and the class explicitly states Stage 08 may tune below those ceilings. They are **not** final Astral Severance, Namescry, Borrowed Sight or Occult Appraisal balance values.

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

## 3. Astral Severance — partial runtime/control implementation

Canonical candidate design requires a controllable non-combat viewpoint/avatar while the physical body remains vulnerable, with hard range, timeout/interruption return, no unauthorized projection interaction, and logout/death restoration.

Borrowed Sight's generic observed-entity camera channel still deliberately refuses `ASTRAL_SEVERANCE`; an arbitrary observed `LivingEntity` cannot stand in for Astral identity.

### 3.1 Canonical lifecycle already merged

PR #138 established the dedicated server-owned lifecycle:

- one bounded server-generated projection identity per physical caster;
- generic observed-entity `ASTRAL_SEVERANCE` admission fails closed;
- hard duration/range/global active-session ceilings;
- exact-id return and fail-closed foreign/stale identity handling;
- positive post-mitigation body damage termination;
- dimension-change termination;
- logout cleanup;
- Soul Anchor-compatible final-death settlement;
- expiry and server-stop cleanup;
- Astral state included in aggregate 07.07 cleanup/accounting.

The physical player remains the real gameplay body. Projection never becomes inventory/equipment/progression/health/death authority and never silently teleports the physical body.

### 3.2 Canonical control tranche

PR #235 adds:

- `AstralProjectionEntity`, a dedicated non-owning server-side world representation using the server-authored projection UUID;
- server-owned logical `ProjectionPose` distinct from physical-player position;
- exact-session `ControlIntent` with positive monotonic sequence numbers;
- finite strafe/vertical/forward axes bounded to `[-1, 1]`;
- finite yaw/pitch deltas;
- server-selected `ControlLimits` that clamp step distance and look delta;
- range validation against the server-owned origin;
- loaded-only destination admission using `getChunkNow` rather than chunk acquisition/tickets;
- accepted logical pose mirrored to the projection representation only;
- representation loss revalidated from the bounded active Astral set and failing closed without waiting for MOVE input;
- dedicated C2S `AstralMoveIntentPayload` / `AstralReturnIntentPayload` and NeoForge packets;
- caster identity derived exclusively from `IPayloadContext.player()`;
- no caster UUID or authoritative world coordinates in client payloads;
- independent one-per-tick MOVE and RETURN ingress windows with bounded tracked-caster capacity and per-`MinecraftServer` histories;
- production RETURN wiring requiring an exact active projection and a sequence newer than the last processed MOVE sequence;
- Minecraft/NeoForge 1.21.1-compatible stream codecs plus codec round-trip tests.

### 3.3 Deliberate fail-closed MOVE boundary

MOVE transport is registered, decoded, validated and rate-limited, but production `BlackArcanaMod` deliberately does not install a MOVE gameplay handler yet.

`MinecraftNoeticRuntime.applyAuthorizedAstralControl(...)` requires server-selected `AstralSeveranceRuntime.ControlLimits`. The current specification/config authority does not freeze production values or a source for `maxStepBlocks` and `maxLookDeltaDegrees`. Test fixture numbers and `NoeticSafetyCeilings` must not become accidental Stage 08 balance defaults.

Therefore MOVE remains fail-closed at the transport-to-gameplay seam until a reviewed canonical server-side control-limit/config authority exists. RETURN can be wired now because it does not require inventing a missing balance value.

## 4. Astral Severance lifecycle and remaining implementation plan

Everything below remains normative. Where the current runtime now implements a planned boundary, the requirement remains an invariant rather than being deleted from the plan.

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

The current lifecycle/representation/control substrate satisfies the identity and server-position authority portions of this contract. Resource/cooldown/cast-channel authority remains outside this tranche.

The client may own only presentation and bounded intent for an already-authorized projection. It must never be able to declare itself projected, choose an arbitrary astral position, extend duration, bypass range, suppress interruption, select another entity as its astral body, or settle gameplay resources.

### 4.2 Conceptual lifecycle states

The implementation may use different names, but the design must preserve these conceptual transitions:

1. **inactive** — no astral projection exists;
2. **admission pending/validated** — the normal canonical cast/channel pipeline validates identity, progression, resource, cooldown, hazard and projection preconditions;
3. **projected** — server owns one bounded projection tied to one physical body;
4. **terminating** — a terminal condition has been accepted and further projection intent is rejected;
5. **restored/closed** — camera/input presentation returns to the body and all ephemeral projection state is gone.

This remains the lifecycle contract even though production code does not need to expose an enum with these exact names.

Exactly one active Astral Severance projection per viewer/caster is permitted by the current runtime. Repeated activation must not create stacked viewpoints, duplicate avatars, extra resource settlement or replayable session handles.

### 4.3 Physical body contract

The physical player entity remains the real gameplay body throughout projection.

Invariants:

- health, death, effects, hazards, inventory, equipment, progression and world ownership remain attached to the physical body;
- projection does not make the body invulnerable, untargetable, unloaded or replaced;
- body damage is an interruption condition per the approved candidate specification;
- body death terminates the projection before/with normal death settlement and cannot be hidden by camera state;
- Soul Anchor or other canonical death-prevention semantics remain owned by their existing pipeline; Astral Severance must not create a parallel death path;
- ordinary server/player position authority remains the body position; an astral viewpoint is not a silent teleport of the physical body.

### 4.4 Astral identity contract

The astral representation has its own bounded, server-authored identity and must **not** borrow identity from an arbitrary observed `LivingEntity`.

Normative rules:

- astral representation is non-combat and non-owning;
- it grants no inventory, equipment, container, loot, damage-credit, projectile, proc, pickup or entity-ownership identity;
- it cannot be persisted as an ordinary player clone;
- it cannot become a second caster or second root-cast authority;
- it cannot receive hidden target data beyond an explicitly approved perception contract.

The current `AstralProjectionEntity` is the representation selected for this runtime checkpoint; future changes must preserve all rules above.

### 4.5 Movement and input contract

The implemented client→server seam carries bounded movement/look **intent**, never authoritative coordinates or settlement.

Normative rules:

- server validates the projection/session identity before applying intent;
- authenticated caster identity comes from network context, never the payload;
- server clamps movement to the approved movement model and hard range from the physical body/approved origin;
- wrong-session, stale, replayed, out-of-order or post-termination intents fail closed;
- input handling is rate-limited/bounded and avoids per-intent world scans;
- no movement intent may force-load a chunk;
- no client prediction may become server gameplay authority;
- physical-player movement/input must not be accidentally applied to the body while the projection is intended to control only the astral viewpoint, except for explicit cancellation/return controls.

The packet identity/sequence/axis shape is now implementation-backed. The production source/value contract for `ControlLimits` remains intentionally unfrozen, so MOVE gameplay execution remains fail-closed.

### 4.6 Loaded-only spatial boundary

Astral Severance inherits the existing Noetic principle of bounded loaded-only observation.

Rules:

- same-dimension by default;
- never create chunk tickets or force-load destination/adjacent chunks;
- entering an unavailable/unloaded region terminates or refuses movement rather than loading it;
- range is server-calculated against the canonical physical-body/approved-origin position;
- existing `NoeticSafetyCeilings.MAX_RANGE_BLOCKS` is an absolute ceiling, not the final spell range;
- existing `MAX_DURATION_TICKS` is an absolute ceiling, not the final spell duration;
- Stage 08 may tune below those ceilings only after the rest of the specification gate is closed.

The current movement substrate chooses refusal for unavailable/out-of-range movement while consuming a valid sequence so a refused packet cannot later be replayed into validity. A different terminal policy would require explicit review.

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

Rules:

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
- hard range violation where the final gameplay policy chooses terminal return;
- body damage, per candidate specification;
- body death/final death settlement;
- logout/disconnect;
- server stop;
- dimension change;
- projection representation loss/unload;
- required chunk becoming unavailable where the final gameplay policy chooses terminal return;
- authorization/session invalidation;
- invalid/stale/replayed session state where the final policy requires termination rather than refusal;
- provider/resource/channel failure where the eventual cost contract requires continued upkeep.

Current movement admission refuses out-of-range or unavailable destinations rather than terminating the session, while representation loss terminates. Final range/chunk terminal-vs-refusal policy remains subject to explicit gameplay review and must not be inferred from safety ceilings.

### 4.10 Restoration and recovery

The safest recovery rule is **fail closed to the physical body**.

Unless a later persistence design explicitly proves safe resumability:

- active astral projection is ephemeral and must not resume automatically after logout/reconnect or server restart;
- the server does not restore a stale remote projection position as player location;
- the client camera/input adapter returns to the physical body when an authoritative END/close is received or when its server-authored projection representation disappears;
- reconnect/session reset clears stale projection presentation before accepting a new BEGIN;
- server restart cleanup leaves the physical body's ordinary persisted state authoritative;
- no duplicate astral representation may survive cleanup.

Server-side session/representation cleanup is implemented; client camera/input restoration remains future work.

### 4.11 Resource, cooldown and progression boundary

No exact Astral Severance cost/cooldown/scaling value is frozen in Stage 07.

Current supported design says only:

- cost class: channel/resource drain;
- progression class: T3;
- hard implementation safety ceilings exist above final balance values.

Before promotion:

- resource authority must be explicitly selected without creating a second mana system;
- if an external provider owns the resource, exact provider transaction/query support must be verified;
- cooldown identity/group must be explicit and server-owned;
- scaling equation or explicit `NO SCALING` decision must be written;
- final RPG Skill Tree gate must use a real contract and must not transfer projection runtime authority to RPG Skill Tree;
- production MOVE `ControlLimits` must come from a reviewed bounded server-side authority, not safety ceilings/test fixtures;
- eventual client presentation follows Stage 05 `07-presentation-data-contracts.md`, not client recomputation.

These remain specification blockers, not permission for Stage 07 to invent Stage 08 numbers.

### 4.12 WorldEffectPolicy relationship

Astral Severance currently performs no terrain mutation, so it must not manufacture a world-mutation path merely to satisfy an abstraction.

If future approved projection interaction mutates world state, it must use the canonical Stage 04 `WorldEffectPolicy`/protection/budget path applicable to that operation. Camera/viewpoint motion itself is not permission for block mutation.

### 4.13 Performance budgets

Astral Severance must remain bounded by construction:

- no global entity/player/chunk scans;
- no force-loading;
- no per-tick full-state network snapshots;
- movement/input handling bounded to active authorized projections;
- lifecycle lookup indexed by server-owned session/viewer identity;
- representation-loss revalidation iterates only the hard-bounded active Astral set;
- ingress histories are bounded per server/caster and do not share tick history across server instances;
- interaction remains disabled by default, avoiding remote raycast/action spam;
- camera BEGIN/END remains event/lifecycle driven when client presentation is implemented;
- any required server position update is bounded and rate-controlled rather than broadcast as an unbounded stream;
- cleanup is proportional to bounded active projection state.

The implemented transport uses one MOVE and one RETURN admission window per authenticated caster per server tick. These are protocol abuse bounds, not Stage 08 spell balance values.

## 5. Astral Severance test plan and current coverage

The original required test campaign remains normative. Implemented rows are not deleted merely because coverage now exists.

### 5.1 Pure/state tests

Required deterministic coverage includes:

- inactive → admitted → projected → terminating → closed transition legality;
- duplicate activation denied/idempotent;
- stale/replayed session intent rejected;
- post-close movement/input ignored;
- range and duration safety-ceiling enforcement;
- exact-once cleanup semantics;
- no arbitrary observed-entity identity accepted as the astral body;
- restoration target remains the physical body.

Current unit/runtime coverage exercises server-owned identity, duplicate/invalid lifecycle behavior, monotonic control sequences, wrong-session/stale/replay rejection, range/loaded-only movement and cleanup. Final canonical cast/upkeep/config transitions still need exact tests when those contracts are frozen.

### 5.2 Server/runtime tests

Required tests include:

- activation still passes through the canonical cast/channel admission path;
- body damage terminates projection;
- death terminates projection without bypassing Soul Anchor/final-death authority;
- logout terminates and cleans projection;
- dimension change terminates/fails closed;
- server stop cleans all active projections within the global bound;
- unloaded/unknown spatial state never force-loads;
- crossing hard range terminates/refuses movement according to the reviewed gameplay policy;
- projection representation loss terminates without requiring new client input;
- no interaction path can attack/cast/use/break/place/open/pick up from the projection by default;
- wrong player/session cannot control another projection;
- no duplicate root-cast/damage/proc attribution exists;
- provider absence/failure remains fail-closed where a future resource/gate adapter is optional.

Current runtime/GameTests cover dedicated representation materialization, server-owned movement application, preservation of the physical body and representation-loss cleanup, in addition to lifecycle coverage from the merged Astral tranche. Canonical cast/upkeep wiring, finalized control-limit policy and complete interaction-exploit coverage remain open.

### 5.3 Network/client tests

Now that movement/return payloads exist, required coverage includes:

- malformed/bounded codec cases;
- stale and wrong-session rejection;
- server wins over client position/prediction;
- authenticated caster identity comes from server connection context rather than payload;
- END restores camera/control idempotently;
- target/avatar loss restores camera safely;
- reconnect clears stale client projection state;
- physical-client-only classes remain absent from dedicated-server classloading.

Implemented network tests cover payload field shape, protocol/sequence/finite-axis validation, 1.21.1-compatible MOVE/RETURN codec round trips with no trailing bytes, and dedicated-server classloading safety through the CI smoke gate. Client camera/input restoration and prediction behavior remain open because that client path is not implemented yet.

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

- no safety ceiling or test fixture becomes a balance default;
- no qualitative `mana/channel`, `upkeep`, `cooldown` or `range` phrase becomes an invented number;
- no provider resource/host is assumed without a verified transaction/presentation seam;
- every spell needs an explicit scaling equation or explicit `NO SCALING` decision;
- every cooldown needs canonical identity/group semantics if present;
- progression must be frozen through the actual RPG Skill Tree contract only when that boundary is real;
- provenance must be linked per final spell/specification;
- final config surfaces must be bounded and validated.

Until `07-familiars-divination-specification-gate.md` is closed and Astral Severance is connected through its canonical cast/channel and client-control path, 07.07 remains `IN PROGRESS` and Stage 08 remains blocked from consuming this domain as canonical balance input.

## 9. Automated evidence

Canonical merged substrate evidence remains authoritative for the code it actually exercises:

- final PR #72 runtime head: `673aff57e15ec29a6fc0d6a94f0034726b99a4c1`;
- Black Arcana CI #1562 / `34069825298`: GREEN;
- 103/103 Foundation GameTests and dedicated-server smoke;
- runtime merge: `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`;
- exact-SHA post-merge CI #1563 / `34070253755`: GREEN;
- artifact `black-arcana-5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, ID `10000268004`, SHA-256 `35c8436ab3cbd2f75e8cc6f7ae5554edb7a330205f5166265f96979b6fa65b16`;
- Borrowed Sight final GREEN code head: `45f970edd10e20d41315cd1471471fadbef731fd`, CI #2010 / `34186494393`;
- Borrowed Sight canonical merge: PR #77 / `4053c060bb7e4c3f57ca06f49295868277a6eb57`;
- Astral lifecycle canonical merge: PR #138 / `3469b454de2b65d0c15e89e7d689fe760dd30994`;
- Astral control final branch head `8b9fd3ce0bb2347dc672b85db058eeb891d850d9` passed push workflow `34778875762` and PR workflow `34778877787`;
- Astral control canonical merge: PR #235 / `29454a7dd604ba0ea0200724d53bd9526b09cb10`;
- exact-SHA post-merge workflow `34779849669` passed JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke and canonical QA artifact publication;
- canonical artifact `black-arcana-29454a7dd604ba0ea0200724d53bd9526b09cb10`, ID `10325066285`, SHA-256 `8c5d47037661e2b697196e15ef0ca272dce5e4d496b11aef99edc323b54e69b4`.

This evidence is not reclassified as real-client acceptance or as proof that the specification gate is closed.

## 10. 07.07 completion rule

07.07 may become canonical only when all of the following are true:

- existing Noetic/familiar/gaze/sanctuary substrate remains intact;
- Borrowed Sight production path remains server-authoritative and real-client acceptance is correctly recorded/deferred under D031;
- Astral Severance has a reviewed bounded server-authoritative avatar/viewpoint lifecycle and control path;
- Astral Severance does not create client-authoritative movement, duplicate caster identity, force-loading or remote interaction bypass;
- production MOVE uses a reviewed bounded server-side `ControlLimits` authority rather than safety ceilings/test fixtures;
- Astral activation/upkeep terminates in the canonical Stage 02 cast/channel transaction rather than a parallel authority path;
- client camera/input is implemented with fail-closed restoration to the physical body;
- all seven candidate spells satisfy the per-spell specification gate;
- exact provider bridges used by any final spell are verified against the installed version/API/source;
- required automated tests are green on the reconciled exact HEAD;
- any mandatory real-client rows are directly observed or explicitly deferred only where D031 permits;
- `plans/STATUS.md` and this directory README match the real `main` state.

Creating or updating this plan does not itself satisfy those gates and does not promote Stage 07 or Stage 08.