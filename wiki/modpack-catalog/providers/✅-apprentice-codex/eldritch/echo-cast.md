# Echo Cast

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:echo_cast`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 20 ticks`
- `setAllowCrafting(false)`
- `requiresLearning() = false`
- `allowLooting() = false`

## Preconditions and multicast state

Casting requires a **Multicast Echo Staff** in either hand. The provider rejects casts once the configured maximum echo amplifier has been reached.

A successful cast applies or increments the provider's `Echo Spell` effect:

- effect duration: **300 ticks / 15 s**;
- first application uses amplifier 0;
- repeated Echo Casts increment the amplifier up to `multicastEchoStaffMaxMulticastCount() - 1`, a server-config-owned limit.

## What it does

Provider guide semantics: the effect causes the next spell cast with the Multicast Echo Staff to trigger multiple times. Echoing Echo Cast itself increases the future echo count.

The actual repeated-spell execution is provider-owned. Black Arcana must not observe each echo as a distinct player intent and award/settle duplicate costs, mastery, procs or hazards without a dedup contract.

## Acquisition

This is explicitly non-craftable/non-lootable and does not require learning. It is a latent Multicast Echo Staff capability rather than an ordinary scroll-progression spell.

## Deduplication

Occupies the **next-spell multicast/echo amplifier** niche. Black Arcana should not implement generic recast duplication over Iron's provider casts without a strict causal identity, because Apprentice's Codex already owns that behavior for its staff.

## Confidence

`SOURCE-PINNED ITEM-BOUND SPELL + EFFECT DURATION / SERVER-CONFIG MAX MULTICAST + FULL ECHO EXECUTION QA PENDING`