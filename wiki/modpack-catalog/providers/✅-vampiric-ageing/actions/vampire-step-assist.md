# Vampire Step Assist

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:step_assist_action`
- Faction: Vampire
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Vampire Age 2 and `step_assist_skill`.

## Source-default contract

Configured persistent-style duration (`Integer.MAX_VALUE` then clamped/converted); cooldown default 0; `STEP_HEIGHT` modifier `+0.5` using `ADD_VALUE`.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation adds the provider-native step-height modifier for its action lifecycle; deactivation removes it.

## Specific evidence and QA boundary

`getCooldown()` returns the raw `stepAssistCooldown` config integer **without multiplying by 20**. Any nonzero deployed cooldown needs unit validation; default zero conceals this discrepancy.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
