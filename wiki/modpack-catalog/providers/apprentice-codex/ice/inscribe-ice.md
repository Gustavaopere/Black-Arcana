# Inscribe Ice

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:inscribe_ice`
- **Iron's school:** Ice
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 2 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 30`
- `manaCostPerLevel = 15`
- `castTime = 0`

Iron's owns the effective per-level spell-power/mana settlement. The provider's raw formulas are:

- dagger hit damage: `1 + 2 * spellPower / 100`, then `DamageMultiplierKey.INSCRIBE_ICE`;
- burst damage: `12 * spellPower / 100`, then the same server multiplier;
- projectile count: `round(3 * spellPower / 100)`, forced to the next odd number when even;
- fan arc: `clamp(60 + (projectileCount - 3) * 10, 60, 120)` degrees.

The user's configured damage multiplier remains runtime/config QA.

## Projectile lifecycle

Exact dagger entity behavior:

- projectile speed: **1.68 blocks/tick**;
- maximum life: **100 ticks / 5 s**;
- initial block-collision grace: **4 ticks**;
- no gravity;
- valid combat-target filtering is provider-owned;
- projectile is anti-magic susceptible and discards on anti-magic;
- successful dagger damage applies/advances `Notched Frozen`.

## Notched Frozen and third-hit burst

Exact `NotchedFrozenEffect` values:

- duration: **300 ticks / 15 s**;
- maximum stack amplifier: **1**.

Therefore the first successful dagger hit applies amplifier 0, the second advances to amplifier 1, and the next successful application triggers the burst. This matches the provider guide's "third successful inscription" description.

While active, the effect extends existing frozen ticks by 2 each effect tick; the effect itself is provider-owned and is not a Black Arcana Corruption/Strain channel.

## Burst and chain propagation

Exact burst implementation:

- blast half-extent: **2.5 blocks** (5×5×5 AABB);
- direct burst uses the spell's full burst damage;
- chain propagation starts at **50%** of the original burst damage;
- chained bursts continue using that chain damage value;
- a processed-entity set prevents the same entity from recursively bursting twice within one chain;
- burst removes `Notched Frozen` from the origin;
- nearby valid living targets carrying `Notched Frozen` can chain-burst after receiving damage;
- players are explicitly excluded from secondary burst candidates by this burst helper;
- no knockback is applied by the burst damage settlement.

This causality is one provider-owned chain. Black Arcana must not treat each chained detonation as a new independent proc source or generate additional offensive proc chains from it.

## What it does

The provider guide describes a fan of ice daggers that inscribe ice magic into damaged mobs. On the third successful inscription the mark bursts for heavy damage, and that burst can trigger nearby inscriptions in turn.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **multi-projectile Ice mark → third-hit burst → bounded chain propagation** niche. Black Arcana should not reproduce the same stack/burst identity under a new name or particle set.

## Confidence

`SOURCE-PINNED SPELL + PROJECTILE + EFFECT + BURST CHAIN / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`