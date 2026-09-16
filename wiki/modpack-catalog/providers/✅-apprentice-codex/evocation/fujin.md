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

## Provider lifecycle

The spell summons a `FujinKatanaEntity`, injects the computed projectile damage and 10-block range, and releases that weapon when the continuous cast completes.

The katana entity — not the top-level spell tick callback — owns projectile cadence. At the exact source pin the executable constants are:

- first slash at weapon tick **10**;
- subsequent slashes every **5 ticks**;
- slash animation speed `3.0`;
- one `FujinSlashProjectileEntity` spawned per slash.

Each projectile receives the damage frozen into the katana, the **10-block** maximum travel distance and the provider combat-owner UUID.

This executable entity cadence is authoritative for the audited snapshot. A comment in the top-level spell mentions a "10 tick interval", but the actual `FujinKatanaEntity.SLASH_INTERVAL_TICKS` value is **5**; the catalog therefore records the executable behavior rather than promoting the stale comment.

The source deliberately leaves firing cadence to the katana entity so ordinary cast-speed modification does not alter the internal 5-tick slash interval.

## Causality and progression

Repeated katana projectiles during the channel remain children of one continuous provider cast. Do not award spell-cast progression per projectile or infer cast-speed-scaled projectile frequency when the provider deliberately isolates that cadence.

Black Arcana must not duplicate the katana timer, projectile spawn, combat-owner attribution or projectile damage settlement.

## Deduplication

Occupies the **continuous summoned katana that emits short-range projectiles on a fixed provider-owned cadence** niche.

## Confidence

`SOURCE-PINNED SPELL + KATANA ENTITY / EXACT CONFIG+DAMAGE+10-BLOCK RANGE+FIRST-SLASH TICK 10+5-TICK INTERVAL+OWNER HANDOFF / PROJECTILE COLLISION DETAIL RUNTIME QA PENDING`