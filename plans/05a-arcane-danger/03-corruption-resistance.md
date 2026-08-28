# 05A.03 — Corruption Resistance

## Objective
Create a persistent corruption channel that is independent from Arcane Resistance and produces meaningful long-term consequences without becoming a decorative bar or duplicating Enshrouded.

## Separation
Arcane Resistance answers: “can the caster physically/spiritually withstand dangerous arcane energy now?”

Corruption Resistance answers: “how strongly does forbidden magic alter the caster over time?”

High Arcane Resistance + low Corruption Resistance is valid: the caster survives immediate backlash but accumulates corruption. The opposite build is also valid.

## State
Create bounded per-player corruption state with:
- current corruption units;
- last meaningful update/recovery metadata;
- schema/version information;
- threshold/band evaluation;
- bounded provenance/telemetry counters only where needed.

Persist through the existing Overworld/global `BlackArcanaSavedData`. Relog/restart must not cleanse corruption.

## Resistance
Use a separate registered provider registry/channel. It may reuse the same diminishing-return utility as Arcane Resistance but has independent constants/caps and independent contribution sources.

A profile may define:
- base corruption on committed dangerous cast;
- optional corruption per confirmed eligible damage;
- minimum unavoidable corruption floor;
- resistance multiplier/cap;
- threshold consequence hooks.

## Consequences
Stage 05A establishes a small bounded consequence framework, not dozens of content effects. Threshold transitions may publish events/hooks and apply a minimal test effect/diagnostic. Actual spell/domain-specific corruption consequences belong to later content/balance stages.

Corruption is explicitly NOT Enshrouded Shroud exposure/corruption. Future interaction requires a bridge/provider.

## RED
Tests:
- zero corruption resistance leaves full configured corruption acquisition;
- resistance lowers acquisition monotonically without going negative;
- unavoidable profile floor survives high resistance;
- corruption persists through save/load;
- malformed/oversized persisted values clamp/fail safely;
- threshold transitions fire once per crossing rather than every tick;
- provider absence contributes zero and does not disable Black Arcana;
- Arcane Resistance cannot accidentally substitute for Corruption Resistance.

## GREEN
Implement persistent state, separate provider resolution, bounded acquisition and threshold transition model.

## REFACTOR
Prefer lazy/event-driven updates rather than a global player scan every tick.

## Acceptance
Corruption survives restart, has a distinct resistance build channel and exposes meaningful threshold transitions without creating an unrelated second survival-mod corruption system.
