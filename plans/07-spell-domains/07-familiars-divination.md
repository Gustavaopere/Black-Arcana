# 07.07 — Familiars & Divination

## State

`IN PROGRESS — SERVER SUBSTRATE + BORROWED SIGHT + ASTRAL LIFECYCLE CANONICAL / ASTRAL CONTROL PARTIAL / SPECIFICATION GATE OPEN`

PR #72 merged the bounded server-side Noetic/familiar/gaze/sanctuary substrate at `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`. PR #77 merged the bounded server-authored Borrowed Sight BEGIN/END presentation channel and physical-client camera adapter at `4053c060bb7e4c3f57ca06f49295868277a6eb57`. PR #138 merged the dedicated bounded server-owned Astral Severance projection/session lifecycle at `3469b454de2b65d0c15e89e7d689fe760dd30994`.

The current `feat/stage07-astral-severance-control` tranche extends that Astral lifecycle with a dedicated projection representation, server-owned logical pose/movement substrate and bounded C2S MOVE/RETURN transport. It does **not** promote Stage 07.07 as complete: Astral client camera/input redirection, canonical cast/channel/upkeep wiring, a production MOVE control-limit authority, the complete per-spell specification gate and real-client acceptance remain open. Stage 08 must not consume 07.07 as canonical balance input yet.

The detailed completeness matrix is `07-familiars-divination-specification-gate.md`. The implementation checkpoint is `07-astral-severance-runtime-checkpoint.md`.

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

`NoeticSafetyCeilings` defines absolute implementation ceilings. In particular, generic observation maximum range is 128 blocks and maximum duration is 600 ticks. Those values are safety caps, not final Astral Severance, Namescry, Borrowed Sight or Occult Appraisal balance defaults.

## 2. Borrowed Sight — production code path implemented

Canonical design requires channeling the viewpoint of an owned familiar or explicitly consenting bonded target, with range/channel cost and return on interruption/unload.

PR #77 preserves the existing server-owned admission/ownership/session authority and adds presentation derived from those canonical sessions:

- `NoeticObservationRuntime.activeSessions()` exposes immutable bounded value snapshots; it does not create a second session authority;
- `NoeticViewSyncPlanner` projects only `BORROWED_SIGHT`; `ASTRAL_SEVERANCE`, `NAMESCRY` and `OCCULT_APPRAISAL` cannot enter that camera channel;
- `NoeticViewTransitionTracker` emits bounded idempotent BEGIN/END transitions;
- active sessions continuously revalidate the canonical observation policy;
- target unload or authorization loss closes server-owned state rather than creating client authority;
- `NoeticViewNetworkBridge` sends only server-authored presentation to the authoritative viewer;
- `BorrowedSightClientController` moves only the local physical camera and restores it on END/target loss;
- the client cannot choose target, admission, duration, ownership or privacy state.

Automated evidence proves compilation, deterministic server/domain contracts and dedicated-server safety. It does **not** prove actual camera feel, rendering compatibility, input behavior or restoration in the user's full physical-client modpack. Those remain direct real-client validation work under D031.

## 3. Astral Severance — partial runtime/control implementation

Canonical candidate design requires a controllable non-combat viewpoint/avatar while the physical body remains vulnerable, with hard range, timeout/interruption return, no unauthorized projection interaction and safe restoration.

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

### 3.2 Current control tranche

The current branch adds:

- `AstralProjectionEntity`, a dedicated non-owning server-side world representation using the server-authored projection UUID;
- server-owned logical `ProjectionPose` distinct from physical-player position;
- exact-session `ControlIntent` with positive monotonic sequence numbers;
- finite strafe/vertical/forward axes bounded to `[-1, 1]`;
- finite yaw/pitch deltas;
- server-selected `ControlLimits` that clamp step distance and look delta;
- range validation against the server-owned origin;
- loaded-only destination admission using `getChunkNow` rather than chunk acquisition/tickets;
- accepted logical pose mirrored to the projection representation only;
- representation loss failing closed and terminating the session;
- dedicated C2S `AstralMoveIntentPayload` / `AstralReturnIntentPayload` and NeoForge packets;
- caster identity derived exclusively from `IPayloadContext.player()`;
- no caster UUID or authoritative world coordinates in client payloads;
- separate one-per-tick MOVE and RETURN ingress limiters with bounded tracked-caster capacity;
- production RETURN wiring requiring an exact active projection and a sequence newer than the last processed MOVE sequence;
- Minecraft/NeoForge 1.21.1-compatible stream codecs plus codec round-trip tests.

### 3.3 Deliberate fail-closed MOVE boundary

MOVE transport is registered, decoded, validated and rate-limited, but production `BlackArcanaMod` deliberately does not install a MOVE gameplay handler yet.

`MinecraftNoeticRuntime.applyAuthorizedAstralControl(...)` requires server-selected `AstralSeveranceRuntime.ControlLimits`. The current specification/config authority does not freeze production values or a source for `maxStepBlocks` and `maxLookDeltaDegrees`. Test fixture numbers and `NoeticSafetyCeilings` must not become accidental Stage 08 balance defaults.

Therefore the correct current behavior is fail-closed MOVE execution until a reviewed canonical server-side control-limit/config authority exists. RETURN can be wired now because it does not require inventing a missing balance value.

## 4. Astral Severance authority and remaining implementation plan

### 4.1 Authority model

Black Arcana server runtime owns:

- whether a projection may start;
- projection/session identity;
- physical-body identity;
- astral representation identity and logical pose;
- allowed dimension and loaded-region boundary;
- range/duration admission;
- movement acceptance;
- interruption/termination;
- cleanup/restoration authority;
- eventual resource/cooldown settlement through the canonical cast/channel pipeline.

The client may own only presentation and bounded intent for an already-authorized projection. It must never declare itself projected, choose an authoritative position, extend duration, bypass range, suppress interruption, select another entity as its astral body or settle gameplay resources.

### 4.2 Lifecycle states

The conceptual lifecycle remains:

1. **inactive** — no projection exists;
2. **admission pending/validated** — canonical cast/channel pipeline validates identity, progression, resource, cooldown, hazard and projection preconditions;
3. **projected** — server owns one bounded projection tied to one physical body;
4. **terminating** — terminal condition accepted; further control is rejected;
5. **restored/closed** — client presentation returns to the body and ephemeral projection state is gone.

One active Astral Severance projection per caster is the current bounded invariant.

### 4.3 Physical body contract

- health, death, effects, hazards, inventory, equipment, progression and world ownership remain attached to the physical body;
- projection does not make the body invulnerable, untargetable, unloaded or replaced;
- body damage interrupts projection;
- final death terminates projection without bypassing Soul Anchor/death-prevention authority;
- ordinary player position remains the body position.

### 4.4 Astral identity contract

`AstralProjectionEntity` supplies a dedicated server-authored representation rather than borrowing identity from an arbitrary observed entity.

The representation is non-owning and must not gain inventory, equipment, container, loot, damage-credit, projectile, proc, pickup, root-cast or persistence authority. It cannot become a second player/caster clone.

### 4.5 Movement and input contract

The implemented C2S seam carries bounded movement/look intent only. Server rules remain:

- exact projection/session identity required;
- authenticated caster comes from connection context;
- monotonic sequence rejects stale/replayed/out-of-order intent;
- axes and look deltas are numerically bounded before domain application;
- server computes candidate pose;
- hard range and loaded-only destination checks are server-owned;
- no movement packet force-loads a chunk;
- client prediction cannot become gameplay authority;
- physical-player movement must not accidentally move the body when Astral input redirection is later enabled;
- explicit RETURN remains independently available under its own ingress cap.

The remaining unresolved item is the production source/value contract for `ControlLimits`, not the packet authority model.

### 4.6 Loaded-only spatial boundary

- same-dimension by default;
- never create chunk tickets or force-load destination/adjacent chunks;
- unavailable/unloaded destinations are refused rather than loaded;
- range is server-calculated from the canonical server-owned origin;
- `NoeticSafetyCeilings.MAX_RANGE_BLOCKS` and `MAX_DURATION_TICKS` remain absolute implementation ceilings, not final balance values.

### 4.7 Interaction boundary

Without a separate approved contract, projection must not:

- attack or damage entities;
- cast another spell from the astral position;
- create projectile/kill/proc attribution;
- use, break or place blocks;
- open or mutate containers;
- pick up/drop/move items;
- interact with block entities;
- mount/possess entities;
- bypass protection/claims/server permissions;
- expose arbitrary inventory, capability, attachment, NBT or hidden-player state.

Any future projection interaction must be specified independently and terminate in canonical server safety/protection pipelines.

### 4.8 Privacy and player policy

Astral camera freedom must not become a generic surveillance bypass. Existing Noetic privacy rules remain authoritative for explicit player-targeted data. Projection cannot use unloaded traversal to locate players, expose provider-hidden state or grant arbitrary remote metadata.

### 4.9 Termination triggers

Server projection must terminate safely on at least:

- explicit RETURN/cancel;
- channel end where applicable;
- duration expiry;
- body damage;
- body death/final-death settlement;
- logout/disconnect;
- server stop;
- dimension change;
- projection representation loss;
- authorization/session invalidation;
- eventual provider/resource/channel failure where upkeep requires it.

Rejected movement outside hard range/unavailable loaded space currently fails closed at movement admission; final gameplay policy may choose refusal versus terminal return only through an explicit reviewed contract.

### 4.10 Restoration and recovery

Fail closed to the physical body:

- projection is ephemeral and does not automatically resume after logout/reconnect/restart;
- server never restores remote projection position as player position;
- future client camera/input adapter must restore to the physical body on authoritative close or representation loss;
- reconnect/session reset must clear stale client projection presentation before accepting a new projection;
- no duplicate representation may survive cleanup.

### 4.11 Resource, cooldown and progression boundary

No exact Astral Severance resource cost, cooldown, scaling or final progression values are frozen here.

Current supported classes only:

- cost class: channel/resource drain;
- progression class: T3;
- hard safety ceilings above final balance values.

Before promotion:

- resource authority must be selected without creating a second mana system;
- external resource transaction support must be verified if used;
- cooldown identity/group must be explicit and server-owned;
- scaling equation or explicit `NO SCALING` decision must be written;
- final RPG Skill Tree gate must use the real progression boundary without transferring runtime authority;
- MOVE `ControlLimits` must come from a reviewed bounded server authority, not safety ceilings/test fixtures.

### 4.12 WorldEffectPolicy relationship

Current Astral Severance performs no terrain mutation and does not manufacture a world-mutation path. Any future approved world interaction must use the canonical Stage 04 protection/budget authority applicable to that operation.

### 4.13 Performance budgets

Astral Severance remains bounded by construction:

- no global entity/player/chunk scans;
- no force-loading;
- no per-tick full-state network snapshots;
- movement handling indexed by authenticated caster/exact active projection;
- ingress is bounded per caster/tick and tracked-caster capacity is bounded;
- interaction remains disabled by default;
- cleanup is proportional to bounded active projection state.

## 5. Astral Severance test plan and current evidence

### 5.1 Pure/state coverage

Implemented deterministic coverage includes server-owned identity, duplicate/invalid lifecycle behavior, monotonic control sequences, wrong-session/stale/replay rejection, range/loaded-only movement and cleanup. Remaining canonical cast/upkeep/config behavior must receive exact tests when those contracts are frozen.

### 5.2 Server/runtime coverage

Current runtime/GameTests cover dedicated representation materialization, server-owned movement application and preservation of the physical player body. Existing lifecycle coverage includes damage, logout/dimension/death/server-stop behavior from the merged lifecycle tranche.

Still required before end-to-end completion:

- canonical cast/channel admission invokes projection lifecycle exactly once;
- finalized range/control-limit gameplay policy tests;
- no remote interaction exploit path;
- client camera/input restoration and body/projection input separation;
- provider/resource failure behavior once a resource authority exists.

### 5.3 Network/client coverage

Implemented network tests cover:

- payload field shape containing no caster UUID or authoritative coordinates;
- protocol/sequence/finite-axis validation;
- 1.21.1-compatible MOVE/RETURN codec round trips with no trailing bytes;
- dedicated-server classloading safety through the full CI smoke gate.

Still required:

- physical client input capture/redirection;
- server correction versus any client prediction;
- camera BEGIN/END restoration;
- representation-loss restoration;
- reconnect stale-client-state cleanup.

### 5.4 Real-client acceptance

Astral Severance cannot be declared client-validated from automated CI alone. Final QA must directly observe start/return, camera/control feel, body vulnerability, damage interruption, range/timeout behavior, logout/reconnect restoration, death/Soul Anchor interaction, GUI/F1 behavior, camera-mod/Epic Fight coexistence, no stuck camera and no remote interaction exploit. Until observed, client acceptance remains deferred under D031.

## 6. Other 07.07 spells — specification status

The family contains:

- Astral Severance;
- Namescry;
- Gaze of Stillness;
- Nullifying Gaze;
- Occult Appraisal;
- Borrowed Sight;
- Pact Sanctuary.

The canonical completeness audit is `07-familiars-divination-specification-gate.md`. Runtime progress does not remove missing resource cost, cooldown semantics, scaling equations, final progression gates, config surfaces or provenance across the family.

## 7. Familiar-provider boundary

Familiar ownership remains provider-native first:

- ownership must be proven by an explicit bounded provider/adapter;
- `OWNED`, `NOT_OWNED` and `UNSUPPORTED` remain distinct;
- unknown/provider-error state fails closed;
- physical mod presence or thematic similarity does not establish ownership;
- verified Ars familiar ownership does not automatically authorize other companion systems;
- each additional provider requires exact-version/API/source verification;
- RPG Skill Tree may gate progression/mastery through a real contract but does not own familiar identity or Noetic runtime.

## 8. Specification gate

Every spell must define fantasy, host integration, invocation, target rules, resource cost, cooldown, scaling equation, progression gate, world-effect mode, boss/PvP behavior, config surface, tests and provenance.

Therefore:

- no safety ceiling or test fixture becomes a balance default;
- no qualitative `mana/channel`, `upkeep`, `cooldown` or `range` phrase becomes an invented number;
- no provider resource/host is assumed without verified authority/transaction support;
- every spell needs an explicit scaling equation or explicit `NO SCALING` decision;
- every cooldown needs canonical identity/group semantics if present;
- progression must be frozen through the actual RPG Skill Tree boundary;
- provenance must be linked per final spell;
- final config surfaces must be bounded and validated.

Until `07-familiars-divination-specification-gate.md` closes and Astral Severance reaches its canonical cast/client control path, 07.07 remains `IN PROGRESS` and Stage 08 remains blocked from consuming it as balance input.

## 9. Automated evidence

Canonical merged substrate evidence:

- PR #72 runtime head `673aff57e15ec29a6fc0d6a94f0034726b99a4c1`, CI `34069825298`, 103/103 Foundation GameTests + dedicated-server smoke;
- PR #72 merge `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, post-merge CI `34070253755`;
- Borrowed Sight final GREEN head `45f970edd10e20d41315cd1471471fadbef731fd`, CI `34186494393`;
- Borrowed Sight canonical merge PR #77 / `4053c060bb7e4c3f57ca06f49295868277a6eb57`;
- Astral lifecycle canonical merge PR #138 / `3469b454de2b65d0c15e89e7d689fe760dd30994`.

Current control branch evidence before final documentation reconciliation:

- synchronized implementation ancestry includes `main@c321063f41c34525cebd5e6936a560253c677442` via merge `3123f007a65a8ac03e701d90b8c8b968c8062425`;
- exact branch head `76ed71977bff5b0c1b59555f1032b22aecf535a1` passed Black Arcana CI run `34776232542` through unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke;
- main-only canonical artifact publication correctly skipped on the branch run.

Documentation commits after `76ed719...` require a fresh exact-head CI before merge. Automated evidence is not reclassified as real-client acceptance or as proof that the seven-spell specification gate is closed.

## 10. 07.07 completion rule

07.07 may become canonical only when all of the following are true:

- existing Noetic/familiar/gaze/sanctuary substrate remains intact;
- Borrowed Sight remains server-authoritative and real-client acceptance is correctly recorded/deferred under D031;
- Astral Severance lifecycle/representation/control remains server-authoritative;
- client camera/input is implemented without client-authoritative movement or duplicate caster identity;
- production MOVE uses a reviewed bounded server-side control-limit authority;
- Astral activation/upkeep terminates in the canonical cast/channel transaction rather than a parallel route;
- remote interaction remains prohibited unless separately approved through canonical safety/protection authority;
- all seven spells satisfy the per-spell specification gate;
- provider bridges used by final spells are verified against installed versions/APIs;
- required automated tests are green on the reconciled exact HEAD;
- mandatory real-client rows are directly observed or explicitly deferred only where D031 permits;
- `plans/STATUS.md` and this directory README match real `main` state.

This plan records the current boundary; it does not itself promote Stage 07 or Stage 08.
