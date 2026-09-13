# 05A.11 — HUD, Tooltip & Preflight

## Objective
Expose danger clearly before casting without making client prediction authoritative or adding a permanent clutter bar.

## Presentation
- Spell tooltip/radial metadata shows danger tier and concise resistance recommendation.
- Contextual preflight may show current effective Arcane Resistance, expected risk class and hard-gate reason only when backed by a bounded server-authored read-only projection.
- Corruption/strain feedback appears only when relevant and when an explicit synchronized presentation contract exists.
- Exact server settlement remains authoritative; client values are advisory presentation derived from synchronized bounded data.

## Networking
No client packet may submit resistance, corruption, backlash damage, danger tier, gate result, loadout slot or bypass decisions. Synchronization is event-driven and bounded, not per-tick full-state spam.

## Implemented automated presentation lanes

### Selected-spell Arcane Resistance forecast

The contextual HUD has a server-authored read-only Arcane Resistance forecast for the currently selected spell:

- the client submits only a bounded spell id and monotonic request id;
- the server resolves the canonical danger profile and computes effective Arcane Resistance through a runtime-scoped preview mirror of gameplay resistance providers;
- preview availability fails closed unless every gameplay Arcane Resistance provider has a side-effect-free mirror and the aggregate snapshot is diagnostic-free;
- standard equipment, RPG Skill Tree hazard attributes and optional Curios equipment currently install preview mirrors;
- preview queries do not open hazard sessions, reserve corruption/strain state, consume emergency protection or award progression/mastery;
- the server rate-limits forecast requests and the client refreshes only for selected non-normal danger tiers while contextual selection feedback can be displayed;
- stale responses are rejected by request id, danger-profile reload clears the cached forecast, and a dynamic forecast is rendered only when its tier/threshold revision matches current static server-authored preflight metadata;
- for non-normal danger tiers the HUD can display current/minimum/recommended Arcane Resistance plus factual threshold status: blocked below minimum, below recommended, recommendation met, or unavailable;
- meeting the recommended threshold is not labeled safe because residual danger/Backlash semantics remain authoritative;
- the original synchronized static danger metadata remains the fallback when a matching dynamic forecast is unavailable or has not arrived.

### Read-only predictable cast gates

The same bounded selected-spell forecast now carries a server-authored categorical projection of the established query-only cast gates:

- `ArcanaCastEngine.previewReadOnlyGates(...)` evaluates identity/loadout, progression, cooldown and resource-cost availability in canonical order;
- the server derives the loadout slot from the canonical server loadout; the client never submits it;
- the runtime returns no projection when no engine is installed for the spell;
- replay admission, target resolution, world policy and hazard preparation are deliberately excluded because they are cast-time authority or are not safe read-only projections;
- the payload transports only `CLEAR`, `IDENTITY`, `PROGRESSION`, `COOLDOWN`, `COST` or `UNAVAILABLE`, never arbitrary denial detail;
- `CLEAR` is presented as “no predictable gate blocks”, not as a cast-success guarantee;
- exceptions, missing runtime data or unavailable projection paths fail closed.

### Loadout hazard tooltip

The loadout editor now shows the synchronized static hazard preflight on hover:

- the tooltip is derived only from `HazardPreflightPayload` already synchronized by the server;
- it shows danger tier and the same minimum/recommended Arcane Resistance metadata used by the radial/static fallback;
- it performs no additional request, prediction or gameplay mutation.

### Corruption / strain presentation

No Corruption/strain client state is retained in this closure. The current client networking surface has no bounded synchronized Corruption/strain snapshot contract, so this task does not invent a new authority/state-sync surface merely for optional presentation. A future UI addition requires an explicit server-authored bounded snapshot contract plus stale-state and anti-spam evidence.

The detailed authority/anti-abuse contract and automated evidence are recorded in `docs/qa/stage05a11-resistance-forecast.md`.

## Automated evidence

- gate/runtime/networking full pipeline: workflow `33422931351` at `44dda0c3586cb17d5461c18ccbb75432d9ac1626`;
- presentation RED: workflow `33471498889`, failing only on the intentionally absent gate/tooltip helpers;
- presentation GREEN: workflow `33471722454` at `7c617983a266e084cacb98682e669cce561e333f`, passing unit tests, diff sanity, NeoForge build, JAR inspection, Foundation GameTest server and dedicated-server smoke.

## Still open

The deterministic/automated implementation scope of 05A.11 is present. The task remains operationally open only for the real-client presentation gate:

- verify gate wording and resistance forecast together in a real client;
- verify loadout hover tooltip placement/readability across the required resolutions and GUI scales;
- verify reconnect/datapack stale-state behavior and accessibility settings;
- record evidence in `docs/qa/casting-ux-manual-matrix.md` without marking any row passed unless it was actually exercised.

## Acceptance
Automated tests cover payload bounds/state clearing, authoritative denial text, resistance forecast payload/codec invariants, fail-closed preview-provider completeness/diagnostics, read-only gate ordering/runtime ownership, server-derived loadout slot, bounded gate transport, stale forecast revision fallback and static loadout tooltip derivation. Manual Stage 05/09 visual matrix covers common GUI scales, disabled HUD, accessibility settings, stale reconnect state, selected-spell hazard/gate forecast presentation and loadout tooltip usability.
