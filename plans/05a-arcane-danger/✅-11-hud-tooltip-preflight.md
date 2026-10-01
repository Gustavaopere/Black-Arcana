# 05A.11 — Hazard Preflight Presentation Data Contract

## Objective

Expose bounded server-authored Arcane Danger facts for client presentation without making prediction authoritative.

HUD/tooltip wording, layout and readability are owned by `plans/visual-production/05a-arcane-danger/11-hud-tooltip-presentation.md`.

## Networking/authority

No client packet may submit resistance, Corruption, Backlash damage, danger tier, gate result, loadout slot or bypass decisions. Synchronization is event-driven and bounded, never per-tick full-state spam.

### Arcane Resistance forecast

- client submits only bounded spell id and monotonic request id;
- server resolves canonical danger profile and effective Arcane Resistance through the approved side-effect-free preview mirror;
- preview fails closed unless all gameplay resistance providers have safe mirrors and aggregate diagnostics are clean;
- equipment, RPG Skill Tree hazard attributes and optional Curios mirrors remain runtime-scoped provider integrations;
- preview performs no hazard activation/reservation/settlement or progression/mastery award;
- server rate-limits requests;
- stale response ids/profile revisions are rejected;
- static synchronized danger metadata remains fallback when dynamic forecast is unavailable.

### Predictable gates

`ArcanaCastEngine.previewReadOnlyGates(...)` evaluates approved query-only identity/loadout, progression, cooldown and cost availability in canonical order. The server derives the loadout slot. Replay admission, target resolution, world policy and hazard preparation remain cast-time authority and are excluded.

Transport remains bounded to approved categories such as `CLEAR`, `IDENTITY`, `PROGRESSION`, `COOLDOWN`, `COST` and `UNAVAILABLE`. `CLEAR` is never a success guarantee.

### Corruption/strain state

No client Corruption/strain snapshot is invented by this task. A future UI requires an explicit bounded server-authored snapshot plus stale-state/anti-spam contract.

## Automated evidence

- runtime/network pipeline: workflow `33422931351` at `44dda0c3586cb17d5461c18ccbb75432d9ac1626`;
- presentation-helper RED: `33471498889`;
- GREEN checkpoint: workflow `33471722454` at `7c617983a266e084cacb98682e669cce561e333f`.

## Remaining engineering acceptance

Payload bounds, provider-preview completeness, stale-state rejection, server-derived slot, gate ordering and fail-closed behavior remain engineering authority. Perceptual HUD/tooltip validation is delegated to visual production.
