# Bullet Stream

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:bullet_stream`
- **Iron's school:** Lightning
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 20`
- `spellPowerPerLevel = 100`
- `baseManaCost = 3`
- `manaCostPerLevel = 2`
- `castTime = 600 ticks / 30 s`
- fixed effective cast time: equipment cast-time modifiers do **not** alter the duration
- range: **32 blocks**
- spin-up: **40 ticks / 2 s**

Raw per-tick shot damage:

`0.5 + spellPower / 100`

then multiplied by `DamageMultiplierKey.BULLET_STREAM`.

## Exact minigun lifecycle

The summoned minigun:

- follows the caster and continuously aims at line of sight;
- begins firing once the 40-tick spin-up completes;
- calls its firing path **every server tick** after spin-up while the channel continues;
- applies damage with no knockback through the provider combat helper;
- refreshes current damage from the owner's current spell power rather than relying only on summon-time damage;
- plays its continuous firing sound every 10 firing ticks;
- after release, remains for a 10-tick spin-down lifecycle before discard.

Provider guide semantics state that its shots can ignore target invulnerability frames and that cancelling during spin-up still triggers normal cooldown. The spell intentionally keeps its 30-second maximum channel independent of equipment cast-time modifiers.

## Causality

A single Bullet Stream channel can generate hundreds of provider-owned hit callbacks. They are **not** hundreds of spell casts. Any mastery/perk/Black Arcana bridge must key off a suitable original cast identity and prevent per-tick offensive proc multiplication.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **spin-up → long sustained magical minigun barrage / i-frame bypass** niche. This is a particularly strong no-duplicate case for future Chaos/Lightning rapid-fire magic.

## Confidence

`SOURCE-PINNED SPELL + MINIGUN ENTITY / PROVIDER GUIDE I-FRAME SEMANTICS + PACK CONFIG MULTIPLIER QA PENDING`