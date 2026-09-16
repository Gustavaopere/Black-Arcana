# Unite Luna

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:unite_luna`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 160`
- `manaCostPerLevel = 160`
- `castTime = 0`
- `setAllowCrafting(false)`
- `allowLooting() = false`

Raw moon-projectile damage:

`20 * spellPower / 100`

then multiplied by `DamageMultiplierKey.UNITE_LUNA`.

## Spawn lifecycle

A successful server-side cast normalizes the caster look direction, creates one `UniteLunaMoonEntity`, seeds its damage, picks a collision-safe spawn position near the caster eye/weapon area and launches it along that direction.

Spawn placement attempts several offsets before falling back to the base position; it therefore does not blindly instantiate the moon inside nearby solid geometry.

## What it does

Provider guide semantics: a latent spell unique to the Unite Luna Staff. Waving it creates a crescent moon that obliterates hostile/disturbing entities. The guide states that attempts to negate the moon's magic are converted into greater power.

The exact anti-negation/counterspell amplification behavior belongs to `UniteLunaMoonEntity`; this catalog does not infer the formula from guide text without the entity audit.

## Acquisition / item binding

Explicitly non-craftable and non-lootable. Provider guide identifies it as a latent staff capability.

## Deduplication

Occupies the **high-damage Holy crescent projectile with provider anti-negation behavior** niche. Black Arcana anti-magic systems must not both negate and independently amplify the same provider projectile.

## Confidence

`SOURCE-PINNED SPELL + PROJECTILE SPAWN / MOON ANTI-MAGIC AMPLIFICATION FORMULA + PACK CONFIG QA PENDING`