# 05.03 — Contextual Feedback — Runtime/Data Contract

## State

`IMPLEMENTED / PHYSICAL STATE VALIDATION PENDING`

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

## Remaining engineering acceptance

- authoritative denial remains distinguishable from advisory forecast;
- stale forecast/reload/reconnect state cannot override current snapshots;
- cast-result correlation never guesses current selected-spell identity;
- future presentation data additions pass their server-authored contract gate;
- dedicated server remains free of client classloading.
