# 05.07 — Presentation Data Contracts

## State

`PLANNING / NO RUNTIME CHANGE / SERVER-AUTHORED PRESENTATION BOUNDARIES`

This document defines which Casting & UX data the current client may present safely, which current contracts are incomplete for the intended UI, and which future presentation refinements require a new bounded server-authored synchronization contract before implementation.

Baseline audited for this plan: `main@ef867a59c3be52f0592618b23300507ed40e4241`.

This file is planning only. It does **not** add packets, registries, HUD elements, timers, charge bars, cost previews, cooldown mappings or provider integrations.

## 1. Purpose

Stage 05 already has a working server-authoritative cast flow and a contextual client presentation layer. Several planned UX refinements, however, require more data than the client currently receives.

The purpose of this plan is to prevent a common failure mode: implementing a visually useful HUD by silently reconstructing server gameplay state on the client.

Every planned presentation datum must therefore be classified before implementation as one of:

1. `AVAILABLE NOW / PRESENTATION-SAFE` — current synchronized state is sufficient for the intended display;
2. `AVAILABLE SERVER-SIDE / CLIENT MAPPING INCOMPLETE` — relevant server state exists, but the client lacks a safe identity mapping needed to display it for the selected spell;
3. `SERVER-OWNED / NOT SYNCHRONIZED` — authoritative runtime state exists but no current client presentation contract exposes it;
4. `PROVIDER-OWNED / DO NOT DUPLICATE` — the state belongs to another provider and Black Arcana must not mirror it without an explicit supported seam;
5. `INTENTIONALLY WITHHELD` — the state is deliberately not synchronized until a separate bounded contract is approved.

The classification is an authority gate, not a visual-design preference.

## 2. Architectural authority

This plan preserves the existing decisions in `plans/DECISIONS.md`:

- D004 — no mandatory second Black Arcana mana pool/HUD;
- D006 — server authority over legality, costs, cooldowns, progression, targeting and world effects;
- D018 — cooldowns are keyed by caster plus canonical cooldown group;
- D019 — target legality and geometry use server-computed facts;
- D020 — client payloads contain bounded identity/intention rather than authoritative gameplay values reconstructed by the client;
- D021 — datapack presentation metadata is declarative, not executable gameplay authority;
- D023 — synchronization is event-driven rather than a full per-tick state stream;
- D024 — charge/channel sessions are server-owned and release converges on the canonical cast engine;
- D029 — Arcane Danger extends the same canonical cast transaction rather than creating a parallel path;
- D031 — missing real-client evidence remains explicit and is never inferred from automated evidence.

No data contract described here transfers gameplay authority to Stage 05 client code.

## 3. Audited current presentation matrix

The following matrix is based on production code present on the audited `main`, not on old planning assumptions.

| Presentation datum | Current authoritative/runtime source | Current client contract | Classification | Current safe use |
|---|---|---|---|---|
| Spell identity | `ArcanaSpellDefinition.id()` | `SpellPresentationPayload.Entry.spellId` | `AVAILABLE NOW / PRESENTATION-SAFE` | resolve synchronized spell identity |
| Display name | `ArcanaSpellDefinition.translationKey()` | `SpellPresentationPayload.Entry.translationKey` | `AVAILABLE NOW / PRESENTATION-SAFE` | localized label with canonical-ID fallback |
| Spell icon id | `ArcanaSpellDefinition.iconId()` | `SpellPresentationPayload.Entry.iconId` | `AVAILABLE NOW / PRESENTATION-SAFE` | icon lookup with text fallback |
| Accepted loadout | server loadout/persistence | `LoadoutSnapshotPayload` cached by `ClientArcanaSyncState` | `AVAILABLE NOW / PRESENTATION-SAFE` | editor/radial selection reconciliation |
| Cast result / denial | canonical server cast result | `CastResultPayload` | `AVAILABLE NOW / PRESENTATION-SAFE` | authoritative bounded result feedback |
| Static danger preflight | server danger-profile synchronization | `HazardPreflightPayload` | `AVAILABLE NOW / PRESENTATION-SAFE` | danger tier / minimum-recommended metadata |
| Dynamic Arcane Resistance forecast | bounded server forecast request/response | `HazardResistanceForecastPayload` with stale-response protections | `AVAILABLE NOW / PRESENTATION-SAFE` | current forecast when it still matches static metadata |
| Predictable gate category | canonical bounded server gate forecast already used by Stage 05/05A presentation | existing server-authored forecast surface | `AVAILABLE NOW / PRESENTATION-SAFE WITH CURRENT BOUNDS` | category only; `CLEAR` is not guaranteed cast success |
| Cooldown group state | server cooldown service | `CooldownSnapshotPayload.Entry(groupId, remainingTicks)` | `AVAILABLE SERVER-SIDE / CLIENT MAPPING INCOMPLETE` | group snapshot may be cached, but generic selected-spell cooldown display is not yet authorized |
| Spell → cooldown group mapping | `ArcanaCooldownPolicyRegistry` maps `ArcanaSpellId` to `ArcanaCooldownSpec` | no current field in `SpellPresentationPayload` exposes the mapping | `SERVER-OWNED / NOT SYNCHRONIZED` | none for a generic per-spell cooldown widget |
| Exact resource/cost preview | canonical cost providers / `ArcanaSpellDefinition.cost()` and provider runtime | not present in `SpellPresentationPayload` | `SERVER-OWNED OR PROVIDER-OWNED / NOT SYNCHRONIZED` | omit or show unavailable; never duplicate formulas client-side |
| Charge policy/state | `ArcanaCooldownPolicyRegistry`, `ArcanaChargeSpec`, server charge service | no charge snapshot payload in the current network package | `SERVER-OWNED / NOT SYNCHRONIZED` | none |
| Active channel session/progress | `ArcanaChannelManager` + `ArcanaChannelSpec` | no channel-session payload in the current network package | `SERVER-OWNED / NOT SYNCHRONIZED` | none as authoritative progress |
| Black Arcana ritual/domain remaining timer | Black Arcana-owned active runtime where applicable | no generic Stage 05 ritual/domain timer payload | `SERVER-OWNED / NOT SYNCHRONIZED` | none through Stage 05 today |
| Corruption / Strain current values | Black Arcana persistent hazard state | intentionally absent from current Stage 05 client synchronization | `INTENTIONALLY WITHHELD` | do not expose until separately approved |
| Live target legality | server targeting/world/protection facts | no generic authoritative live-target stream | `SERVER-OWNED / PRIVACY-SENSITIVE` | use bounded forecast/denial only where a current contract exists |
| External-provider mana/cooldowns | external provider | provider-owned UI/contracts | `PROVIDER-OWNED / DO NOT DUPLICATE` | leave with provider unless an exact supported integration contract requires otherwise |

## 4. Spell identity, display name and icon

### Current contract

`SpellPresentationPayload.Entry` currently contains exactly:

- `spellId`;
- `translationKey`;
- `iconId`.

The payload is protocol-versioned and bounded by `ArcanaProtocol` limits.

### Planning disposition

The planned icon refinement can use the existing synchronized `iconId` without adding gameplay authority.

Rules:

- failure to resolve an icon is a presentation failure only;
- text/canonical-id fallback remains mandatory;
- missing artwork must never invalidate a cast;
- the client must not infer domain, school, provider, cost or cooldown policy from icon path conventions;
- adding new metadata such as domain/provider labels requires an explicit synchronized presentation field rather than filename heuristics.

Status: `READY FOR OPTIONAL PRESENTATION IMPLEMENTATION` if separately approved.

## 5. Cooldown presentation

### 5.1 What exists

The current server cooldown policy registry maps a spell id to an `ArcanaCooldownSpec`.

That spec contains:

- canonical `groupId`;
- `durationTicks`;
- persistent flag.

The current client cooldown snapshot contains only:

- `groupId`;
- `remainingTicks`.

D018 explicitly allows shared canonical cooldown groups. Therefore `groupId == spellId` is **not** a valid client assumption.

### 5.2 Current gap

`SpellPresentationPayload` does not currently expose a selected spell's cooldown-group mapping.

As a result, the presence of `CooldownSnapshotPayload` does not by itself authorize a generic radial/HUD implementation to look up the selected spell by its spell id in the cooldown map.

Doing so would work only accidentally for policies whose group id happens to equal the spell id and would break shared/renamed groups.

### 5.3 Required future contract

Before generic per-spell cooldown/readiness is implemented, the client needs a bounded server-authored relationship between spell identity and the canonical cooldown group.

Acceptable planning shapes include either:

- extending synchronized spell presentation metadata with an optional canonical cooldown-group id; or
- sending a resolved per-spell cooldown presentation entry that already binds spell id to its authoritative group state.

This plan does not choose the Java packet/class implementation.

Required properties:

- spell id and group id both bounded and validated;
- shared groups represented explicitly;
- reload/group migration invalidates stale mapping;
- a new server snapshot always supersedes client extrapolation;
- no client cooldown value may affect cast admission.

### 5.4 Countdown extrapolation

After a valid server-authored mapping exists, the client may visually decrement a received `remainingTicks` value between snapshots as **presentation-only estimation**.

It must not interpret local zero as authoritative permission to cast. The next cast still goes through the server cooldown gate.

Status: `BLOCKED ON PRESENTATION MAPPING CONTRACT` for generic spell cooldown affordance.

## 6. Provider-resource and cost preview

### 6.1 What exists

`ArcanaSpellDefinition` contains an `ArcanaCost`, and the canonical cast pipeline resolves real cost through Black Arcana-owned cost-provider boundaries.

Stage 07 `SpellImplementationSpec.resourceCost` is descriptive implementation metadata only. Its own contract states that gameplay authority remains in the server runtime.

Neither source authorizes the client to duplicate provider formulas.

### 6.2 Why a string from planning/specification is insufficient

An exact cost may depend on:

- the provider that owns the resource;
- server config;
- progression/perk modifiers;
- composite resource policies;
- inventory/health/provider state;
- availability or compatibility of an optional integration;
- operation-specific ownership such as a Black Arcana-owned spell hosted by Iron's.

A descriptive wiki/spec value can be useful documentation but is not a live server preview.

### 6.3 Required future contract

If exact cost preview is promoted to an approved UX requirement, the server must provide a bounded **presentation result**, not a client formula.

The future contract should distinguish at minimum:

- exact preview available;
- preview unavailable;
- provider/authority label where safe and useful;
- one or more bounded display components for composite costs;
- staleness/revision identity where provider/config changes can alter the preview.

The preview must never reserve, debit or commit a resource.

### 6.4 Iron-hosted Black Arcana nuance

For a Black Arcana-owned spell hosted by Iron's, such as the existing `black_arcana:irons_integration_probe` route:

- Iron's owns the supported host registration/presentation/invocation surface;
- Black Arcana owns validation and its transactional cost settlement;
- Iron's native mana is neutralized for that Black Arcana-owned transaction to prevent double charge;
- a future Black Arcana cost preview must therefore describe the Black Arcana transaction, not blindly display Iron's normal native spell mana semantics.

For unrelated Iron's-owned spells, Iron's remains authority for its own resource/cost UI.

Status: `BLOCKED ON BOUNDED SERVER/PROVIDER PREVIEW CONTRACT` for exact Black Arcana HUD cost display.

## 7. Charge pools

### 7.1 What exists

The server has:

- `ArcanaChargeSpec` with canonical group id, maximum charges, recharge ticks and persistence;
- an absolute maximum of 16 charges per spec;
- server cooldown/charge policy mapping;
- server-owned charge runtime/persistence services.

### 7.2 What the client lacks

The audited network package has no charge-state snapshot payload and `ClientArcanaSyncState` stores no charge pool state.

Therefore the client cannot authoritatively display:

- available charges;
- maximum charges;
- recharge progress;
- next recharge boundary;
- shared charge-group relationships.

### 7.3 Required future contract

If charge display is approved, synchronize a bounded event-driven view containing enough server-authored state to display the pool without reproducing recharge authority on the client.

Candidate planning fields may include:

- canonical charge group id;
- spell id mapping where needed for UI lookup;
- available charges;
- maximum charges;
- remaining ticks to the next recharge or an equivalent bounded server time anchor;
- revision/session information required to reject stale state.

Synchronization should occur on events such as login/session establishment, consumption, recharge transition, policy reload/migration and other state-changing boundaries. It must not become a full per-tick charge stream.

Status: `BLOCKED ON CHARGE PRESENTATION CONTRACT`.

## 8. Channel / charge-to-release presentation

### 8.1 What exists

`ArcanaChannelManager` owns active channel sessions by caster and stores server facts including:

- cast id;
- spell id;
- loadout slot;
- server start tick;
- `ArcanaChannelSpec`.

`ArcanaChannelSpec` defines server-owned minimum and maximum channel duration. Release computes elapsed time from server ticks and then converges on the canonical cast engine under D024.

### 8.2 What the client lacks

There is no current channel-session payload in the audited network package and no active channel session in `ClientArcanaSyncState`.

Local key-down duration therefore cannot be promoted to authoritative channel progress.

### 8.3 Required future lifecycle contract

If an approved spell needs a visible channel bar, the client should receive a bounded server-authored lifecycle rather than reconstructing session ownership locally.

Candidate conceptual data:

- session/cast identity;
- spell id;
- accepted server start anchor;
- minimum channel threshold;
- maximum channel threshold;
- lifecycle state such as accepted, cancelled, released or expired.

The exact wire format remains an implementation decision.

Rules:

- begin must be acknowledged by server-owned state before the UI labels the session authoritative;
- local elapsed time may animate between server facts but remains presentation only;
- cancel/release/expiry from the server wins immediately;
- disconnect/session change clears the presentation;
- one client key lifecycle must not create a second cast pipeline;
- release still enters the canonical coordinator exactly once.

Status: `BLOCKED ON CHANNEL LIFECYCLE PRESENTATION CONTRACT`.

## 9. Ritual and domain timers

Black Arcana now has downstream ritual/domain runtime state on `main`, but Stage 05 does not currently expose a generic synchronized timer contract for those systems.

A visual timer may be added only for state whose owner can provide a bounded authoritative presentation seam.

### Black Arcana-owned state

A future timer contract may expose a bounded active-state identity plus remaining duration/server end boundary where the owning runtime can do so safely.

The HUD must not:

- scan entities/chunks for ritual/domain markers;
- infer remaining duration from particles;
- infer start time from the first client-observed entity/block;
- force chunks to remain loaded for presentation;
- extend or refresh the runtime state merely because its timer is visible.

### External-provider state

For provider-owned rituals, fields or timers:

- verify exact provider version/API first;
- use only a supported presentation seam;
- do not mirror a provider timer from observation when no contract exists;
- absence/incompatibility disables only that optional presentation feature.

Status: `BLOCKED ON OWNER-SPECIFIC TIMER CONTRACT`.

## 10. Corruption and Strain values

`plans/STATUS.md` explicitly records that Corruption/Strain client values are intentionally absent until a bounded server-authored synchronization contract is separately approved.

This plan preserves that decision.

Therefore:

- do not add current Corruption value to Stage 05 merely because the server persists it;
- do not add current Strain value to Stage 05 merely because the server persists it;
- do not calculate either from cast history on the client;
- do not expose provider/equipment facts that would allow a client reconstruction to be treated as authority;
- a future synchronization proposal must define why the player needs the value, its privacy/abuse surface, bounds, update frequency, stale-state policy and relationship to Stage 05A.

Status: `INTENTIONALLY WITHHELD / SEPARATE APPROVAL REQUIRED`.

## 11. Targeting and hidden-information boundary

The client may know what it is visually aiming at, but D019 makes target legality a server-owned fact.

A future target affordance must not leak or infer:

- hidden/invisible player state not otherwise available;
- protected-area facts beyond a bounded response intended for the caster;
- claim/team/PvP relationships from client guesses;
- unloaded entity/chunk information;
- linked-target lists that the server has not authorized.

Current authoritative denial and existing bounded forecast categories remain the preferred presentation path.

A live green reticle may never mean guaranteed success unless an explicit future server contract proves exactly the subset being represented, and even then later gates may still deny the final cast.

## 12. External-provider ownership and deduplication

`06-modpack-coexistence.md` remains canonical for installed UI/provider coexistence.

This data plan adds one rule: **visibility is not ownership**.

If Spell Actionbar, Iron's, Ars Nouveau or another installed UI can display a resource, cooldown or spell state, Black Arcana does not gain authority to mirror that state merely because it is visible to the player.

For every future provider-backed preview, record:

1. which spell/operation owns the transaction;
2. which provider owns the underlying state;
3. which exact supported seam exposes presentation data;
4. whether Black Arcana is presenting its own operation or duplicating an unrelated provider operation;
5. how double-processing/double-charge/double-cooldown is prevented;
6. how absence/version drift fails closed.

The existing Iron-hosted Black Arcana route remains the critical mixed-ownership example: host UI ownership does not transfer the Black Arcana transaction to Iron's.

## 13. Future contract design rules

Any new Stage 05 presentation synchronization must satisfy all of the following before implementation is approved.

### 13.1 Bounded payloads

Define hard limits for:

- entry count;
- identifier length;
- display text/translation identifiers;
- numeric ranges;
- timer/cooldown duration;
- optional composite cost components.

Reject malformed or over-limit data rather than truncating authoritative identity silently.

### 13.2 Protocol versioning

New wire state must participate in the existing versioned protocol strategy or an explicitly reviewed compatible extension.

Do not add an unversioned side channel for convenience.

### 13.3 Event-driven updates

Preserve D023.

Preferred update triggers include:

- login/session establishment;
- accepted metadata reload;
- successful cast/state mutation;
- charge consume/recharge transition;
- channel lifecycle transition;
- owned timer creation/update/termination where the update is actually needed;
- provider availability/config revision where safely observable.

Do not send a full presentation snapshot every tick.

### 13.4 Stale-state identity

Any datum that can become invalid while displayed must define its invalidation key.

Depending on the surface, that can require:

- spell id;
- group id;
- cast/session id;
- request sequence;
- registry/reload revision;
- player session identity.

Reconnect must clear state from the previous player/session before new snapshots arrive.

### 13.5 No provider implementation leakage

Common/client presentation contracts must contain Black Arcana-owned DTO/value data, not optional-provider implementation classes.

An adapter may translate provider state into a bounded Black Arcana presentation value only through a verified seam.

### 13.6 Preview is never settlement

No presentation request may:

- reserve resources;
- consume charges;
- start cooldowns;
- activate hazard state;
- mutate progression;
- perform world effects;
- create an authoritative cast merely to discover whether it would work.

Preview APIs must remain side-effect-free or use a separately designed safe projection contract.

## 14. Candidate future presentation shapes

The following are **conceptual schemas for later design**, not existing Java classes and not an instruction to implement all of them.

### 14.1 Resolved spell-state presentation

A spell-keyed bounded view could contain optional presentation fields such as:

- spell id;
- cooldown group id and current remaining ticks;
- charge group id, available/max charges and next-recharge presentation;
- optional bounded cost-preview result;
- revision/session token.

A single aggregate packet is not automatically preferred. Separate event-driven streams may be safer when state ownership/lifecycles differ.

### 14.2 Channel lifecycle presentation

A channel event/view could carry:

- cast/session id;
- spell id;
- accepted server timing anchors;
- minimum/maximum channel bounds;
- lifecycle transition.

The client animates; the server decides.

### 14.3 Owned active-effect timer presentation

An owned active-state timer view could contain:

- stable active-state identity;
- bounded type/display identity;
- server-authored remaining/end-time presentation;
- lifecycle transition;
- optional icon/translation metadata.

It must not become a universal world-entity tracker.

## 15. Rendering policy by confidence

Stage 05 surfaces should represent confidence explicitly.

### Authoritative current fact

Examples:

- synchronized spell identity;
- server cast denial;
- accepted loadout snapshot;
- newly received cooldown-group remaining ticks.

May be presented directly.

### Server-authored forecast

Examples:

- current resistance forecast;
- predictable gate category.

Must be labeled/worded as forecast where appropriate and must respect stale-response rules.

### Client interpolation

Examples:

- visual countdown between two server cooldown snapshots;
- visual channel bar movement between accepted server lifecycle facts.

May improve smoothness but cannot grant gameplay authority.

### Unavailable

When no supported contract exists, omit the datum or show a concise unavailable state. Never fill the gap with guessed provider state.

## 16. Implementation gate for each planned refinement

Before code is written for a new Stage 05 datum:

1. fetch latest `origin/main` and record SHA;
2. confirm no concurrent PR owns the same presentation/network surface;
3. identify the exact runtime authority;
4. cite the current code/provider seam that supplies the value;
5. classify the datum using Section 1;
6. if a new contract is required, define payload bounds and stale-state semantics first;
7. write deterministic RED tests for codec/state/revision behavior where applicable;
8. implement minimal GREEN without creating a second gameplay authority;
9. run networking/common-side tests and dedicated-server classloading checks;
10. run the complete Black Arcana CI;
11. execute affected real-client Stage 05 rows;
12. re-fetch `origin/main`, reconcile, and revalidate exact HEAD before merge.

A planned visual refinement is not permission to alter frozen cast, cooldown, cost, hazard or provider authority semantics.

## 17. Validation plan for future presentation contracts

### Automated

For each new contract, test as applicable:

- protocol/version rejection;
- maximum entry/string/numeric bounds;
- duplicate identity rejection;
- stale revision/sequence rejection;
- reconnect/session clearing;
- reload invalidation;
- shared cooldown/charge groups;
- unavailable provider behavior;
- side-effect-free preview behavior;
- dedicated-server startup without client-only class loading.

### Real client

For each rendered feature, verify:

- the value matches the authoritative server transition that produced it;
- old values disappear after reconnect/reload/state replacement;
- interpolation never visually becomes a promise of cast success;
- small viewport/GUI scale remains readable;
- external provider/actionbar overlap remains acceptable;
- unavailable provider data degrades without crashes or invented values;
- F1/hidden-GUI and configured Stage 05 presentation behavior remain coherent.

Manual evidence must be attached to the exact tested build. CI does not substitute for visual/input acceptance.

## 18. Relationship to Stage 05 completion

Creating this plan does not reopen completed deterministic Stage 05 runtime work and does not change Stage 05 from `IMPLEMENTED / FINAL VALIDATION DEFERRED`.

The refinements classified here remain optional/planned unless a real-client validation failure or an explicit design decision promotes one to a required fix.

Therefore:

- missing cost/charge/channel/timer UI is not automatically a Stage 05 blocker;
- a currently required manual row remains governed by `05-final-client-validation-handoff.md`;
- if a validation failure requires one of these contracts, that specific contract becomes `REQUIRED TO FIX A VALIDATION FAIL` and must then be implemented/tested before the affected row can pass;
- other future presentation work may remain `OPTIONAL FOLLOW-UP` or be carried into Stage 09.

## 19. Non-goals

This plan does not authorize:

- a new permanent Black Arcana mana bar;
- a client-side cost calculator;
- `groupId == spellId` cooldown assumptions;
- client-owned charge/recharge state;
- client-owned channel duration;
- per-tick full-state networking;
- ritual/domain world scans for timer inference;
- Corruption/Strain synchronization without separate approval;
- provider resource/cooldown mirroring from unrelated spells;
- a new provider adapter without exact-version seam verification;
- changes to `ArcanaCastEngine`, cost settlement, cooldown semantics, Arcane Danger, WorldEffectPolicy or provider authority;
- any runtime change merely because this planning document exists.

## 20. Exit criteria for this planning task

05.07 is planning-complete when:

- every currently desired Stage 05 presentation datum is classified by authority and current client availability;
- the cooldown group mapping gap is explicit and no spell-id shortcut is permitted;
- exact cost preview is blocked from client-side/provider-formula duplication;
- charge and channel UI are blocked until bounded server-owned contracts exist;
- ritual/domain timer presentation is owner-specific and world-scan-free;
- Corruption/Strain remain intentionally withheld unless separately approved;
- mixed Iron-host/Black Arcana transaction authority is preserved;
- future synchronization is bounded, versioned, event-driven and stale-safe;
- the Stage 05 validation state remains unchanged;
- no Java/runtime/network implementation is included in this planning change.
