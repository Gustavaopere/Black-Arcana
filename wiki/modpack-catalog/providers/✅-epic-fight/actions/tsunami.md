# Tsunami

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:tsunami`
- Owner/reachability: `minecraft:trident` with vanilla **Riptide**
- Semantic type: deliberate supernatural tide/mobility attack
- State: `COUNTED_EXACT`

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Tsunami when the trident has Riptide.

Because Riptide is the first selector branch, this path takes precedence over the Channeling and Loyalty branches in the same exact selector.

## Exact provider behavior

The exact artifact packages dedicated Tsunami animation resources and provider Tsunami particle paths. Exact control flow also chooses a strengthened action variant when the server player is in water or rain.

Water/rain state modifies this same Tsunami identity. It does not create a second semantic root.

## Deduplication boundary

Dash/movement, particles, animation, hits, damage and the strengthened environmental variant are parameters or consequences of the one provider-owned action.

## Authority boundary

Epic Fight remains authority for movement, resource state, animation, target/hit processing and all settlement. Black Arcana catalogs the action but must not duplicate it.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
