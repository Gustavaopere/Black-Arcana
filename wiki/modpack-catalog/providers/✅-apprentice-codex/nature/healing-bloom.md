# Healing Bloom

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:healing_bloom`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 300 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 100`
- `manaCostPerLevel = 20`
- `castTime = 50 ticks`
- placement/targeting range: **8 blocks**

Bloom max health:

`round(20 * spellPower / 100)`

Effect range:

`min(16, round(4 * spellPower / 100))` blocks.

Fruit maturation interval:

`max(600, round(1200 * (4 - spellPower / 100)))` ticks.

This preserves the exact source arithmetic: the floor is 600 ticks / 30 s.

## One-bloom-per-caster lifecycle

Server placement is resolved through `HealingBloomPlacementHelper` and rejected if invalid.

For ServerPlayers, `HealingBloomManager` enforces one managed bloom:

- if one already exists, ordinary casting is rejected;
- sneaking marks the cast as an explicit **force replace** operation;
- the force-replace flag and validated position are stored in cast data;
- successful spawn registers the new bloom through the provider manager, which owns replacement/lifecycle cleanup.

## Spawned bloom state

The entity is seeded with:

- owner;
- anchor block position;
- effect range;
- calculated maximum health;
- calculated Comfort Berry growth interval.

Provider guide semantics: the bloom softly lights its surroundings, heals nearby entities and produces Comfort Berries over time.

## Authority

The provider manager owns the single-instance invariant and replacement. Black Arcana must not create a parallel bloom registry or issue duplicate cleanup when the same provider entity is replaced/destroyed.

## Deduplication

Occupies the **one-per-caster placed healing/light/fruit-producing plant** niche.

## Confidence

`SOURCE-PINNED SPELL + PLACEMENT/MANAGER ENTRYPOINTS / BLOOM ENTITY HEAL-FRUIT CADENCE + PERSISTENCE RUNTIME QA PENDING`