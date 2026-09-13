# 05.02 — Radial Selection — Runtime Contract

## State

`IMPLEMENTED / PHYSICAL INPUT VALIDATION PENDING`

Final radial geometry, cards, icons and visual states are owned by `plans/visual-production/05-casting-ux/02-radial-wheel-presentation.md`.

## Canonical runtime contract

- `RadialLayout.SLOTS_PER_PAGE` is **8**; a 16-slot loadout spans at most two pages.
- The radial consumes the synchronized loadout and legitimate server-authored presentation/preflight data only.
- Selection is non-casting. Selecting changes `ClientLoadoutSelection`; a separate cast intent is required.
- Toggle/hold behavior is client configuration only and grants no gameplay authority.
- Page navigation is bounded and must keep all legal loadout slots reachable.
- Opening requires a client player, no competing `Screen`, and a non-empty synchronized loadout.
- Hover/focus is local presentation state and cannot emit a cast by itself.
- Close must restore input predictably and never leave a stuck key/cursor state.

## Authority rules

The radial may not execute a spell on selection, alter server loadout state, decide cooldown/cost/progression/target legality, force-load chunks, synthesize provider economy, mutate Arcane Danger or create a local fallback cast.

Any readiness/cooldown/cost/danger fact shown by presentation must come from an approved bounded synchronized contract. Unknown or stale facts are omitted/unavailable rather than guessed.

## Performance/runtime rules

- render/input logic consumes bounded local synchronized snapshots;
- no world entity/chunk scan for admission;
- no per-frame network request;
- no unbounded forecast request stream from hover movement;
- session change clears stale selection/presentation state as defined by Stage 05 synchronization contracts.

## Automated coverage

`RadialLayoutTest`, `RadialToggleInputTest` and `SmallViewportLayoutContractTest` preserve deterministic layout/input invariants. PR #57 hardened the 854×480 / GUI-scale-4 path and workflow `34010968124` was GREEN.

## Remaining engineering acceptance

- `TOGGLE` and `HOLD` close semantics observed in a real client;
- first/second page remain reachable;
- selection remains distinct from casting;
- no stuck input after close;
- no presentation refinement introduces a client admission shortcut.
