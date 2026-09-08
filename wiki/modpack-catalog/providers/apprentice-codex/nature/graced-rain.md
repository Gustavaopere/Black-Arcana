# Graced Rain

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:graced_rain`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 15`
- `manaCostPerLevel = 5`
- `castTime = 400 ticks / 20 s`
- target range: **16 blocks**

Heal amount seeded into the cloud:

`2 * spellPower / 100`

The spell UI displays healing per second as `healAmount * 2`; exact cloud heal cadence is owned by `GracedRainCloudEntity`.

Effect radius:

`1 + floor(spellPower / 200)` blocks.

Growth interval:

`max(1, 5 - round(spellPower / 100))` ticks.

## Target/anchor modes

At cast start the spell can:

- attach the cloud to a valid living target;
- anchor it to a validated block target;
- otherwise anchor it around the resolved target position.

Block anchoring is validated before creating the cloud; invalid anchor geometry rejects placement rather than spawning an unmanaged effect.

## What it does

Provider guide semantics: summons a rain cloud with healing power; entities under it recover health and nearby vegetation is nourished/grown.

The cloud entity owns healing/growth cadence and release lifecycle. One cloud tick affecting many entities/plants remains child behavior of one provider cast.

## Provider modifier

The spell implements the provider's Craftsman's Delight affected-spell contract. Any bonus is provider-owned and must not be duplicated as an external process/healing modifier without a real bridge.

## Deduplication

Occupies the **anchored/following healing + plant-growth cloud** niche.

## Confidence

`SOURCE-PINNED SPELL + CLOUD CONFIG / EXACT HEAL-GROWTH ENTITY CADENCE + RUNTIME QA PENDING`