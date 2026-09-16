# Spectral Wing

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:spectral_wing`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 2 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseManaCost = 150`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 0`

Initial launch constants:

- horizontal look-direction scale: **0.75**;
- minimum vertical launch speed: **1.05**;
- start grace: **10 ticks**.

Recast boost constants:

- forward boost speed: **2.75**;
- added upward speed: **0.22**;
- spin visual duration: **10 ticks**;
- visual wing-effect refresh: **20 ticks**.

## Preconditions

The exact spell rejects casting when:

- caster is not a player;
- an Elytra is equipped in the chest slot;
- Iron's Angel Wings effect is active;
- player is in water/bubble or swimming.

## What it does

First cast launches the player, starts fall-flying and activates provider-owned Spectral Wing state. Recasting while that spell-started state is active applies a strong look-direction boost instead of starting a second independent wing state.

Provider guide semantics state that the wings disappear when landing or touching water. The state/lifecycle is owned by Apprentice's Codex capability/event code.

## Authority and safety

This is not Black Arcana flight state. Black Arcana must not mirror velocity, cooldown or active-state bookkeeping in a second mobility controller. Any future stamina/progression observation must preserve the provider's single server-authoritative activation identity.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **launch → glide → recast directional surge** mobility niche. A Black Arcana movement spell should not clone this sequence merely with different wing particles.

## Confidence

`SOURCE-PINNED SPELL + STATE ENTRY CONSTANTS / STATE-EXIT EVENT + FULL CLIENT/MODPACK FLIGHT QA PENDING`