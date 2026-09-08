# Slash Blade

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:slash_blade`
- **School:** Evocation
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Long
- **Cooldown:** 1.5 s
- **Interruptible:** no
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 3`
- `castTime = 15 ticks`

Damage:

`spellPower / 100 * SLASH_BLADE damage multiplier`

Block-penetration damage multiplier:

`clamp(20 + spellLevel * 5, 10, 90)%`

The displayed/ideal range is defined by the provider's `SlashBladeKatanaEntity.getAttackDepth()` rather than duplicated in the spell class; this catalog does not invent that entity constant without a dedicated entity audit.

## Weapon lifecycle

The spell summons a provider-owned katana. Damage and block-penetration values are written into the katana when it is created and are refreshed again at the initial weapon cast so completion-time spell-power/cast modifiers are reflected.

During the long cast the katana enters its standby state. When the cast completes successfully, the provider calls the katana's own slash sequence and keeps the weapon through that sequence. A cancelled cast releases the weapon without the slash.

The standby animation speed is scaled from the actual Iron's cast duration, so cast-time modifiers affect presentation without creating a second cast timer.

## Authority / deduplication

The summoned katana owns the concrete slash hit geometry and block-penetration settlement. Iron's owns the standard mana/cast/cooldown lifecycle.

Black Arcana must not re-run the slash hitbox, apply a second penetration multiplier, or count multiple entities hit by the area slash as multiple casts.

## Confidence

`SOURCE-PINNED SPELL COEFFICIENTS + CAST/WEAPON HANDOFF / KATANA HIT GEOMETRY DETAIL NOT YET EXPANDED / RUNTIME QA PENDING`