# Earthdive Wall Teleport

- Provider: **Bosses of Mass Destruction** (`bosses_of_mass_destruction`)
- Version: `1.3.3`
- Exact physical/publisher SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`
- Owner item: **Earthdive Spear**
- Provider settlement seam: `WallTeleport`
- Semantic type: deliberate supernatural traversal action
- State: `COUNTED_EXACT`

## Identity and trigger

The Earthdive Spear exposes provider item-use surfaces including charge/use/release handling. Charged release delegates to the provider's `WallTeleport` behavior.

The semantic root is the deliberate short-range wall-teleport action. Charge state, animation and downstream teleport effects are parts of this same identity.

## Settlement

Exact artifact evidence closes a provider-owned attempt to teleport the user through solid geometry at short range.

No additional teleport identity is created by the resulting position change, feedback or cooldown/state machinery.

## Exact acquisition

Exact shaped recipe uses:

- Obsidian Heart;
- Void Thorn;
- Stick.

Exact provider data supplies:

- **Obsidian Heart** in the Obsidilith arena chest;
- **Void Thorn** in Void Blossom entity loot.

The exact Void Blossom arena logic automatically spawns that boss when a player enters the arena proximity. That automatic proximity spawn is world/boss lifecycle and is not counted as a deliberate player summon.

## Reachability disposition

The recipe and both provider-native ingredient routes are closed at catalog level. Therefore Earthdive Wall Teleport is strict-counted as `COUNTED_EXACT`.

## Evidence boundary

The card does not invent teleport distance, charge duration, cooldown or collision edge cases beyond what the exact audit retained.

Source: `../EXACT-1.3.3-ARTIFACT-AUDIT.md`.
