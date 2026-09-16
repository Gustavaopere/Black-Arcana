# Combustion Jet

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:combustion_jet`
- **Iron's school:** Fire
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 200`
- `baseManaCost = 30`
- `manaCostPerLevel = 10`
- `castTime = 0`
- fixed range: **10 blocks**

Raw damage:

`1 + spellPower / 100`

then multiplied by `DamageMultiplierKey.COMBUSTION_JET`.

Burn duration:

`max((spellLevel - 1) * 40, 10)` ticks.

## Exact heat-wave geometry/lifecycle

The exact wave entity establishes:

- travel speed: **2.25 blocks/tick**;
- wave width: **9 blocks**;
- wave height: **1 block**;
- wave depth: **1.5 blocks**;
- explicit horizontal knockback strength: **1.0**;
- fixed maximum travel distance seeded as 10 blocks by the spell;
- each target UUID is affected at most once by a wave instance;
- block collision is evaluated through a narrow central collision volume so the wide visual/damage wave is not trivially erased by side geometry;
- anti-magic susceptibility is provider-owned.

The damage call itself uses no automatic knockback, after which the wave applies its own directional knockback. This is one provider-owned settlement and must not be double-processed.

## What it does

Provider guide semantics: emits a broad heat wave in the view direction. Fire-resistant targets cannot receive the intended heat damage according to provider semantics, but the spell still attempts to push targets back. Successfully affected living targets receive the configured burn duration.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **broad Fire force-wave / burn / directional knockback** niche. This is especially relevant to Chaos design: a generic red force blast is not distinct merely because Black Arcana calls it Chaos.

## Confidence

`SOURCE-PINNED SPELL + WAVE ENTITY / PACK CONFIG MULTIPLIER + FIRE-IMMUNITY RUNTIME QA PENDING`