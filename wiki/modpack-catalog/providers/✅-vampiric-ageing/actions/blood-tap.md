# Blood Tap / Drain Blood

- Provider: **Vampiric Ageing** (`vampiricageing`)
- Installed version line: `1.21-1.4.21`
- Exact version-correlated source pin: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- Registered action: `vampiricageing:drain_blood_action`
- Faction: Vampire
- Evidence status: `SOURCE_PINNED / CONDITIONAL / +0 STRICT`

## Unlock and admission

Vampire Age 3 and the provider-native `blood_drain_skill` grant.

## Source-default contract

Enabled true; duration 45 seconds; cooldown 150 seconds.

These are **source defaults**, not measured deployed values.

## Provider-owned execution

Activation opens the lasting-action window. Actual blood settlement happens in `AgeingEventHandler.onHurt` for eligible damage inflicted by a Vampire Player while active: Vampirism resolves bite type and target-specific debit, then `VampirePlayer.drinkBlood(...)` settles blood and produces the BloodDrink event.

## Specific evidence and QA boundary

This is **not** generic damage-proportional lifesteal. When the DRAINING ageing method applies, the entity-backed BloodDrink event may also credit Age progress. Never duplicate either blood settlement or ageing credit.

## Black Arcana integration

Vampirism/Werewolves native `IActionHandler` and Vampiric Ageing state remain the action, cooldown, duration and resource authority. Black Arcana may catalog/observe the registered identity but must not execute an independent duplicate or grant its underlying ActionSkill.

The exact source line catalogs this identity, but provider-runtime behavior and effective deployed configuration have **not** been directly verified; this action adds **+0** to the current strict minimum.

Evidence: [canonical action audit](../ACTION-CATALOG.md), [provider README](../README.md), [technical audit](../TECHNICAL-AUDIT.md), [integration rules](../INTEGRATION-RULES.md).
