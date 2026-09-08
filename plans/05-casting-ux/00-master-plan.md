# 05 — Casting & UX Master Plan

## State

`PLANNING DOCUMENT / CURRENT RUNTIME IMPLEMENTED / FINAL REAL-CLIENT VALIDATION DEFERRED`

This file is the canonical planning map for `plans/05-casting-ux/`.

It does **not** claim that every UX enhancement described below already exists. The current deterministic Stage 05 runtime is implemented on `main`; the mandatory manual closeout remains governed by `05-final-client-validation-handoff.md` and `docs/qa/casting-ux-manual-matrix.md`.

Baseline used to author this plan: `main@cad9b133fc06048f718c6a408a7e9aca2c360364`.

Coexistence reconciliation baseline: `main@acbea2c897805e0d51476360c27adfd20fabfc64`.

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

## 4. Plan package

Stage 05 is divided into the following canonical planning documents:

1. `01-input-loadouts.md` — input lifecycle, slot semantics, loadout editing, persistence and synchronization;
2. `02-radial-wheel.md` — radial interaction, paging, visual affordances, selection/cast separation and compact layouts;
3. `03-contextual-hud.md` — selected-spell, cooldown/gate/hazard/result presentation and anti-clutter rules;
4. `04-accessibility-client-config.md` — rebindability, presentation preferences, motion/flash/particle policy and optional controller boundary;
5. `05-final-client-validation-handoff.md` — exact real-client closeout campaign;
6. `06-modpack-coexistence.md` — coexistence with installed casting/actionbar/combat/keybinding surfaces and exact-version integration gates.

This master plan defines how those documents fit together. Detailed implementation or validation work belongs in the corresponding subplan rather than being duplicated here.

## 5. Canonical player flow

### 5.1 Configure

Player opens the loadout editor through a rebindable mapping.

The editor operates on a **draft** only. It may improve filtering, search, icons and ordering in future work, but applying always sends a bounded update request to the server. The UI must converge on the subsequently synchronized accepted state.

### 5.2 Select

Player selects through one of these presentation paths:

- radial selection;
- a direct quick-slot mapping;
- selected-slot state reconciled against the current synchronized loadout.

Selection alone must not execute gameplay.

### 5.3 Cast

An explicit cast input emits one bounded cast intent containing only canonical identity/intention fields. Authoritative values are resolved server-side.

Any future invocation surface — weapon, spellbook, staff, controller binding or accessibility shortcut — must terminate in the same canonical server cast pipeline rather than creating another execution route.

### 5.4 Feedback

After intent, the client may present only synchronized or server-authored information:

- selection state;
- cooldown state where synchronized;
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

The current editor is a bounded membership list. Planned UX improvements may include:

- search by synchronized display name;
- provider/domain/school grouping only when that metadata is actually available from a supported presentation contract;
- explicit slot ordering/reordering while preserving the 16-slot server bound;
- clear indication of which first-eight slots have direct quick-cast mappings;
- icons plus concise hazard metadata;
- server rejection feedback after apply rather than optimistic authority.

No grouping label may be invented from client heuristics when provider metadata is absent.

### 7.3 Improve radial affordances

The original Stage 05 design target was a compact 6–10-slot ring; the implemented bound is eight visible slots per page.

Planned improvements may add:

- icon + short name on normal viewports;
- selected-state emphasis;
- cooldown/readiness affordance using synchronized cooldown data;
- static danger affordance where available;
- page indicator and keyboard/mouse navigation clarity;
- optional resource/cost summary only if a bounded server-authored presentation contract exists.

Nested domain/loadout navigation is **not** automatically approved. It should be added only if real usability testing shows paging is insufficient and the added hierarchy does not slow combat selection.

### 7.4 Expand contextual feedback carefully

The original Stage 05 candidate list included selected spell, short cooldown, provider-specific cost, charge/channel state, denial reason and temporary ritual/domain timers.

Current implementation already covers part of this surface. Future additions must satisfy these rules:

- cooldown: use synchronized server state;
- provider cost: do not recompute provider economics client-side; add a bounded presentation contract if exact preview is needed;
- channel/charge: display only server-owned session state or bounded client prediction explicitly labeled as presentation;
- ritual/domain timers: only for Black Arcana-owned active state or a supported provider presentation seam;
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

## 9. Networking and state rules

Every UX addition must answer four questions before code is approved:

1. Who owns the state?
2. Does the client need a snapshot or only presentation metadata?
3. What is the payload bound?
4. What invalidates stale client state?

Expected defaults:

- loadout: server-owned persistent snapshot;
- selected slot: client presentation state reconciled against server loadout;
- cooldown: server-owned synchronized snapshot;
- cast result/denial: server-authored event result;
- hazard/gate forecast: bounded request/response, stale-response protected;
- client config: local presentation state only.

Do not add per-tick full-state synchronization.

## 10. Performance budgets

Stage 05 is not allowed to become a client or server tick-cost sink.

- input polling may inspect registered mappings but must not scan world entities/chunks;
- radial/loadout rendering works from local synchronized snapshots;
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
- rejected loadout update → server state wins;
- unavailable hazard forecast → show unavailable/static fallback, never partial value as complete;
- provider preview unavailable → omit or label unavailable;
- network/session reset → clear stale client state before new snapshots;
- incompatible optional integration → disable only that presentation seam.

## 12. Implementation order for any remaining Stage 05 work

When a planned refinement is approved for implementation:

1. fetch latest `origin/main` and record SHA;
2. verify no concurrent PR owns the same Stage 05 surface;
3. read this master plan and the relevant subplan;
4. inspect current runtime/tests rather than relying on old branch history;
5. add deterministic RED tests for pure/state behavior where applicable;
6. implement the minimum GREEN change;
7. add/adjust GameTests only where world/network integration requires them;
8. run full Black Arcana CI;
9. execute the specific real-client rows affected by visual/input behavior;
10. fetch `origin/main` again and reconcile;
11. rerun CI on the reconciled HEAD;
12. merge only after exact-head gates are green;
13. record final main SHA and any still-deferred manual rows.

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
- automatic casting merely from radial selection;
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
