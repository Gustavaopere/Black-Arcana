# Auto Magnet

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:auto_magnet`
- **Iron's school:** Ender
- **Levels:** 1–5
- **Minimum rarity:** Common
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 40`
- `manaCostPerLevel = 10`
- `castTime = 0`
- collection range: `8 + 4 * (spellLevel - 1)` = **8 / 12 / 16 / 20 / 24 blocks**
- collection mana charge: `10` by default, or `0` when the provider server config disables collection mana cost

## Provider behavior

The cast toggles `AutoMagnetFamiliarManager` on the server. Crouching selects **REVERSE** collection mode; normal casting selects **NORMAL** mode. The provider sends the resolved mode back as action-bar presentation.

The public guide describes an owner-following magnet that gathers dropped items/XP while respecting inventory behavior. Exact per-entity collection cadence and inventory insertion rules remain provider-manager authority.

## Resource authority

The ongoing collection mana cost is provider-owned. Black Arcana must not impose an additional mana/strain payment merely because Auto Magnet collected an item, nor infer a cast/progression event from each collected stack or XP orb.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **toggleable owner-following item/XP magnet with normal/reverse modes** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CAST+RANGE+COLLECTION-MANA CONFIG / INVENTORY INSERTION+ENTITY CADENCE+RUNTIME QA PENDING`