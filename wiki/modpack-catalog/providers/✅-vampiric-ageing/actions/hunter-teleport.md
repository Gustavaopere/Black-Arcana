# Hunter Teleport

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:hunter_teleport_action`
- Faction: Hunter
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Cumulative Tainted Age at least 8; unavailable during Limited Bat Mode.

## Source-default contract

Enabled true; cooldown 20 seconds; maximum look distance 35 blocks.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

The provider ray-traces the player's look direction, resolves a target BlockPos, probes liquid/collision suitability with temporary placement and rollback, and settles the successful destination through `ServerPlayer` teleport plus Vampirism particles/sounds.

## Specific evidence and QA boundary

An integration must consume provider success rather than repeat destination selection or teleport. Effective current Tainted Age and deployed enablement must be read from canonical Hunter state.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
