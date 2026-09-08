# Demi-creator Wings

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:demicreator_wings`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 90 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 800`
- `spellPowerPerLevel = 250`
- `baseManaCost = 300`
- `manaCostPerLevel = 100`
- `castTime = 40 ticks`
- recast count: `2`

Activation-area value:

`1 + round(spellPower / 100)`

Duration:

`20 * round(30 * spellPower / 800)` ticks.

At unmodified default spell power, the nominal values are approximately:

| Level | Area value | Duration |
|---:|---:|---:|
| 1 | 9 | 30 s |
| 2 | 12 | 39 s |
| 3 | 14 | 49 s |

The exact geometric interpretation of the manager's area value should be taken from runtime/manager audit rather than relabeled as diameter/radius without evidence.

## Provider lifecycle

The spell is player-only and rejects dimensions disallowed by provider configuration. The first cast activates a `DemicreatorWingsManager` core/session; an active recast path deactivates it. Timeout also deactivates provider state.

The public guide describes a fixed core that grants temporary creative-style flight only inside the bounded area, ending on recast, expiry or leaving the valid zone.

## Authority

This is provider-owned temporary flight. Black Arcana must not create a second flight permission flag or duplicate duration/recast management. RPG progression must not award Mastery per flight tick.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **bounded temporary creative-flight zone tied to a provider-managed core/recast lifecycle** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CAST+AREA-VALUE+DURATION FORMULAS+RECAST / MANAGER GEOMETRY+FLIGHT PERMISSION EDGE CASES+RUNTIME QA PENDING`