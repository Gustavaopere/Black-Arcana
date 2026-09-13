# 07A.06 — Sigils & Ritual Presentation

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Provide the requested mandalas/symbols/ritual readability as an original Black Arcana presentation layer reusable by Black Arcana and safe provider-hosted surfaces without making visuals authoritative.

## Clean-room rule

Mahou Tsukai 1.21.1 v1.36.28 is All Rights Reserved. Do not copy its projector images, circle textures, models, animations, sounds, text or other assets. The project also already forbids protected-asset reuse through D002/SOURCES/THIRD_PARTY_NOTICES.

The visual language must therefore be created from original geometry/assets or separately compatible licensed material with provenance recorded.

## Planned presentation contract

A data-driven sigil definition may describe only bounded presentation data such as:

- stable presentation id;
- ring/arc/line primitives;
- original glyph references from Black Arcana-owned assets;
- palette token;
- animation phase/speed within hard limits;
- radius/height/opacity limits;
- telegraph role (ritual, cast, warning, extraction, anchor, domain boundary);
- optional provider presentation key.

It must not contain commands, scripts, remote code, arbitrary file paths or gameplay effects.

## Server/client boundary

The server owns ritual/cast/session state. The client may render a sigil snapshot/events derived from that state.

Client rendering cannot:

- complete a ritual;
- choose cost/result;
- create an unlock;
- classify polarity;
- change target legality;
- bypass world safety;
- author arbitrary remote images.

## Provider reuse

### Eidolon

When a safe exact-version presentation hook exists, Black Arcana may visually coordinate with an Eidolon altar/ritual surface. The authoritative completion remains Black Arcana for Black Arcana mechanics unless provider identity/causality is sufficient for the reviewed adapter.

### Iron's

Use the sigil layer for telegraphs/channel indicators only where it improves readability and does not fight Iron's own client presentation. Provider spell visuals remain provider-owned.

### Ars Nouveau

Do not replace Ars glyph rendering. Optional integration is only for a Black Arcana-owned ritual/fusion state that needs a distinct telegraph and has a safe rendering seam.

## Visual grammar

Create a coherent original grammar rather than one bespoke texture per spell:

- concentric rings = containment/ritual scope;
- broken rings = unstable/forbidden state;
- radial anchors = material/offering slots;
- directed lines = transfer/sourcing direction;
- central seal = ritual/spell identity;
- outer warning marks = hazard/world-policy state;
- Luminal/Umbral/Arcane presentation palettes remain presentation only.

Accessibility requirements:

- polarity and danger must not be communicated by color alone;
- telegraphs need shape/motion/readability differences;
- reduced-motion config must retain gameplay-readable timing;
- low-particle mode must retain target/hazard boundaries.

## Remote/projector imagery

Arbitrary remote URL images are out of scope for v1 because they complicate provenance, moderation, privacy, cache invalidation and deterministic rendering. A future explicitly reviewed feature may revisit user-authored local/server-pack assets with strict size/type/provenance controls.

## Ritual material interaction

The requested “draw symbol and place materials” flow is implemented through original Black Arcana ritual anchors/offering positions or safe provider-native ritual slots. It does not copy Mahou's recipe/circle activation logic and does not require self-cutting.

Materials are server-validated and consumed/reserved through the canonical Stage 06 ritual transaction. Visual placement is never the sole proof of payment.

## Tests first

RED/unit/integration tests must cover:

- malformed/oversized sigil definitions rejected;
- unknown glyph/presentation ids fail safely;
- client packet cannot complete ritual or change authoritative values;
- reduced-motion/low-particle presentation does not alter server timing;
- ritual offering reservation/completion remains exactly-once;
- optional provider presentation missing -> gameplay either uses approved Black Arcana presentation fallback or fails closed according to the mechanic's identity requirement;
- no network payload accepts arbitrary remote URL asset references in v1.

## Acceptance

- original art/provenance only;
- presentation is reusable but non-authoritative;
- readable ritual material placement without self-harm activation;
- accessibility and payload budgets defined;
- no Mahou asset dependency.
