# 05 — Casting Runtime & Client Contracts

## State

`IMPLEMENTED / PHYSICAL RUNTIME-INPUT VALIDATION PENDING`

Stage 05 contains engineering/runtime authority for casting input, loadouts, selection semantics, synchronized presentation data, client configuration authority and provider coexistence boundaries.

Presentation-heavy work is owned by `plans/visual-production/05-casting-ux/`. Mixed 05.01–05.06 plans were split so UI/HUD/art/accessibility/animation and perceptual QA no longer live in the numbered runtime stage. 05.08–05.16 and their presentation checkpoints moved to that visual lane.

## Canonical engineering map

- `00-master-plan.md` — runtime/client architecture after extraction.
- `00-execution-status.md` — engineering closeout ledger.
- `🟡-PENDENTE-01-input-loadouts.md` — input/loadout authority, persistence and session semantics.
- `🟡-PENDENTE-02-radial-wheel.md` — non-casting radial selection/input authority.
- `🟡-PENDENTE-03-contextual-hud.md` — synchronized feedback/data/correlation contract.
- `🟡-PENDENTE-04-accessibility-client-config.md` — client-config authority/persistence/input semantics.
- `🟡-PENDENTE-05-final-client-validation-handoff.md` — physical runtime/input/provider validation only; perceptual presentation QA is split out.
- `🟡-PENDENTE-06-modpack-coexistence.md` — provider/invocation/one-settlement/input authority coexistence.
- `✅-07-presentation-data-contracts.md` — whether gameplay-derived data is authoritative/safe to render.

## Visual handoff

See `../visual-production/05-casting-ux/README.md` for editor/radial/HUD presentation, visual semantics, focus/navigation, iconography, targeting/inspection, VFX/audio/animation, onboarding, coexistence readability and real-client presentation QA.

## Authority boundary

The client expresses bounded intent and renders legitimately available state. The server remains authoritative for spell identity/admission, progression, cost, cooldown, target resolution, Arcane Danger and world effects. Provider-specific resources/state remain provider-owned unless an exact integration contract is proven.

Moving/splitting presentation plans changes planning ownership and future work sequencing only; it does not rewrite historical implementation evidence.