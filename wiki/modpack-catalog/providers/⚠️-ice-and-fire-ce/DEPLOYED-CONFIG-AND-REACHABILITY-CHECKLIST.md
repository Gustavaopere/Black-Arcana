# Ice And Fire CE 2.1.2 — deployed config and reachability checklist

Status: `FAIL-CLOSED / REQUIRED BEFORE STRICT PROMOTION`

## Fixed identity gate

- filename: `iceandfire-2.1.2.jar`;
- mod id: `iceandfire`;
- runtime: `2.1.2`;
- SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`.

If any field changes, stop and re-audit before promotion.

## Required deployed config evidence

Capture the actual current instance file used by Ice And Fire CE's Jupiter config and record `tools.phantasmalBladeAbility`. Exact 2.1.2 source identifies the provider-native path as `config/iceandfire/iaf-common.json`. Do not substitute the source default (`true`) for the deployed value.

## Required reachability evidence

For each of the nine candidate action families in [`ACTIVE-MAGIC-INVENTORY.md`](ACTIVE-MAGIC-INVENTORY.md), prove at least one authoritative current-pack survival route using exact current data/JAR or deterministic assembled-pack observation: recipe, entity/boss drop or loot table, trade/reward, or another deterministic provider-native acquisition route.

Variant items that resolve to one semantic action family should be deduplicated. Creative/command availability is insufficient.

## Promotion rule

Promote only rows individually proven reachable/enabled. No strict semantic count changes until the corresponding evidence is captured.
