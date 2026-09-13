# 05 — Casting Runtime & Client Contracts

## State

`IMPLEMENTED / PHYSICAL RUNTIME-INPUT VALIDATION PENDING`

Stage 05 now contains only engineering/runtime authority for casting input, loadouts, selection semantics, synchronized presentation data, client configuration authority and coexistence boundaries.

The former presentation-heavy 05.08–05.16 plans and their implementation checkpoints moved to `plans/visual-production/05-casting-ux/`. Mixed 05.01–05.04 plans were split so final UI/HUD/art/accessibility presentation no longer lives in this numbered runtime stage.

## Canonical engineering map

- [`00-master-plan.md`](00-master-plan.md) — runtime/client architecture after extraction.
- [`00-execution-status.md`](00-execution-status.md) — engineering closeout ledger.
- [`🟡-PENDENTE-01-input-loadouts.md`](🟡-PENDENTE-01-input-loadouts.md) — input/loadout authority, persistence and session semantics.
- [`🟡-PENDENTE-02-radial-wheel.md`](🟡-PENDENTE-02-radial-wheel.md) — non-casting radial selection/input authority contract.
- [`🟡-PENDENTE-03-contextual-hud.md`](🟡-PENDENTE-03-contextual-hud.md) — synchronized feedback/data/correlation contract.
- [`🟡-PENDENTE-04-accessibility-client-config.md`](🟡-PENDENTE-04-accessibility-client-config.md) — client-config authority/persistence/input semantics.
- [`🟡-PENDENTE-05-final-client-validation-handoff.md`](🟡-PENDENTE-05-final-client-validation-handoff.md) — physical runtime/input/full-pack closeout procedure; visual-only rows are delegated to visual production.
- [`🟡-PENDENTE-06-modpack-coexistence.md`](🟡-PENDENTE-06-modpack-coexistence.md) — provider/input/authority coexistence.
- [`✅-07-presentation-data-contracts.md`](✅-07-presentation-data-contracts.md) — gate for whether a gameplay-derived datum is safe to render.

## Visual handoff

See [`../visual-production/05-casting-ux/README.md`](../visual-production/05-casting-ux/README.md) for:

- editor/radial/HUD presentation;
- visual language and state semantics;
- keyboard focus/navigation presentation;
- icon/resource resolution;
- targeting/aim presentation;
- spell inspection;
- VFX/audio/animation;
- onboarding/contextual help;
- visual/accessibility/full-pack presentation QA.

## Authority boundary

The client expresses bounded intent and renders legitimately available state. The server remains authoritative for spell identity/admission, progression, cost, cooldown, target resolution, Arcane Danger and world effects. Provider-specific resources/state remain provider-owned unless an exact integration contract is proven.

Moving presentation plans does not change implemented runtime behavior or historical evidence; it changes planning ownership and future work sequencing only.
