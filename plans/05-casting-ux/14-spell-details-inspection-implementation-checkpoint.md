# 05.14 — Spell Details & Inspection Presentation — Implementation Checkpoint

## State

`PHASE B IMPLEMENTED / AUTOMATED GATES GREEN / REAL-CLIENT VALIDATION PENDING`

This checkpoint records the implemented Stage 05.14 Phase B refinement. The canonical planning authority remains `14-spell-details-inspection-presentation.md`; this file records implementation evidence and does not broaden that contract.

## Baseline and scope

- reconciled baseline: `main@bc5428b5855e4d5821d5bd901fb591a62ecf3cbe`;
- implementation branch: `feat/stage05-spell-inspection`;
- reconciled implementation HEAD before this checkpoint: `23050c18fe710e430bf7082c3b3932c6785eca04`;
- implemented phase: **Phase B — minimal static inspection only**.

Implemented behavior:

- the loadout editor is the primary inspection surface;
- pointer hover and keyboard focus use the same bounded inspection tooltip;
- the tooltip includes the synchronized display name;
- the tooltip includes the canonical spell ID with a localized identity label;
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

No payload/schema/provider adapter was added.

## TDD evidence

### RED

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

### Corrected GREEN

HEAD `cbaf3c26080150087de3c7be236824d7a0377948`, workflow `34735689265`:

- Unit tests — GREEN;
- Diff sanity — GREEN;
- NeoForge build — GREEN;
- built JAR verification — GREEN;
- Foundation GameTests — GREEN;
- dedicated-server smoke — GREEN.

The canonical ID is now literal presentation identity followed by the localized label, so the identity remains observable even without a loaded language table while the physical client still receives the localized label.

### Reconciled GREEN

`main` advanced only in unrelated catalog/wiki files. The branch was merged with current `main` as a real two-parent merge without rebasing or discarding concurrent work.

Reconciled HEAD `23050c18fe710e430bf7082c3b3932c6785eca04`, workflow `34735843304`:

- Unit tests — GREEN;
- Diff sanity — GREEN;
- NeoForge build — GREEN;
- built JAR verification — GREEN;
- Foundation GameTests — GREEN;
- dedicated-server smoke — GREEN.

Effective diff against the reconciled `main` remains limited to the Stage 05.14 implementation/test/localization files.

## Files introduced or changed

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
