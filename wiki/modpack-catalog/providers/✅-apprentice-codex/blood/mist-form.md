# Mist Form

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mist_form`
- **Iron's school:** Blood
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 15`
- `baseManaCost = 150`
- `manaCostPerLevel = 30`
- `castTime = 30 ticks`
- nearby-awareness suppression radius: `32 blocks`

## Duration

Exact spell source computes the applied Mist Form duration as:

`round(10 * 20 * spellPower / 100)` ticks

or equivalently ten seconds scaled by effective spell power.

## What it does

The provider guide describes a temporary mist-like state that:

- slightly improves mobility;
- allows passage through some blocks;
- briefly distracts/suppresses nearby enemy awareness when activated;
- can destabilize/cancel when the user attacks;
- makes the user **extremely vulnerable to fire and Holy spells**.

The spell source applies the provider's `MIST_FORM` effect server-side and explicitly suppresses nearby awareness in a 32-block radius at cast completion.

## Safety / overlap

This is a transformation/phasing/evasion spell with a strong weakness tradeoff. It overlaps Black Arcana observation/displacement and Blood-state design at the semantic level but remains an Iron's Blood spell owned by Apprentice's Codex.

Black Arcana must not:

- mirror the effect into a second transformation state;
- independently suppress the same mobs' awareness;
- grant phasing merely because this provider effect is active without an explicit bridge;
- award continuous mastery for every Mist Form tick.

## Acquisition

Uses the Iron's spell registry/scroll model. Exact 0.9.7.1 loot and recipe acquisition remains pending provider data audit.

## Confidence

`SOURCE-PINNED SPELL CONFIG + SERVER APPLICATION PATH + PROVIDER GUIDE / EFFECT INTERNAL DETAILS AND PACK RUNTIME QA PENDING`