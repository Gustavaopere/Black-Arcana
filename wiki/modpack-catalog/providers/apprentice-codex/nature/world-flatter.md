# World Flatter

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:world_flatter`
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
- `castTime = 200 ticks / 10 s`
- block target range: **8 blocks**

Raw combat damage:

`3 + 2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.WORLD_FLATTER`.

Entity reach:

`8 + 4 * spellPower / 100` blocks.

Armor-penetration/reduction tier:

- amplifier = `min(3, max(0, floor(spellPower / 200)))`;
- displayed armor-reduction percent = `(amplifier + 1) * 20`, bounded by implementation to 20–80% across amplifier values.

Base break speed:

`4 * spellPower / 100`

with optional provider Craftsman's Delight break-speed bonus.

## Tool semantics

Without Craftsman's Delight, the provider uses an **Iron Pickaxe / Iron tier** as the dummy tool/harvest baseline. With the accessory equipped it upgrades that baseline to **Netherite Pickaxe / Netherite tier** and may copy eligible main-hand enchantments.

The spell targets a valid living entity first; otherwise it resolves a provider-approved breakable block through outlined/raycast target paths. `WorldFlatterDrillEntity.canBreakTarget(...)` owns the block eligibility check.

## What it does

Provider guide semantics: summons a magical drill that pierces enemies through armor and, when aimed into the ground, excavates a large hole.

## World safety

The drill entity is authoritative for actual break scheduling/protection/drop behavior. Black Arcana must not replay or widen those breaks. Black Arcana-originated excavation remains subject to `WorldEffectPolicy`.

## Deduplication

Occupies the **armor-penetrating magical drill + terrain excavation** niche.

## Confidence

`SOURCE-PINNED SPELL + TOOL/TIER INPUT / DRILL BREAK JOB + PROTECTION/DROP QA PENDING`