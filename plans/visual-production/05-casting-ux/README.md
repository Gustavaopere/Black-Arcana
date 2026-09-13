# Visual Production — Stage 05 Casting & UX

This folder owns the presentation half of the former mixed Stage 05 planning package.

The numbered Stage 05 folder remains authoritative for input intent, server-owned loadouts, network/data authority, synchronization, stale-state handling and runtime/provider integration invariants. This folder owns UI/HUD composition, information architecture, visual semantics, iconography, presentation accessibility, targeting/inspection surfaces, VFX/audio/animation, contextual help and perceptual real-client acceptance.

## Split presentation plans

- `01-loadout-editor-presentation.md`
- `02-radial-wheel-presentation.md`
- `03-contextual-hud-presentation.md`
- `04-accessibility-presentation.md`
- `🟡-PENDENTE-05-final-client-validation-handoff.md` — visual/perceptual half only; runtime/input/provider checks remain numbered.
- `06-modpack-coexistence-presentation.md`

## Moved presentation plans

- 05.08 — Visual Language & State Semantics
- 05.09 — Keyboard Focus & Navigation
- 05.10 — Loadout Editor Information Architecture
- 05.11 — Contextual Feedback Orchestration
- 05.12 — Iconography & Resource Resolution
- 05.13 — Targeting & Aim Presentation
- 05.14 — Spell Details & Inspection Presentation
- 05.15 — Casting VFX / Audio / Animation Presentation
- 05.16 — Onboarding / Discoverability / Contextual Help

All presentation files consume server-authored/runtime contracts and must not introduce gameplay authority.

Historical implementation checkpoints for 05.10–05.16 remain under `checkpoints/`. Exact mixed pre-extraction documents used for audit remain under `_migration-source/`.