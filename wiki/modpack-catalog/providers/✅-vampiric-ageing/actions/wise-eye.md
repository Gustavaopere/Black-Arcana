# Wise Eye

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:hunter_wise_eye_action`
- Faction: Hunter
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Hunter Age 5 and `wise_eye_skill`.

## Source-default contract

Source config defines `wiseEyeDuration=120`, raw `wiseEyeCooldown=10` and slowdown enabled true.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation sets the provider `AgeingPlayerCache.hasBypassInvisibility` flag and optionally applies `MOVEMENT_SPEED -0.95 ADD_MULTIPLIED_TOTAL`; deactivation clears both.

## Specific evidence and QA boundary

The 1.4.21 **executable source** implements `getDuration()` using **Hunter Step Assist duration**, not `wiseEyeDuration`. `getCooldown()` returns the raw configured 10 without `×20`. Do not state runtime duration as 120 seconds or interpret invisibility bypass as Night Vision.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
