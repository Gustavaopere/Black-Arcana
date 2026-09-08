# 07.07 — Familiars & Divination

## State

`IN PROGRESS — SERVER SUBSTRATE MERGED / BORROWED SIGHT CODE PATH IMPLEMENTED / ASTRAL SEVERANCE + SPECIFICATION GATE PENDING`

PR #72 merged the bounded server-side Noetic/familiar/gaze/sanctuary substrate at `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`. PR #77 now adds the bounded server-authored Borrowed Sight BEGIN/END presentation channel and physical-client camera adapter on top of that canonical substrate.

This does **not** promote Stage 07.07 as a completed domain. Astral Severance still lacks its canonical astral avatar/viewpoint implementation, the complete per-spell specification gate is still open, and real-client Borrowed Sight acceptance has not been executed. Stage 08 must therefore not treat 07.07 as canonical balance input yet.

## Implemented server substrate

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

## Borrowed Sight — production code path implemented

Canonical design requires channeling the viewpoint of an owned familiar or explicitly consenting bonded target, with range/channel cost and return on interruption/unload.

PR #77 preserves the existing server-owned admission/ownership/session authority and adds only presentation derived from those canonical sessions:

- `NoeticObservationRuntime.activeSessions()` exposes immutable bounded value snapshots for projection; it does not create a second session authority;
- `NoeticViewSyncPlanner` projects only `BORROWED_SIGHT`; `ASTRAL_SEVERANCE`, `NAMESCRY` and `OCCULT_APPRAISAL` cannot enter this camera channel;
- `NoeticViewTransitionTracker` is bounded by the canonical active-session ceiling and emits idempotent BEGIN/END transitions only when desired presentation changes;
- `MinecraftNoeticRuntime` resolves only the transition viewer and that viewer's already-loaded `ServerLevel` target by UUID, without global-player iteration or chunk forcing;
- `NoeticViewNetworkBridge` registers a play-to-client payload and sends only to the authoritative viewer when the channel is present;
- `BorrowedSightClientController`, loaded only from the `Dist.CLIENT` entrypoint, resolves only the server-authored runtime entity id from the already-loaded client level, moves only the physical camera, and restores it to the local player's body on END or target loss;
- the client adapter creates no client-to-server gameplay packet path and cannot choose target, admission, duration, ownership or privacy state.

NeoForge 1.21–1.21.1 documentation confirms payload handlers registered without `PayloadRegistrar#executesOn(HandlerThread.NETWORK)` execute on the main thread by default. PR #77 does not switch handler thread.

### Borrowed Sight evidence boundary

Exact code checkpoint before this documentation update: PR #77 head `d221408400ecec4a4430df510823cfc6efc4be41`.

Black Arcana CI #1994 / `34185238779` passed on that exact head:

- JUnit;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTest server;
- dedicated-server smoke.

That automated evidence proves compilation, deterministic server/domain contracts and dedicated-server safety for the implemented code path. It does **not** prove actual first-person camera feel, rendering compatibility, input behavior or restoration in the user's full physical-client modpack. Those remain direct real-client validation work under D031.

## Astral Severance — NOT IMPLEMENTED end-to-end

Canonical design requires a controllable non-combat viewpoint/avatar while the physical body remains vulnerable, with hard range, timeout/interruption return, no unauthorized projection interaction, and logout/death restoration.

The current server observation API accepts an already-loaded `LivingEntity` target and owns session/snapshot state only. Borrowed Sight's new camera channel deliberately refuses `ASTRAL_SEVERANCE`; reusing an arbitrary observed entity as the astral body would violate the required identity, authority and interaction model.

A future Astral Severance implementation must therefore define and implement a canonical bounded astral viewpoint/avatar lifecycle before any client camera/input path is enabled for that observation kind. Until then it remains fail-closed.

## Specification gate

`plans/07-spell-domains/README.md` requires every spell to define fantasy, host integration, invocation, target rules, resource cost, cooldown, scaling equation, progression gate, world-effect mode, boss/PvP behavior, config surface, tests and provenance.

The existing candidate entries for the 07.07 spell family do not yet freeze all of those fields. Borrowed Sight's production presentation path does not authorize Stage 08 to invent missing balance values. Until the per-spell specifications and Astral Severance mechanics are completed/reviewed, 07.07 remains `IN PROGRESS`.

## Existing automated evidence — merged server substrate

- final PR #72 runtime head: `673aff57e15ec29a6fc0d6a94f0034726b99a4c1`;
- Black Arcana CI #1562 / `34069825298`: GREEN;
- 103/103 Foundation GameTests and dedicated-server smoke;
- runtime merge: `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`;
- exact-SHA post-merge CI #1563 / `34070253755`: GREEN;
- artifact `black-arcana-5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, ID `10000268004`, SHA-256 `35c8436ab3cbd2f75e8cc6f7ae5554edb7a330205f5166265f96979b6fa65b16`.

This evidence remains authoritative for the code it actually exercises; it is not reclassified as client acceptance.
