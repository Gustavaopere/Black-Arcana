# Force Field

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:force_field`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 15 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 20`
- `baseManaCost = 15`
- `manaCostPerLevel = 0`
- `castTime = 100 ticks / 5 s`

Mana drain per intercepted hit:

`forceFieldDrainManaBasePerHit / max(1, spellPower / 100)`

If **Protection Spell Supporter** is equipped, that result is halved.

The same provider accessory doubles the effective cast duration after normal Iron's cast-time resolution.

## Defense lifecycle

Every server cast tick calls the provider's `ForceFieldDefenseEvent.interceptNearbyProjectiles(...)`. The defense event, not the spell class itself, owns projectile/attack interception, mana consumption, rejection/repulsion and any supported spell-projectile semantics.

Provider guide semantics: deploy an invisible all-direction field that repels enemy attacks, consumes a large amount of mana when it knocks something away, and can repel certain spells.

## Causality/resource authority

Intercepting an attack is one provider-owned defensive settlement. A Black Arcana observer must not:

- subtract mana again;
- destroy/reflect the same projectile a second time;
- award a separate cast per intercepted projectile;
- convert the intercepted attack into an offensive proc chain unless a future integration contract explicitly supports it.

## Deduplication

Direct overlap with Black Arcana Order/barrier concepts. An Order spell must provide materially different law/seal/enforcement semantics, not merely another omnidirectional projectile wall.

## Confidence

`SOURCE-PINNED SPELL + DEFENSE EVENT ENTRYPOINT / EXACT INTERCEPTABLE TARGET SET + PACK DRAIN CONFIG QA PENDING`