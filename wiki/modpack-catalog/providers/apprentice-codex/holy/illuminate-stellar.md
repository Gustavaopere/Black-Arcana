# Illuminate Stellar

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:illuminate_stellar`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 80`
- `manaCostPerLevel = 80`
- `castTime = 0`
- `setAllowCrafting(false)`
- `allowLooting() = false`

Raw damage per spawned star:

`2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.ILLUMINATE_STELLAR`.

## Exact star fan

A cast spawns **3–4** Illuminate Stellar star entities.

- total even-distribution yaw spread: **120°**;
- each star gets an additional random yaw offset up to ±10°;
- pitch randomization up to ±10°;
- fallback assisted target search: **64 blocks**, raycast width **2**;
- spawn positions are collision-checked progressively closer to the caster before falling back to the base position.

Each child star receives the provider damage value, drift direction and optional fallback target. The star entity owns subsequent targeting/travel/hit behavior.

## What it does

Provider guide semantics: a latent spell unique to the Illuminate Stellar Staff. Waving the staff spreads twinkling stars that fly toward entities with malevolent intent.

## Acquisition / item binding

The spell is explicitly non-craftable and non-lootable. The provider guide identifies it as a latent staff capability; exact staff exposure/equipment rules remain provider-owned.

## Causality/deduplication

Three or four spawned stars remain child effects of **one** provider cast. Mastery, hazards and offensive proc integrations must not count each star as a new cast.

## Confidence

`SOURCE-PINNED SPELL + SPAWN FAN / STAR ENTITY HOMING-HIT DETAILS + PACK CONFIG MULTIPLIER QA PENDING`