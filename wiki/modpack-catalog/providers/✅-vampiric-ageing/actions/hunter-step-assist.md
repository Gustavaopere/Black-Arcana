# Hunter Step Assist

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:step_assist_hunter_action`
- Faction: Hunter
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Hunter Age 4 and `step_assist_hunter_skill`.

## Source-default contract

Effectively persistent configured duration; cooldown default 0; `STEP_HEIGHT +0.5 ADD_VALUE`.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Provider activation applies the Hunter step-height modifier and deactivation removes it within the native action lifecycle.

## Specific evidence and QA boundary

As with Vampire Step Assist, the cooldown getter returns the raw config integer rather than converting seconds to ticks. Nonzero deployed values remain timing-QA-gated.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
