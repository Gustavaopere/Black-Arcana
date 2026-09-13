# Visual Production Extraction Audit

This ledger records the separation of presentation/asset work from numbered Black Arcana engineering plans.

## Classification rules

- **MOVED** — document is predominantly UI/HUD/art/client-presentation work and moved intact.
- **SPLIT** — runtime/authority requirements stay in the numbered stage; presentation requirements move here.
- **RETAINED** — a visual-looking statement is actually a runtime contract (for example cosmetic fallback mode, synchronized visual identity/key or renderer-safe state) and therefore remains engineering.
- **AUDITED / NO EXTRACTION** — no concrete texture/UI/model/animation/VFX/audio production specification was found.

## Stage 05 — Casting & UX

### MOVED

- `05.05 — Final Real-Client Validation Handoff` -> `visual-production/05-casting-ux/`; numbered location is now an engineering-boundary stub.
- 05.08–05.16 -> `visual-production/05-casting-ux/` intact.
- implementation checkpoints for 05.10–05.16 -> `visual-production/05-casting-ux/checkpoints/` intact.

### SPLIT

- 05.01 — server-owned loadout/input/session stays runtime; editor/search/icon/apply-state presentation moved.
- 05.02 — selection/cast separation stays runtime; radial geometry/cards/icons/visual states moved.
- 05.03 — synchronized data/correlation/stale-state stays runtime; HUD layout/hierarchy/wording moved.
- 05.04 — config registration/authority/input semantics stays runtime; visual accessibility/tuning moved.
- 05.06 — Iron's hosted-cast authority, one-root/one-settlement and optional-provider boundaries stay runtime; HUD overlap, key ergonomics, Spell Actionbar/Epic Fight client coexistence and animation/readability QA moved to `06-modpack-coexistence-presentation.md`.
- 05.07 is **RETAINED** because it defines whether data is authoritative/safe to render, not how it looks.

## Stage 05A — Arcane Danger

- 05A.11 — **SPLIT**. Forecast/gate networking, server ownership and stale-state remain engineering; HUD/tooltip wording/layout/readability moved.

## Stage 06 — Rituals

**AUDITED / NO EXTRACTION** for the current runtime plans. `06.05` is primarily provider/transaction/persistence/activation validation despite mentioning provider presentation. Future concrete ritual asset work belongs under `visual-production/06-rituals/`.

## Stage 07 — Spell Domains

- 07.01 Blood & Curses — **AUDITED / NO EXTRACTION**; no concrete asset-production spec.
- 07.02 Souls & Death — **AUDITED / NO EXTRACTION**; provider-presentation references are routing/identity gates, not art specs.
- 07.03 Projection & Arsenal — **AUDITED / NO EXTRACTION**; presentation/input references are authority boundaries.
- 07.04 Space & Displacement — **AUDITED / NO EXTRACTION**; host presentation ownership stays a provider boundary.
- 07.05 Black Flame — **SPLIT/RETAINED**. Runtime keeps the canonical visual plane, `COSMETIC` mode, bounded frontier and degradation semantics. Concrete forbidden soul-fire identity is extracted to `05-black-pyre-presentation.md`.
- 07.06 Forbidden Domains — **AUDITED / NO EXTRACTION**. Cosmetic field profile is a runtime world-effect classification; no concrete asset spec exists yet.
- 07.07 Familiars & Divination — **SPLIT/RETAINED**. Noetic/Astral identity, movement, loaded-only safety and termination remain runtime; camera transition/feel/restoration presentation and future astral assets are extracted to `07-noetic-camera-presentation.md`. The spell specification gate remains runtime because it blocks canonical gameplay specification.
- 07.08 Hematic Reservoirs — **SPLIT**. Controller/structure/transactions/persistence/network data remain runtime; open-basin form, blood-surface rendering, low/high fill, stale-source presentation and future assets move to `08-hematic-reservoir-presentation.md`.

## Stage 07A — Arcane Polarity, Fusion & Metamagic

- 07A.01 — **RETAINED**; server-derived polarity and read-only presentation metadata are runtime data contracts.
- 07A.02 — **SPLIT**. Umbral Codex/Ankh semantic authority and resurrection/life-drain composition remain runtime; Luminal/Umbral palettes, motifs, extraction links and consequence feedback move to `02-white-black-identity-presentation.md`.
- 07A.03/04 — **RETAINED**; `visual key`/`presentation key` are server-authored identifiers consumed by presentation, not art specs.
- 07A.05 — **RETAINED**; provider presentation references and clean-room prohibitions are routing/provenance boundaries.
- 07A.06 — **SPLIT**. Server ritual state/payload/material/provider authority stays Stage 07A; sigil geometry/palette/animation/telegraph/accessibility moved.
- 07A.07/08 — **AUDITED / NO EXTRACTION**; provider verification/hardening remain engineering. Sigil presentation events/payload ceilings remain runtime safety tests.

## Stages 00–04, 08–09

Audited at directory level. Current plans are foundation/catalog/core/integration/world-safety/progression/release engineering; no standalone presentation-production plan was moved.

## Audit preservation

Exact pre-extraction blobs for mixed documents are stored under `plans/visual-production/_migration-source/` and are explicitly non-canonical. They exist only to prove no historical requirement was silently discarded during separation.