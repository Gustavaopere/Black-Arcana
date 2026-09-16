# Mirage Avoidance

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mirage_avoidance`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 3 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 0`

Exact provider event timings:

- total effect state: `25 ticks = 1.25 s`
- invulnerability: `15 ticks = 0.75 s`
- initial freeze: `2 ticks`
- slide interval constant: `18 ticks`
- vulnerable recovery starts at tick `20`
- horizontal run speed constant: `0.42 blocks/tick` before the linear slide decay
- slow-fall lower vertical clamp while sliding: `-0.08`

## Server-owned state and input lock

The server stores start time, active-until, invulnerability-until and movement input in the provider spell capability, then syncs that state to the client.

While active the provider cancels attacks and block/item/entity interactions. Incoming damage is cancelled only while the invulnerability window is active. Movement is then driven by the provider's timed slide/freeze/recovery rules and persistent game-time sanitization.

The spell rejects recasting while its own input lock remains active.

## What it does

The guide describes a very brief complete evade followed by gliding/sliding movement, independent of spell level/power. The exact source confirms that the spell has no spell-power scaling and has a shorter invulnerability window than the full movement/effect state.

## Causality

Damage cancellation, movement and input suppression are all parts of one Mirage Avoidance activation. They are not independent Black Arcana defensive procs.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **short instant invulnerability + locked evasive slide** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT TIMING+SERVER STATE+DAMAGE CANCEL+INPUT LOCK / CLIENT FEEL+NETWORK CORRECTION+PACK RUNTIME QA PENDING`