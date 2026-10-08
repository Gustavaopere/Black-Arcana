# Limited Hunter Bat Mode

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:limited_hunter_batmode_action`
- Faction: Hunter
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Cumulative Tainted Age at least 10 plus environmental gates: not underwater, not in The End or provider bat blacklist, not mounted, and no disallowed sun state when configured.

## Source-default contract

Normal duration 240 seconds; cooldown 120 seconds; flight speed `0.02`; update exhaustion `0.008`; source-config transformed duration effectively persistent.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation sets Hunter Bat state, changes dimensions/pose, removes armor/toughness contributions, grants flight and configures flight speed. While active, the provider restricts attacks, mounts, block/item interactions, placement and mining. Deactivation restores allowed abilities and clears the canonical provider state.

## Specific evidence and QA boundary

This is a **multisurface** native action. Server/client flight and pose synchronization require dedicated-server QA; checking `mayfly` or pose alone does not prove canonical Bat Mode.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
