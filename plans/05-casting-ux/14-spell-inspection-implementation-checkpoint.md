# 05.14 — Spell Details & Inspection Presentation — Implementation Checkpoint

## State

`PHASE B IMPLEMENTED CANDIDATE / AUTOMATED GATES GREEN BEFORE MAIN RECONCILIATION / FINAL CLIENT VALIDATION DEFERRED`

This checkpoint records only the bounded Phase B runtime implemented from `plans/05-casting-ux/14-spell-details-inspection-presentation.md`.

It does not mark Stage 05 complete and does not authorize any additional spell-detail authority beyond data already available to the physical client.

## Baseline and authority boundary

Implementation branch:

- `feat/stage05-spell-inspection`

Original implementation baseline:

- `main@474a98c0f5deaa592a843d648d3ea393c485f6c4`

Before implementation, the current generic spell presentation entry exposed only canonical identity, a translation key and icon identity. Existing hazard/preflight presentation was already synchronized through its own bounded channel. There was no approved generic client contract for configured cost, affordability, cooldown mapping/readiness, target specification, provider/domain classification, progression requirements or server-valid target state.

Phase B therefore exposes only:

- localized synchronized spell name;
- canonical spell ID;
- existing hazard/preflight line when present.

No packet, payload schema, protocol version, cast path, provider bridge or gameplay authority changed.

## Runtime implemented

`SpellInspectionPresentation` builds a bounded list of components from:

1. the synchronized/localized display name;
2. a localized `Spell ID` / `ID do feitiço` label plus the canonical spell ID;
3. the existing hazard/preflight component when available.

`BlackArcanaLoadoutScreen` is the only rich-inspection surface changed by this checkpoint. Pointer hover and keyboard focus both use the same inspection compositor. The radial and contextual HUD remain compact and unchanged.

Inspection interaction is presentation-only:

- hover/focus sends no network request;
- hover/focus does not cast;
- hover/focus does not mutate the draft;
- `LoadoutNetworkBridge.requestUpdate(...)` remains confined to the existing explicit Apply path;
- no per-hover/per-frame detail request exists.

## Explicitly withheld data

This checkpoint does not expose or infer:

- `ArcanaCost` or affordability;
- cooldown group or readiness;
- charges/channel state;
- `ArcanaTargetSpec`, range, LOS or current target validity;
- provider/domain/school metadata;
- progression requirements;
- world-effect permission;
- Corruption/Strain values;
- effect magnitude/damage formulas;
- copied provider descriptions/tooltips/assets.

Unknown or unavailable fields stay absent rather than being guessed from IDs, namespaces, names or provider conventions.

## TDD evidence

### RED — missing minimal inspection contract

Test-only commit:

- `882f3330ab904ff2bfb6bf47db8756c9004d6ded`

Workflow:

- `34734091033`

Observed result:

- 644 tests executed;
- exactly 3 failures, all in `SpellInspectionPresentationContractTest`;
- production compilation succeeded;
- failures proved the helper was absent, the loadout was still hazard-only, and the inspection ID label was absent.

### GREEN attempt — identity composition edge case

Implementation head:

- `846d6a8550119c0a075b635bf5b2f552c04172ad`

Workflow:

- `34734493295`

Observed result:

- 644 tests executed;
- 643 passed / 1 failed;
- the only failure showed that passing the canonical ID as a translatable argument did not preserve the ID in `Component.getString()` under the test environment;
- loadout wiring, authority exclusions and localization-key presence already passed.

### GREEN — explicit canonical ID component

Reviewed implementation head before latest-main reconciliation:

- `fb494e1d805066138efa8cf04f79b692fcbef0aa`

Workflow:

- `34734637552`

The complete branch pipeline passed:

- JUnit;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTest server;
- dedicated-server smoke.

Canonical QA artifact publication was correctly skipped because this was not `main`.

## Main reconciliation required

After the GREEN above, `main` advanced from `474a98c0...` to `1d61267a2fdeaa273df2415d37500eded32c93b3` through an unrelated provider-catalog documentation merge. The implementation branch therefore became `ahead 8 / behind 1`.

This checkpoint itself does not claim the pre-reconciliation GREEN as final evidence. The branch must merge the current `main`, rerun the complete pipeline on the reconciled HEAD, then pass PR review/CI and exact-SHA post-merge validation before promotion.

## Real-client evidence still required

Because this changes a physical-client tooltip surface, direct validation remains pending for at least:

- pointer hover inspection;
- keyboard-focus inspection;
- spell with and without hazard line;
- long localized spell name/canonical ID;
- `854×480`, `1920×1080`, `3440×1440`;
- GUI scales Auto/2/3/4 where applicable;
- page changes/search reconciliation;
- no accidental draft mutation/cast from inspection;
- Iron's/Spell Actionbar coexistence;
- Epic Fight/EFIS coexistence.

No automated result converts those physical-client rows to PASS.
