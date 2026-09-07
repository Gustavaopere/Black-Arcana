# Bound Bow

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:bound_bow`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 50`
- `manaCostPerLevel = 150`
- `castTime = 30 ticks`
- duration: `2400 ticks = 120 s`
- recast count: `2`
- Power-enchantment progression starts at **130 spell power**
- one additional Power level per **30 spell power** above that threshold
- resulting level is clamped by provider config `boundBowMaxPowerEnchantmentLevel()`
- arrow-forging mana cost is provider-configured through `boundBowForgeArrowManaCost()`
- summon-damage attribute is snapshotted into the provider activation path

## Provider lifecycle

The first cast activates a temporary provider-owned bound bow through `BoundBowManager`; a recast deactivates it. The manager receives spell level, Power enchantment level and current Iron's `SUMMON_DAMAGE` multiplier.

Greater Conjurer's Talisman can suppress the spell's cooldown on provider-defined deactivation/timeout paths. Black Arcana must not reproduce that cooldown mutation.

## Causality and progression

Activating the bow is one provider cast. Forged arrows and bow shots belong to the temporary equipment lifecycle and are not independent spell casts unless the provider exposes a distinct causal event.

## Deduplication

Occupies the **two-minute bound magical bow with spell-power-derived Power enchantment and mana-funded arrow forging** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DURATION+RECAST+POWER THRESHOLDS / CONFIGURED ARROW COST+BOUND ITEM PROJECTILE DETAILS REQUIRE MANAGER/CONFIG QA`