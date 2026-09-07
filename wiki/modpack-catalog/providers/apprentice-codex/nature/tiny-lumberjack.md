# Tiny Lumberjack

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:tiny_lumberjack`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 400 ticks / 20 s`
- block/log target range: **8 blocks**
- combat-entity target range: **3 blocks**
- entity raycast width: **0.5**
- summoned saw reach-speed setting: **10**

Raw combat damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.TINY_LUMBERJACK`.

Base block break-speed input:

`2 + 1.5 * spellPower / 100`

If provider **Craftsman's Delight** break-speed bonuses are enabled, it modifies that speed. The spell can also build a dummy Iron Axe carrying eligible main-hand enchantments through that provider accessory path.

Displayed best-case log break time is:

`round(60 / breakSpeed)` ticks.

## Targeting and world interaction

During channeling the summoned saw prefers a still-valid locked combat target. Otherwise it checks for a nearby valid living target, then a log block target through the provider's log classifier/raycast/outlined-target path.

The saw entity owns the actual tree/block-break workflow and its protection/drop semantics. The spell itself does not directly replace blocks.

Provider guide semantics: shred the entity in line of sight or aim the saw at a tree to fell/process it.

## Authority

This is a provider-native magical tool. Black Arcana must not replay block breaks, drops or durability/enchantment effects after the saw has already processed them. Any Black Arcana-originated destructive magic still needs Black Arcana `WorldEffectPolicy`.

## Deduplication

Occupies the **continuous magical saw / log-felling + close combat** niche.

## Confidence

`SOURCE-PINNED SPELL TARGETING + BREAK-SPEED INPUT / SAW BLOCK-JOB + PROTECTION/DROP QA PENDING`