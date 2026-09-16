# Terra Resonance

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:terra_resonance`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 10 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 12`
- `spellPowerPerLevel = 8`
- `baseManaCost = 80`
- `manaCostPerLevel = 10`
- `castTime = 30 ticks / 1.5 s`
- client/server block-target admission range: **8 blocks**

Search cube side length:

`min(36 + round(spellPower), 127)`, then forced odd by adding 1 when the result is even.

The source explicitly hard-limits the search size to avoid catastrophic performance growth.

## Server-authoritative target admission

Terra Resonance requires a `ServerPlayer` and a validated pending block-hit target. The server verifies that the selected block remains within the 8-block admission range before storing the block position/face in cast data.

The detailed client hit position can influence presentation, but it cannot move the actual search anchor outside the server-approved range.

## Bounded search scheduler

The provider starts a pair of visual resonance pulses and submits the search to `TerraResonanceJobManager`.

Exact scheduler limits at the pinned source:

- second pulse delay: **5 ticks**;
- result delay floor: **60 ticks**;
- total search block budget per level tick: **40,000 inspected blocks**;
- per-job slice: **4,000 inspected blocks**;
- maximum search cube: **127 × 127 × 127**;
- pulse tracking range: **64 blocks**.

Multiple searches share the same level-wide budget. Jobs are rotated through a queue and only receive another slice while budget remains. Results are delivered only to an online, alive, non-removed player still in the same level.

## What it does

Provider semantics are a through-wall resonance/search utility for configured gem/ore-like targets, returning a found/not-found result and provider-defined highlights after the bounded search completes.

The search is delayed and budgeted deliberately; it is not an unbounded synchronous world scan.

## Authority / deduplication

Terra Resonance is one provider cast plus one provider-owned bounded search job. Each inspected block and each highlighted target must not be converted into separate cast, mastery or Black Arcana divination events.

Black Arcana must not:

- launch a second scan after observing this cast;
- widen the provider's 127-cube cap;
- bypass its 8-block anchor validation;
- reinterpret its result packet as authority for Black Arcana world state.

This source is a useful positive reference for bounded divination architecture, but Black Arcana-originated scans must still use Black Arcana-owned contracts and budgets.

## Confidence

`SOURCE-PINNED TARGET ADMISSION + SEARCH-SIZE CAP + LEVEL/JOB BUDGETS / EXACT TARGET TAG/CONTENT + FULL MODPACK RUNTIME QA PENDING`