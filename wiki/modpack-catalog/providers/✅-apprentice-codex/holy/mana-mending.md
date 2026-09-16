# Mana Mending

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_mending`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Continuous
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 25`
- `manaCostPerLevel = 0`
- `castTime = 200 ticks / 10 s`
- repair processing interval: **10 ticks / 0.5 s**.

Repair amount per process:

`spellPower / 100`, then passed through `CraftsmansDelight.applyProcessSpeedBonus(...)`.

Displayed repair per second is exactly twice that per-process value.

## Target selection

Initial target resolution prefers the **offhand**, then main hand.

A valid target must:

- be present in the selected hand;
- not be in the provider's Mana Mending denylist;
- be damageable and currently damaged;
- be compatible with vanilla Unbreaking or Mending enchanting semantics according to provider validation.

The chosen hand/item is locked into cast data before channeling begins.

## Anti-swap and transaction safety

Every server cast tick revalidates:

- same target hand;
- item still valid/damaged;
- locked item identity still matches.

Swapping/replacing the target cancels the cast instead of transferring repair progress to another item.

Repair is accumulated fractionally in cast data, floored to whole durability points when enough progress exists, and applied by reducing the target's damage value. The spell cancels itself once the item reaches full durability.

Provider progress messages are emitted at 10% milestones up to 90%.

## What it does

Provider guide semantics: channel mana into a damaged item held directly in the caster's hands. If both hands hold valid items the offhand is preferred.

## Provider modifier

**Craftsman's Delight** can increase processing speed. That is a provider-native equipment modifier, not a second RPG/Black Arcana repair multiplier.

## Deduplication

Occupies the **continuous direct-held-item magical repair** niche. Black Arcana should not reproduce this as a generic repair channel merely with corruption/VFX added.

## Confidence

`SOURCE-PINNED SPELL + TARGET LOCK + REPAIR LOOP / EXACT DENYLIST CONTENT + CRAFTSMAN'S BONUS CONFIG + FULL RUNTIME QA PENDING`