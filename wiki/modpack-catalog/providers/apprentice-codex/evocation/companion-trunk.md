# Companion Trunk

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:companion_trunk`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 10`
- `spellPowerPerLevel = 10`
- `baseManaCost = 10`
- `manaCostPerLevel = 0`
- `castTime = 0`
- companion health: `round(spellPower)`

## Provider lifecycle

On the server the spell delegates to `CompanionTrunkManager.toggle(...)`. The provider therefore owns whether the companion is created, dismissed, persisted or otherwise transitioned; the spell itself only supplies the computed health value and the player identity.

## Causality and progression

Toggling the companion is one provider cast. Autonomous companion behavior after creation is not a stream of new player casts. RPG/Black Arcana must not award cast progression for passive companion ticks or manager-side maintenance.

## Deduplication

Occupies the **toggleable owner-bound trunk companion whose health scales with Evocation spell power** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+HEALTH FORMULA+SERVER TOGGLE / COMPANION INVENTORY+AI+PERSISTENCE DETAILS REQUIRE MANAGER AUDIT`