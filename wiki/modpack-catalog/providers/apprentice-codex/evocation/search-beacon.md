# Search Beacon

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:search_beacon`
- **Iron's school:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 60 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 80`
- `spellPowerPerLevel = 80`
- `baseManaCost = 100`
- `manaCostPerLevel = 40`
- `castTime = 0`
- base search unit: `round(spellPower)`
- initial search distance: `base search unit * 8`
- additional distance per consumed item: `base search unit`
- absolute maximum search distance is delegated to `SearchBeaconSearchService.getMaxSearchRange()` and is not invented here

## Provider lifecycle

Server-side pre-cast validates placement/summoning through `SearchBeaconSummoning.validate(...)`, including rejection when a beacon is already active. A successful cast delegates the search workflow to `SearchBeaconSummoning.summonFromSpell(...)` with the computed initial and per-item ranges.

## Causality and progression

The structure-location workflow is provider-owned. Repeated internal search steps or extra range purchased with items are not independent casts or divination milestones unless a real provider event exposes them as such.

## Deduplication

Directly occupies the **provider-native structure-search beacon with spell-power-scaled initial range and item-funded range extension** niche. Black Arcana Familiars & Divination must not add a generic structure locator without a materially different contract.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+RANGE FORMULAS+SERVER SUMMON VALIDATION / MAX SEARCH CAP+ITEM CONSUMPTION+SEARCH SERVICE DETAILS REQUIRE SERVICE AUDIT`