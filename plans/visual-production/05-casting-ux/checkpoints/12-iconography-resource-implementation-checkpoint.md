# 05.12 — Iconography & Resource Resolution — Implementation Checkpoint

## State

`IMPLEMENTED CANDIDATE / AUTOMATED GATES GREEN / FINAL CLIENT VALIDATION DEFERRED`

This checkpoint records only the bounded Phase A–C runtime implemented from `plans/05-casting-ux/12-iconography-resource-resolution.md`.

It does not mark Stage 05 complete and does not convert any real-client validation row from `PENDING` to `PASS`.

## Baseline and reconciliation

Implementation branch:

- `feat/stage05-iconography-resource-resolution`

Implementation baseline:

- `main@40fedc5b1658e90b51565690851c2ad113203763`

Immediately before the Phase A–C implementation, `main` still pointed to that SHA.

The original 05.12 planning baseline predates Stage 05.10 implementation. Runtime inspection on the implementation baseline showed that 05.10 had already introduced:

- `SpellIconResolver`;
- a packaged project-owned placeholder texture;
- loadout-editor icon rendering.

Therefore the implementation followed current runtime authority rather than repeating obsolete planning assumptions.

## Runtime promoted by this checkpoint

### Phase A — shared resource resolution lifecycle

`SpellIconResolver` now:

- parses only the synchronized literal `iconId` through `ResourceLocation.tryParse`;
- resolves only against the normal client resource manager supplied by the caller;
- stores positive and negative resource-existence outcomes in one bounded client-only cache;
- caps cache cardinality at `ArcanaProtocol.MAX_PRESENTATION_ENTRIES` (`512`);
- invalidates all positive and negative assumptions on client resource reload;
- continues to return the existing project-owned placeholder for malformed, missing or failed lookups;
- performs no filesystem traversal, JAR inspection, network access, provider lookup or gameplay mutation.

NeoForge 1.21.1 / 21.1.x client reload registration is wired through:

- `RegisterClientReloadListenersEvent` on the mod event bus;
- `ResourceManagerReloadListener` as the invalidation listener.

The resolver remains under the physical-client entrypoint and dedicated-server startup remains isolated from client resource classes.

### Phase B — radial consumption

`BlackArcanaRadialScreen` now:

- reads the newest synchronized presentation entry for the spell when resolving its icon;
- uses the same shared `SpellIconResolver` as the editor;
- renders a bounded icon inside the existing radial card bounds;
- preserves slot/focus/selection text as a non-icon identity route;
- preserves current radial geometry and hit testing;
- preserves selection-only wedge activation and introduces no cast request path.

### Phase C — loadout editor consumption

`BlackArcanaLoadoutScreen` no longer freezes resolved icon outcomes in a screen-lifetime map.

Instead it:

- reads the newest synchronized presentation entry for the row when resolving its icon;
- delegates physical resource existence to the shared reload-aware resolver;
- preserves the existing search, order, draft, apply and server reconciliation semantics;
- keeps exactly one existing `LoadoutNetworkBridge.requestUpdate(...)` authority path.

This means a resource reload can invalidate prior positive or negative resource results, and a newer synchronized `iconId` for the same spell is not masked by a stale screen-local resolved-icon snapshot.

## Explicit exclusions

This checkpoint does not implement:

- HUD iconography or 05.12 Phase D;
- result-to-spell icon attribution;
- new `SpellPresentationPayload` fields;
- provider-specific icon APIs;
- provider/domain inference from icon namespace/path;
- HTTP or runtime downloads;
- arbitrary filesystem or JAR resource lookup;
- copied/recolored/traced provider artwork;
- final Black Arcana spell art production;
- animated icons;
- gameplay availability derived from missing art;
- cast/loadout/progression authority changes;
- any new packet or protocol version;
- any manual client PASS.

## TDD evidence

RED commit:

- `829592d1bfbd969f29394f1f06af217a81d2af77`

RED workflow:

- `34426654667`

Observed RED result:

- 635 tests executed;
- 5 failures;
- failures were confined to the intended missing 05.12 boundaries: resolver invalidation/cache lifecycle, exact reload registration, stale loadout resolved-icon snapshot and missing radial shared-resolution consumption.

GREEN implementation head:

- `a0b28c8f54a7e9f9555e6d086e4ecda17ed41777`

GREEN workflow:

- `34427275224`

The GREEN workflow passed:

- JUnit;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTest server;
- dedicated-server smoke.

The branch run correctly skipped canonical QA artifact publication because artifact publication is main-only.

## Validation still required

The following remain direct-observation work on an exact promoted build:

- radial icon-present and icon-missing rendering;
- all-icons-missing fallback;
- mixed namespaces;
- resource-pack reload appearance/disappearance behavior;
- loadout row readability and draft independence;
- 854×480, 1920×1080 and 3440×1440 viewport checks;
- GUI scales Auto/2/3/4 where available;
- semantic state readability without relying on icon art;
- provider-HUD coexistence;
- F1/hidden-GUI behavior where applicable.

No source inspection, unit test, GameTest or CI run is treated as evidence for those physical-client rows.

## Promotion gate remaining

Before merge:

1. fetch `origin/main` again;
2. reconcile if it advanced;
3. review the exact branch diff;
4. run the complete CI on the reconciled exact HEAD;
5. open/review the PR;
6. repeat the `main` sync immediately before merge;
7. merge only the verified HEAD;
8. confirm final `main` SHA;
9. require exact-SHA post-merge CI including canonical QA artifact publication.

Stage 05 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED` regardless of this checkpoint until the accumulated real-client campaign is actually executed.
