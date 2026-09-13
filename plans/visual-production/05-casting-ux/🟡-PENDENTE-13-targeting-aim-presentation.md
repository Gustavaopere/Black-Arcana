# 05.13 — Targeting & Aim Presentation

## State

`PLANNING / NO RUNTIME CHANGE / CLIENT TARGET PRESENTATION HARDENING`

This document defines the canonical Stage 05 plan for target/aim presentation around Black Arcana casting without transferring target resolution, cast admission, world-safety policy or effect authority to the client.

Baseline used for this audit: `main@4ce5699cc76b511804956f903559ae8f7e44ba12`.

This is a planning artifact only. It does **not** add Java runtime behavior, reticles, target overlays, packets, protocol fields, target locks, world scans, provider bridges, resource assets or manual PASS evidence.

---

## 1. Why this plan exists

Stage 05 already has a deterministic input/loadout/radial/HUD runtime and a server-authoritative cast pipeline. The client can also observe Minecraft's current `hitResult` and, for an entity hit, encode an entity UUID into `CastIntentPayload.targetHint`.

What Stage 05 does **not** yet freeze as one presentation contract is how future aim/target UI may communicate:

- what the player is locally pointing at;
- what target mode the selected Black Arcana spell uses;
- whether a local candidate is only advisory or is actually server-confirmed;
- range/line-of-sight uncertainty;
- block/entity/ray/area/linked target affordances;
- stale target observations;
- cast-result correlation after the aim state changes;
- world-mutation safety without leaking or duplicating server policy;
- coexistence with Epic Fight, Iron's, Spell Actionbar and other installed combat/casting presentation.

Without an explicit plan, future target UI could accidentally make a local raycast look authoritative, implement a second target resolver on the client, probe protection systems every frame, infer a cast result from the currently highlighted target, or expose world-safety information that the server never synchronized.

05.13 closes that planning gap.

---

## 2. Current verified runtime facts

### 2.1 `ArcanaTargetReference` is explicitly server-resolved

Current:

`src/main/java/dev/gustavopere/blackarcana/api/ArcanaTargetReference.java`

is documented as a pure-Java reference to a **server-resolved target**.

The sealed interface currently permits exactly:

- `ArcanaTargetReference.EntityRef(UUID entityId)`;
- `ArcanaTargetReference.BlockRef(String dimensionId, int x, int y, int z)`.

The same source explicitly states that Minecraft adapters encode their live result into this form so spell effects do not rely on ad-hoc string parsing or client-authored coordinates.

Therefore:

**an `ArcanaTargetReference` is not permission for a client renderer to author authoritative target coordinates.**

### 2.2 Current target kinds are bounded and server-owned

Current:

`src/main/java/dev/gustavopere/blackarcana/api/ArcanaTargetSpec.java`

contains exactly these `Kind` values:

- `SELF`;
- `ENTITY`;
- `RAY`;
- `BLOCK`;
- `CONE`;
- `SPHERE`;
- `CYLINDER`;
- `PROJECTILE`;
- `LINKED`.

The same record bounds:

- `maxRange` to a finite value from `0.0` through `ABSOLUTE_MAX_RANGE`;
- `maxTargets` from `1` through `ABSOLUTE_MAX_TARGETS`;
- line-of-sight requirement;
- player eligibility;
- friendly eligibility.

Those fields are authoritative spell/runtime rules. 05.13 does not authorize the client to recompute or override them independently.

### 2.3 Current client emits intent only

Current:

`src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java`

is explicitly documented as a physical-client input adapter that emits intent only while gameplay validation remains server-side.

When `castSlot(int slot)` executes today:

1. it reads the synchronized loadout;
2. reconciles/selects the local slot;
3. reads `Minecraft.hitResult`;
4. if that result is an `EntityHitResult`, it encodes an `ArcanaTargetReference.EntityRef` as `targetHint`;
5. otherwise `targetHint` remains blank;
6. it sends one `CastIntentPayload` with a new `castId`, canonical `spellId`, slot and bounded hint.

The client does **not** currently send authoritative block coordinates, cone geometry, sphere center, cylinder center, ray endpoint or linked-target list.

### 2.4 `CastIntentPayload.targetHint` is bounded but not authoritative

Current:

`src/main/java/dev/gustavopere/blackarcana/network/CastIntentPayload.java`

contains:

- `protocolVersion`;
- `castId`;
- `spellId`;
- `loadoutSlot`;
- `targetHint`.

The payload validates protocol, IDs, slot bounds and `MAX_TARGET_HINT_LENGTH`.

That wire validation proves only that the intent is structurally bounded. It does **not** prove that the hinted entity exists, is loaded, is in range, is visible, is eligible, is friendly/hostile, is a projectile when required, or will survive server validation until execution.

### 2.5 Ingress keeps the hint advisory

Current:

`src/main/java/dev/gustavopere/blackarcana/core/cast/ArcanaCastIngressService.java`

states that client target hints remain advisory. The ingress copies the hint into `ArcanaCastRequest` only so a server-owned `TargetSelector` can re-resolve and validate against live world state.

The ingress also resolves spell identity and server execution runtime before calling the canonical cast engine.

05.13 must never create a UI-side alternate ingress or execution path.

### 2.6 Server targeting re-resolves live state

Current:

`src/main/java/dev/gustavopere/blackarcana/core/targeting/ServerEntityTargetSelector.java`

implements `ArcanaServices.TargetSelector` and documents that:

- coordinates/entity sets are resolved from live server state;
- client target data is advisory only for explicit `ENTITY`/`PROJECTILE` selection;
- no path intentionally force-loads chunks.

Current server behavior includes:

- `SELF` — resolves caster on the server;
- `ENTITY` — parses the advisory entity hint, finds the live server entity, then applies bounded target selection;
- `PROJECTILE` — same advisory hint path, additionally requiring a projectile;
- `BLOCK` — performs a server-side block ray from caster eye/view direction;
- `RAY` — performs server-side entity ray selection bounded by blocks/range;
- `SPHERE` — resolves candidates from a bounded server-side area;
- `CONE` — resolves candidates from server view/geometry;
- `CYLINDER` — resolves from server-owned target geometry;
- `LINKED` — resolves through the server linked-target path.

The implementation also contains loaded-chunk, range/LOS and candidate-policy checks appropriate to its paths.

A future client overlay is therefore a **visual aid**, not a mirror authority.

### 2.7 Cast results do not carry target identity

Current:

`src/main/java/dev/gustavopere/blackarcana/network/CastResultPayload.java`

contains exactly:

- `protocolVersion`;
- `castId`;
- `status`;
- `code`;
- `detail`.

It does not currently include:

- `spellId`;
- loadout slot;
- target reference;
- resolved target count;
- authoritative impact position.

Therefore a future target overlay must not attribute a received result to whatever entity/block/reticle is currently under the crosshair unless a safe correlation contract actually proves that association.

05.11 remains the authority for transient result/selection correlation. 05.13 extends the same anti-misattribution rule to target presentation.

### 2.8 World mutation has a separate canonical admission route

Current world-safety authority is not a client target check.

Current:

`src/main/java/dev/gustavopere/blackarcana/core/world/WorldEffectAdmissionService.java`

is documented as the canonical admission route for actual terrain work. It combines:

- `ConfigurableWorldEffectPolicy`;
- declared per-spell world-effect profile/bounds;
- `LoadedChunkGuard`;
- cumulative `WorldEffectBudgetLedger`.

The service denies undeclared mutation, missing safety profile, incompatible mutation type, work beyond declared bounds and unloaded-chunk work before budget settlement.

Therefore:

**a client block highlight, AOE outline or “in range” reticle can never imply world-mutation permission unless an explicit bounded server-authored presentation contract says exactly that.**

05.13 introduces no such permission contract by itself.

---

## 3. Relationship to existing Stage 05 plans

05.13 is deliberately presentation-only and depends on existing authority layers rather than replacing them.

### `05.01 — Input & Loadouts`

Owns input lifecycle, loadout selection and intent emission.

05.13 must reuse the canonical input path. It must not introduce a second “target confirmed → cast” execution route.

### `05.02 — Radial Wheel`

Owns spell selection and radial geometry.

05.13 may eventually show targeting-mode hints around selected spell context, but radial selection must remain non-casting and must not lock a world target.

### `05.03 — Contextual HUD`

Owns contextual HUD density and anti-clutter behavior.

05.13 targeting presentation must remain compact/contextual and must not grow into a permanent tactical scanner.

### `05.04 — Accessibility & Client Config`

Owns presentation-only preferences.

Any future target marker animation/flash/particle must consume reduced-motion/reduced-flash/particle policy where applicable. Essential target meaning must remain available without those effects.

### `05.05 — Final Client Validation Handoff`

Owns Stage 05 manual acceptance evidence.

05.13 does not mark any existing matrix row PASS. If a targeting refinement is later implemented, affected rows are added/retested through the same exact-build evidence procedure.

### `05.06 — Modpack Coexistence`

Owns installed UI/combat/input coexistence.

05.13 must not assume that Iron's, Spell Actionbar, Epic Fight or EFIS exposes a target-overlay integration API merely because each is installed.

### `05.07 — Presentation Data Contracts`

Owns the authority question: whether a datum is legitimate to present.

05.13 follows 05.07 strictly. If the server does not synchronize a fact, the client may not promote a local estimate into a server-authoritative semantic.

### `05.08 — Visual Language & State Semantics`

Owns semantic meaning.

05.13 must distinguish local observation/advisory aim from server-authoritative outcome using non-color-only cues.

### `05.09 — Keyboard Focus & Navigation`

Owns screen-local focus.

Keyboard focus in radial/editor must never be conflated with world target focus/lock.

### `05.10 — Loadout Editor Information Architecture`

Owns loadout-editor organization.

Targeting mode metadata may be shown in a future editor only if it is sourced from an approved bounded presentation contract; do not infer behavior from spell names/icons.

### `05.11 — Contextual Feedback Orchestration`

Owns transient priority/correlation.

05.13 must not let a new current aim candidate rewrite the identity of an older authoritative result.

### `05.12 — Iconography & Resource Resolution`

Owns safe spell-art resolution.

Target markers and reticles are a separate presentation family. A spell icon is not a target marker, target type, target-validity proof or permission indicator.

---

## 4. Authority model

The target presentation model is split into three explicit authority levels.

The labels in this section are **planning vocabulary**, not claims that matching enums/classes already exist.

### 4.1 `LOCAL_OBSERVATION`

Examples:

- the current client `hitResult`;
- entity currently under the local crosshair;
- local camera direction;
- local cursor/reticle location;
- purely client-computed screen-space marker placement.

This level may drive immediate responsive presentation but proves no server admission fact.

### 4.2 `SERVER_AUTHORED_PREVIEW`

This level exists only when a real bounded synchronized/response contract explicitly provides a fact.

Examples could include a future server-authored targeting preview, but **no generic Stage 05 target-preview payload is present at this baseline**.

Until such a contract exists, the UI must omit server-confirmed target-validity semantics rather than fabricate them.

### 4.3 `AUTHORITATIVE_RESULT`

Current cast outcome comes from `CastResultPayload`/canonical server runtime.

This level may prove success/denial for a `castId`, but the current payload does not itself prove resolved target identity.

A result therefore cannot be visually attached to a current target candidate by inference.

---

## 5. Canonical targeting presentation lifecycle

A future 05.13 implementation must use this lifecycle conceptually.

### 5.1 No selected spell / no cast context

Default:

- no Black Arcana target overlay;
- no world scan;
- no target history;
- no permanent range ring.

This preserves Stage 05 low-clutter behavior.

### 5.2 Selected spell becomes target-relevant

The client may display presentation describing the selected spell's known targeting mode **only if the required metadata is legitimately available**.

The current client does not have a dedicated synchronized `ArcanaTargetSpec` presentation payload. Therefore a first implementation must audit how/if target-spec information reaches the client before rendering mode/range/LOS claims.

If no approved client contract exists:

- keep generic aim presentation only;
- do not infer target kind from `spellId`, translation key, icon path, provider namespace or spell name.

### 5.3 Local observation changes

A local crosshair entity/block observation may update responsive presentation.

Rules:

- label it advisory/local through semantics, not “valid target”;
- do not send network traffic merely because the crosshair moved;
- do not perform protection queries;
- do not enumerate world entities for UI convenience;
- do not create target locks as gameplay state;
- do not retain stale entity references after dimension/session change.

### 5.4 Cast intent is emitted

`ClientInputController` remains the canonical emission surface unless a reviewed implementation deliberately refactors shared client intent construction without changing authority.

At send time:

- `castId` is the correlation key for the submitted intent;
- `spellId` and slot identify the attempted client context;
- `targetHint` remains advisory;
- any local presentation snapshot associated with that send is evidence only of what the client observed, not what the server resolved.

A future bounded client-local correlation record may include the local observed candidate for presentation diagnostics, but it must be bounded by count/age and cleared on session reset. It must never be used to approve gameplay.

### 5.5 Server resolves target

The server uses canonical live state through `ServerEntityTargetSelector` and the cast engine.

The client does not duplicate this phase.

### 5.6 Result arrives

The current result is authoritative for its `castId` only.

If the player moved the camera or target candidate changed while the request was in flight:

- the new current aim stays current;
- the old result remains tied only to its safe cast correlation;
- no marker may visually jump the old result onto the new candidate;
- if no safe target identity was synchronized, render the result without target attribution.

---

## 6. Target-kind presentation matrix

This section defines safe presentation boundaries for the **currently verified** `ArcanaTargetSpec.Kind` values.

It does not require all rows to gain custom UI.

| Kind | Current server resolution fact | Client presentation boundary |
|---|---|---|
| `SELF` | server resolves live caster | optional self-cast indicator; no world target required |
| `ENTITY` | advisory entity hint re-resolved/validated server-side | local crosshair candidate may be highlighted as advisory; never claim valid/range/LOS/friendly legality locally |
| `PROJECTILE` | advisory entity hint plus server projectile/type/range/LOS policy | local projectile candidate may be advisory only; no client authority |
| `BLOCK` | server raycasts from live caster eye/view | local block crosshair may assist aim, but must not author authoritative coordinates or imply mutation permission |
| `RAY` | server raycasts/collects bounded entity candidates | reticle/direction aid may be local; endpoint/hit entity is not authoritative |
| `SPHERE` | server resolves bounded candidates from live state | any future radius visualization requires legitimate target-spec/range data; decorative estimate must never masquerade as exact server volume |
| `CONE` | server uses target spec + server target geometry/live facing | any future cone guide requires authoritative presentation metadata; no client-computed candidate list becomes authority |
| `CYLINDER` | server resolves through server-owned geometry/live state | any future cylinder guide follows the same metadata and uncertainty rules |
| `LINKED` | server resolves through linked-target resolver and bounded candidates | do not reveal or precompute chain members unless a bounded server-authored presentation contract explicitly permits it |

The safe default for any kind whose required metadata is not synchronized is **less presentation**, not guessed presentation.

---

## 7. Reticle and target-marker semantics

### 7.1 Reticle means aim, not legality

A Black Arcana reticle may communicate:

- that the player is in a casting/aim context;
- local pointing direction;
- local observation presence;
- target-mode category where legitimately known.

It must not communicate by default:

- cast will succeed;
- target is server-valid;
- target is inside authoritative range;
- line of sight is server-valid;
- provider resource is sufficient;
- cooldown is ready;
- progression gate is passed;
- world mutation is permitted;
- Backlash cannot occur.

Those belong to their corresponding server-authored contracts.

### 7.2 Target candidate is distinct from selected spell

The UI must preserve separate semantic identities for:

- selected spell;
- pointer/crosshair observation;
- advisory target candidate;
- authoritative cast result.

Changing one does not rewrite the others.

### 7.3 No color-only validity language

A green/red target outline is dangerous if green silently means “server-valid”.

If colors are later used:

- they require an accompanying shape/symbol/text semantic where important;
- advisory/local state must remain distinguishable from server-authored allow/deny state;
- unknown must not reuse success/readiness styling.

### 7.4 Occlusion and through-wall markers

Default rule:

- do not reveal entities through walls merely because the client world knows they exist;
- do not implement x-ray/ESP-like target highlighting;
- preserve normal visible-world expectations unless a Black Arcana spell explicitly owns a separately reviewed perception mechanic.

A spell such as a future or existing perception/sight mechanic must use its own approved runtime/visibility contract, not a generic 05.13 loophole.

---

## 8. Range, LOS and eligibility presentation

### 8.1 No local authoritative range claim

Even when an exact `maxRange` value becomes presentation-authorized, client camera/entity interpolation can differ from live server resolution.

Therefore client range UI is at most:

- an informational bound;
- an advisory estimate;
- or a server-authored preview fact when such a contract explicitly exists.

It is never a substitute for server validation.

### 8.2 No local authoritative LOS claim

Server target selection owns LOS according to live server blocks/entities and target policy.

A local ray can help the player aim, but the UI must not render `LOS VALID` as an authoritative fact unless the server provides that exact fact through a bounded presentation contract.

### 8.3 Friendly/player eligibility

`ArcanaTargetSpec` includes `allowPlayers` and `allowFriendly`.

A future UI may expose those rules only after a legitimate client presentation source is identified. It must not derive friendship/team eligibility from arbitrary client heuristics and then render it as server truth.

### 8.4 Projectile eligibility

For `PROJECTILE`, the server explicitly verifies the hinted live entity is a projectile.

A local crosshair hit may visually suggest a candidate, but it does not prove the server will classify or accept that entity identically when the request is processed.

---

## 9. Area/geometry previews

Area previews are useful but high-risk for false authority.

### 9.1 Required gate before implementation

Before rendering an exact sphere/cone/cylinder/ray volume, implementation must verify:

1. the selected spell's target kind/spec/geometry is actually available to the physical client through an approved bounded contract;
2. the values are presentation-safe and not provider-private state;
3. the client can render them without duplicating server candidate selection;
4. stale metadata invalidation is defined;
5. the preview is semantically labeled advisory unless the server contract states otherwise.

### 9.2 No candidate enumeration for previews

A geometry preview should normally render shape/extent, not scan and mark every entity within it.

Forbidden default pattern:

`every frame -> enumerate all nearby entities -> reproduce server eligibility -> paint accepted targets`

That would duplicate target policy, create client tick cost and drift from live server authority.

### 9.3 Bounds

Any preview work must remain bounded by already available local presentation data and fixed render budgets.

No global/world scans are permitted.

---

## 10. Staleness and supersession

Target presentation is especially sensitive to stale state.

### 10.1 Local observation invalidation

A local candidate becomes stale when any relevant local context changes, including:

- crosshair/hit result changes;
- selected spell changes;
- selected loadout slot changes;
- screen opens and world-input context is suspended;
- dimension changes;
- disconnect/session reset;
- observed entity disappears from the client world;
- a future target-spec presentation snapshot is replaced/invalidated.

### 10.2 Pending cast context

If a future 05.11/05.13 correlation cache records a local candidate at send time:

- key it by `castId`;
- bound by count and age;
- never reuse the record for another cast id;
- clear on disconnect/session reset;
- treat it as attempted-client-context only;
- do not mutate gameplay if it expires.

### 10.3 Result supersession

Latest current target and latest authoritative result are different channels.

A new target observation may visually supersede an old aim marker, but it must not relabel an older result.

An authoritative denial may suppress noisy advisory target styling temporarily under 05.11 priority rules without changing what target the server resolved.

---

## 11. World-safety and protection boundary

05.13 must not become a client-side protection oracle.

### 11.1 Canonical authority

Terrain work remains admitted through `WorldEffectAdmissionService` and its policy/profile/chunk/budget checks.

Entity interactions remain subject to their canonical server-side admission/protection paths where applicable.

### 11.2 No per-frame policy probes

Do not add a network call such as “may I modify this block?” every frame while the player moves the crosshair.

That would:

- create unnecessary traffic;
- race with live server state;
- risk exposing protection structure;
- still not guarantee cast-time admission;
- couple rendering to mutable world policy.

### 11.3 No protection leakage

Generic targeting UI should not reveal:

- hidden protection-region boundaries;
- ownership data not otherwise exposed;
- unloaded chunk state beyond what normal client state already reveals;
- server-only entity eligibility lists;
- future mutation-policy decisions before the server deliberately authors a presentation response.

If a future product requirement needs world-safety preview, it requires a separate bounded, privacy-reviewed server-authored contract.

---

## 12. Provider and modpack coexistence

Current physical modlist baseline confirms adjacent surfaces:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Spell Actionbar `1.1.4`;
- Epic Fight `21.17.3.1`;
- `efiscompat 3.1.0`;
- Controlling `19.0.5`.

### 12.1 Coexistence first

05.13 default:

- Black Arcana target presentation belongs to Black Arcana casts;
- provider UI remains provider-owned;
- do not hide/replace/monkey-patch provider crosshairs/actionbars;
- do not infer provider targeting rules from visual similarity;
- do not assume EFIS gives Black Arcana a target API;
- do not assume Spell Actionbar exposes target authority;
- do not require Controlling.

### 12.2 Epic Fight camera/combat modes

Epic Fight can materially change combat presentation/camera behavior.

Before any screen-space marker or reticle implementation is approved:

- test real-client alignment during relevant Epic Fight states;
- verify no reliance on an undocumented Epic Fight camera API;
- use vanilla/NeoForge supported client rendering seams first;
- if exact integration is required, inspect the exact installed API/version before coding;
- fail safely when the optional integration is absent.

### 12.3 Provider-native target UI

If an external provider already owns a target marker for its own spells, Black Arcana should not duplicate it for provider-hosted casts unless Black Arcana is actually the canonical cast authority for that transaction.

Authority follows the transaction, not thematic similarity.

---

## 13. Accessibility

Target presentation must remain usable without relying on a single sensory channel.

Requirements for future implementation:

- advisory/local candidate must have non-color-only distinction from authoritative result;
- reticle scale/shape remains legible at supported GUI/viewport combinations;
- important meaning cannot require animation;
- reduced motion disables/softens nonessential target pulsing/travel animation;
- reduced flashes prevents essential status from being encoded only as flashing;
- particle density cannot hide target identity/status;
- text labels/tooltips remain bounded and do not cover the central playfield unnecessarily;
- screen readers/narration integration may be evaluated only through real supported Minecraft APIs rather than invented accessibility hooks.

05.13 does not itself add new client-config fields. A new preference is justified only by real usability need and remains presentation-only.

---

## 14. Performance and boundedness

Targeting UX must not become a scan loop.

### 14.1 Allowed default work

Per-frame/tick presentation may use already-local bounded state such as:

- selected spell identity;
- current vanilla client hit result;
- camera/screen transform needed to draw the current marker;
- bounded synchronized presentation metadata already in memory;
- bounded client-local correlation records.

### 14.2 Forbidden default work

Do not perform:

- global entity scans;
- full chunk scans;
- filesystem/JAR scans;
- remote downloads;
- per-frame provider reflection/discovery;
- per-frame protection queries;
- per-frame server target-preview requests;
- unbounded target history;
- unbounded marker sets;
- forced chunk loads.

### 14.3 Diagnostics

If target diagnostics are later added:

- aggregate/rate-limit logging;
- no per-frame warning spam for ordinary miss/no-target state;
- do not log sensitive protection/ownership data unnecessarily.

---

## 15. Dedicated-server and physical-client boundary

All target rendering remains physical-client-only.

Current server target selection classes must remain free to load on a dedicated server without referencing client rendering classes.

Future implementation must preserve:

- common/API/network payload classes free of client GUI classes;
- server target selector free of `Minecraft` client singleton/render classes;
- client renderer/input helper registered only on physical client;
- no dedicated-server classloading of reticle/overlay/resource classes.

CI dedicated-server smoke remains a mandatory regression gate after implementation.

---

## 16. Clean-room and asset provenance

05.13 does not authorize copying another magic mod's:

- crosshair texture;
- target ring;
- lock-on marker;
- shader;
- animation;
- sound;
- source code;
- wording.

Other mods may be studied conceptually for interaction patterns, but Black Arcana presentation must remain original or use assets with verified compatible rights/provenance.

If new visual/audio assets are eventually added, Stage 09 provenance rules and repository notices apply where required.

---

## 17. Proposed implementation phases

These phases are future work only. They do not create runtime by being listed here.

### Phase A — authority/data audit

Before touching rendering:

1. sync latest `origin/main`;
2. inspect `ArcanaTargetSpec`, `ArcanaTargetGeometry`, `ServerEntityTargetSelector`, `ClientInputController`, cast payloads and active spell registry/runtime;
3. determine exactly which target metadata, if any, is currently available on the physical client;
4. classify each desired UI datum under 05.07;
5. do not add a protocol field until the product need and authority owner are explicit.

### Phase B — minimal advisory reticle/candidate semantics

If approved:

- use current local hit result only as `LOCAL_OBSERVATION`;
- keep selection/cast paths unchanged;
- add semantic differentiation from server-authored result;
- no range/LOS/protection claim;
- no target lock;
- no new networking merely for crosshair movement.

### Phase C — target-kind/geometry presentation

Only after Phase A proves a legitimate client metadata source:

- show target-kind affordance where useful;
- render bounded shape guides without candidate enumeration;
- mark them advisory unless server-authored preview semantics exist;
- validate small/ultrawide viewport behavior.

### Phase D — result/candidate correlation hardening

Coordinate with 05.11:

- if client-local pending `castId` context is implemented, keep it bounded and presentation-only;
- never infer resolved target identity from that record;
- unknown/unmatched results remain generic authoritative results.

### Phase E — optional exact-provider/camera compatibility

Only after a demonstrated real conflict:

- inspect exact installed provider API/source;
- add the narrowest boundary/adapter;
- no optional provider becomes core authority;
- absence/incompatibility fails safely.

---

## 18. Future TDD and automated test matrix

Implementation should begin with deterministic pure/state tests where the behavior can be separated from Minecraft rendering.

Do **not** create these tests merely because this plan exists. Exact test class/file names must be chosen from the implementation branch's current test structure rather than guessed in planning.

Required behavioral coverage when implemented:

### 18.1 Authority semantics

- local candidate is advisory, never authoritative;
- unknown target metadata does not render guessed valid/ready state;
- current target change does not relabel an existing authoritative result;
- stale pending correlation is discarded;
- disconnect/session reset clears pending target/correlation presentation state.

### 18.2 Target-kind semantics

For every implemented kind affordance:

- `SELF` requires no world candidate;
- entity/projectile local candidate remains advisory;
- block local observation does not imply mutation permission;
- area guide does not enumerate/authorize server targets;
- linked presentation does not expose guessed chain members.

### 18.3 Bounds

- pending correlation cache count/age is bounded if introduced;
- marker list is bounded if more than one marker is ever supported;
- no unbounded history is retained;
- malformed/missing optional metadata fails to safe fallback.

### 18.4 Existing behavior regression

- radial selection remains non-casting;
- quick/selected cast still emits one canonical intent;
- loadout behavior unchanged;
- authoritative server target tests remain unchanged unless an intentional server contract change is separately approved;
- dedicated-server classloading remains safe.

### 18.5 Integration/GameTests

Only add or adjust GameTests if implementation changes a world/network contract that actually requires server integration evidence.

A presentation-only client change should not rewrite server target behavior merely to manufacture test coverage.

---

## 19. Real-client validation matrix for an implemented 05.13 refinement

Any implemented visual/input targeting refinement requires direct physical-client evidence.

Minimum viewport/GUI matrix remains aligned with Stage 05 hardening:

- `854×480`;
- `1920×1080`;
- `3440×1440`;
- GUI scale `Auto`;
- GUI scale `2`;
- GUI scale `3`;
- GUI scale `4` where selectable/applicable.

Applicable scenarios:

1. selected spell with no local target;
2. entity under crosshair;
3. entity leaves crosshair before result;
4. target entity disappears/unloads before result;
5. target changes while a cast result is in flight;
6. block crosshair observation;
7. server denial after a visually plausible local candidate;
8. no-target/miss path;
9. each target-kind affordance actually implemented from legitimate metadata;
10. small viewport central-playfield readability;
11. ultrawide alignment;
12. reduced-motion/reduced-flash behavior where target VFX uses them;
13. F1/HUD-hidden behavior consistent with chosen Minecraft overlay seam;
14. radial/loadout screen open — world casting remains suppressed;
15. Epic Fight relevant combat/camera state;
16. Iron's/Spell Actionbar present simultaneously;
17. no duplicated provider target authority;
18. disconnect/reconnect clears stale target presentation.

If geometry previews are implemented, also verify camera movement, partial occlusion and server denial at apparent preview boundaries without presenting the local shape as guaranteed success.

Manual evidence must record exact build/SHA and follow `05-final-client-validation-handoff.md`.

---

## 20. Implementation gate

No 05.13 runtime implementation begins until all applicable boxes are satisfied.

### Authority

- [ ] Latest `origin/main` fetched and SHA recorded.
- [ ] Correct branch/PR checked for equivalent work.
- [ ] `plans/DECISIONS.md` re-read for current casting/target/world-safety contracts.
- [ ] Current `ArcanaTargetSpec`/geometry/selector implementation inspected.
- [ ] Desired UI fact classified as local observation, server-authored preview or authoritative result.
- [ ] No local estimate is being promoted to server truth.

### API/client seam

- [ ] Exact Minecraft 1.21.1 / NeoForge 21.1.248 client hit-result/rendering APIs verified before code is written.
- [ ] No invented render event, method or provider hook.
- [ ] Physical-client registration boundary identified.
- [ ] Dedicated-server classloading remains clean.

### Networking

- [ ] Existing payload is sufficient, or a real missing datum is documented before protocol change.
- [ ] Any new synchronization is bounded, versioned, event-driven and stale-safe.
- [ ] No per-frame target-preview request.
- [ ] `castId` correlation cannot become gameplay authority.

### World safety/privacy

- [ ] No client-side replacement for `WorldEffectAdmissionService`.
- [ ] No per-frame protection queries.
- [ ] No hidden protection/ownership leakage.
- [ ] No force-loading or global scans.

### UX/accessibility

- [ ] Advisory/local and authoritative semantics are visibly distinct without color alone.
- [ ] 05.08 semantics preserved.
- [ ] 05.11 result priority/correlation preserved.
- [ ] 05.03 low-clutter HUD rule preserved.
- [ ] Reduced-motion/reduced-flash rules applied where relevant.

### Coexistence

- [ ] Current physical modlist rechecked.
- [ ] Epic Fight/EFIS behavior tested before adding compatibility code.
- [ ] Iron's/Spell Actionbar authority remains provider-owned.
- [ ] Optional integration fails safely.

### Validation

- [ ] Deterministic RED tests added first where pure/state behavior exists.
- [ ] Minimum GREEN implementation follows.
- [ ] Full CI run on exact branch HEAD.
- [ ] Affected real-client rows executed on exact build.
- [ ] `origin/main` fetched again immediately before merge.
- [ ] Branch reconciled if main advanced.
- [ ] CI re-run after final reconciliation.
- [ ] Merge only after exact-head evidence is valid.
- [ ] Final main SHA recorded.

---

## 21. Fail-closed rules

When information is missing or uncertain:

- unknown target spec on client → omit exact target-mode/range guide;
- no local hit → neutral/no-candidate presentation;
- local entity hit → advisory candidate only;
- local block hit → advisory aim only, no mutation-permission claim;
- missing server preview contract → no server-valid marker;
- unknown result target → render result without target attribution;
- expired pending cast context → drop presentation correlation only;
- provider camera/API uncertain → no provider-specific bridge;
- protection state unavailable → do not guess allow/deny;
- target disappears → clear current candidate rather than keep ghost marker;
- dimension/session changes → clear all transient target presentation state.

Fail-closed here means withholding unsupported claims, not blocking a legitimate server cast merely because optional client presentation is absent.

---

## 22. Non-goals

05.13 does **not** authorize:

- client-authoritative targeting;
- client-authored authoritative block coordinates;
- client-side replication of `ServerEntityTargetSelector`;
- target-lock gameplay state without a separately approved server contract;
- aim assist that changes server targeting rules;
- automatic cast on target acquisition;
- hidden-entity/x-ray highlighting;
- per-frame entity/chunk/protection scans;
- per-frame target validation packets;
- inferred provider targeting contracts;
- monkey-patching external HUD/crosshair code;
- changing world-safety admission;
- exposing Corruption/Strain or unrelated withheld state;
- copying target UI/assets/code from another mod;
- claiming manual Stage 05 validation from automated CI.

---

## 23. Stage-state rule

Creating or merging this plan does **not** change Stage 05 from:

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

05.13 is a forward-looking Stage 05 refinement/authority gate.

It becomes mandatory only if:

- direct real-client validation reveals a targeting/readability/authority failure that requires it; or
- an explicit reviewed decision promotes a specific 05.13 refinement to required hardening.

Otherwise it may remain `OPTIONAL FOLLOW-UP` or be carried to Stage 09 according to the master-plan classification rules.

No manual PASS is inferred from this document, from a docs-only CI run or from the existence of a future targeting UI.

---

## 24. Definition of done for this planning substage

05.13 planning is complete when:

- current target kinds and server/client boundaries are documented from real code;
- `targetHint` is explicitly classified as advisory;
- local observation, server-authored preview and authoritative result semantics are separated;
- area/range/LOS/protection preview gates are explicit;
- stale/superseded target handling is defined;
- cast-result target misattribution is prohibited;
- WorldEffect admission remains server-owned;
- performance/privacy/accessibility/coexistence constraints are explicit;
- future test and real-client evidence requirements are defined;
- master/README index 05.13 without changing runtime status.

At that point the implementation team has an executable authority-safe plan without pretending that the client already possesses target truth it does not currently synchronize.
