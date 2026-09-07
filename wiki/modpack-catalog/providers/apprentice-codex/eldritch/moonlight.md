# Moonlight

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:moon_light`
- **Iron's school:** Eldritch
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1200`
- `spellPowerPerLevel = 900`
- `baseManaCost = 120`
- `manaCostPerLevel = 30`
- `castTime = 40 ticks`
- cannot be interrupted
- standby visual starts from a 10-tick base delay, scaled against effective cast duration

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.MOON_LIGHT`.

Attack distance by spell level:

`8 + (spellLevel - 1) * 8` blocks.

## What it does

The spell summons a Moonlight katana during the charge and, on successful completion, performs the blade slash plus a separate spatial charge-cut entity over the configured distance.

Provider guide semantics describe the flash-cut as rending space and severing both magical effects on the target and spellcasting itself. The cast is explicitly uninterruptible.

The provider's katana/charge-cut entities own exact hit, dispel/interruption and damage causality. Black Arcana must not apply a second anti-magic settlement when observing the same hit.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **uninterruptible Eldritch flash-cut / long spatial slash / magic-effect and casting disruption** niche. Black Arcana anti-magic must remain mechanically distinct and must not rebrand this provider spell.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / KATANA+CHARGE-CUT INTERNAL EFFECT DETAILS + RUNTIME CONFIG QA PENDING`