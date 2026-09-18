# 05.03 — Contextual Feedback — Runtime/Data Contract

## State

`IMPLEMENTED / DETERMINISTIC ACCEPTANCE COMPLETE / REAL-CLIENT VALIDATION CARRIED TO STAGE 09`

HUD layout, hierarchy, anti-clutter, wording and visual accessibility are owned by `plans/visual-production/05-casting-ux/03-contextual-hud-presentation.md`.

## Runtime purpose

Provide bounded synchronized facts that a contextual client surface may present without making preview or UI state authoritative.

## Canonical contract

- `BlackArcanaHudLayer` is client-only and consumes synchronized/client-session state; dedicated-server startup must not classload it.
- No client player, competing screen, disabled contextual presentation or no recent context yields no HUD work.
- Selected-spell state is reconciled against the synchronized server loadout.
- Static danger metadata comes from synchronized preflight data.
- Dynamic Arcane Resistance forecast is server-authored and valid only while its spell/profile revision matches current static metadata.
- Predictable gate projection is server-authored and bounded to approved categories; `CLEAR` never means cast success is guaranteed.
- Cast denial/success/effect-failure comes from the authoritative bounded `CastResultPayload`.
- Current `CastResultPayload` identifies a result by `castId` but does not itself prove the current selection produced that result. Presentation must not guess attribution.
- Session/reconnect/reload/provider-profile changes clear or invalidate stale presentation state according to its identity/revision contract.

## Correlation rule

A forecast cannot rewrite an authoritative result. If client-side pending context is used only to correlate a known emitted `castId`, it remains bounded presentation metadata and never becomes server admission, replay, resource, cooldown or identity authority.

## Optional data remains gated

Generic selected-spell cooldown, provider cost, reusable charge pools, active channel progress and ritual/domain timers may be presented only after the corresponding bounded server-authored contract is approved under `✅-07-presentation-data-contracts.md` or its successor.

Do not infer these facts from local timers, ids, particles, world scans or provider heuristics.

## Performance/network rules

- event/context driven;
- no entity/chunk/world scan in render paths;
- no per-frame network request;
- bounded forecast request rate outside render;
- bounded snapshot and any future correlation/dedup cache by count and age;
- no per-tick full-state synchronization.

## Automated stale-revision hardening

`HazardForecastReloadRaceTest` pins the in-flight reload race where a forecast request is issued under one hazard-profile revision, an identical-looking preflight is accepted as a new revision, and the old response arrives afterward. Client forecast request IDs are allocated by `ClientArcanaSyncState`; each accepted preflight, reconnect clear or player-identity reset advances the minimum valid request boundary, so a pre-revision response cannot repopulate forecast state while a request allocated after the boundary remains acceptable. No gameplay-authority or payload-schema change is required.

The test-only RED checkpoint `ecfa1709ef1acd51c62d9981b63513d5a15d8118` failed workflow `35043584131` at unit tests before the revision-aware state seam existed. Runtime HEAD `c6e2fa854f776df8d074d24f6da1e7f758b9153c` then passed workflow `35043812423` for unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke. This is deterministic engineering evidence. The corresponding real-client state observation is carried to Stage 09 and is not inferred as PASS.

Review follow-up PR #279 strengthened the regression shape so it no longer replays only an already-accepted request ID: it accepts one forecast under revision A, allocates a distinct higher request under revision A without receiving its response, crosses the reload boundary, then delivers that outstanding pre-reload response and requires rejection before proving a post-reload request remains acceptable. Test-only HEAD `12b3ef4bda0c729bbd49b4f3bf7ef2b8b5926173` passed workflow `35046833742` for unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke. This strengthens deterministic coverage. It does not convert any manual matrix row to PASS; those rows remain deferred to Stage 09 under D035.

## Completion and Stage 09 carry

Current server-authored denial/forecast/correlation, stale-state and dedicated-server classloading contracts are deterministically covered and complete for Stage 05 progression. Any future presentation datum remains subject to the 05.07 server-authored contract gate. Direct real-client correlation/reload/reconnect observations remain PENDING and are carried to Stage 09 under D035.
