# Thermal Process

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:thermal_process`
- **Iron's school:** Fire
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 150`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 200 ticks`
- fixed range: **12 blocks**

Raw damage formula:

`0.5 + 1.5 * spellPower / 100`

then multiplied by `DamageMultiplierKey.THERMAL_PROCESS`.

Base item-processing speed:

`2 * spellPower / 100 items/second`

When the provider's Craftsman's Delight bonus is enabled/equipped, that provider item may further modify process speed and casting mobility. Black Arcana must not reapply those bonuses.

## What it does

The provider guide describes a summoned magical flamethrower that continuously sears targets along the caster's line of sight. Sustained heat applies an intense-heat behavior and can process smeltable items. The guide explicitly states that the spell does not ignite unrelated terrain/entities around the beam.

The summoned thrower entity owns the continuous execution. The spell seeds level, damage, range and processing speed into that entity, then releases it when casting completes/cancels.

## Compatibility surface

The spell is explicitly marked as affected by:

- Apprentice's Codex **Craftsman's Delight**;
- Apprentice's Codex **Magi Agent Suit** behavior.

Those are provider-internal modifiers. They are not RPG Skill Tree perks and must not be double-counted by Black Arcana mastery/attribute hooks without a real integration contract.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **continuous Fire damage + smelting/processing utility** niche. A Black Arcana spell that simply acts as a magical furnace/flamethrower would duplicate provider functionality unless its domain, resource, risk and world-effect contract are materially different.

## Confidence

`SOURCE-PINNED SPELL / SUMMONED THROWER + OPTIONAL ITEM MODIFIERS EXIST / PACK CONFIG MULTIPLIER + RUNTIME QA PENDING`