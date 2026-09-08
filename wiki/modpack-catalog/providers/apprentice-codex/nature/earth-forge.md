# Earth Forge

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:earth_forge`
- **School:** Nature
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 100`
- `spellPowerPerLevel = 0`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`

Target range:

`8 * spellPower / 100` blocks.

Placement radius parameter:

`max(1, 1 + floor(spellPower / 100))`.

Sneaking forces radius to **1**, yielding the single-block mode described by the provider guide.

## Server placement plan

Before cast, the provider resolves a validated block face, derives a center point and enumerates only positions allowed by `EarthForgePlacementRules.canReplaceWithDirt(...)`. Center, effect direction and radius are serialized into cast data.

On cast, the plan is reconstructed against **current world state** rather than blindly trusting the pre-cast list, then submitted as an `EarthForgeJob`.

## Exact bounded job

`EarthForgeJob`:

- waits 2 ticks before the first placement;
- places the center first;
- places at most **one dirt block every 2 game ticks** thereafter;
- randomizes remaining target order;
- rechecks replaceability immediately before each placement;
- ends when all candidates are consumed.

For a valid ServerPlayer owner, dirt placement is performed through `BlockTools.useItemOnBlockByPlayerMainHand(...)` with a Dirt stack, preserving player-interaction/loader protection semantics. Only non-player/no-longer-valid-player fallback uses direct `setBlockAndUpdate` after provider replacement checks.

## What it does

Provider guide semantics: create a flat patch of dirt at line of sight; sneaking reduces it to one block.

## World safety

This provider spell already has a bounded asynchronous placement job and player interaction path. Black Arcana must not wrap the same cast in a second placement loop. BA-originated terrain creation still requires `WorldEffectPolicy` and equivalent budgets.

## Deduplication

Occupies the **bounded dirt-plane construction** niche.

## Confidence

`SOURCE-PINNED SPELL + PLACEMENT JOB / NON-PLAYER FALLBACK POLICY + MODPACK PROTECTION QA PENDING`