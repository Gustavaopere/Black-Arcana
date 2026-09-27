# Ice And Fire CE 2.1.2 — deployed config and reachability checklist

Status: `PARTIAL PROMOTION COMPLETE / 7 STRICT / 2 FAIL-CLOSED BLOCKERS REMAIN`

## Fixed identity gate

- filename: `iceandfire-2.1.2.jar`;
- mod id: `iceandfire`;
- runtime: `2.1.2`;
- SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`.

If any field changes, stop and re-audit before further promotion.

## Closed exact reachability

Exact current-JAR run `36323035696` closes provider-native recipe/loot reachability for seven independent semantic families:

- Cockatrice Scepter;
- Deathworm Gauntlet;
- Gorgon Head;
- Pixie Wand;
- Siren Flute;
- Summoning Crystal;
- Stymphalian Feather Bundle.

Those seven are already `COUNTED_EXACT` and require no repeated acquisition enumeration unless the physical JAR changes.

Ghost Sword acquisition is also closed by exact recipe/advancement evidence, but its action remains config-gated.

## Remaining deployed config evidence

Capture the actual current instance file used by Ice And Fire CE's Jupiter config and record:

- `tools.phantasmalBladeAbility`.

Exact 2.1.2 source identifies the provider-native path as `config/iceandfire/iaf-common.json`. Do not substitute the source default (`true`) for the deployed value.

If the deployed value is proven true and no overriding runtime gate is found, Ghost Sword can be promoted individually.

## Remaining reachability evidence

Only **Dread Lich Staff** remains acquisition-unproven.

Exact source proves Dread Lich equips `IafItems.LICH_STAFF`, but:

- exact provider data contains no `iceandfire:lich_staff` recipe/loot/advancement reference;
- no explicit provider-native drop-chance/drop override has been proven for the staff;
- generic vanilla equipment-drop behavior is not used as an inferred catalog route.

Close this row only with authoritative current-pack evidence: exact provider loot/drop logic, deterministic assembled-pack observation, or another explicit survival acquisition route.

## Promotion rule

Promote the two remaining rows independently when their specific blockers are proven. Do not reopen the seven already strict-counted families unless the physical identity changes.
