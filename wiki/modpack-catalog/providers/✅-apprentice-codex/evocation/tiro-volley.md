# Tiro Volley

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:tiro_volley`
- **Iron's school:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 13`
- `manaCostPerLevel = 3`
- `castTime = 200 ticks`
- damage per musket shot: `(4 + spellPower / 1000) * providerDamageMultiplier`
- musket spawn rate: `clamp(2 + (spellPower - 100) * 6 / 400, 1, 10)` muskets/s
- look-target chance: **2/3**
- look-target range: **32 blocks**
- nearest-target fallback range: **12 blocks**
- random-target range: **32 blocks**
- maximum due spawns processed in one cast callback: **32**

The source schedules ideal musket spawn times against integer server ticks so average rate remains stable instead of assuming fractional ticks.

## Provider lifecycle

The server initializes serializable cast timing state once and then spawns only the muskets whose scheduled times are due. Target selection and musket entities remain provider-owned. The bounded `MAX_SPAWNS_PER_CAST_CALL = 32` prevents a lag spike from producing an unbounded catch-up burst in one callback.

## Causality and progression

Every spawned musket belongs to one continuous provider cast. Neither catch-up spawning nor multiple autonomous shots may be treated as independent Black Arcana casts or Mastery grants.

## Deduplication

Occupies the **continuous spell-power-scaled volley of independently spawned magical muskets with bounded catch-up scheduling** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DAMAGE+SPAWN RATE+TARGETING BOUNDS+PER-CALL CAP / MUSKET ENTITY HIT SEMANTICS QA PENDING`