# 05.02 — Radial Wheel

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

## Contract

Provide a compact client-only spell selector rather than persistent screen clutter.

- `BlackArcanaRadialScreen` renders the synchronized loadout and server-authored presentation/preflight metadata.
- `RadialLayout` bounds visible slots by page and adapts geometry to the current viewport.
- Selection is non-casting: left-click changes `ClientLoadoutSelection`, marks contextual UX state and closes the wheel. A separate explicit cast input is required.
- Toggle and hold behavior are client-configurable; selection/config state never grants gameplay authority.
- Unavailable/gated information is presentation derived from synchronized server state, not a client admission decision.

## Automated coverage

`RadialLayoutTest`, `RadialToggleInputTest` and `SmallViewportLayoutContractTest` cover layout, toggle semantics and small-view geometry. PR #57 additionally hardened 854×480 / GUI-scale-4 behavior and passed exact-SHA full CI at workflow `34010968124` (#1170).

## Deferred acceptance

Common resolutions, GUI scales, real mouse/key interaction and input-lock recovery after closing the wheel remain manual-matrix rows and are not marked PASS from automated tests.
