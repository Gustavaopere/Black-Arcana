# Stage 05A.11 — Selected-spell Arcane Resistance forecast

This note records the automated contract for the Stage 05A.11 selected-spell resistance presentation sublane. It does **not** close the full 05A.11 task or the Stage 05 real-client gate.

## Authority boundary

- The client submits only a bounded spell identifier plus a monotonic request id.
- The server resolves the canonical danger profile and computes the effective Arcane Resistance preview.
- The client never submits resistance, danger tier, threshold status or bypass decisions.
- The preview never opens a hazard session, reserves corruption/strain state, consumes emergency protection or mutates RPG progression.
- Actual cast admission and denial details remain authoritative in the normal Stage 02/05 cast pipeline.

## Provider coverage

A runtime-scoped preview registry mirrors only Arcane Resistance providers with an explicitly side-effect-free presentation path. The preview is unavailable unless the mirror count matches the gameplay registry and the aggregate snapshot contains no diagnostics.

Current mirrored providers:

- standard equipment;
- RPG Skill Tree hazard attributes through the existing read-only progression query;
- Curios equipment snapshots when the optional integration is available.

An unknown future gameplay provider therefore makes the forecast unavailable until it also installs a safe preview provider. Partial resistance is never presented as complete.

## Transport and anti-abuse

- request: one spell id + request id;
- response: availability, danger tier, effective/minimum/recommended Arcane Resistance and server-derived threshold status;
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
- factual threshold state: `Blocked: resistance below minimum`, `Below recommended resistance`, `Resistance recommendation met`, or `Unavailable`.

Meeting the recommended resistance is deliberately **not** labeled safe: the danger profile and residual Backlash semantics remain authoritative and may still carry risk. The static danger metadata remains the fallback if no matching dynamic forecast has arrived.

## Explicitly still open

This sublane does not yet provide a complete pre-cast simulation of every canonical denial gate. In particular, strain, cooldown/resource/progression conditions and other admission failures remain authoritative only through the normal cast result unless a future read-only projection is explicitly designed for them. Spell-tooltip coverage and the required real-client visual/input matrix also remain open.
