# 02.05 — Networking & Data-driven Content

## Objective
Keep client presentation synchronized without trusting it.

## Work
- Versioned payloads for cast intent/results, loadouts, cooldown snapshots and presentation metadata.
- Data registry/codec for spell metadata and balance parameters.
- Server-to-client sync only for data needed to render UI.
- Reject incompatible payload versions cleanly.
- Bound packet sizes and frequency; no per-tick full-state sync.

## Acceptance
Dedicated-server integration tests verify malformed/spammy requests are denied safely and normal casts synchronize minimal state.
