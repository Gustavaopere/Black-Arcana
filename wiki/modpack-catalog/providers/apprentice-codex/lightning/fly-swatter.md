# Fly Swatter

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:fly_swatter`
- **Iron's school:** Lightning
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous lock-on
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 300 ticks / 15 s`
- lock-on/search range: **128 blocks**
- fixed explosion radius seeded into launcher: **3 blocks**

Raw missile damage:

`3 + 2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.FLY_SWATTER`.

Maximum locked targets:

`min(8, round(2 * spellPower / 100))`

Lock-on time per target:

`max(10, 40 - round(10 * spellPower / 100))` ticks.

## Lock-on lifecycle

During continuous casting the provider keeps `FlySwatterCastData` containing:

- current candidate entity id;
- current lock-on progress ticks;
- a serialized list of confirmed entity ids.

Holding the same valid entity in the caster raycast advances its lock timer. Looking away or losing the target resets current lock progress. Once the threshold is reached the entity id is appended to the confirmed lock list, up to the calculated maximum.

On cast completion, **only the confirmed list** is copied into the launcher; if it is non-empty the launcher begins firing. The launcher then owns homing/explosion execution.

## What it does

Provider guide semantics: summons a magical launcher, locks onto targets in line of sight, then sends homing attacks toward them.

A lock-on list is one cast outcome, not one independent cast per target/missile. Future progression bridges must not multiply mastery/procs by confirmed target count.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **continuous multi-lock → homing explosive volley** niche. Black Arcana should not add an equivalent target-painted missile launcher under Chaos/Lightning semantics without a materially different contract.

## Confidence

`SOURCE-PINNED SPELL + SERIALIZED LOCK DATA / MISSILE HOMING ENTITY DETAILS + PACK CONFIG MULTIPLIER QA PENDING`