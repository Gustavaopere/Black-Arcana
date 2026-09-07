# Mana Charge

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_charge`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Continuous
- **Cooldown:** 120 s
- **Cast mana cost:** 0
- **Recovered resource:** canonical Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 25`
- `baseManaCost = 0`
- `manaCostPerLevel = 0`
- `castTime = 100 ticks / 5 s`

Displayed mana recovery per second:

`spellPower * DamageMultiplierKey.MANA_CHARGE config multiplier`

The configuration plumbing reuses the provider's damage-multiplier infrastructure name, but the resulting value is mana recovery, not damage.

## Exact recovery cadence

Every **10 cast ticks / 0.5 s**, the spell computes half of the per-second recovery value and calls `MagicTools.recoverManaSafely(...)` against the same `MagicData` that owns the caster's Iron's mana.

Therefore, over an uninterrupted second, two half-second recovery settlements equal the displayed recovery-per-second value, subject to the provider's safe recovery/cap semantics.

## Authority

This spell proves that Apprentice's Codex does **not** introduce a parallel mana resource for this capability. It writes into canonical Iron's `MagicData` mana.

Black Arcana/RPG integrations must never mirror the recovered amount into another mana channel or independently reimburse mana from the same Mana Charge ticks.

## What it does

Provider guide semantics: rapidly recover mana while channeling. The long cooldown is part of the provider's balance identity.

## Deduplication

Occupies the **zero-cast-cost, long-cooldown active mana regeneration channel** niche.

## Confidence

`SOURCE-PINNED SPELL + RECOVERY CADENCE / PACK RECOVERY MULTIPLIER + IRON'S CAP RUNTIME QA PENDING`