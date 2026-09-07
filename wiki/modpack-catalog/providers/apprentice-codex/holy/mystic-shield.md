# Mystic Shield

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mystic_shield`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 15 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 25`
- `baseManaCost = 15`
- `manaCostPerLevel = 3`
- `castTime = 200 ticks / 10 s`

Counterattack multiplier:

`spellPower / 100 * DamageMultiplierKey.MYSTIC_SHIELD config multiplier`

If **Protection Spell Supporter** is equipped, the resulting reflect/counter multiplier is doubled.

## Defense lifecycle

On server cast start, `MysticShieldDefenseEvent.spawnShieldEntity(...)` creates the provider shield and resets its stored-damage state if spawning succeeds.

On cast completion/cancellation, `MysticShieldDefenseEvent.releaseStoredDamage(...)` owns release/cleanup and determines how accumulated attacks become the counterattack.

Provider guide semantics: deploy a magical barrier that blocks attacks from the front; when released, it fires a counterattack projectile based on attacks absorbed while active.

## Authority

The shield entity/event pair owns absorption, stored-damage bookkeeping and reflected projectile creation. Black Arcana must not maintain a second absorbed-damage ledger or emit a second counter projectile from the same blocked attack.

Protection Spell Supporter is a provider equipment modifier, not RPG Skill Tree authority.

## Deduplication

Direct overlap with Order/barrier/counter concepts. A BA barrier needs materially different law/seal/risk semantics rather than another frontal store-and-reflect shield.

## Confidence

`SOURCE-PINNED SPELL + DEFENSE EVENT ENTRY/EXIT / EXACT ABSORBABLE ATTACK SET + COUNTER PROJECTILE FORMULA QA PENDING`