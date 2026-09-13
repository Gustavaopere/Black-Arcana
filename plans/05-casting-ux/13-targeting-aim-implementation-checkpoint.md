# 05.13 — Targeting & Aim Presentation — Implementation Checkpoint

## State

`PHASE B IMPLEMENTED CANDIDATE / AUTOMATED GATES GREEN / FINAL CLIENT VALIDATION DEFERRED`

This checkpoint records only the bounded Phase B runtime promoted from `plans/05-casting-ux/13-targeting-aim-presentation.md`.

It does not mark Stage 05 complete, does not introduce client target authority and does not convert any real-client validation row from `PENDING` to `PASS`.

## Baseline and authority audit

Implementation branch:

- `feat/stage05-targeting-local-observation`

Implementation baseline:

- `main@84e9635b446b605140ab349fa2edc51f3462d518`

The branch was created from that exact current `main` after checking for equivalent 05.13 runtime work. The only pre-existing 05.13 branch found was the historical planning branch `docs/stage05-13-targeting-aim-presentation`; no equivalent open runtime PR existed.

The runtime audit reconfirmed the boundaries frozen by D006, D019, D020 and D025:

- target validation remains server-authoritative;
- `ClientInputController` emits bounded intent only;
- `targetHint` remains advisory;
- `ArcanaTargetSpec` and `ArcanaTargetGeometry` are not synchronized as a generic client presentation contract;
- `CastResultPayload` does not prove resolved target identity;
- world-effect admission remains server-owned;
- no installed provider/camera integration is required for this Phase B client-only cue.

Therefore the implementation intentionally withholds target kind, exact range, LOS, eligibility, protection state, server-valid target claims and exact area geometry.

## Runtime promoted by this checkpoint

### Local observation semantics

`TargetAimPresentationSemantics` defines exactly three presentation states:

- `MISS`;
- `BLOCK`;
- `ENTITY`.

These are `LOCAL_OBSERVATION` states only. They describe the current vanilla client hit-result type and never mean:

- server-valid target;
- in authoritative range;
- LOS accepted;
- progression/cost/cooldown accepted;
- world mutation permitted;
- cast guaranteed to succeed.

The three states use distinct non-color markers and explicit localized text so target meaning is not encoded by color alone.

Vanilla hit classification uses `HitResult.Type` rather than concrete hit-result class identity. This is deliberate because a `BlockHitResult` may represent `Type.MISS`; `MISS` therefore remains neutral instead of being mislabeled as a surface observation.

### Physical-client GUI layer

`TargetAimPresentationLayer` is registered through the existing NeoForge 1.21.1 `RegisterGuiLayersEvent` physical-client seam.

It renders only when all of the following are true:

- Black Arcana contextual HUD is enabled;
- a physical client player and connection exist;
- no screen currently owns input;
- the normal Stage 05 selection window is still recent;
- a synchronized loadout has a locally selected spell.

The cue:

- reads only `Minecraft.hitResult`;
- maps `HitResult.Type.MISS/BLOCK/ENTITY` through the pure semantics helper;
- renders a bounded neutral line below the screen center;
- reuses `SELECTION_DURATION_TICKS` rather than introducing permanent target scanning;
- disappears naturally when the existing selection context expires.

No target history, target lock, candidate list or per-frame world enumeration is retained.

## Explicit exclusions

This checkpoint does not implement:

- synchronized `ArcanaTargetSpec` or geometry metadata;
- target-kind-specific reticles;
- exact range, LOS, friendly/player/projectile eligibility presentation;
- sphere/cone/cylinder/ray/linked geometry previews;
- authoritative target-valid/invalid styling;
- client-side replication of `ServerEntityTargetSelector`;
- client protection/world-safety queries;
- per-frame target-preview packets;
- target locks or aim assist;
- cast-result-to-target attribution;
- provider-specific target/camera bridges;
- x-ray/through-wall target markers;
- gameplay, progression, persistence or protocol changes.

Unknown/missing information continues to fail closed by withholding unsupported presentation claims rather than blocking legitimate server casting.

## TDD evidence

### RED 1 — missing Phase B runtime

Test-only commit:

- `7a559caf7d29923f88d6c56adad5cf802554136d`

Workflow:

- `34731173030`

Observed result:

- 639 tests executed;
- 4 failures;
- failures were confined to the intentionally absent 05.13 semantics, GUI layer and EN/PT advisory labels;
- Java compilation succeeded before the expected JUnit RED.

### GREEN 1 — initial bounded implementation

Candidate head:

- `644e0e04f426b15bfa7132f2f0f4a977b81bca7b`

Workflow:

- `34731356673`

The complete branch pipeline passed JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke.

Manual diff review then identified a vanilla semantic edge case: classifying concrete `BlockHitResult` objects directly could label a `HitResult.Type.MISS` as `BLOCK`.

### RED 2 — vanilla MISS regression

Test-only commit:

- `34b289cb7aa303ecadfe28de0108dcfe6c68c5c7`

Workflow:

- `34731602409`

Observed result:

- 639 tests executed;
- 2 failures;
- one proved the missing `fromHitType(HitResult.Type)` contract;
- one proved the layer was still using concrete `instanceof` classification;
- no unrelated test failed.

### GREEN 2 — type-correct local observation

Reviewed implementation head:

- `1a05dec1d305fae7862395baa8b59b6e0abbe1e2`

Workflow:

- `34731724433`

The complete branch pipeline passed:

- JUnit;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTest server;
- dedicated-server smoke.

The branch correctly skipped canonical QA artifact publication because artifact publication is main-only.

## Validation still required

This implementation changes visible physical-client presentation, so automated evidence is not a substitute for direct observation.

At minimum, the exact promoted build still requires physical-client checks for:

- no local hit / vanilla MISS;
- local block/surface hit;
- local entity hit;
- candidate changing or disappearing while the selection window is active;
- expiry at the configured selection duration;
- screen/radial/loadout suppression;
- contextual HUD disabled;
- 854×480, 1920×1080 and 3440×1440 layouts;
- GUI scales Auto/2/3/4 where applicable;
- F1/hidden-GUI behavior according to the chosen GUI-layer seam;
- Epic Fight camera/combat coexistence;
- Iron's/Spell Actionbar coexistence;
- no visual implication that the local cue is server target validation.

No source inspection, unit test, GameTest, build or CI result converts those physical-client rows to PASS.

## Promotion gate remaining

Before merge:

1. fetch `origin/main` again;
2. reconcile if it advanced;
3. review the exact branch diff;
4. run complete CI on the final documentation-inclusive HEAD;
5. open and review the PR;
6. require PR CI GREEN;
7. repeat the `main` sync immediately before merge;
8. merge only the verified exact head;
9. confirm final `main` SHA;
10. require exact-SHA post-merge CI including canonical QA artifact publication.

Stage 05 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED` regardless of this checkpoint until the accumulated real-client campaign is actually executed.
