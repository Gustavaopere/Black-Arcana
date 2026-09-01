# Stage 05A.11 — Selected-spell hazard preflight presentation

This note records the automated contract for the Stage 05A.11 selected-spell presentation lanes. It does **not** close the Stage 05 real-client gate.

## Authority boundary

- The client submits only a bounded spell identifier plus a monotonic request id.
- The server resolves the canonical danger profile, computes the effective Arcane Resistance preview and evaluates only the established query-only cast gates.
- The client never submits resistance, danger tier, threshold status, loadout slot, gate result or bypass decisions.
- The server derives the loadout slot from the canonical server loadout before evaluating the gate projection.
- The preview never claims replay admission, resolves targets, authorizes world mutation, opens a hazard session, reserves corruption/strain state, consumes emergency protection, reserves resource cost, starts cooldowns, executes a spell or mutates RPG progression.
- Actual cast admission and denial details remain authoritative in the normal Stage 02/05 cast pipeline.

## Provider coverage

A runtime-scoped preview registry mirrors only Arcane Resistance providers with an explicitly side-effect-free presentation path. The resistance preview is unavailable unless the mirror count matches the gameplay registry and the aggregate snapshot contains no diagnostics.

Current mirrored providers:

- standard equipment;
- RPG Skill Tree hazard attributes through the existing read-only progression query;
- Curios equipment snapshots when the optional integration is available.

An unknown future gameplay provider therefore makes the forecast unavailable until it also installs a safe preview provider. Partial resistance is never presented as complete.

## Predictable cast gates

`ArcanaCastEngine.previewReadOnlyGates(...)` evaluates, in canonical order, only services whose established contract is query-only:

1. identity/loadout;
2. progression;
3. cooldown;
4. resource cost availability.

The bounded server-authored result is one of `CLEAR`, `IDENTITY`, `PROGRESSION`, `COOLDOWN`, `COST` or `UNAVAILABLE`. Arbitrary denial detail is not transported by this forecast.

`CLEAR` means only that none of those predictable read-only gates currently blocks the selected spell. It is deliberately **not** a promise that a later cast will succeed: replay admission, target resolution, world policy and hazard preparation remain cast-time authority.

If the runtime has no engine for the spell, the spell cannot be resolved, a preview service fails, or the combined projection cannot be produced safely, the forecast fails closed as unavailable.

## Transport and anti-abuse

- request: one spell id + request id;
- response: availability, danger tier, effective/minimum/recommended Arcane Resistance, server-derived resistance threshold status, gate-forecast availability and bounded gate category;
- server request limiter: 4 requests / 20 ticks per player with bounded tracked-player state;
- client refresh: at most once every 20 ticks, only for a selected non-normal danger tier while contextual selection feedback can be displayed;
- stale responses are ignored by request id;
- datapack hazard-preflight replacement clears the cached forecast;
- a dynamic forecast is rendered only when its danger tier and thresholds match the current static server-authored preflight revision, preventing an in-flight stale response from overriding newer danger metadata.

## Presentation

For non-normal danger tiers the contextual HUD can display:

- current effective Arcane Resistance;
- minimum server threshold;
- recommended server threshold;
- factual threshold state: `Blocked: resistance below minimum`, `Below recommended resistance`, `Resistance recommendation met`, or `Unavailable`;
- a separate bounded preflight line for the predictable gate category.

Meeting the recommended resistance is deliberately **not** labeled safe: the danger profile and residual Backlash semantics remain authoritative and may still carry risk. Likewise, a clear gate projection is worded as `no predictable gate blocks`, not as cast success.

The loadout editor now shows the synchronized static hazard preflight as a hover tooltip. It performs no new request or prediction and uses the same server-authored danger tier/minimum/recommended metadata already used by the radial/HUD fallback.

## Corruption / strain presentation decision

No Corruption/strain client presentation is added in this closure. The current client networking surface has no bounded Corruption/strain snapshot contract suitable for factual display, and adding a new state sync solely to satisfy an optional presentation lane would broaden the network/authority surface without an established need. Future UI for those values requires an explicit bounded server-authored synchronization contract and its own stale-state/anti-spam acceptance evidence.

## Automated evidence

The gate/runtime/networking sublane first passed the full pipeline on workflow `33422931351` at `44dda0c3586cb17d5461c18ccbb75432d9ac1626`.

The HUD gate presentation and loadout tooltip were developed with an explicit RED at workflow `33471498889`, where compilation failed only because the new presentation helpers did not yet exist. The corresponding GREEN head `7c617983a266e084cacb98682e669cce561e333f` passed workflow `33471722454` through unit tests, diff sanity, NeoForge build, JAR inspection, Foundation GameTest server and dedicated-server smoke.

## Explicitly still open

The automated 05A.11 presentation scope described above is implemented, but Stage 05/05A cannot be declared complete until the required real-client visual/input matrix is exercised. In particular, gate wording, loadout tooltip placement/readability, GUI scales, reconnect/stale state and accessibility behavior still require real Minecraft client evidence in `docs/qa/casting-ux-manual-matrix.md`.
