# Shock

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:shock`
- **Iron's school:** Lightning
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Instant
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 500`
- `spellPowerPerLevel = 50`
- `baseManaCost = 15`
- `manaCostPerLevel = 2`
- `castTime = 0`
- combat targeting range: **24 blocks**

Raw damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.SHOCK`.

## Targeting

Server-side targeting uses two provider raycast passes:

1. thin assisted raycast width **1.0** over 24 blocks;
2. if no target, wide assisted raycast width **4.0** over the same combat range.

If neither pass resolves a valid combat target, the spell still creates its visual bolt toward a block/empty position up to **16 blocks**, but applies no entity damage.

The visual Shock Bolt life is randomized from **5–8 ticks**. Damage itself is settled immediately server-side before the visual bolt entity is spawned.

## What it does

Provider guide semantics: fires a compact lightning bolt converted from elemental energy. It is a simple, low-cooldown direct Lightning attack rather than a persistent projectile authority.

## Causality

The bolt entity is presentation after immediate server-side damage settlement. A future integration must not treat later visual-bolt callbacks as a second damaging cast.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **fast low-cooldown assisted-target direct lightning strike** niche. A Black Arcana lightning zap with the same targeting/cooldown identity would be redundant.

## Confidence

`SOURCE-PINNED SPELL + SERVER TARGETING / PACK CONFIG MULTIPLIER + VISUAL CLIENT QA PENDING`