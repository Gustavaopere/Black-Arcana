# Deep Sensor

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:deep_sensor`
- **Iron's school:** Eldritch
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 100 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 60`
- `manaCostPerLevel = 20`
- `castTime = 0`
- fixed sensing range: **24 blocks**
- effect duration: `round(spellPower * 6)` ticks

## What it does

A successful cast applies the provider's `Sense Sensor` effect to the caster.

Provider guide semantics: while active, the player senses nearby vibrations through walls in a Sculk Sensor-like way and sees visual cues whose color communicates distance: red is nearer, blue is farther. The effect suppresses vibrations caused by the player's own movement, but does **not** suppress item use, block placement or block breaking.

This is a perception/sensing capability, not a generic wallhack contract. The provider owns which vibration events become cues and how they are rendered.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot acquisition remains in the provider-wide acquisition audit.

## Deduplication

Directly overlaps Black Arcana Divination. A Black Arcana vibration-sensing spell that merely highlights through walls would duplicate Deep Sensor unless it has materially different information semantics, costs/risks and targeting constraints.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / EFFECT EVENT FILTERING + FULL CLIENT RENDER QA PENDING`