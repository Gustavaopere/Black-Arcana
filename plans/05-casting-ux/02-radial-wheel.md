# 05.02 — Radial Wheel

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

This document preserves the current radial contract and defines the plan for any remaining radial-selection refinement. Anything labeled planned is not an implementation claim.

## Goal

Provide a compact, fast spell selector for active combat without turning the selector into a client-side casting engine or permanently occupying screen space.

The radial must make a full bounded loadout navigable while keeping the common selection path short.

## Current canonical contract

- `BlackArcanaRadialScreen` renders the synchronized loadout and server-authored presentation/preflight metadata.
- `RadialLayout.SLOTS_PER_PAGE` is **8**.
- A 16-slot canonical loadout therefore spans at most two current radial pages.
- `RadialLayout` adapts geometry to viewport size and exposes a compact card fallback for very small viewports.
- Selection is non-casting: left-click changes `ClientLoadoutSelection`, marks contextual UX state and closes the wheel. A separate explicit cast input is required.
- Toggle and hold behavior are client-configurable; selection/config state never grants gameplay authority.
- `TOGGLE` allows the open key to close the screen predictably.
- `HOLD` closes the radial when the radial key is released.
- Page navigation is available through left/right or Page Up/Page Down.
- Unavailable/gated information is presentation derived from synchronized server state, not a client admission decision.
- The radial never force-loads or queries world state to decide cast legality.

## Current rendering baseline

Normal viewports currently use bounded cards around the ring with:

- slot number;
- short spell display name;
- selected/hovered visual states;
- center title;
- static synchronized hazard/preflight line;
- page indicator when multiple pages exist.

Compact viewports reduce cards to slot numbers and expose the focused spell name through a tooltip.

## Interaction model

### Open

Open only when:

- a client player exists;
- no other `Screen` owns focus;
- the synchronized loadout is non-empty.

### Hover

Hover is client presentation state only. It may change visual emphasis and preview presentation but cannot send a cast.

### Select

A valid click selects the canonical loadout slot and closes the radial.

### Cast

Casting remains a separate explicit input after selection.

### Close

Close must release/restore normal input predictably and must not leave a stuck key or cursor state.

## UX geometry requirements

### Normal viewport

Target:

- eight visible sectors maximum;
- center remains readable;
- slot cards do not overlap each other;
- mouse hit sectors align with visual wedge/card positions;
- outer hit radius does not extend into unrelated screen regions excessively;
- text truncates/bounds instead of leaving the viewport.

### Small viewport

The compact fallback may reduce text density, but must preserve:

- slot identity;
- selected/hovered feedback;
- usable hit regions;
- focused spell identification;
- ability to close/page/select.

### Ultrawide

The radial remains centered rather than scaling its radius with full monitor width.

## Planned radial refinements

The following are `PLANNED / NOT YET CLAIMED AS IMPLEMENTED`.

### 1. Render synchronized spell icons

`SpellPresentationPayload.Entry` already carries `iconId`.

Plan:

- render icon + short name on normal cards;
- use icon + slot number when space is constrained;
- retain text fallback for unresolved/missing icon resources;
- keep icon failure presentation-only;
- never allow a missing icon to remove or re-identify a spell.

### 2. Cooldown/readiness affordance

The radial may show a compact cooldown/readiness affordance only from synchronized server-owned cooldown state.

Preferred presentation hierarchy:

- ready: no extra clutter or a subtle ready marker;
- cooling down: compact numeric/arc/overlay indicator;
- unknown/stale: omit rather than guess.

No local timer may be treated as authoritative unless it is explicitly derived from a synchronized server boundary and bounded against stale snapshots.

### 3. Danger affordance

Dangerous spells may expose the already synchronized static hazard tier/preflight through a concise marker.

Rules:

- use icon/symbol/text in addition to color;
- do not imply recommended Arcane Resistance guarantees safety;
- keep detailed current/minimum/recommended values in center/tooltip/HUD rather than every wedge;
- if forecast data is unavailable, static danger metadata may remain while current resistance is omitted.

### 4. Provider-resource/cost affordance

The original Stage 05 target included resource/cost information.

Do **not** derive cost from client-side provider rules.

If this refinement is approved:

1. identify whether an existing synchronized bounded presentation contract already exposes enough data;
2. if not, design a server-authored presentation field/payload with strict size bounds;
3. keep provider economy authority with the provider/server;
4. display `Unavailable`/omit when exact preview cannot be proven.

### 5. Keyboard-only radial selection

Current page navigation supports keyboard, but wedge selection is mouse-driven.

Planned accessibility improvement:

- define a deterministic keyboard selection path that does not conflict with direct quick-cast mappings;
- preserve the rule that selecting is not casting;
- ensure keyboard focus cannot become stuck after close;
- avoid introducing hidden default key conflicts.

Do not choose a concrete default mapping until the current modlist keymap is audited.

### 6. Page transition clarity

A full 16-slot loadout can span two pages.

Plan:

- make current page visually explicit;
- preserve selected slot when switching pages;
- start on the page containing the selected slot;
- keep paging inputs predictable in both `TOGGLE` and `HOLD` modes.

### 7. Nested navigation remains conditional

The original design allowed nested domain/loadout navigation only if usability remained fast.

Current policy:

- do not add nested domains merely because 16 slots exist;
- two-page radial paging is the baseline;
- only introduce hierarchy if real-client evidence shows paging is insufficient;
- any hierarchy metadata must be server-authored/supported, not inferred from IDs;
- no extra hierarchy may add a second cast path.

## Presentation state model

Each visible slot should conceptually distinguish these independent facts:

- `SELECTED` — current client selection;
- `HOVERED` — current pointer/focus;
- `READY/COOLDOWN` — synchronized cooldown presentation when available;
- `DANGEROUS` — synchronized static hazard metadata when applicable;
- `PREVIEW UNAVAILABLE` — current forecast/gate presentation unavailable;
- `MISSING ART` — icon fallback only, never gameplay state.

Do not collapse all of these into one color code.

## Authority rules

The radial may not:

- execute the spell on selection;
- alter server loadout state;
- decide cooldown legality;
- decide resource legality;
- decide progression eligibility;
- resolve targets;
- force-load chunks;
- synthesize a provider cost;
- change Arcane Danger state;
- create a local fallback cast when networking/provider state is unavailable.

## Performance plan

Rendering should operate entirely on already-synchronized/local presentation snapshots.

- no world entity scan during render;
- no chunk lookup during render;
- no per-frame network request;
- no forecast request solely because the mouse crosses every wedge unless a separate bounded request policy explicitly permits it;
- text/icon layout remains bounded by visible eight-slot page size.

## Automated coverage

`RadialLayoutTest`, `RadialToggleInputTest` and `SmallViewportLayoutContractTest` cover layout, toggle semantics and small-view geometry. PR #57 additionally hardened 854×480 / GUI-scale-4 behavior and passed exact-SHA full CI at workflow `34010968124` (#1170).

## Test plan for future radial work

### Pure/unit

- eight-slot page bound;
- page count and clamping for 0–16 slots;
- selected-page initialization;
- hit-region mapping;
- compact/normal geometry;
- keyboard navigation state;
- icon fallback state;
- cooldown/hazard presentation state mapping.

### Real client

- 854×480;
- 1920×1080;
- 3440×1440;
- GUI scale Auto/2/3/4 where available;
- `TOGGLE` open/close;
- `HOLD` release close;
- first and second page selection;
- mouse and approved keyboard-only selection paths;
- no stuck input after close;
- visual distinction without relying solely on color.

## Deferred acceptance

Common resolutions, GUI scales, real mouse/key interaction and input-lock recovery after closing the wheel remain manual-matrix rows and are not marked PASS from automated tests.

## Exit criteria

05.02 is fully validated only when:

- all current 16 loadout slots are reachable through bounded paging;
- selection remains distinct from casting;
- layouts remain usable across the required viewport/GUI-scale matrix;
- `TOGGLE` and `HOLD` are directly observed working;
- no input lock remains after close;
- any added cooldown/cost/hazard affordance is server-authored or safely unavailable;
- applicable manual rows have direct evidence.
