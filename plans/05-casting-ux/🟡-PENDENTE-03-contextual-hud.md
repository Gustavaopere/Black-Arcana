# 05.03 — Contextual HUD & Feedback

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

This document records the current HUD contract and the plan for any remaining feedback/presentation work. Planned additions are not implementation claims.

`11-contextual-feedback-orchestration.md` is the canonical planning authority for overlap, priority, supersession, timing and correlation between selection context, advisory forecast and authoritative cast-result feedback.

## Goal

Show the minimum information necessary to cast confidently without turning Black Arcana into a permanently occupied HUD stack.

The HUD should answer, only when relevant:

- what spell is selected;
- whether a recently attempted cast succeeded or was denied;
- why an authoritative denial occurred;
- whether a dangerous spell is below minimum/recommended Arcane Resistance;
- whether a bounded predictable gate currently blocks the selected dangerous spell;
- whether the player should look elsewhere for more detailed information.

## Philosophy

Show information when it matters; do not add a permanent Black Arcana resource bar by default.

Combat readability has priority over completeness. Persistent detail belongs in tooltips/editor surfaces unless the player needs it immediately during casting.

## Current canonical contract

- `BlackArcanaHudLayer` returns immediately while contextual HUD is disabled.
- It returns while no client player exists.
- It returns while another `Screen` owns focus.
- It returns while there is no recent selection or cast result.
- `MINIMAL` feedback shows only recent denials.
- `STANDARD` may show selected spell plus selection-time hazard/gate information.
- `VERBOSE` may additionally show successful-cast feedback.
- Recent selection may show the selected spell plus synchronized hazard/gate presentation.
- Recent cast results show the bounded authoritative server denial detail. The client does not synthesize a gate reason.
- Selected-spell presentation and latest cast-result presentation are independently sourced and can be recent at the same time.
- `CastResultPayload` currently carries `castId/status/code/detail` but no `spellId` or loadout slot. Current selection therefore cannot be treated as authoritative identity for that result.
- The current renderer can juxtapose current selected-spell context with a latest result when their windows overlap; 05.11 records this as a presentation-correlation hardening gap rather than an implemented fix.
- Layout is anchorable/scalable, wraps text and can scale down to remain within small viewports.
- Provider adapters may expose presentation data, but gameplay authority remains server-side.
- Dedicated-server startup must remain free of client classloading.

## Current information sources

### Selected spell

Uses the current reconciled client selection against the synchronized server loadout plus synchronized spell presentation metadata.

This identifies the **current selection**, not necessarily the spell that produced the latest received cast result.

### Static danger preflight

Uses synchronized danger tier and minimum/recommended Arcane Resistance metadata.

### Current hazard resistance forecast

Uses a bounded server-authored forecast only when its tier/minimum/recommended metadata still matches the current static preflight.

A stale forecast must not override new static metadata after reload/reconnect.

### Predictable gate category

Uses the server-authored bounded gate forecast when available.

Current categories include:

- `CLEAR`;
- `IDENTITY`;
- `PROGRESSION`;
- `COOLDOWN`;
- `COST`;
- `UNAVAILABLE`.

`CLEAR` means only that the predictable projected gate set is clear. It is not a guarantee that the eventual cast succeeds.

### Cast result

Uses the synchronized `CastResultPayload`. Denial text comes from the bounded server-authored detail.

The payload identifies the cast by `castId` but does not currently include spell/slot identity. Without a separately proven correlation context, the safe presentation is therefore the authoritative result itself, not a claim that the currently selected spell produced it.

## Information hierarchy

For future arbitration under 05.11, semantic emphasis should prioritize:

1. authoritative cast denial;
2. authoritative success when `VERBOSE` permits it;
3. current hard-block/warning forecast for the current selected spell;
4. current selected-spell identity/context;
5. lower-value explanatory detail.

This is semantic priority, not a claim that the current renderer already implements all arbitration rules or that physical vertical line order must literally match the list.

An authoritative result must never be rewritten by a preview. A forecast and a result may coexist, but the UI must keep their meanings distinct and must not visually attribute the result to the current selection unless a safe cast-id correlation exists.

If future additions exceed a compact readable panel, information should move into another contextual surface rather than allowing the HUD to grow indefinitely.

## Planned HUD refinements

The following are `PLANNED / NOT YET CLAIMED AS IMPLEMENTED`.

`07-presentation-data-contracts.md` is the authority and synchronization gate for every new datum described below. A desired visual element is not implementable merely because the corresponding server runtime state exists.

`11-contextual-feedback-orchestration.md` is additionally required whenever a refinement changes transient-event priority, lifetime, deduplication or result/selection association.

### 1. Cooldown affordance

The original Stage 05 design target included a short cooldown indicator.

Current audited boundary:

- `CooldownSnapshotPayload` synchronizes authoritative cooldown state by canonical `groupId`;
- `SpellPresentationPayload` does not currently synchronize the selected spell's cooldown-group mapping;
- D018 allows shared cooldown groups, so the client must never assume `groupId == spellId`.

Plan:

- add generic per-spell cooldown/readiness only after a bounded server-authored spell→cooldown-group relationship exists;
- use the received server-owned remaining time only through that valid mapping;
- prefer a concise remaining-time/readiness indicator;
- hide it while irrelevant/ready unless persistent display proves necessary;
- any local countdown between snapshots is presentation-only and a later server snapshot wins;
- clear or omit stale/unmapped cooldown information rather than extrapolating beyond the synchronized contract;
- do not create a second client cooldown authority.

Status: `BLOCKED ON PRESENTATION MAPPING CONTRACT` for a generic selected-spell cooldown widget.

### 2. Provider-resource/cost summary

The original design target included provider-specific cost.

Plan:

- do not compute Iron's mana, Ars Source, Malum spirits, item, health or composite costs client-side from duplicated formulas;
- do not use descriptive `SpellImplementationSpec.resourceCost` text as live gameplay authority;
- first verify whether an existing server-authored bounded presentation contract is sufficient;
- if not, design a dedicated bounded presentation result under `07-presentation-data-contracts.md`;
- mark unavailable when a provider cannot safely preview exact cost;
- never reserve/debit a resource from HUD preview;
- preserve mixed ownership for Black Arcana-owned spells hosted by Iron's: host presentation does not transfer Black Arcana transaction authority to Iron's.

Status: `BLOCKED ON BOUNDED SERVER/PROVIDER PREVIEW CONTRACT` for exact cost display.

### 3. Charge/channel presentation

D024 requires channeling to converge on the canonical cast engine.

`07-presentation-data-contracts.md` distinguishes two separate server-owned concepts that currently lack Stage 05 client state:

- reusable charge pools (`ArcanaChargeSpec` plus server charge runtime);
- active channel sessions (`ArcanaChannelManager` plus `ArcanaChannelSpec`).

If future Black Arcana spells require these visuals, planned HUD presentation may show, once the appropriate bounded contract exists:

- available/max charge pool state and recharge presentation;
- accepted charging/channel state;
- bounded channel progress;
- minimum/maximum timing markers exposed by the server contract;
- cancel/release affordance text.

Rules:

- client-reported channel duration is never authoritative;
- HUD progress is presentation only;
- local key timing cannot substitute for a server-accepted channel lifecycle;
- release still enters the same canonical server coordinator;
- charge consume/recharge remains server-owned;
- no charge/channel bar exists for spells that do not use that mechanic.

Status: `BLOCKED ON CHARGE/CHANNEL PRESENTATION CONTRACTS`.

### 4. Ritual/domain timer presentation

The original Stage 05 candidate list included temporary grand-ritual/domain timers.

Only add a timer when:

- Black Arcana owns the active state and exposes a bounded owner-specific timer presentation contract; or
- an external provider exposes a supported bounded presentation seam.

Do not poll the world or infer remaining duration from particles/entities, first-observed spawn time or chunk state.

Status: `BLOCKED ON OWNER-SPECIFIC TIMER CONTRACT`.

### 5. Cast target feedback

Potential future contextual improvement:

- show a concise server-authorized target failure category after denial;
- do not render live client target legality as authoritative;
- do not expose hidden entity/player information through preview.

Any target preview must preserve D019 server geometry and privacy/protection boundaries.

### 6. Iconography

Where appropriate, use synchronized spell icon plus semantic symbols for:

- selected spell;
- cooldown only after the mapping contract exists;
- danger;
- blocked gate;
- unavailable preview.

Icons supplement text and color; they do not replace necessary labels.

The existing synchronized `SpellPresentationPayload.Entry.iconId` is sufficient for the spell-icon presentation refinement; missing artwork still falls back to text and never changes cast validity.

### 7. Feedback correlation hardening

The current result schema echoes `castId` but not spell/slot identity.

Planned safe options are defined by 05.11:

- baseline: render result without spell attribution when no correlation exists;
- optional no-protocol hardening: keep a small bounded client-only pending context keyed by emitted `castId`, containing attempted spell/slot solely for presentation correlation;
- unknown/unmatched result id: retain generic authoritative result, omit guessed spell identity;
- richer server-authored result identity: only through a separately reviewed bounded protocol change if product requirements actually need it.

A client correlation table is never admission, replay, cost, cooldown or spell-identity authority for the server.

## Anti-clutter rules

- no permanent Black Arcana mana/resource bar by default;
- no permanent selected-spell panel while idle beyond configured duration;
- no full spell description in combat HUD;
- no repeating success spam in `MINIMAL` or `STANDARD`;
- no unbounded cast-result/history queue;
- no duplicate provider HUD if the provider already owns the exact same resource presentation unless an explicit integration design justifies it;
- no more lines than can fit safely after wrapping/scaling; overflow triggers a design change, not off-screen rendering.

## Denial wording policy

The client must distinguish:

### Preview

A forecast/preflight is informational and may become stale or fail at later cast gates.

### Authoritative denial

A cast-result denial is the actual bounded server result for that request.

The UI must not merge these into language that implies the preview itself denied the cast.

When a denial and advisory forecast disagree, the denial owns outcome emphasis. If the denial cannot be safely correlated to a spell identity, it remains authoritative but must be shown without guessed attribution.

## Hazard wording policy

Danger presentation must remain factual:

- below minimum -> blocked by the relevant hazard threshold where the server says so;
- below recommended -> warning, not guaranteed failure;
- recommendation met -> does not mean Backlash/corruption risk is eliminated;
- unavailable -> no guessed effective resistance.

Never state that a recommended threshold makes dangerous magic safe.

## Stale-state and overlap policy

HUD state is cleared/reconciled on session change.

A dynamic forecast may render only when it matches the current static preflight metadata for the same spell.

Transient-event arbitration additionally follows 05.11:

- cast A result arriving after selection changes to B must not be described as B's result unless a safe cast-id correlation proves the attempted identity;
- B's forecast remains scoped to B and must not rewrite A's authoritative result;
- the current bounded result model is latest-received-result wins; an older result is not pinned merely because a newer success is visually suppressed at `STANDARD`;
- repeated identical text is not a dedup key; any future presentation dedup uses `castId`;
- another `Screen` hides the contextual HUD but does not pause or extend transient selection/result timers;
- reconnect/session change clears any future pending-correlation or presentation-dedup state.

On reload/provider/profile change:

- new static preflight wins;
- mismatched older forecast is ignored;
- cooldown spell→group mapping, if implemented later, must be invalidated/replaced with the authoritative policy revision rather than retained blindly;
- future charge/channel/timer presentation must define its own bounded stale-state identity under `07-presentation-data-contracts.md`;
- reconnect clears prior session presentation before new snapshots arrive.

## F1 / vanilla GUI policy

Real-client validation must confirm Black Arcana follows the expected vanilla hidden-GUI behavior.

If current layer ordering causes unexpected F1 behavior, fix it through supported NeoForge/vanilla HUD semantics rather than introducing a second independent overlay stack.

## Accessibility requirements

- state must not rely exclusively on color;
- text must wrap or truncate safely;
- HUD scale 0.5–2.0 must remain bounded;
- every exposed anchor must remain on-screen;
- reduced motion/flashes must be respected by future HUD animations;
- essential denial/risk information should remain readable without particle or motion cues.

## Performance plan

`BlackArcanaHudLayer` is intentionally event/context driven.

Preserve:

- early return while idle;
- no entity/chunk/world scans during render;
- no per-frame network requests;
- bounded synchronized snapshots;
- forecast request rate limiting outside the render loop;
- bounded text wrapping and finite scale-fit attempts;
- any future pending-cast correlation or result-dedup cache bounded by count and age.

Future cooldown/charge/channel/timer synchronization must remain event-driven under D023 rather than becoming a per-tick full-state stream.

## Automated coverage

`HudLayoutTest`, `HazardForecastPresentationTest` and `SmallViewportLayoutContractTest` cover deterministic HUD geometry and synchronized presentation behavior. The project CI verifies dedicated-server startup, guarding the no-client-classloading boundary.

## Test plan for future HUD changes

### Pure/unit

- line priority/order;
- selection/result time windows;
- `MINIMAL/STANDARD/VERBOSE` density;
- stale forecast rejection;
- cast A → select B before result A → no false B attribution;
- rapid A/B results → latest received result owns the result channel;
- forecast `CLEAR` followed by authoritative denial → denial owns outcome emphasis;
- unmatched `castId` → result remains present without guessed spell/slot;
- another `Screen` during the result window → hidden presentation does not pause/extend the timer;
- anchor/scale containment;
- line wrapping/truncation;
- semantic status mapping;
- shared cooldown-group mapping once implemented;
- client interpolation remains presentation-only.

### Network/state

- reconnect clears stale result/forecast and any future pending correlation/dedup state;
- reload invalidates mismatched forecast;
- forecast request id/spell/preflight correlation remains bounded;
- unavailable provider preview remains unavailable;
- cooldown mapping rejects/omits an unmapped selected spell rather than assuming spell id equals group id;
- future charge/channel/timer additions use bounded server-authored state only;
- future cost preview is side-effect-free and does not settle resources.

### Real client

- 854×480, 1920×1080, 3440×1440;
- GUI scale Auto/2/3/4 where available;
- all five anchors at 0.5×/1×/2×;
- authoritative denial timing/readability;
- cast A → change selection → receive A result, verifying no false association after hardening is implemented;
- rapid cast/result overlap at each feedback level after hardening is implemented;
- idle disappearance;
- hazard minimum/recommended scenarios;
- CLEAR/COOLDOWN/COST and supported additional gate states;
- F1/hidden GUI;
- reduced motion/flash interactions where applicable;
- any newly implemented cooldown/charge/channel/timer display against the exact server transition that produced it.

## Deferred acceptance

Actual readability, overlap and visual timing across the real-client resolution/GUI-scale matrix remain PENDING until directly observed.

Missing optional cost/charge/channel/timer presentation is not automatically a Stage 05 blocker. If a direct validation failure promotes one of those features to required work, its corresponding data contract must be implemented and validated first.

05.11 planning does not itself make feedback-correlation hardening a blocker. It becomes required only if an explicit reviewed decision or direct validation evidence promotes the observed association gap to required Stage 05 work.

## Exit criteria

05.03 is fully validated only when:

- idle behavior remains low-clutter;
- server denial is displayed accurately;
- dangerous-spell forecast wording remains factual;
- stale forecast/gate state cannot override current snapshots;
- any implemented result-correlation hardening obeys 05.11 and never turns client presentation context into gameplay authority;
- any implemented cooldown/cost/charge/channel/timer feature obeys `07-presentation-data-contracts.md` and never invents client authority;
- all anchors/scales remain readable in the required manual matrix;
- no provider economics or gameplay authority is duplicated client-side;
- dedicated server remains free of client-class loading;
- applicable manual matrix rows have direct evidence.