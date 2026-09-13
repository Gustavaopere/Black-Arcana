# 05.14 — Spell Details & Inspection Presentation — Implementation Checkpoint

## State

`PHASE B IMPLEMENTED / AUTOMATED GATES GREEN / REVIEW FIX GREEN / REAL-CLIENT VALIDATION PENDING`

This checkpoint records the implemented Stage 05.14 Phase B refinement and the subsequent review-driven bounded-wrapping correction. The canonical planning authority remains `14-spell-details-inspection-presentation.md`; this file records implementation evidence and does not broaden that contract.

## Baseline and scope

- current reconciled baseline: `main@6397b4b40778cb7867331342c0ce1a22617fc688`;
- implementation branch: `feat/stage05-spell-inspection`;
- reconciled implementation HEAD before this checkpoint update: `0a15a91a3c6b52d8b776441f39b46a64f5e6ff66`;
- implemented phase: **Phase B — minimal static inspection only**;
- review vehicle: PR #224 — `feat: add Stage 05.14 spell inspection presentation`.

Implemented behavior:

- the loadout editor is the primary inspection surface;
- pointer hover and keyboard focus use the same bounded inspection tooltip;
- the tooltip includes the synchronized display name;
- the tooltip includes the canonical spell ID with a localized identity label;
- display name, canonical ID and optional hazard content are wrapped with `Font.split(...)` against the logical screen width minus a fixed horizontal reserve before rendering;
- an already-authorized hazard/preflight line is composed when available;
- radial and contextual HUD remain compact and are not expanded into rich inspection surfaces;
- inspection itself sends no cast intent and no inspection network request;
- Apply remains the only loadout update path.

## Authority boundary

The implementation exposes only fields already legitimate under the Stage 05 presentation contract:

- synchronized/static spell identity;
- localized spell name derived from the synchronized translation key;
- canonical spell ID;
- optional existing hazard/preflight presentation.

It does **not** infer or expose:

- `ArcanaCost` or provider affordability;
- cooldown group or per-spell readiness;
- `ArcanaTargetSpec`, range, LOS or target validity;
- provider/domain/school metadata;
- progression requirements;
- world-mutation permission;
- current Corruption/Strain;
- damage/effect magnitude;
- any provider-owned tooltip/description text.

No payload/schema/provider adapter was added. The wrapping correction is presentation-only and does not create a new network or authority path.

## TDD evidence

### Initial RED

Commit `882f3330ab904ff2bfb6bf47db8756c9004d6ded` added only `SpellInspectionPresentationContractTest`.

Workflow `34734091033`:

- 644 tests executed;
- 3 failures;
- failures were restricted to the absent 05.14 contracts: helper, loadout tooltip wiring and localized identity label.

### First implementation candidate

HEAD `846d6a8550119c0a075b635bf5b2f552c04172ad`, workflow `34734493295`:

- 644 tests executed;
- 1 failure remained in canonical-ID text observability;
- loadout wiring and localization-presence contracts were already satisfied.

### Localization composition correction

HEAD `4f076d3e7e7eea9637bc18305b8e0daaefc1576b`, workflow `34735498791`:

- 644 tests executed;
- the same single canonical-ID observability assertion remained red because the unit-test language table is not loaded as a physical client language manager.

### Corrected initial GREEN

HEAD `cbaf3c26080150087de3c7be236824d7a0377948`, workflow `34735689265`:

- Unit tests — GREEN;
- Diff sanity — GREEN;
- NeoForge build — GREEN;
- built JAR verification — GREEN;
- Foundation GameTests — GREEN;
- dedicated-server smoke — GREEN.

The canonical ID is literal presentation identity followed by the localized label, so the identity remains observable even without a loaded language table while the physical client still receives the localized label.

### First main reconciliation GREEN

`main` advanced in unrelated catalog/wiki files. The branch was merged with that `main` as a real two-parent merge without rebasing or discarding concurrent work.

Reconciled HEAD `23050c18fe710e430bf7082c3b3932c6785eca04`, workflow `34735843304`:

- Unit tests — GREEN;
- Diff sanity — GREEN;
- NeoForge build — GREEN;
- built JAR verification — GREEN;
- Foundation GameTests — GREEN;
- dedicated-server smoke — GREEN.

The canonical implementation checkpoint then advanced to `4724fdb2af600e20189615394106eb19a7a494bd`; workflow `34735993938` passed the same automated gate set.

## Review-driven bounded-wrapping correction

The first PR #224 workflow rerun `34736313697` was GREEN, but formal review identified a valid P2: `renderComponentTooltip` was receiving unwrapped `Component` lines, so a long localized display name or canonical ID could exceed the usable logical viewport at small window sizes or high GUI scale.

The fix was handled with a new TDD cycle rather than changing production code first.

### Review-fix RED

Commit `5e86a5717546801f446349ad18adee896ba05628` added a deterministic contract requiring viewport-bounded wrapping for both a long display name and a long canonical ID, plus source-level enforcement that pointer and keyboard use the same wrapped tooltip path.

Workflow `34736802496` failed specifically at **Unit tests** before implementation; the remaining build/test steps were skipped. This is the expected RED baseline.

### Review-fix GREEN candidate

The production correction was split across:

- `f2fe389e2b274cb50ffc278ed6d3827a4d12d98e` — `SpellInspectionPresentation.wrappedLines(...)` uses `Font.split(...)` with `max(1, logicalViewportWidth - 24)`;
- `ee326c9dcc44df3c3ca093105260f76cbd0efb7d` — the loadout screen renders the resulting `List<FormattedCharSequence>` through `GuiGraphics.renderTooltip(...)`, with both pointer hover and keyboard focus still calling the same `inspectionTooltip(...)` method.

Workflow `34736964385` on `ee326c9dcc44df3c3ca093105260f76cbd0efb7d` passed:

- Unit tests — GREEN;
- Diff sanity — GREEN;
- NeoForge build — GREEN;
- built JAR verification — GREEN;
- Foundation GameTests — GREEN;
- dedicated-server smoke — GREEN.

### Second main reconciliation GREEN

While the corrective candidate was validating, `main` advanced to `6397b4b40778cb7867331342c0ce1a22617fc688` through the shared Phase 2BQ ledger reconciliation. That concurrent commit touched only catalog/wiki files.

A real two-parent merge was created as `0a15a91a3c6b52d8b776441f39b46a64f5e6ff66`, with parents:

1. `ee326c9dcc44df3c3ca093105260f76cbd0efb7d` — Stage 05.14 review fix;
2. `6397b4b40778cb7867331342c0ce1a22617fc688` — current concurrent `main`.

No rebase, force update or concurrent-work discard was used. Comparison against `main@6397b4b40778cb7867331342c0ce1a22617fc688` is limited to the six Stage 05.14 files.

Workflow `34737286149` on reconciled HEAD `0a15a91a3c6b52d8b776441f39b46a64f5e6ff66` passed:

- Unit tests — GREEN;
- Diff sanity — GREEN;
- NeoForge build — GREEN;
- built JAR verification — GREEN;
- Foundation GameTests — GREEN;
- dedicated-server smoke — GREEN.

## Files introduced or changed

- `plans/05-casting-ux/14-spell-details-inspection-implementation-checkpoint.md`;
- `src/main/java/dev/gustavopere/blackarcana/client/SpellInspectionPresentation.java`;
- `src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java`;
- `src/main/resources/assets/black_arcana/lang/en_us.json`;
- `src/main/resources/assets/black_arcana/lang/pt_br.json`;
- `src/test/java/dev/gustavopere/blackarcana/client/SpellInspectionPresentationContractTest.java`.

## Deferred phases

Not implemented by this checkpoint:

- Phase C — static server-authored detail extensions;
- Phase D — dynamic player-specific preview extensions;
- Phase E — real-pack coexistence/polish validation beyond the existing bounded behavior.

Any future description, cost, cooldown, target/use, provider/domain or progression detail remains gated by 05.07 and the explicit contracts in the 05.14 plan.

## Manual validation

Automated gates do not substitute for physical-client evidence. The applicable 05.14 real-client matrix remains **PENDING**, including:

- pointer vs keyboard inspection parity;
- small/high-GUI-scale containment;
- ultrawide placement;
- long localization behavior;
- hazard composition;
- no draft mutation/cast caused by inspection;
- coexistence with Iron's, Spell Actionbar and Epic Fight/EFIS;
- resource/language reload behavior.

No manual PASS is inferred from CI.
