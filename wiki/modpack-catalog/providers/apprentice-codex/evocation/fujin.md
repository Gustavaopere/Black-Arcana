# Fujin

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:fujin`
- **Iron's school:** Evocation
- **Levels:** 1–10
- **Minimum rarity:** Uncommon
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 75`
- `baseManaCost = 5`
- `manaCostPerLevel = 1`
- `castTime = 100 ticks`
- projectile damage: `(1 + spellPower / 200) * providerDamageMultiplier`
- projectile range: **10 blocks**

The source explicitly leaves firing cadence to the summoned katana entity so ordinary cast-speed modification does not alter its intended internal interval.

## Provider lifecycle

The spell summons a `FujinKatanaEntity`, injects the computed projectile damage and 10-block range, and retains that weapon through the continuous cast. On completion the weapon is released. Projectile cadence and hit semantics belong to the katana entity rather than the top-level spell class.

## Causality and progression

Repeated katana projectiles during the channel remain children of one continuous provider cast. Do not award spell-cast progression per projectile or infer cast-speed-scaled projectile frequency when the provider deliberately isolates that cadence.

## Deduplication

Occupies the **continuous summoned katana that emits short-range projectiles on its own fixed internal cadence** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DAMAGE+10-BLOCK RANGE+CADENCE AUTHORITY / KATANA FIRING INTERVAL+PROJECTILE COLLISION REQUIRE ENTITY AUDIT`