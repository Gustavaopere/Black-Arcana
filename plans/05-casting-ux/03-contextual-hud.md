# 05.03 — Contextual HUD & Feedback

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

This document records the current HUD contract and the plan for any remaining feedback/presentation work. Planned additions are not implementation claims.

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
- Layout is anchorable/scalable, wraps text and can scale down to remain within small viewports.
- Provider adapters may expose presentation data, but gameplay authority remains server-side.
- Dedicated-server startup must remain free of client classloading.

## Current information sources

### Selected spell

Uses the current reconciled client selection against the synchronized server loadout plus synchronized spell presentation metadata.

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

## Information hierarchy

The contextual panel should prioritize lines in this order:

1. selected spell;
2. danger/resistance status when relevant;
3. predictable gate state when relevant;
4. authoritative cast denial;
5. success feedback only in `VERBOSE`.

If future additions exceed a compact readable panel, information should move into another contextual surface rather than allowing the HUD to grow indefinitely.

## Planned HUD refinements

The following are `PLANNED / NOT YET CLAIMED AS IMPLEMENTED`.

### 1. Cooldown affordance

The original Stage 05 design target included a short cooldown indicator.

Plan:

- use synchronized server-owned cooldown state;
- prefer a concise remaining-time/readiness indicator;
- hide it while irrelevant/ready unless persistent display proves necessary;
- clear or omit stale cooldown information rather than extrapolating beyond the synchronized contract;
- do not create a second client cooldown authority.

### 2. Provider-resource/cost summary

The original design target included provider-specific cost.

Plan:

- do not compute Iron's mana, Ars Source, Malum spirits, item, health or composite costs client-side from duplicated formulas;
- first verify whether an existing server-authored bounded presentation contract is sufficient;
- if not, design a dedicated bounded presentation field/payload;
- mark unavailable when a provider cannot safely preview exact cost;
- never reserve/debit a resource from HUD preview.

### 3. Charge/channel presentation

D024 requires channeling to converge on the canonical cast engine.

If a Black Arcana spell exposes a server-owned charge/channel session, planned HUD presentation may show:

- charging state;
- bounded progress;
- minimum/maximum timing markers where the server contract exposes them;
- cancel/release affordance text.

Rules:

- client-reported channel duration is never authoritative;
- HUD progress is presentation only;
- release still enters the same canonical server coordinator;
- no channel bar exists for spells that do not use that mechanic.

### 4. Ritual/domain timer presentation

The original Stage 05 candidate list included temporary grand-ritual/domain timers.

Only add a timer when:

- Black Arcana owns the active state; or
- an external provider exposes a supported bounded presentation seam.

Do not poll the world or infer remaining duration from particles/entities.

### 5. Cast target feedback

Potential future contextual improvement:

- show a concise server-authorized target failure category after denial;
- do not render live client target legality as authoritative;
- do not expose hidden entity/player information through preview.

Any target preview must preserve D019 server geometry and privacy/protection boundaries.

### 6. Iconography

Where appropriate, use synchronized spell icon plus semantic symbols for:

- selected spell;
- cooldown;
- danger;
- blocked gate;
- unavailable preview.

Icons supplement text and color; they do not replace necessary labels.

## Anti-clutter rules

- no permanent Black Arcana mana/resource bar by default;
- no permanent selected-spell panel while idle beyond configured duration;
- no full spell description in combat HUD;
- no repeating success spam in `MINIMAL` or `STANDARD`;
- no duplicate provider HUD if the provider already owns the exact same resource presentation unless an explicit integration design justifies it;
- no more lines than can fit safely after wrapping/scaling; overflow triggers a design change, not off-screen rendering.

## Denial wording policy

The client must distinguish:

### Preview

A forecast/preflight is informational and may become stale or fail at later cast gates.

### Authoritative denial

A cast-result denial is the actual bounded server result for that request.

The UI must not merge these into language that implies the preview itself denied the cast.

## Hazard wording policy

Danger presentation must remain factual:

- below minimum -> blocked by the relevant hazard threshold where the server says so;
- below recommended -> warning, not guaranteed failure;
- recommendation met -> does not mean Backlash/corruption risk is eliminated;
- unavailable -> no guessed effective resistance.

Never state that a recommended threshold makes dangerous magic safe.

## Stale-state policy

HUD state is cleared/reconciled on session change.

A dynamic forecast may render only when it matches the current static preflight metadata for the same spell.

On reload/provider/profile change:

- new static preflight wins;
- mismatched older forecast is ignored;
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
- bounded text wrapping and finite scale-fit attempts.

## Automated coverage

`HudLayoutTest`, `HazardForecastPresentationTest` and `SmallViewportLayoutContractTest` cover deterministic HUD geometry and synchronized presentation behavior. The project CI verifies dedicated-server startup, guarding the no-client-classloading boundary.

## Test plan for future HUD changes

### Pure/unit

- line priority/order;
- selection/result time windows;
- `MINIMAL/STANDARD/VERBOSE` density;
- stale forecast rejection;
- anchor/scale containment;
- line wrapping/truncation;
- semantic status mapping.

### Network/state

- reconnect clears stale result/forecast;
- reload invalidates mismatched forecast;
- unavailable provider preview remains unavailable;
- cooldown/cost/channel additions use server-authored state only.

### Real client

- 854×480, 1920×1080, 3440×1440;
- GUI scale Auto/2/3/4 where available;
- all five anchors at 0.5×/1×/2×;
- authoritative denial timing/readability;
- idle disappearance;
- hazard minimum/recommended scenarios;
- CLEAR/COOLDOWN/COST and supported additional gate states;
- F1/hidden GUI;
- reduced motion/flash interactions where applicable.

## Deferred acceptance

Actual readability, overlap and visual timing across the real-client resolution/GUI-scale matrix remain PENDING until directly observed.

## Exit criteria

05.03 is fully validated only when:

- idle behavior remains low-clutter;
- server denial is displayed accurately;
- dangerous-spell forecast wording remains factual;
- stale forecast/gate state cannot override current snapshots;
- all anchors/scales remain readable in the required manual matrix;
- no provider economics or gameplay authority is duplicated client-side;
- dedicated server remains free of client-class loading;
- applicable manual matrix rows have direct evidence.
