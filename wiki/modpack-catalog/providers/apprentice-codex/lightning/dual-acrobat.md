# Dual Acrobat

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:dual_acrobat`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 75`
- `spellPowerPerLevel = 65`
- `baseManaCost = 5`
- `manaCostPerLevel = 5`
- `castTime = 60 ticks / 3 s`
- range: **16 blocks**

Raw shot damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.DUAL_ACROBAT`.

## Cast lifecycle

The spell summons a dual-SMG entity for the duration of continuous casting. While channeling it refreshes the weapon's damage from current spell power every cast tick so provider item effects such as Focus Staffbow adjustments remain reflected.

Cast completion or cancellation releases the summoned weapon. The weapon entity owns actual firing cadence and hit settlement.

The spell is marked as affected by the provider's Magi Agent Suit contract; that provider equipment may change interruptibility and is not RPG Skill Tree authority.

## What it does

Provider guide semantics: summons two magical SMGs and sprays fire forward after a brief charge. The shots cause no knockback and can ignore target invulnerability frames.

A three-second barrage is one continuous provider cast. Per-shot callbacks must not be promoted into independent Black Arcana/RPG casts or proc chains.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short continuous dual-SMG Lightning barrage / no-knockback i-frame bypass** niche.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / SMG FIRING ENTITY + PACK CONFIG MULTIPLIER QA PENDING`