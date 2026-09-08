# 05 — Casting & UX Master Plan

## State

`PLANNING DOCUMENT / CURRENT RUNTIME IMPLEMENTED / FINAL REAL-CLIENT VALIDATION DEFERRED`

This file is the canonical planning map for `plans/05-casting-ux/`.

It does **not** claim that every UX enhancement described below already exists. The current deterministic Stage 05 runtime is implemented on `main`; the mandatory manual closeout remains governed by `05-final-client-validation-handoff.md` and `docs/qa/casting-ux-manual-matrix.md`.

Baseline used to author this plan: `main@cad9b133fc06048f718c6a408a7e9aca2c360364`.

Coexistence reconciliation baseline: `main@acbea2c897805e0d51476360c27adfd20fabfc64`.

Presentation-contract audit baseline: `main@ef867a59c3be52f0592618b23300507ed40e4241`.

Visual-semantics planning baseline: `main@019eb1723b7a70b9fd888ce44d1eb9b85dfa7b13`.

Keyboard-focus planning baseline: `main@2df7cdedd0a73b5aed87ca9709699e139355fc84`.

Loadout-editor planning baseline: `main@db7f4858b3c5eda3bba957db7de194228b6d4df6`.

Feedback-orchestration reconciliation baseline: `main@310c280419b49e5a57077e3460d956ac3dcd27e1`.

Iconography/resource-resolution planning baseline: `main@48cb9a430e0526899e8ae1588283b31de71cadfb`.

Targeting/aim planning audit baseline: `main@4ce5699cc76b511804956f903559ae8f7e44ba12`; reconciled with `main@5b343dbb91ff15a08ca3a09d1e4ca9ac177b3dd2` before indexing.

Spell-details/inspection planning audit baseline: `main@ede7dc310499ec21941504e8e6754d4f7c7f512e`.

Environment authority at this checkpoint:

- Minecraft `1.21.1`;
- NeoForge `21.1.248` from the current physical modlist;
- Java `21`;
- `Controlling 19.0.5` is present and may improve vanilla keybinding discovery, but Black Arcana must not require it for core input;
- `Spell Actionbar 1.1.4` is present as an external casting UI surface;
- `Iron's Spells 'n Spellbooks 1.21.1-3.16.3` is present as an external spell/resource provider;
- `Epic Fight 21.17.3.1` and `efiscompat 3.1.0` are present as combat/animation environment and Iron's-specific compatibility respectively;
- no top-level general controller framework such as Controlify/Controllable/MidnightControls was found in the current physical modlist, so gamepad-specific support is not a current guaranteed provider contract.

Presence/version does not establish an integration API. Direct bridges require exact-version API/source verification.

## 1. Purpose

Stage 05 exists to make Black Arcana usable in combat and exploration without transferring gameplay authority to the client.

The intended player experience is:

1. configure a bounded personal spell loadout;
2. select a spell quickly through a radial or direct slot workflow;
3. explicitly cast it through a dedicated input;
4. receive concise server-authored cooldown, danger, gate and denial feedback;
5. keep the screen clean while idle;
6. customize presentation without changing gameplay rules.

The UX should feel fast enough for active combat while remaining compatible with a large modpack that already has many keybindings, HUD elements and magic providers.

## 2. Non-negotiable architecture

All Stage 05 work preserves the canonical Black Arcana decisions:

- client input expresses intent only;
- the server validates spell identity, loadout slot, progression, cost, cooldown, target, hazard and world effects;
- selection is never equivalent to casting;
- no client preference changes damage, power, range, cost, cooldown, progression, Arcane Danger or world mutation;
- no second casting pipeline is created for radial, quick-cast, books, weapons, controller support or future UI surfaces;
- no permanent Black Arcana mana/resource bar is introduced by default;
- provider-specific resources remain owned by their provider;
- event-driven synchronization is preferred over per-tick full-state packets;
- GUI/HUD code remains physical-client-only and dedicated-server safe.

Relevant architectural decisions include D004, D005, D006, D019, D020, D023, D024, D029 and D031 in `plans/DECISIONS.md`.

## 3. Current verified runtime baseline

The plan must start from what actually exists.

### 3.1 Input

`BlackArcanaKeyMappings` currently registers:

- radial: default `R`;
- cast selected spell: default `V`;
- loadout editor: unbound by default;
- eight direct quick-cast mappings: all unbound by default.

All remain normal Minecraft key mappings and therefore rebindable.

### 3.2 Loadout bounds

The canonical cast request allows up to **16 loadout slots**.

Current client direct quick-cast bindings cover the first **8** slots. The radial also shows **8 slots per page**, so a full 16-slot loadout is represented as two radial pages.

This distinction is intentional factual baseline, not permission for the client to reinterpret slot ownership.

### 3.3 Loadout editor

The current editor:

- builds an unsaved client draft from the synchronized server loadout;
- lists available synchronized spells;
- toggles membership;
- prevents duplicate entries in the draft;
- enforces the absolute slot bound;
- sends an update request only when applied;
- closes after sending, while the accepted server state remains canonical.

The canonical loadout representation is an **ordered dense list**, not sixteen sparse nullable cells. Removing an entry compacts later positions; gaps between populated spells are not representable by the current server/protocol model.

### 3.4 Radial

The current radial:

- is client-only;
- renders up to eight slots per page;
- adapts its geometry to viewport size;
- supports `TOGGLE` and `HOLD` behavior;
- selects but never casts;
- shows synchronized static hazard/preflight information;
- supports compact fallback cards on very small viewports.

### 3.5 HUD

The current contextual HUD is event-driven and may show synchronized selection, cast-result, hazard-resistance and predictable-gate presentation. It does not create an always-visible Black Arcana resource bar.

Current selection identity and latest cast-result state are independently sourced. `CastResultPayload` carries `castId/status/code/detail`, but not spell id or loadout slot. Therefore current selected spell identity must not be treated as proven identity for the latest result when their timing overlaps. `11-contextual-feedback-orchestration.md` is the planning authority for hardening that association.

### 3.6 Client configuration

Current presentation-only options are:

- contextual HUD enabled/disabled;
- HUD scale;
- HUD anchor;
- selection duration;
- feedback duration;
- feedback level: `MINIMAL`, `STANDARD`, `VERBOSE`;
- radial behavior: `TOGGLE`, `HOLD`;
- particle density multiplier;
- reduced motion;
- reduced flashes.

### 3.7 Current screen keyboard behavior

Current Stage 05 screens already have partial keyboard support, but not complete keyboard-only navigation:

- radial: `Left`/`Page Up` and `Right`/`Page Down` change pages, while wedge hover/selection remains pointer-driven;
- loadout editor: Enter applies, Backspace/Delete clears the draft, and Left/Right/Page Up/Page Down change pages, while row focus/toggle remains pointer-driven.

`09-keyboard-focus-navigation.md` is the planning authority for completing keyboard-only focus/navigation without changing those existing semantics silently or creating new gameplay authority.

### 3.8 Current spell-icon presentation behavior

`SpellPresentationPayload.Entry` currently synchronizes:

- `spellId`;
- `translationKey`;
- `iconId`.

The current payload requires `iconId` to be non-blank and within `ArcanaProtocol.MAX_ICON_ID_LENGTH`, but the payload itself does not parse the string as a Minecraft resource identifier or prove that the referenced client resource exists.

Current `BlackArcanaRadialScreen`, `BlackArcanaLoadoutScreen` and `BlackArcanaHudLayer` consume presentation names but do not call `entry.iconId()` or render spell textures. At baseline `48cb9a43...`, `src/main/resources/assets/black_arcana/` contains only `lang/` and no project spell-icon texture tree.

`12-iconography-resource-resolution.md` is the planning authority for introducing safe client-side icon resolution/fallback later without changing spell identity or gameplay authority.

### 3.9 Current targeting/aim behavior

Current `ClientInputController.castSlot` reads `Minecraft.hitResult` and only emits a non-blank `targetHint` when the local hit is an `EntityHitResult`. That hint is encoded as an `ArcanaTargetReference.EntityRef` and remains advisory.

Current `ArcanaTargetSpec.Kind` values are exactly `SELF`, `ENTITY`, `RAY`, `BLOCK`, `CONE`, `SPHERE`, `CYLINDER`, `PROJECTILE` and `LINKED`. `ServerEntityTargetSelector` resolves these modes from live server state; explicit `ENTITY`/`PROJECTILE` paths may consult the advisory entity hint, while block/ray/area/linked paths remain server-resolved.

`CastResultPayload` contains `castId/status/code/detail` but no resolved target identity. `WorldEffectAdmissionService` plus `ConfigurableWorldEffectPolicy` remain authoritative for actual terrain work. Therefore the client currently has no generic server-authored target-validity/world-mutation-permission contract.

`13-targeting-aim-presentation.md` is the planning authority for future reticle/target/geometry presentation around that boundary.

### 3.10 Current spell-details/inspection behavior

The current generic synchronized spell presentation entry contains only `spellId`, `translationKey` and `iconId`.

The server-side `ArcanaSpellDefinition` additionally contains canonical `ArcanaCost cost` and `requestsWorldMutation`, but those server/runtime fields are **not** automatically client presentation data. Current generic presentation does not synchronize a long description, provider/domain/school classification, spell→cooldown-group relationship, target spec, charge/channel state, damage/effect magnitude or progression requirement.

The current loadout editor may show a synchronized hazard/preflight tooltip on pointer hover, while the current radial shows bounded spell-name/hazard context. Neither surface is a generic full spell dossier.

`14-spell-details-inspection-presentation.md` is the planning authority for any future richer tooltip/detail/inspection surface. It requires field-level authority classification, static-vs-dynamic separation and fail-closed omission rather than reconstructing runtime/provider facts from IDs or names.

## 4. Plan package

Stage 05 is divided into the following canonical planning documents:

1. `01-input-loadouts.md` — input lifecycle, slot semantics, loadout editing, persistence and synchronization;
2. `02-radial-wheel.md` — radial interaction, paging, visual affordances, selection/cast separation and compact layouts;
3. `03-contextual-hud.md` — selected-spell, cooldown/gate/hazard/result presentation and anti-clutter rules;
4. `04-accessibility-client-config.md` — rebindability, presentation preferences, motion/flash/particle policy and optional controller boundary;
5. `05-final-client-validation-handoff.md` — exact real-client closeout campaign;
6. `06-modpack-coexistence.md` — coexistence with installed casting/actionbar/combat/keybinding surfaces and exact-version integration gates;
7. `07-presentation-data-contracts.md` — audited server/client presentation authority, currently synchronized data and the contract gates for cooldown mapping, cost, charges, channels and timers;
8. `08-visual-language-state-semantics.md` — cross-surface meaning for selection/focus, forecast, authoritative result, danger, temporal state, unavailable/fallback presentation, accessibility and clean-room visual identity;
9. `09-keyboard-focus-navigation.md` — deterministic keyboard-only focus/navigation for radial and loadout screens while preserving current mouse behavior, server authority and global keybinding boundaries;
10. `10-loadout-editor-information-architecture.md` — dense ordered slot semantics, reordering, search, icon fallback, draft lifecycle, apply/reconciliation limits and the metadata/protocol gates for richer editor feedback;
11. `11-contextual-feedback-orchestration.md` — bounded arbitration, priority, supersession, correlation and timing across current selection context, advisory forecast and authoritative cast-result channels;
12. `12-iconography-resource-resolution.md` — synchronized spell-icon resource parsing/resolution, fallback, reload/cache lifecycle, namespace boundaries, accessibility and clean-room asset provenance;
13. `13-targeting-aim-presentation.md` — authority-safe reticle/aim/target presentation across current server target kinds, advisory target hints, stale-state/result correlation, world-safety boundaries, accessibility, performance and modpack coexistence;
14. `14-spell-details-inspection-presentation.md` — bounded spell inspection/details, field-level presentation authority, static/dynamic separation, provider/resource/cooldown/target/world/progression boundaries, localization, accessibility, performance and fail-closed behavior.

This master plan defines how those documents fit together. Detailed implementation or validation work belongs in the corresponding subplan rather than being duplicated here.

## 5. Canonical player flow

### 5.1 Configure

Player opens the loadout editor through a rebindable mapping.

The editor operates on a **draft** only. `10-loadout-editor-information-architecture.md` defines how future slot awareness, reordering, search, icon use, reset and apply reconciliation must preserve the current dense ordered server model. Applying always sends a bounded complete ordered update request to the server; the synchronized server snapshot remains canonical.

The loadout editor is also the preferred future surface for rich spell inspection under 05.14 because the player is already in a configuration context. Hover/focus/details interaction remains client-local presentation and must not toggle the draft or cast unless the existing explicit editor action is separately invoked.

### 5.2 Select

Player selects through one of these presentation paths:

- radial selection;
- a direct quick-slot mapping;
- selected-slot state reconciled against the current synchronized loadout.

Selection alone must not execute gameplay.

A future keyboard-focus layer may choose the radial slot that receives the existing selection operation, but moving focus itself remains client-local and non-casting.

### 5.3 Cast

An explicit cast input emits one bounded cast intent containing only canonical identity/intention fields. Authoritative values are resolved server-side.

Any future invocation surface — weapon, spellbook, staff, controller binding or accessibility shortcut — must terminate in the same canonical server cast pipeline rather than creating another execution route.

A local crosshair candidate or future reticle/geometry guide remains presentation under 05.13. It must never be promoted into target admission, resolved impact identity or world-safety authority merely because it was visible when the intent was emitted.

### 5.4 Feedback

After intent, the client may present only synchronized or server-authored information:

- selection state;
- cooldown state where the selected spell can be bound to an authoritative synchronized cooldown group under `07-presentation-data-contracts.md`;
- predictable gate category where supported;
- danger tier and Arcane Resistance forecast where supported;
- authoritative cast success/denial feedback;
- bounded provider presentation data exposed through approved contracts.

The client must never infer a successful cast solely from local preflight.

Selection context, advisory forecast and authoritative cast result are independent channels under `11-contextual-feedback-orchestration.md`. A result may render without spell attribution when the client cannot safely correlate its `castId` to the submitted spell/slot; it must never be labeled with the current selection by inference.

Target presentation follows the same anti-misattribution rule under 05.13: if the current aim changes before a result arrives, the result must not be visually attached to the new candidate, and the current `CastResultPayload` does not authorize target attribution by itself.

Spell icon art is supplemental presentation only. A synchronized `iconId` may be resolved under 05.12, but failed art resolution never changes canonical spell identity, selection, admission or cast result.

Spell inspection under 05.14 is similarly supplemental. Static description/detail metadata and dynamic forecast/readiness data must retain their own authority/lifetime; a rich panel never becomes a substitute for cast-time server validation.

## 6. UX principles

### 6.1 Combat speed

The common path should require as few actions as possible:

- radial → select → cast;
- or quick-cast slot → cast intent directly.

Opening the full loadout editor is configuration, not combat flow.

### 6.2 Low clutter

When the player is idle, Black Arcana should largely disappear from the screen.

Persistent bars, permanent spell panels and always-on explanatory text are avoided unless a later requirement demonstrates that contextual presentation is insufficient.

### 6.3 Explicit authority

A visual green/clear state means only what the server-authorized preview contract actually proves. `CLEAR` must not be presented as guaranteed cast success because target resolution, replay admission, world policy and hazard activation can still fail at cast time.

Likewise, a local reticle/entity/block observation under 05.13 may communicate aim/focus but must not use language or styling equivalent to “valid”, “allowed”, “safe” or “will hit” unless an explicit bounded server-authored contract proves that exact fact.

A detail line under 05.14 communicates only the fact its source contract owns. A configured cost does not prove affordability, a static target rule does not prove a current target, and a world-effect warning does not prove mutation permission.

### 6.4 Information hierarchy

The UI should prioritize in this order:

1. selected spell identity;
2. immediate inability to cast;
3. cooldown/readiness;
4. dangerous-spell risk information;
5. additional explanatory detail.

Verbose detail belongs in tooltips or `VERBOSE`/inspection presentation rather than competing with combat visibility. 05.14 is the authority for deciding what such inspection may legitimately contain.

For transient HUD arbitration specifically, 05.11 refines this generic information hierarchy: authoritative denial/result owns outcome emphasis over advisory forecast, while selected spell identity remains independent context rather than implicit result identity.

### 6.5 Visual independence

Important state must not depend exclusively on color. Labels, icons, symbols or text should distinguish selected, unavailable, cooldown, danger and denial states even when color perception is limited.

`08-visual-language-state-semantics.md` is the canonical meaning layer for these cross-surface states. It prevents selection from being rendered as readiness, forecast from being rendered as authoritative result, warning from being rendered as hard block and missing art from being rendered as gameplay unavailability.

Keyboard focus introduced by future 05.09 work must use the `FOCUSED` semantic role from 05.08 and remain distinguishable from pointer hover and selected loadout state.

Target/aim presentation introduced through 05.13 must likewise distinguish local observation from server-authored preview/result through redundant non-color-only cues.

Inspection/detail presentation introduced through 05.14 must distinguish static identity/detail, advisory/dynamic preview, authoritative result, unknown/unavailable data and presentation fallback without flattening them into one stat sheet.

## 7. Planned UX refinements

The following are **planned refinements**, not claims about current runtime.

They may be implemented only through the subplans and only if they preserve the architecture above.

### 7.1 Use the synchronized spell icon

`SpellPresentationPayload.Entry` already carries `iconId`, but current loadout/radial/HUD rendering does not consume it.

`12-iconography-resource-resolution.md` is the canonical resource lifecycle/fallback plan for this refinement.

Plan:

- parse/resolve only the synchronized bounded `iconId` through supported client resource semantics;
- render server-authored spell icon identity in loadout/radial surfaces where the resource actually resolves;
- keep a text/name fallback when an icon cannot be parsed or resolved;
- never infer a replacement texture path from the spell ID or provider namespace;
- never let missing client artwork invalidate spell identity or casting;
- invalidate positive/negative resolution assumptions on resource reload;
- keep provider artwork clean-room/provenance boundaries explicit;
- keep HUD icon use optional when it would compete with denial/danger readability or 05.11 result correlation.

### 7.2 Improve loadout organization

`10-loadout-editor-information-architecture.md` is the canonical plan for this refinement.

Plan:

- expose current dense ordered positions 1–16 rather than pretending the server owns sixteen sparse cells;
- mark positions 1–8 only as eligible for the existing direct quick-cast mappings, not as number-row bindings;
- allow bounded local reordering of populated entries through the existing ordered full-list update contract;
- make removal compaction and trailing-slot addition semantics explicit;
- add bounded client-side search over synchronized display name/canonical id;
- keep provider/domain/school filters unavailable until real bounded server-authored metadata exists;
- use synchronized `iconId` with 05.12-safe text fallback;
- define local dirty/reset/clear/cancel state without claiming server acceptance;
- preserve close-after-apply unless a robust explicit acknowledgement contract is deliberately added;
- never infer acceptance/rejection reason from snapshot equality.

### 7.3 Improve radial affordances

The original Stage 05 design target was a compact 6–10-slot ring; the implemented bound is eight visible slots per page.

Planned improvements may add:

- safely resolved icon + short name on normal viewports under 05.12;
- selected-state emphasis;
- cooldown/readiness affordance only after the selected spell can be mapped to its canonical server-authored cooldown group as required by `07-presentation-data-contracts.md`;
- static danger affordance where available;
- page indicator and keyboard/mouse navigation clarity;
- optional resource/cost summary only if a bounded server-authored presentation contract exists.

Nested domain/loadout navigation is **not** automatically approved. It should be added only if real usability testing shows paging is insufficient and the added hierarchy does not slow combat selection.

### 7.4 Expand contextual feedback carefully

The original Stage 05 candidate list included selected spell, short cooldown, provider-specific cost, charge/channel state, denial reason and temporary ritual/domain timers.

Current implementation already covers part of this surface. `07-presentation-data-contracts.md` is the authority/data-availability gate for the remaining items, while `11-contextual-feedback-orchestration.md` governs transient priority, lifetime, supersession and result/selection correlation.

Future additions must satisfy these rules:

- cooldown: the current client receives cooldown-group snapshots, but generic per-spell display requires an authoritative spell→group mapping; never assume `groupId == spellId`;
- provider cost: do not recompute provider economics client-side; add a bounded presentation contract if exact preview is needed;
- channel/charge: display only server-owned state exposed through a bounded synchronization/lifecycle contract; local key duration is never authority;
- ritual/domain timers: only for Black Arcana-owned active state or a supported provider presentation seam, through an owner-specific bounded contract;
- Corruption/Strain values remain intentionally unsynchronized until separately approved;
- denial: display the server-authored bounded reason;
- result identity: do not attribute a received result to the current selected spell without safe correlation;
- optional selected-spell icon: obey 05.12 and never let current-selection art imply a result association forbidden by 05.11;
- no permanent resource UI by default.

### 7.5 Accessibility completion

Reduced motion, reduced flashes and particle density are already configuration surfaces, but some effects are future-facing.

Plan:

- every new Black Arcana camera/screen/VFX effect must explicitly consume the appropriate preference;
- no essential gameplay information may exist only as a flash, shake, particle or sound;
- reduced modes may change presentation intensity, never gameplay outcome;
- missing or reset client config must recover to documented defaults;
- high-density text must remain bounded on small GUI scales.

### 7.6 Controller/gamepad boundary

The Stage 05 goal historically included controller/keybind accessibility where practical. The current physical modlist does not provide a confirmed general gamepad framework.

Therefore:

- keyboard/mouse rebindability is mandatory now;
- controller-specific integration is `OPTIONAL / PROVIDER-DEPENDENT`;
- do not invent a controller API;
- if a controller provider is later added, verify exact version/API first;
- controller actions must map to the same client intent methods and canonical server pipeline;
- absence or incompatibility must not break keyboard/mouse casting.

### 7.7 Unify visual meaning without forcing visual sameness

`08-visual-language-state-semantics.md` adds a cross-surface semantic contract.

Plan:

- define independent state families for focus/selection, admission/result, temporal state, hazard/risk, confidence and presentation fallback;
- allow orthogonal states to compose instead of flattening everything into one good/bad color;
- preserve the same semantic meaning across editor, radial and HUD even when each surface renders it differently;
- use redundant non-color-only cues for important state;
- keep provider-hosted external UI visually provider-owned while preserving Black Arcana meaning in its own contextual feedback;
- keep palette/assets/animation values as a later implementation/art-review concern rather than inventing them in planning;
- require clean-room provenance for any future visual/audio assets.

### 7.8 Complete keyboard-only screen navigation

`09-keyboard-focus-navigation.md` closes the planning gap between rebindable global casting input and pointer-dependent screen interaction.

Plan:

- keep focus/navigation state client-local and transient;
- do not add new global default mappings for the first implementation;
- preserve the radial's existing page controls and the loadout editor's existing Enter/apply, Delete/clear and page semantics unless a separately reviewed migration changes them;
- add deterministic keyboard focus over current bounded radial/loadout lists;
- activate a focused radial wedge through the existing selection path only, never a cast path;
- toggle a focused loadout row through the existing local `LoadoutDraft` operation, with network update only on apply;
- distinguish keyboard `FOCUSED`, pointer `HOVERED`, selected loadout state and draft membership under 05.08;
- preserve mouse behavior and the no-cast-through-screen invariant;
- keep future controller navigation provider-dependent and mapped to the same screen operations rather than new gameplay logic.

### 7.9 Targeting and aim presentation

`13-targeting-aim-presentation.md` closes the presentation gap around the already server-authoritative target resolver.

Plan:

- treat local crosshair/hit observation as responsive presentation only;
- preserve advisory `targetHint` semantics and the canonical server `TargetSelector` path;
- never infer target kind/range/LOS/friendly/world-policy truth from spell name, icon, namespace or local geometry when the required metadata is not synchronized;
- support future reticle/entity/block/area guides only from bounded legitimate data, with explicit uncertainty semantics;
- do not send network requests merely because the aim candidate changes;
- do not scan global entities/chunks or query protection systems per frame;
- never use current aim to attribute an older `CastResultPayload` to a target;
- preserve `WorldEffectAdmissionService`/`ConfigurableWorldEffectPolicy` authority for terrain work;
- prevent target UI from becoming an oracle for hidden/unloaded/protected information;
- keep important aim state non-color-only and compatible with reduced-motion/reduced-flash policy;
- coexist with Epic Fight, Iron's, Spell Actionbar and EFIS through Black Arcana-owned presentation only unless a real exact-version integration seam is verified.

### 7.10 Spell details and inspection presentation

`14-spell-details-inspection-presentation.md` closes the gap between the current compact combat UX and the need for richer explanatory spell information.

Plan:

- use the loadout editor as the primary candidate for rich inspection; keep radial/HUD detail concise;
- treat current synchronized `spellId`/`translationKey`/`iconId` as the baseline generic static presentation contract;
- do not expose `ArcanaSpellDefinition.cost`, `requestsWorldMutation` or other server/runtime facts merely by reaching into server objects from client GUI code;
- add description/cost/cooldown/target/provider/domain/progression fields only through explicit bounded presentation contracts when a real product need exists;
- preserve the difference between configured static facts, dynamic player-specific previews and authoritative cast results;
- never infer provider/domain/school, cooldown group, target mode, damage/effect magnitude or progression gates from names/namespaces/icons;
- keep provider resources/economics provider-owned and avoid duplicate bars/state;
- preserve 05.13 world/target authority: a world-effect warning is not mutation permission and a target rule is not current target validity;
- make long localization, keyboard focus, small viewports and non-color-only state first-class constraints;
- avoid per-hover network requests, runtime JAR/tooltip scraping, global scans and unbounded detail caches;
- keep provider descriptions/assets/UI clean-room and provider-owned unless rights/contracts explicitly allow reuse.

## 8. Input conflict policy for the large modpack

The pack has many mods and therefore many mappings.

Rules:

- keep only a minimal set of useful defaults;
- direct quick slots remain unbound by default unless a future deliberate keymap decision changes that;
- use vanilla `KeyMapping` registration so conflict-management mods can discover the keys naturally;
- do not require mouse side buttons;
- do not reserve large sequences of number keys by default;
- do not hijack provider keybindings from Iron's, Ars or other magic engines;
- future conflict-resolution UX remains presentation only and must not rewrite another mod's settings silently.

Screen-local focus traversal defined by 05.09 should not register additional global `KeyMapping`s merely to move focus while a Black Arcana `Screen` already owns input.

Inspection/details interaction under 05.14 should likewise remain screen-local where possible and must not create a new global default cast/details key without a separate demonstrated need.

## 9. Networking and state rules

Every UX addition must answer four questions before code is approved:

1. Who owns the state?
2. Does the client need a snapshot or only presentation metadata?
3. What is the payload bound?
4. What invalidates stale client state?

Expected defaults:

- loadout: server-owned persistent ordered dense snapshot;
- loadout draft/order/search state: client-local until Apply;
- selected slot: client presentation state reconciled against server loadout;
- screen focus/input modality: client-local transient state scoped to the open screen; no server synchronization;
- cooldown: server-owned synchronized group snapshot; per-spell presentation additionally requires the authoritative spell→group relationship defined by `07-presentation-data-contracts.md`;
- cast result/denial: server-authored event result identified by `castId`;
- optional pending cast-result correlation: bounded client-local presentation context keyed by emitted `castId`, never gameplay authority;
- hazard/gate forecast: bounded request/response, stale-response protected and scoped to spell/request/preflight;
- spell icon identity: bounded synchronized `iconId`; actual resource syntax/existence remains client presentation resolution under 05.12;
- static spell inspection identity: current generic contract is `spellId` + `translationKey` + `iconId`; richer detail fields remain unavailable until explicitly synchronized under 05.07/05.14;
- inspected spell/focus and formatted static detail cache: client-local presentation state only, reconciled against current synchronized snapshots and cleared/invalidated on relevant screen/session/language/resource changes;
- local aim/crosshair observation: client-local transient presentation only;
- current `targetHint`: bounded advisory intent data, not target authority;
- generic target kind/range/LOS/geometry validity: unavailable to presentation unless the required bounded authoritative data is actually synchronized;
- resolved target identity/impact: not proven by current `CastResultPayload`;
- cost/charge/channel/timer presentation: unavailable until the corresponding bounded server-authored contract exists;
- server `ArcanaSpellDefinition.cost`/`requestsWorldMutation`: server/runtime facts, not generic client presentation data merely because the fields exist;
- long description/provider/domain/school/damage/progression detail: absent from the current generic spell presentation entry and must not be inferred;
- Corruption/Strain current values: intentionally absent until separately approved;
- client config: local presentation state only.

The current loadout snapshot reply proves canonical state, not an explicit accepted/rejected reason. Rich apply-result UX requires a separately reviewed bounded server-authored result contract; do not infer it from snapshot equality.

The current cast-result payload proves status/code/detail for its `castId`, not the identity of the client's current selection or current aim target. Unknown/unmatched result ids remain valid authoritative results but must not receive guessed spell/slot/target attribution.

Static inspection metadata and dynamic preview/result state must not share one ambiguous cache/lifetime. A dynamic hazard/gate/provider preview never becomes permanent definition text simply because a details screen remains open.

Do not add per-tick full-state synchronization.

## 10. Performance budgets

Stage 05 is not allowed to become a client or server tick-cost sink.

- input polling may inspect registered mappings but must not scan world entities/chunks;
- radial/loadout rendering works from local synchronized snapshots;
- keyboard focus traversal operates only on the already bounded screen-local list and must not trigger world/provider scans or server requests;
- loadout search/sort/filter operates only on the bounded synchronized presentation set and must not perform per-keystroke networking;
- loadout reorder operates over at most 16 entries;
- HUD rendering is contextual and returns early while inactive;
- forecast refresh must remain bounded/rate-limited and stale-response protected;
- any future pending-result correlation/dedup cache must be bounded by count and age and cleared on session reset;
- icon resolution must not perform per-frame filesystem/JAR scans, remote downloads or unbounded cache growth, and any positive/negative cache must respect resource reload;
- aim/reticle rendering may use bounded local observation but must not send per-frame target-preview requests, enumerate global entities/chunks or probe protection adapters every frame;
- spell inspection must render primarily from bounded synchronized snapshots; pointer/focus traversal must not request a full server dossier per hover, scrape provider tooltips/JARs or build unbounded formatted-detail/history caches;
- dynamic inspection previews, if ever required, must be rate-limited/correlated/stale-safe rather than hover-driven spam;
- no UI feature may trigger global server scans;
- icon lookup and text layout should be cached or bounded where profiling proves necessary.

## 11. Error and fail-closed policy

The UX must degrade safely.

Examples:

- missing presentation entry → canonical ID/name fallback, no gameplay denial invented;
- malformed/unresolvable `iconId` → 05.12 text/presentation fallback, never an invented path, blocked state or screen-breaking exception;
- missing description/detail field → omit it rather than synthesizing lore/mechanics;
- server runtime field exists but is not presentation-authorized → omit it rather than reading server internals from client UI;
- stale selected slot → reconcile to current synchronized loadout;
- stale/removed inspected spell → reconcile or clear inspection without mutating gameplay/draft state;
- invalid/empty screen focus → clear or clamp focus to a valid visible entry; never activate an off-page/stale item;
- rejected loadout update → server state wins, but do not invent the rejection reason when only a canonical snapshot is available;
- loadout draft search/filter hides an entry → draft membership/order remains unchanged;
- unavailable provider/domain/school metadata → omit those filters/details rather than infer from resource ids;
- cooldown group received without a valid selected-spell mapping → omit generic spell cooldown rather than guess;
- configured cost not synchronized for presentation → omit raw cost; current provider affordability is never inferred from a static descriptor;
- unavailable hazard forecast → show unavailable/static fallback, never partial value as complete;
- authoritative result with unknown/unmatched `castId` → render generic result without guessed spell/slot attribution;
- local aim candidate changes before result → keep the new aim current but do not attach the old result to it;
- target kind/range/geometry metadata unavailable → omit exact target-volume/validity claims rather than reconstruct server rules client-side;
- world/protection preview unavailable → do not imply mutation permission or reveal protected/hidden state;
- provider preview unavailable → omit or label unavailable;
- network/session reset → clear stale client state before new snapshots;
- incompatible optional integration → disable only that presentation seam.

05.08 additionally requires that a presentation fallback remain visually distinct from gameplay unavailability: broken/missing art must not be rendered as a blocked spell, and unknown data must not be rendered as success/readiness.

## 12. Implementation order for any remaining Stage 05 work

When a planned refinement is approved for implementation:

1. fetch latest `origin/main` and record SHA;
2. verify no concurrent PR owns the same Stage 05 surface;
3. read this master plan and the relevant subplan;
4. inspect current runtime/tests rather than relying on old branch history;
5. for new presentation data, classify authority/current synchronization through `07-presentation-data-contracts.md` before changing protocol/UI;
6. for any cross-surface visual state, classify its semantic family/meaning through `08-visual-language-state-semantics.md` before rendering;
7. for keyboard/focus changes, preserve current screen-key contracts and use `09-keyboard-focus-navigation.md` to define focus lifecycle/activation before editing input handling;
8. for loadout-editor changes, preserve dense ordered-list semantics and use `10-loadout-editor-information-architecture.md` before editing draft/order/search/apply behavior;
9. for contextual-feedback changes, preserve independent selection/advisory/result channels and use `11-contextual-feedback-orchestration.md` before editing result correlation, timing, priority or dedup behavior;
10. for spell-icon/resource changes, use `12-iconography-resource-resolution.md` before adding resource lookup, cache/reload behavior or bundled icon assets;
11. for reticle/aim/target-presentation changes, use `13-targeting-aim-presentation.md` before adding target overlays, geometry guides, target-preview synchronization or result/target attribution;
12. for spell-tooltip/detail/inspection changes, use `14-spell-details-inspection-presentation.md` before exposing new static/dynamic fields, provider facts, descriptions or detail caching;
13. add deterministic RED tests for pure/state behavior where applicable;
14. implement the minimum GREEN change;
15. add/adjust GameTests only where world/network integration requires them;
16. run full Black Arcana CI;
17. execute the specific real-client rows affected by visual/input behavior;
18. fetch `origin/main` again and reconcile;
19. rerun CI on the reconciled HEAD;
20. merge only after exact-head gates are green;
21. record final main SHA and any still-deferred manual rows.

## 13. Stage 05 completion rule

Stage 05 may be described as `VALIDATED / COMPLETE` only when:

- the intended deterministic runtime remains present;
- all applicable automated gates are green;
- all applicable rows in `docs/qa/casting-ux-manual-matrix.md` have direct evidence;
- legitimate future-only rows are explicitly carried to Stage 09 rather than falsely passed;
- no unresolved Stage 05 regression remains;
- final evidence is tied to the exact tested build/SHA.

Creating this plan does not change the current status by itself.

## 14. Non-goals

This plan does not authorize:

- a second mana bar;
- client-authoritative casting;
- client-authoritative target resolution, target legality or world-safety decisions;
- client-side cost/cooldown/progression decisions;
- automatic casting merely from radial selection or focus movement;
- sparse loadout slots without a separate canonical server migration;
- an unbounded cast-result/history queue or notification feed;
- a duplicate Iron's/Ars spell execution engine;
- unbounded UI/network updates;
- runtime downloading or arbitrary-filesystem loading of spell art;
- per-frame target-preview/protection/world scans;
- using target presentation as an oracle for hidden/unloaded/protected information;
- treating server runtime fields as client spell-detail data without an explicit presentation contract;
- per-hover full server dossiers, provider-tooltip scraping or private reflection for inspection;
- reconstructing damage/cost/cooldown/target/progression/provider truth from spell IDs, names, namespaces or icons;
- copying third-party descriptions/tooltips/assets/layout trade dress without compatible permission and provenance;
- forced gamepad dependencies;
- silent key remapping of other mods;
- copying third-party UI/assets/code without compatible permission and provenance;
- reopening already-frozen server runtime contracts without an explicit architectural decision.

## 15. Current modpack coexistence rule

The installed pack already contains casting and combat UI surfaces that can overlap Stage 05 presentation.

`06-modpack-coexistence.md` is the canonical plan for this layer.

The default strategy is:

- **coexist, do not duplicate**;
- Black Arcana remains transient/contextual while installed provider action bars retain their own state;
- no Spell Actionbar integration is assumed from presence alone;
- EFIS compatibility for Iron's does not imply a Black Arcana↔Epic Fight bridge;
- Controlling may improve key discovery but is not required;
- no controller API is assumed while no controller provider is physically present;
- direct interoperability code is added only after a real conflict/requirement and exact-version API verification.

Real-pack coexistence findings may become Stage 05 blockers only when they break required input/readability/authority; cosmetic unification remains an optional follow-up.

## 16. Presentation data authority rule

`07-presentation-data-contracts.md` is the canonical plan for deciding whether a planned HUD/radial/loadout datum is currently safe to render or requires a new server-authored contract first.

Current audited boundary:

- spell id/name/icon, accepted loadout, authoritative cast result and existing hazard presentation are available through current bounded synchronization;
- the current generic spell presentation entry does not include a long description, provider/domain/school classification, target spec, progression requirement, damage/effect magnitude, static `ArcanaCost`, `requestsWorldMutation` or spell→cooldown-group relationship;
- `ArcanaSpellDefinition` containing `cost`/`requestsWorldMutation` on the server does not itself authorize client presentation of those fields;
- cooldown snapshots are authoritative by canonical `groupId`, but the current spell presentation payload does not synchronize the spell→cooldown-group relationship, so a generic per-spell cooldown widget must not guess that mapping;
- exact resource/cost preview, charge-pool state, active channel progress and generic ritual/domain timers do not currently have sufficient Stage 05 client contracts;
- Corruption/Strain current values remain intentionally withheld pending separate approval;
- external-provider resources/cooldowns remain provider-owned unless an exact supported presentation seam is deliberately adopted;
- all future synchronization remains bounded, versioned, event-driven, stale-safe and presentation-only.

Missing optional presentation data does not by itself reopen Stage 05 or convert the current manual-validation state. A contract becomes required only if explicitly promoted or needed to fix a directly observed acceptance failure.

## 17. Visual-language and state-semantics rule

`08-visual-language-state-semantics.md` is the canonical meaning layer **after** Section 16 establishes that a datum is legitimate to present.

Current planning rule:

- selection/focus describes interaction identity, never cast legality;
- a server-authored forecast is visually and verbally distinct from an authoritative cast result;
- warning/recommendation state is distinct from a hard blocking state;
- meeting a danger recommendation never means the spell is safe from all Backlash/Corruption risk;
- `DANGER_PRESENT` applies only to synchronized non-`NORMAL` danger tiers; a synchronized `NORMAL` profile does not activate danger styling;
- temporal UI such as cooldown/charges/channels/timers remains unavailable until Section 16/05.07 authorizes the corresponding data contract;
- missing artwork/translation is presentation fallback, not gameplay unavailability;
- unavailable/unknown data is never filled with a guessed ready/success state;
- important state must not rely exclusively on color, motion, flashes, particles or audio;
- editor, radial and HUD may render the same semantic role differently, but they must not assign it contradictory meanings;
- provider-hosted/external UI remains visually provider-owned while Black Arcana retains its own transaction and contextual-feedback semantics;
- new Black Arcana visual/audio assets remain subject to clean-room provenance and compatible licensing/permission.

05.08 is not automatically a Stage 05 completion blocker. A semantic refinement becomes mandatory only when directly observed validation demonstrates a required readability/ambiguity failure or an explicit reviewed decision promotes it to required hardening.

## 18. Keyboard-focus and screen-navigation rule

`09-keyboard-focus-navigation.md` is the canonical planning layer for completing keyboard-only interaction inside Stage 05 screens.

Current planning rule:

- focus is client-local transient state and is never synchronized as gameplay state;
- radial keyboard focus is distinct from pointer hover and selected loadout state;
- loadout row focus is distinct from local draft membership and accepted server loadout state;
- moving focus never casts, mutates server state or sends a network request;
- activating a focused radial wedge must reuse the existing non-casting selection operation;
- activating a focused loadout row must reuse the existing local draft-toggle operation;
- current screen-local page/apply/clear controls are preserved unless a separately reviewed UX migration explicitly changes them;
- the first implementation should use screen-local navigation keys rather than adding global default mappings;
- radial `Tab`/`Shift+Tab` traversal wraps only within the current visible page and never changes page;
- loadout `Up`/`Down` traversal clamps within the current page and never wraps or changes page;
- closing a radial through `TOGGLE`, `HOLD` release or Escape must not implicitly select the focused wedge;
- a Stage 05 screen owning focus must continue suppressing normal world cast input;
- mouse behavior remains supported and pointer/keyboard modality may coexist without collapsing `HOVERED`, `FOCUSED` and `SELECTED` semantics;
- controller navigation remains optional/provider-dependent and, if later added, maps to the same screen operations rather than a new cast engine.

05.09 is not automatically a Stage 05 completion blocker. Keyboard-only hardening becomes mandatory only if the manual accessibility requirements or direct real-client evidence promote the missing interaction to a required fix.

## 19. Loadout-editor information-architecture rule

`10-loadout-editor-information-architecture.md` is the canonical planning layer for future loadout-editor organization and apply-state hardening.

Current planning rule:

- the canonical loadout remains a dense ordered list of at most 16 unique spells;
- gaps between populated positions are not representable and must not be faked client-side;
- positions 1–8 are merely eligible for the existing direct quick-cast mappings, which remain unbound by default;
- positions 9–16 are equally valid loadout positions without current direct quick-cast mappings;
- the existing ordered full-list update path already preserves valid reorder operations, so basic populated-entry reordering does not require a protocol schema change;
- adding appends to trailing unused capacity and removing compacts later entries unless a future canonical server representation changes;
- search may operate locally on synchronized display-name/canonical-id data without changing draft order or server availability;
- provider/domain/school filtering remains unavailable until those fields exist as bounded server-authored presentation metadata;
- synchronized `iconId` may be used only through the 05.12 safe resolution/fallback lifecycle; missing art is presentation fallback, not gameplay unavailability;
- Clear, Reset and Cancel are distinct local draft operations until Apply;
- the current loadout reply is only a canonical snapshot and contains no request id, accepted/rejected flag or reason;
- snapshot equality must never be treated as proof of acceptance;
- explicit save/rejection messaging requires a future bounded server-authored result contract with correlation/stale handling;
- search text input must not cause existing Backspace/Delete/Enter screen shortcuts to fire accidentally;
- no editor refinement creates a second persistence store, cast path or provider authority.

05.10 is not automatically a Stage 05 completion blocker. Individual editor refinements become mandatory only when directly observed acceptance evidence or an explicit reviewed decision promotes them to required hardening.

## 20. Contextual-feedback orchestration rule

`11-contextual-feedback-orchestration.md` is the canonical planning layer for transient Stage 05 feedback arbitration.

Current planning rule:

- selection context, advisory forecast and authoritative cast result are independent bounded channels rather than one ambiguous HUD state;
- authoritative denial/result owns outcome emphasis over predictive/advisory forecast, but advisory context is not rewritten to look like it authored the result;
- `CastResultPayload` currently carries `castId/status/code/detail` without spell id or loadout slot;
- a received result must never be visually attributed to the current selected spell merely because that selection is visible at the same time;
- current bounded result behavior remains **latest received result wins**; Stage 05 does not add an unbounded history or notification queue;
- forecast remains correlated by spell id, request id and matching static preflight values and cannot overwrite authoritative result semantics;
- an optional future no-protocol hardening may keep a small bounded client-local `castId -> attempted spell/slot/send tick` presentation context;
- such client correlation proves only which local intent generated the id and is never admission, replay, cost, cooldown, target or spell-runtime authority for the server;
- an unknown/unmatched result id remains a valid authoritative result but renders without guessed spell/slot attribution;
- any presentation-correlation/dedup record must be bounded by count/age and cleared on disconnect/session reset;
- opening another `Screen` hides the contextual HUD but does not pause or extend selection/result display windows;
- no new protocol field is required merely because this plan exists; a server-authored spell/slot result extension requires a separate reviewed contract if later product requirements demand it.

05.11 is not automatically a Stage 05 completion blocker. Correlation/orchestration hardening becomes mandatory only when a direct validation failure or an explicit reviewed decision promotes the observed presentation race to required work.

## 21. Iconography and resource-resolution rule

`12-iconography-resource-resolution.md` is the canonical planning layer for turning synchronized spell icon metadata into client artwork safely.

Current planning rule:

- canonical spell identity remains `spellId`; icon art is never identity or gameplay authority;
- `SpellPresentationPayload.Entry.iconId` is synchronized, non-blank and length-bounded, but the current payload does not itself parse it as a Minecraft resource identifier or prove resource existence;
- current radial, loadout editor and HUD do not consume `iconId`, so icon rendering remains future work;
- future icon rendering parses/resolves only the explicit synchronized identifier through supported client resource semantics;
- no spell-ID-to-texture, namespace-to-provider or translation-key-to-resource heuristic is allowed when resolution fails;
- malformed, missing or disappearing icon resources degrade to 05.08 `PRESENTATION_FALLBACK`, preserving text/name and all gameplay state;
- positive and negative resource-resolution assumptions must be invalidated appropriately on resource reload;
- a changed synchronized `(spellId, iconId)` association invalidates stale presentation for that spell;
- no per-frame filesystem/JAR scan, remote download, arbitrary filesystem access or unbounded cache is allowed;
- provider namespace/resource presence does not create an integration API, transfer gameplay authority or grant redistribution permission;
- provider artwork must not be copied/recolored/traced/bundled without compatible rights and recorded provenance;
- Black Arcana-owned assets should be original/provenance-safe and remain subject to `SOURCES.md`, `THIRD_PARTY_NOTICES.md` and Stage 09 provenance review;
- radial/editor may consume resolved icons while retaining complete text fallback; HUD icon use remains optional and subordinate to 05.03/05.11 readability/correlation;
- any resolver/reload implementation remains physical-client-only and dedicated-server safe.

05.12 is not automatically a Stage 05 completion blocker. Icon/resource hardening becomes mandatory only when an explicit reviewed decision or direct validation failure promotes the refinement to required work. Creating 05.12 does not add icon assets, runtime code or manual PASS evidence.

## 22. Targeting and aim presentation rule

`13-targeting-aim-presentation.md` is the canonical planning layer for reticle, aim candidate, target marker and target-geometry presentation around the current server-owned targeting runtime.

Current planning rule:

- `ArcanaTargetReference` is the server-resolved target representation; it is not a license for client-authored authoritative target coordinates;
- current `ArcanaTargetSpec.Kind` values are `SELF`, `ENTITY`, `RAY`, `BLOCK`, `CONE`, `SPHERE`, `CYLINDER`, `PROJECTILE` and `LINKED`;
- current `ClientInputController` only emits an advisory entity `targetHint` from local `EntityHitResult`; other target modes remain server-resolved;
- `ArcanaCastIngressService` explicitly preserves advisory target-hint semantics and feeds the canonical server cast engine;
- `ServerEntityTargetSelector` resolves target candidates from live server state with bounded range/LOS/player/friendly/loaded-chunk behavior appropriate to each target path;
- a local crosshair candidate, block outline, ray line or area guide is therefore presentation only unless a future bounded server-authored preview contract proves a stronger fact;
- the current `CastResultPayload` does not carry resolved target identity, so result-to-target attribution must never follow the current crosshair by inference;
- `WorldEffectAdmissionService` plus `ConfigurableWorldEffectPolicy`, loaded-chunk guards, world-effect profiles/budgets and protection gateways remain execution-time world-safety authority;
- target UI must not imply mutation permission or expose hidden/unloaded/protected information through speculative probing;
- target/aim presentation must not send per-frame network requests, perform global entity/chunk scans or query protection adapters every render frame;
- local observation, any future server-authored preview and authoritative result must remain semantically distinct and stale-safe;
- important target state must remain understandable without relying only on red/green color, pulsing, flashes, particles or audio;
- Epic Fight, Iron's, Spell Actionbar and EFIS remain owners of their own UI/combat surfaces; Black Arcana must not monkey-patch or assume integration APIs from presence alone;
- future target marker/reticle assets remain clean-room/provenance-safe and provider art is not copied/recolored/traced/bundled without compatible rights.

05.13 is not automatically a Stage 05 completion blocker. Target/aim hardening becomes mandatory only when a direct real-client acceptance failure or explicit reviewed decision promotes a specific refinement. Creating 05.13 does not add reticles, overlays, protocol fields, target locks, assets, runtime behavior or manual PASS evidence.

## 23. Spell details and inspection presentation rule

`14-spell-details-inspection-presentation.md` is the canonical planning layer for richer tooltip/detail/inspection presentation without turning server/runtime/provider internals into client authority.

Current planning rule:

- current generic `SpellPresentationPayload.Entry` contains only `spellId`, `translationKey` and `iconId`;
- `ArcanaSpellDefinition` additionally contains server-side `cost` and `requestsWorldMutation`, but their existence does not make them generic client presentation data;
- the current loadout hover tooltip is hazard/preflight-specific and the radial exposes bounded name/hazard context; neither is a full spell dossier;
- the loadout editor is the preferred future rich-inspection surface, while radial/HUD remain concise and low-clutter;
- each desired detail field must be classified as synchronized static presentation, future bounded server-authored static detail, dynamic server-authored preview, authoritative event result, provider-owned external detail or unavailable/unknown;
- static configured cost is distinct from current affordability and provider resources remain provider-owned;
- per-spell cooldown requires the authoritative spell→group relationship; `groupId == spellId` must never be assumed;
- charges/channels/timers remain server-owned and unavailable until a bounded lifecycle/presentation contract exists;
- target/range/LOS/world-effect details remain subject to 05.13/Stage 04 authority; a rule/warning is not current target validity or mutation permission;
- long description/provider/domain/school/damage/progression fields are absent from the current generic presentation entry and must not be inferred from names, namespaces, icons or wiki text;
- existing hazard/gate forecast may be composed only with its existing bounded correlation/staleness semantics and never cached as immutable spell definition;
- current Corruption/Strain values remain intentionally withheld until separately approved;
- pointer/keyboard inspection changes presentation only and cannot cast or mutate the loadout draft implicitly;
- descriptions/labels must be localized/bounded, and important states remain non-color-only and small-viewport safe;
- inspection should be snapshot-driven; no per-hover full-server request, provider-tooltip scraping, private reflection, filesystem/JAR scanning or unbounded history/cache;
- provider descriptions/assets/layout remain provider-owned/clean-room unless compatible rights and explicit integration contracts permit use;
- missing detail fails closed by omission/unavailable presentation and never blocks a legitimate server cast merely because optional UI data is absent.

05.14 is not automatically a Stage 05 completion blocker. Spell-inspection hardening becomes mandatory only when a direct real-client acceptance failure or explicit reviewed decision promotes a specific refinement. Creating 05.14 does not add description metadata, detail UI, new payload fields, provider adapters, assets, runtime behavior or manual PASS evidence.