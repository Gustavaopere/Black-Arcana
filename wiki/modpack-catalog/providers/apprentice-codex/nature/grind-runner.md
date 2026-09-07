# Grind Runner

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:grind_runner`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 20`
- `manaCostPerLevel = 5`
- `castTime = 100 ticks / 5 s`
- summon targeting range: **8 blocks**
- ground search below candidate: **4 blocks**
- summon drop height: **4 blocks** over **5 ticks**.

Raw combat damage:

`2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.GRIND_RUNNER`.

Item processing rate:

`8 * spellPower / 100 items/s`, then optional Craftsman's Delight process-speed modifier.

Launch speed:

`0.9 + 0.05 * spellPower / 100`.

## Placement and release

The wheel cannot be summoned without valid ground. Candidate position is derived from target entity hit, block face or maximum look range, then the provider raycasts downward and requires a real collision surface.

On cast completion/cancellation, launch sustain time is derived from actual elapsed channel time:

`min(30, elapsedCastTicks / 2)`.

The wheel entity then owns travel, damage and item-processing behavior.

## Create compatibility

Provider guide semantics state that when Create is present, supported item grinding is handled as if processed by Crushing Wheels or a Millstone. That is a provider-native optional compatibility seam and must not be replaced with a second Black Arcana/Create processing pipeline.

## What it does

Summons an arcane wheel to grind entities and supported items, then releases it forward. The launched wheel can also hit the caster according to provider guide semantics.

## Deduplication

Occupies the **summoned grinder / item processing / released damaging wheel** niche.

## Confidence

`SOURCE-PINNED SPELL + SUMMON/GROUND/LAUNCH PARAMETERS / WHEEL PROCESSING + EXACT CREATE RECIPE BRIDGE QA PENDING`