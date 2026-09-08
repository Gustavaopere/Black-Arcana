# Arcane Blast

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:arcane_blast`
- **Iron's school:** Ender
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Long
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 40`
- `spellPowerPerLevel = 5`
- `baseManaCost = 20`
- `manaCostPerLevel = 4`
- `castTime = 30 ticks`

Raw damage before the provider config multiplier:

`spellPower / 10`

Effective range:

`16 + 4 * spellPower / 10` blocks.

Both damage and range therefore respond to actual Ender spell power, not only nominal spell level.

## Provider behavior

The server raycasts from the caster eye using a narrow `0.1` width and accepts only provider-valid combat targets. A successful hit uses Apprentice's Codex `ARCANE_BLAST` damage and then applies/increments **Arcane Charge** on the caster for `200 ticks`.

Arcane Charge amplifier is capped by this cast path at `2`, producing up to three charge tiers (`0..2`). The effect is provider state later consumed by Arcane Beam.

The public guide describes the spell as an internal arcane explosion/beam-like strike that accelerates mana circulation, bypasses armor and is ineffective against the provider's demonic targets. Exact demon-tag membership remains provider data/runtime authority.

## Causality

One successful Arcane Blast is one provider hit plus one Arcane Charge state mutation. Black Arcana must not count the charge application as a second offensive cast/proc identity.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 survival scroll/loot/crafting availability remains part of the provider-wide acquisition audit.

## Deduplication

Occupies the **fast direct Ender/arcane hit that builds a short-lived charge resource for another spell** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT DAMAGE+RANGE+CHARGE PATH / PACK CONFIG MULTIPLIER + DEMON ELIGIBILITY + RUNTIME QA PENDING`