# Visual Production Extraction Audit

This ledger records the separation of presentation/asset work from numbered Black Arcana engineering plans.

## Classification rules

- **MOVED** — document is predominantly UI/HUD/art/presentation and was moved intact.
- **SPLIT** — runtime/authority requirements stay in the numbered stage; presentation requirements move here.
- **RETAINED** — a visual-looking statement is actually a runtime contract (for example, a cosmetic fallback mode or render-safe synchronized identity) and therefore remains in engineering.
- **AUDITED / NO EXTRACTION** — no concrete texture/UI/model/animation/VFX/audio production specification was found; generic fantasy wording is not treated as an asset plan.

## Stage 05 — Casting & UX

### Moved intact

- `05.08 — Visual Language & State Semantics` -> `visual-production/05-casting-ux/`.
- `05.09 — Keyboard Focus & Navigation` -> `visual-production/05-casting-ux/`.
- `05.10 — Loadout Editor Information Architecture` -> `visual-production/05-casting-ux/`.
- `05.11 — Contextual Feedback Orchestration` -> `visual-production/05-casting-ux/`.
- `05.12 — Iconography & Resource Resolution` -> `visual-production/05-casting-ux/`.
- `05.13 — Targeting & Aim Presentation` -> `visual-production/05-casting-ux/`.
- `05.14 — Spell Details & Inspection Presentation` -> `visual-production/05-casting-ux/`.
- `05.15 — Casting VFX / Audio / Animation Presentation` -> `visual-production/05-casting-ux/`.
- `05.16 — Onboarding / Discoverability / Contextual Help` -> `visual-production/05-casting-ux/`.
- implementation checkpoints for 05.10–05.16 -> `visual-production/05-casting-ux/checkpoints/`.

### Split

- `05.01 — Input & Loadouts`: server-owned loadout/input/session rules stay in Stage 05; editor layout, search/filter, icon and apply-state presentation move to visual production.
- `05.02 — Radial Wheel`: selection/cast separation and authority rules stay in Stage 05; radial geometry, cards, icons, visual states and presentation QA move to visual production.
- `05.03 — Contextual HUD & Feedback`: synchronized data/authority/correlation/stale-state contracts stay in Stage 05; HUD layout, hierarchy, wording, anti-clutter and accessibility presentation move to visual production.
- `05.04 — Accessibility & Client Configuration`: config registration/authority/persistence/input semantics stay in Stage 05; visual accessibility behavior and presentation tuning move to visual production.
- `05.05 — Final Real-Client Validation Handoff`: runtime/input/coexistence validation remains Stage 05; visual-only acceptance is delegated to the visual-production QA backlog.
- `05.06 — Modpack Coexistence`: provider/input authority remains Stage 05; observed visual overlap/readability fixes belong to visual production.
- `05.07 — Presentation Data Contracts`: retained in Stage 05 because it defines whether data is safe/authoritative to render, not how it looks.

## Stage 05A — Arcane Danger

- `05A.11 — HUD, Tooltip & Preflight`: **SPLIT**. Forecast/gate networking, server ownership and stale-state rules remain engineering; HUD/tooltip wording/layout/readability requirements move to `visual-production/05a-arcane-danger/`.

## Stage 06 — Rituals

Existing plans are primarily transaction/provider/runtime contracts. No standalone concrete texture/model/animation/audio production plan was identified in the Stage 06 file set during this audit. Future ritual presentation belongs under `visual-production/06-rituals/`.

## Stage 07 — Spell Domains

Spell-domain plans often mention a visual plane, cosmetic fallback, telegraph or fantasy identity. Those statements remain engineering when they define gameplay-safe degradation, world-mode behavior or synchronized runtime state.

Concrete asset-production details (textures/models/animations/VFX/audio) are deferred to `visual-production/07-spell-domains/`. The current domain plans are not moved wholesale because they are overwhelmingly authoritative mechanics/safety plans.

Examples retained in engineering:

- Black Pyre's `COSMETIC`/visual plane exists as a runtime degradation mode; the future appearance of that plane belongs to visual production.
- Astral projection identity/viewpoint/entity lifecycle remains runtime/client-control engineering; the projection's final model/texture/VFX/audio presentation belongs to visual production.

## Stage 07A — Arcane Polarity, Fusion & Metamagic

- `07A.06 — Sigils & Ritual Presentation`: **SPLIT**. Original visual grammar, glyph/asset rules, animation/palette/telegraph presentation and accessibility move to visual production. Server ritual state, payload safety, material settlement and provider-authority boundaries stay in Stage 07A.

## Stages 00–04, 08–09

Audited at directory level. Their current plans are foundation/catalog/core/integration/world-safety/progression/release engineering. No standalone presentation production plan is moved from those stages in this extraction.
