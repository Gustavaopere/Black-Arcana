# Improved Senses

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:improved_senses_action`
- Faction: Werewolf
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Werewolf Age 5 and, by default, the native Werewolves `SENSE` skill; action exists only when Werewolves support is loaded.

## Source-default contract

Source duration 120 seconds (converted to ticks); raw cooldown config 10; slowdown enabled true.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation sets provider invisibility-bypass cache state and optionally adds `MOVEMENT_SPEED -0.95 ADD_MULTIPLIED_TOTAL`; deactivation removes both.

## Specific evidence and QA boundary

`getCooldown()` returns the raw config integer without `×20`. This is a Werewolves overlay, not a new sense/magic runtime. Werewolves 2.0.3.3 is present in the current cataloged pack, but effective deployed gates and timing require runtime QA.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
