# Water Walking

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:water_walking_action`
- Faction: Vampire
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Vampire Age 4 skill gate and native action admission.

## Source-default contract

Enabled true; cooldown 0; config duration `Integer.MAX_VALUE` before provider clamp/tick conversion.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation sets `IVampSpecialAttributes.ageing$setWaterWalking(true)` on the Vampirism special-attributes surface; deactivation clears the state. Provider client activation mirrors that state.

## Specific evidence and QA boundary

The action uses the Vampirism special-attributes/mixin route, not an independent fluid simulation. Persistent duration describes source behavior and is not a guarantee about deployed config.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
