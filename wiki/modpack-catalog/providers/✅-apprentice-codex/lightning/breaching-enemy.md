# Breaching Enemy

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:breaching_enemy`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 60`
- `manaCostPerLevel = 15`
- `castTime = 20 ticks`
- pellet count: **12**
- range: **8 blocks**

Raw per-provider damage input is `spellPower / 100`, then multiplied by `DamageMultiplierKey.BREACHING_ENEMY` before being seeded into the summoned shotgun entity.

## Cast lifecycle

The spell summons the shotgun during the cast. On successful completion it refreshes the weapon damage from current spell power, fires once and keeps the weapon only for its provider firing animation/lifecycle. Cancelling the cast releases the weapon without firing.

The spell is marked as affected by the provider's Magi Agent Suit contract, which may modify interruptibility. That equipment behavior is provider-owned and is not an RPG Skill Tree perk.

## What it does

Provider guide semantics: summons a magical shotgun and fires a short-range 12-pellet blast. Its defining behavior is extremely strong knockback at close range.

The exact pellet spread/individual hit/knockback settlement lives in the provider shotgun entity. Black Arcana must not independently replay 12 damage/proc events from one completed cast.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short-range magical shotgun / multi-pellet / heavy knockback** niche. A Chaos-force shotgun would not be distinct merely by changing damage school or VFX.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / SHOTGUN PELLET ENTITY SETTLEMENT + PACK CONFIG MULTIPLIER QA PENDING`