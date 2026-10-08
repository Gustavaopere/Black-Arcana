# Celerity

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:celerity_action`
- Faction: Vampire
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Vampire Age 1; age-granted Celerity ActionSkill enabled by the provider lifecycle.

## Source-default contract

Enabled true; action duration 8 seconds; cooldown 60 seconds; `minecraft:movement_speed` modifier `ADD_MULTIPLIED_TOTAL` amount `1.025` under id `vampiricageing:celerity_speed_increase`.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation applies the provider movement-speed attribute modifier; deactivation removes it. Server-side particles occur during active state.

## Specific evidence and QA boundary

The amount `1.025` is the **raw source value**, not an established +2.5% bonus. Effective installed movement speed requires runtime measurement.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
