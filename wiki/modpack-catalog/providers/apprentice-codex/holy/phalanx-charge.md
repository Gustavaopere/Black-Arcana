# Phalanx Charge

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:phalanx_charge`
- **Iron's school:** Holy
- **Levels:** 1–4
- **Minimum rarity:** Uncommon
- **Cast type:** Continuous
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 15`
- `manaCostPerLevel = 5`
- `castTime = 200 ticks / 10 s`
- cast cannot be interrupted.

Raw thrust damage:

`3 + 6 * spellPower / 100`

then multiplied by `DamageMultiplierKey.PHALANX_CHARGE`.

Base thrust/beam length:

`6 + 1.5 * spellPower / 100` blocks.

## Guard state

The spell summons provider-owned spear/shield weaponry and continuously refreshes `Phalanx Stance` in 5-tick windows while channeling.

If **Protection Spell Supporter** is equipped:

- effective channel time is doubled;
- the provider chooses the movement-enabled Phalanx Stance amplifier instead of the fixed stance amplifier.

That accessory behavior is provider-owned and is not an RPG Skill Tree perk.

## Completion

On completion, the weapon begins its thrust sequence with current damage and beam length. The source performs the thrust even through the provider weapon entity rather than a second Black Arcana hit path.

Provider guide semantics: summon spear and shield, immediately assume a guarding stance, then thrust sharply forward when the stance ends.

## Deduplication

Occupies the **uninterruptible Holy guard-channel → forward thrust** niche. Black Arcana Order should not duplicate it with a differently named shield/spear stance.

## Confidence

`SOURCE-PINNED SPELL + GUARD STATE / WEAPON THRUST ENTITY + PACK CONFIG MULTIPLIER QA PENDING`