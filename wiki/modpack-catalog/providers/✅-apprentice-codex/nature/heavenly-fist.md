# Heavenly Fist

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:heavenly_fist`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 80`
- `manaCostPerLevel = 20`
- `castTime = 0`
- target range: **32 blocks**

Damage:

`(4 + 6 * spellPower / 100) * HEAVENLY_FIST damage multiplier`

Impact radius:

`2.5 + 2.0 * spellPower / 100`

Optional pressing capacity before flooring:

`8 * spellPower / 100`, then optionally modified by Craftsman's Delight process-speed logic.

## Target resolution

The server resolves a single locked center along the caster's view line. Resolution precedence is:

1. valid combat entity before the first blocking block;
2. processable dropped item when Create pressing support is active;
3. adjacent center of the hit block face;
4. otherwise the cast is denied.

The client does not author the final AoE center.

## Delayed provider-owned impact

A short-lived `HeavenlyFistFistEntity` is spawned at the locked center. Its exact lifecycle is bounded:

- attack animation begins at tick 4;
- impact settles once at tick **25**;
- entity discards at tick **30**;
- entity is non-persistent, non-pickable and cannot be damaged by normal gameplay.

At the single impact, the provider:

- resolves unique combat targets inside the configured radius;
- applies Heavenly Fist damage without knockback;
- applies `GRAVITY_BOUND` for **200 ticks / 10 s** to successfully damaged living targets;
- optionally processes dropped items through the provider's Create pressing processor;
- optionally runs the provider crystal-harvest processor for a valid real player owner;
- emits bounded visual tremor particles, with a visual block limit of **18**.

## Causality / ownership

The delayed fist entity is downstream execution of one already-admitted cast. Damage targets, pressed item stacks, harvested crystals and visual tremor blocks are not independent magical casts.

Create recipe semantics and Craftsman's Delight modifiers remain provider-owned. Black Arcana must not re-run pressing/compacting, reapply damage, or treat the particle tremor as terrain destruction.

For any future Mastery/progression bridge, the safe causal unit is the original Heavenly Fist cast unless a provider-native discrete processing event is explicitly contracted.

## Confidence

`SOURCE-PINNED TARGETING + COEFFICIENTS + IMPACT ENTITY LIFECYCLE / OPTIONAL CREATE PROCESSING + CRYSTAL HARVEST FULL PACK QA PENDING`