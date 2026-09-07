# 05 — Casting & UX

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

The deterministic Stage 05 runtime is implemented on `main`. The remaining acceptance surface is the real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md`; automated CI is supporting evidence and does not convert those manual rows to PASS.

## Objective

Deliver direct, low-clutter casting after server contracts and integrations are stable: no universal staff requirement, no permanent extra mana HUD, fast loadouts, readable authoritative failure reasons, and rebindable input.

## Canonical implementation

- `ClientInputController` owns client intent emission only. Quick-cast and selected-cast input send `CastIntentPayload`; gameplay admission remains in the server runtime.
- `LoadoutNetworkBridge` synchronizes edits while `ArcanaServerRuntimeManager.handleLoadoutUpdate` validates spell availability and persists accepted loadouts through `BlackArcanaSavedData`.
- `BlackArcanaRadialScreen` is a client-only selector. Choosing a wedge changes selection and closes the screen; it never executes a cast.
- `BlackArcanaHudLayer` is contextual/event-driven, uses synchronized server presentation/cooldown/hazard/result state, and displays the bounded server-authored denial detail rather than inventing a client-side gate reason.
- `BlackArcanaClientConfig` owns presentation-only preferences: HUD enable/scale/anchor, feedback duration/intensity, radial hold/toggle, particle density, reduced motion and reduced flashes. These settings do not participate in gameplay validation.
- `BlackArcanaClient` is a physical-client entrypoint (`Dist.CLIENT`); dedicated-server runtime registration remains in the common mod entrypoint without loading client classes.

## Automated evidence

Stage 05 has focused JUnit coverage for client selection, loadout drafts, HUD layout, radial layout/toggle semantics and small-viewport geometry. Server loadout persistence/validation and the complete project pipeline are exercised by the canonical CI suite.

Follow-up hardening is canonical:

- PR #56 fixed same-key `TOGGLE` radial close; merge `206e37134b37447b9573541c7013e36dd45654a6`; post-merge workflow `34008702833` (#1152) GREEN.
- PR #57 hardened the 854×480 / GUI-scale-4 layouts. Final head `01a77eab641896173585b66c6310662d820c9f0c` passed workflow `34010736078` (#1169); merge `f2bb9a19db92d869e4443b2047ad1c913f8d2a29` passed exact-SHA workflow `34010968124` (#1170), including JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke.
- Canonical artifact for that hardening checkpoint: `black-arcana-f2bb9a19db92d869e4443b2047ad1c913f8d2a29`, artifact ID `9982472491`, SHA-256 `1ba6949ceb04f261646548b6d99a158f4f40211a5017ca1911c0e1a732f86cdb`.

## Exit criteria

The deterministic exit criterion is satisfied: a player can equip/select/cast Black Arcana spells through a concise workflow while spell availability, progression, cooldown, resource cost and denial remain server-authoritative.

Real-client keyboard/controller variants, GUI focus, death/relog behavior, common resolutions/GUI scales and presentation accessibility remain `FINAL VALIDATION DEFERRED` until directly observed through the Stage 05 manual runbook. No manual PASS is inferred from CI.
