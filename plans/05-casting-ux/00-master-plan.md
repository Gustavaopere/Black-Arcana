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
10. `10-loadout-editor-information-architecture.md` — dense ordered slot semantics, reordering, search, icon fallback, draft lifecycle, apply/reconciliation limits and the metadata/protocol gates for richer editor feedback.

This master plan defines how those documents fit together. Detailed implementation or validation work belongs in the corresponding subplan rather than being duplicated here.

## 5. Canonical player flow

### 5.1 Configure

Player opens the loadout editor through a rebindable mapping.

The editor operates on a **draft** only. `10-loadout-editor-information-architecture.md` defines how future slot awareness, reordering, search, icon use, reset and apply reconciliation must preserve the current dense ordered server model. Applying always sends a bounded complete ordered update request to the server; the synchronized server snapshot remains canonical.

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

### 5.4 Feedback

After intent, the client may present only synchronized or server-authored information:

- selection state;
- cooldown state where the selected spell can be bound to an authoritative synchronized cooldown group under `07-presentation-data-contracts.md`;
- predictable gate category where supported;
- danger tier and Arcane Resistance forecast where supported;
- authoritative cast success/denial feedback;
- bounded provider presentation data exposed through approved contracts.

The client must never infer a successful cast solely from local preflight.

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

### 6.4 Information hierarchy

The UI should prioritize in this order:

1. selected spell identity;
2. immediate inability to cast;
3. cooldown/readiness;
4. dangerous-spell risk information;
5. additional explanatory detail.

Verbose detail belongs in tooltips or `VERBOSE` presentation rather than competing with combat visibility.

### 6.5 Visual independence

Important state must not depend exclusively on color. Labels, icons, symbols or text should distinguish selected, unavailable, cooldown, danger and denial states even when color perception is limited.

`08-visual-language-state-semantics.md` is the canonical meaning layer for these cross-surface states. It prevents selection from being rendered as readiness, forecast from being rendered as authoritative result, warning from being rendered as hard block and missing art from being rendered as gameplay unavailability.

Keyboard focus introduced by future 05.09 work must use the `FOCUSED` semantic role from 05.08 and remain distinguishable from pointer hover and selected loadout state.

## 7. Planned UX refinements

The following are **planned refinements**, not claims about current runtime.

They may be implemented only through the subplans and only if they preserve the architecture above.

### 7.1 Use the synchronized spell icon

`SpellPresentationPayload.Entry` already carries `iconId`, but current loadout/radial rendering is primarily text/card based.

Plan:

- render server-authorized spell icons in loadout and radial surfaces;
- keep a text/name fallback when an icon cannot be resolved;
- never let missing client artwork invalidate spell identity or casting;
- keep resource identifiers bounded and presentation-only.

### 7.2 Improve loadout organization

`10-loadout-editor-information-architecture.md` is the canonical plan for this refinement.

Plan:

- expose current dense ordered positions 1–16 rather than pretending the server owns sixteen sparse cells;
- mark positions 1–8 only as eligible for the existing direct quick-cast mappings, not as number-row bindings;
- allow bounded local reordering of populated entries through the existing ordered full-list update contract;
- make removal compaction and trailing-slot addition semantics explicit;
- add bounded client-side search over synchronized display name/canonical id;
- keep provider/domain/school filters unavailable until real bounded server-authored metadata exists;
- use synchronized `iconId` with text fallback;
- define local dirty/reset/clear/cancel state without claiming server acceptance;
- preserve close-after-apply unless a robust explicit acknowledgement contract is deliberately added;
- never infer acceptance/rejection reason from snapshot equality.

### 7.3 Improve radial affordances

The original Stage 05 design target was a compact 6–10-slot ring; the implemented bound is eight visible slots per page.

Planned improvements may add:

- icon + short name on normal viewports;
- selected-state emphasis;
- cooldown/readiness affordance only after the selected spell can be mapped to its canonical server-authored cooldown group as required by `07-presentation-data-contracts.md`;
- static danger affordance where available;
- page indicator and keyboard/mouse navigation clarity;
- optional resource/cost summary only if a bounded server-authored presentation contract exists.

Nested domain/loadout navigation is **not** automatically approved. It should be added only if real usability testing shows paging is insufficient and the added hierarchy does not slow combat selection.

### 7.4 Expand contextual feedback carefully

The original Stage 05 candidate list included selected spell, short cooldown, provider-specific cost, charge/channel state, denial reason and temporary ritual/domain timers.

Current implementation already covers part of this surface. `07-presentation-data-contracts.md` is the authority/data-availability gate for the remaining items.

Future additions must satisfy these rules:

- cooldown: the current client receives cooldown-group snapshots, but generic per-spell display requires an authoritative spell→group mapping; never assume `groupId == spellId`;
- provider cost: do not recompute provider economics client-side; add a bounded presentation contract if exact preview is needed;
- channel/charge: display only server-owned state exposed through a bounded synchronization/lifecycle contract; local key duration is never authority;
- ritual/domain timers: only for Black Arcana-owned active state or a supported provider presentation seam, through an owner-specific bounded contract;
- Corruption/Strain values remain intentionally unsynchronized until separately approved;
- denial: display the server-authored bounded reason;
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
- cast result/denial: server-authored event result;
- hazard/gate forecast: bounded request/response, stale-response protected;
- cost/charge/channel/timer presentation: unavailable until the corresponding bounded server-authored contract exists;
- Corruption/Strain current values: intentionally absent until separately approved;
- client config: local presentation state only.

The current loadout snapshot reply proves canonical state, not an explicit accepted/rejected reason. Rich apply-result UX requires a separately reviewed bounded server-authored result contract; do not infer it from snapshot equality.

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
- no UI feature may trigger global server scans;
- icon lookup and text layout should be cached or bounded where profiling proves necessary.

## 11. Error and fail-closed policy

The UX must degrade safely.

Examples:

- missing presentation entry → canonical ID/name fallback, no gameplay denial invented;
- missing icon → text fallback;
- stale selected slot → reconcile to current synchronized loadout;
- invalid/empty screen focus → clear or clamp focus to a valid visible entry; never activate an off-page/stale item;
- rejected loadout update → server state wins, but do not invent the rejection reason when only a canonical snapshot is available;
- loadout draft search/filter hides an entry → draft membership/order remains unchanged;
- unavailable provider/domain/school metadata → omit those filters rather than infer from resource ids;
- cooldown group received without a valid selected-spell mapping → omit generic spell cooldown rather than guess;
- unavailable hazard forecast → show unavailable/static fallback, never partial value as complete;
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
9. add deterministic RED tests for pure/state behavior where applicable;
10. implement the minimum GREEN change;
11. add/adjust GameTests only where world/network integration requires them;
12. run full Black Arcana CI;
13. execute the specific real-client rows affected by visual/input behavior;
14. fetch `origin/main` again and reconcile;
15. rerun CI on the reconciled HEAD;
16. merge only after exact-head gates are green;
17. record final main SHA and any still-deferred manual rows.

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
- client-side cost/cooldown/progression decisions;
- automatic casting merely from radial selection or focus movement;
- sparse loadout slots without a separate canonical server migration;
- a duplicate Iron's/Ars spell execution engine;
- unbounded UI/network updates;
- forced gamepad dependencies;
- silent key remapping of other mods;
- copying third-party UI assets/code without compatible permission;
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
- synchronized `iconId` may be used with safe text fallback; missing art is presentation fallback, not gameplay unavailability;
- Clear, Reset and Cancel are distinct local draft operations until Apply;
- the current loadout reply is only a canonical snapshot and contains no request id, accepted/rejected flag or reason;
- snapshot equality must never be treated as proof of acceptance;
- explicit save/rejection messaging requires a future bounded server-authored result contract with correlation/stale handling;
- search text input must not cause existing Backspace/Delete/Enter screen shortcuts to fire accidentally;
- no editor refinement creates a second persistence store, cast path or provider authority.

05.10 is not automatically a Stage 05 completion blocker. Individual editor refinements become mandatory only when directly observed acceptance evidence or an explicit reviewed decision promotes them to required hardening.
