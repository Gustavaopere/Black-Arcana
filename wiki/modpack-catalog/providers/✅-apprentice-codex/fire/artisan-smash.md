# Artisan Smash

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:artisan_smash`
- **Iron's school:** Fire
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 900`
- `spellPowerPerLevel = 400`
- `baseManaCost = 40`
- `manaCostPerLevel = 20`
- `castTime = 30 ticks`
- projectile speed seeded by spell: **1.5**

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.ARTISAN_SMASH`.

Splash radius:

`min(2 + spellPower / 600, 8)` blocks.

## What it does

The spell summons a magical grenade launcher, charges, and fires an explosive shell on successful cast completion. The launcher is released without firing if the cast is cancelled.

Provider guide semantics state that the shell blasts a wide area but **does not destroy terrain or item entities**, while still being capable of hitting the caster. That non-griefing explosive identity is provider-owned.

## Equipment interaction

The spell implements the provider's Magi Agent Suit affected-spell contract. The suit may change interruptibility/attack-spell handling. Those are Apprentice's Codex equipment semantics, not RPG Skill Tree perks and not Black Arcana casting authority.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **charged summoned grenade launcher / scalable Fire splash without terrain destruction** niche. Black Arcana should not recreate an equivalent explosive shell merely as a Chaos spell unless its mechanics and risk/world-safety identity are materially distinct.

## Confidence

`SOURCE-PINNED SPELL / SUMMONED LAUNCHER + SHELL SEMANTICS / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`