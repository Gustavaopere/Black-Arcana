# Assist Wings

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:assist_wings`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`
- allowed air-jump count: `1 + spellLevel` = **2 / 3 / 4** for levels 1–3

The vertical impulse uses:

`0.6 + caster jumpBoostPower`

rather than spell power.

## Lifecycle and authority

The provider stores the number of completed air jumps in server spell data. Touching ground resets the bounded air-jump counter. The spell also maintains an owner-linked wing entity with removal grace.

When mounted, the spell fails for arbitrary vehicles. It has explicit provider integration for **Hoverride Broom** and lets the broom own the movement application after server validation.

For a player not riding that broom, the server owns spell-state mutation and sends a dedicated player packet for the vertical jump so ordinary server velocity correction does not overwrite client horizontal motion.

## What it does

The guide describes a jump/air-mobility aid with limited mid-air reuses and fall-safety behavior. The current source additionally proves the bounded jump counter and special broom path.

## Causality

Repeated air jumps belong to one provider spell mechanic/state family. RPG/Black Arcana must not award progression per movement tick or duplicate the provider's jump impulse.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **bounded reusable air-jump / wing-assist mobility** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT JUMP COUNT+IMPULSE+SERVER STATE / FALL-SAFETY EDGE CASES + SABLE/BROOM PHYSICAL QA PENDING`