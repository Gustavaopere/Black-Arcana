# Silent Assassin

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:silent_assassin`
- **Iron's school:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 16 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 100`
- `manaCostPerLevel = 40`
- `castTime = 50 ticks`
- base damage: `10 * (spellPower / 100) * providerDamageMultiplier`
- headshot multiplier: `min(500, 100 + round(50 * spellPower / 100))%`
- unaware/sneak multiplier: `min(500, 100 + round(75 * spellPower / 100))%`
- range: **128 blocks**
- nearby-awareness suppression radius after a qualifying lethal unaware hit: **16 blocks**

## Provider lifecycle

The long cast summons/holds a rifle entity and continuously updates its reticle from provider-assisted aim. At completion the provider resolves the assisted raycast, determines headshot status, checks whether the target qualifies for the unaware bonus, applies the final damage once through the summoned weapon, then drives the visual hit result.

If an unaware-bonus shot is lethal, provider firearm logic may suppress nearby awareness within the fixed 16-block radius.

## Causality and progression

Headshot and unaware multipliers are modifiers on the same provider shot, not separate damage events for progression. Awareness suppression is a consequence of that shot and must not create additional offensive credit.

## Deduplication

Occupies the **very-long-range summoned sniper rifle with headshot and unaware-target multipliers plus stealth-kill awareness suppression** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DAMAGE+HEADSHOT+UNAWARE+RANGE / ASSISTED-AIM COLLISION AND AWARENESS AI DETAILS REQUIRE UTILITY/ENTITY QA`