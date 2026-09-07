# 05.03 — Contextual HUD & Feedback

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

## Contract

Show information when it matters; do not add a permanent Black Arcana resource bar by default.

- `BlackArcanaHudLayer` returns immediately while idle, when contextual HUD is disabled, or while another screen owns focus.
- Recent selection may show the selected spell plus synchronized hazard/gate presentation.
- Recent cast results show the bounded authoritative server denial detail. The client does not synthesize a gate reason.
- Successful-cast feedback is presentation-level and depends on the configured feedback level.
- Layout is anchorable/scalable and wraps/bounds content for small viewports.
- Provider adapters may expose presentation data, but gameplay authority remains server-side.

## Automated coverage

`HudLayoutTest`, `HazardForecastPresentationTest` and `SmallViewportLayoutContractTest` cover deterministic HUD geometry and synchronized presentation behavior. The project CI verifies dedicated-server startup, guarding the no-client-classloading boundary.

## Deferred acceptance

Actual readability, overlap and visual timing across the real-client resolution/GUI-scale matrix remain PENDING until directly observed.
