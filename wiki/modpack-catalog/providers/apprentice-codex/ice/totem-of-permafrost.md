# Totem of Permafrost

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:totem_of_permafrost`
- **Iron's school:** Ice
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 200`
- `spellPowerPerLevel = 150`
- `baseManaCost = 30`
- `manaCostPerLevel = 15`
- `castTime = 0`
- recast count: `2`

Raw damage per pulse is `spellPower / 100`, then multiplied by `DamageMultiplierKey.TOTEM_OF_PERMAFROST`.

The provider fixes:

- radius: **3 blocks**;
- targeting range: **8 blocks**;
- nominal duration: **120 ticks / 6 s**;
- Slowness amplifier: `min(2, round(spellPower / 500))`.

The user's server-config damage multiplier remains runtime/config QA.

## Placement and recast lifecycle

Initial placement is server-resolved and rejects invalid/supportless placement or a nearby conflicting totem. The spell stores server cast data for the chosen location.

When an active recast exists, casting again removes the stored totem instead of placing a second independent instance. This lifecycle is provider-owned; Black Arcana must not duplicate cleanup, cooldown or ownership settlement.

## Exact totem pulse behavior

The exact totem entity establishes:

- first pulse: **tick 10** after creation;
- pulse interval: **15 ticks**;
- freeze increment per successful pulse: **40 ticks**;
- frozen-tick cap: **300 ticks**;
- Slowness duration per successful pulse: **40 ticks**;
- combat radius: provider radius 3 with a fixed-height AABB and line-of-sight requirement;
- no knockback from pulse damage;
- pulse targets are filtered through provider combat-target rules;
- owner must remain alive and in the same level, otherwise the totem discards itself.

The entity is stationary while its support remains valid, cannot be attacked/pushed normally, is not saved persistently, and is not a permanent world object.

## What it does

Provider guide semantics: place a temporary totem strongly imbued with Ice magic. It repeatedly damages nearby enemies and attempts to restrict their movement. The guide explicitly notes that Greater Conjurer's Talisman cannot prevent this spell from entering cooldown.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 acquisition is tracked separately in the provider-wide scroll/loot/recipe audit.

## Deduplication

Occupies the **temporary placed Ice area-denial totem / repeated pulse / freeze + Slowness** niche. Black Arcana should not create an equivalent persistent-ish cold ward merely by renaming the object. Any Black Arcana ward/ritual must retain its own authority, world-safety policy and materially different lifecycle.

## Confidence

`SOURCE-PINNED SPELL + TOTEM ENTITY / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`