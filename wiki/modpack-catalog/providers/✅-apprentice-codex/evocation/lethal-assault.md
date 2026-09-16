# Lethal Assault

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:lethal_assault`
- **Iron's school:** Evocation
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 1.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 500`
- `spellPowerPerLevel = 200`
- `baseManaCost = 20`
- `manaCostPerLevel = 5`
- `castTime = 0`
- burst size: **3**
- range: **48 blocks**
- damage per burst projectile: `(spellPower / 300) * providerDamageMultiplier`

The source explicitly divides the spell-power contribution by three because the summoned rifle fires a three-shot burst.

## Provider lifecycle

An instant cast creates/reuses a summoned rifle entity through `AbstractSummonWeaponSpell`. At initial cast completion the provider snapshots the current damage into the rifle and starts the three-round firing sequence. Weapon presentation and burst execution remain provider-owned.

`IMagiAgentSuitAffectedSpell` means provider equipment may change interruption semantics; that compatibility is not reproduced by Black Arcana.

## Causality and progression

The three shots are one spell cast and one summoned-weapon burst. Do not award spell Mastery three times merely because the provider emits three attack resolutions.

## Deduplication

Occupies the **instant summoned 48-block three-round magical rifle burst** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+3-SHOT COUNT+RANGE+DAMAGE / RIFLE SHOT TIMING+COLLISION+MAGI AGENT SUIT DETAILS QA PENDING`