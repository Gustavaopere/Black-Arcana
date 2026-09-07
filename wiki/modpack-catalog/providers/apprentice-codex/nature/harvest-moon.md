# Harvest Moon

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:harvest_moon`
- **School:** Nature
- **Levels:** 1–4
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 12`
- `spellPowerPerLevel = 12`
- `baseManaCost = 60`
- `manaCostPerLevel = 20`
- `castTime = 50 ticks / 2.5 s`
- job budget: **32 harvest actions per tick**

Search range:

`8 * spellPower / 10`

The executable cast floors this range to an integer of at least 1 block before collecting targets.

## Target collection

The provider collects mature harvestable targets around the caster using a bounded cuboid:

- X/Z: `origin ± range`;
- Y: from one block below the player through three blocks above;
- out-of-world positions are skipped;
- already-visited positions are deduplicated;
- blocks in the provider `HARVEST_MOON_DENYLIST` are excluded.

The collector has provider-specific handling for mature vanilla crops, Nether Wart, Sweet Berry Bushes, Comfort Berry Bushes, attached melons/pumpkins, root-preserving columns such as sugar cane/cactus/bamboo, chorus clusters and supported generic age-based crops. Actions are sorted nearest-first before the job starts.

## Bounded harvesting job

On a successful server cast by a real `ServerPlayer`, the spell freezes a copy of the caster's current main-hand stack and submits the collected actions to `HarvestMoonJobManager`/`HarvestMoonJob` with a fixed **32-block/action budget per tick**.

That copied tool context is intentional: later job ticks do not silently adopt a different main-hand item after the cast.

The spell is therefore one cast followed by provider-owned bounded follow-up work. Individual harvested blocks/crops are not separate casts or separate progression-authority events.

## What it does

Provider semantics are mass harvesting rather than destructive area clearing. Mature plants are processed through specialized actions intended to preserve roots/stems or normal harvesting behavior where applicable.

## World safety / integration boundary

Harvest Moon is a provider-owned world-processing mechanic. Black Arcana must not reuse its collector/job as a bypass around Black Arcana `WorldEffectPolicy`, nor re-harvest the same targets after observing the provider cast.

Any future RPG/Mastery integration must collapse the entire submitted harvest job back to the single causal Harvest Moon cast unless a separate provider contract explicitly exposes a safer discrete milestone.

## Confidence

`SOURCE-PINNED CAST + TARGET COLLECTOR + JOB BUDGET / DATAPACK DENYLIST CONTENT + FULL MODPACK HARVEST COMPAT RUNTIME QA PENDING`