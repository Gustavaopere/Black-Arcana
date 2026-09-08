# Bound Sword

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:bound_sword`
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
- weapon damage: `(3 + 3 * spellPower / 100) * SUMMON_DAMAGE attribute * providerDamageMultiplier`

## Provider lifecycle

The first cast activates provider-owned bound-sword state through `BoundSwordManager`. A later recast deactivates it. The provider can optionally attempt a dual-wield compatibility path when the real compat is present and the player deliberately crouches during initial pre-cast.

Greater Conjurer's Talisman behavior is provider-native: on manual deactivation/recast the spell may remove its own cooldown according to the provider's existing talisman contract.

## Causality and progression

The temporary weapon session is one cast lifecycle. Physical swings made while the bound sword is active are not automatically new spell casts. Any RPG bridge must distinguish provider activation from downstream melee-hit causality and avoid double credit with combat systems.

## Deduplication

Occupies the **two-minute provider-bound summoned melee weapon with summon-damage scaling and optional dual-wield compatibility** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DURATION+RECAST+WEAPON DAMAGE / BOUND ITEM STATS+DUAL-WIELD COMPAT DETAILS REQUIRE MANAGER QA`