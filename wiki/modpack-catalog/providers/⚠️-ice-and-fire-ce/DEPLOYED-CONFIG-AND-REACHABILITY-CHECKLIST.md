# Ice And Fire CE 2.1.2 — deployed config and reachability checklist

Status: `PARTIAL PROMOTION COMPLETE / 8 STRICT / 1 FAIL-CLOSED BLOCKER REMAINS`

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

Dread Lich Staff is now also `COUNTED_EXACT` through a separately audited runtime route: exact physical/publisher 2.1.2 binary equips `IafItems.LICH_STAFF` into `MAINHAND`; neither `DreadLichEntity` nor `DreadMobEntity` overrides death-loot handling, and the Dread Lich does not override slot drop chance. Current-pack NeoForge 21.1.250 `Mob` bytecode initializes hand equipment drop chance to `0.085`, reads that chance in `dropCustomDeathLoot`, performs the random threshold check and calls `spawnAtLocation` for the equipped stack. Audit run: `36327488231`.

Ghost Sword acquisition is also closed by exact recipe/advancement evidence, but its action remains config-gated.

## Remaining deployed config evidence

Capture the actual current instance file used by Ice And Fire CE's Jupiter config and record:

- `tools.phantasmalBladeAbility`.

Exact 2.1.2 source identifies the provider-native path as `config/iceandfire/iaf-common.json`. Do not substitute the source default (`true`) for the deployed value.

The deployed-evidence collector now captures this exact file/key without copying the surrounding Jupiter JSON. Accepted evidence is `status=OBSERVED` with a boolean value from the actual current instance plus matching physical 2.1.2 fingerprint; `NOT_FOUND`, `KEY_NOT_FOUND`, `PARSE_ERROR` and `INVALID_TYPE` remain fail-closed.

If the deployed value is proven true and no overriding runtime gate is found, Ghost Sword can be promoted individually.

## Dread Lich Staff reachability — closed

The earlier rule forbidding generic vanilla-drop inference is satisfied by direct current-runtime inspection rather than assumption. Run `36327488231` materialized NeoForge `21.1.250` for Minecraft 1.21.1 and directly verified the inherited `Mob` equipment-drop mechanics; the same run hash-gated exact Ice And Fire CE File `8757837` and verified the Dread Lich equipment path. No source default or unrelated version is substituted.

See [`DREAD-LICH-STAFF-EXACT-RUNTIME-REACHABILITY.md`](DREAD-LICH-STAFF-EXACT-RUNTIME-REACHABILITY.md).

## Promotion rule

Only Ghost Sword remains to promote. Require observed deployed `tools.phantasmalBladeAbility=true` with matching physical fingerprint and no overriding runtime gate. Do not reopen the eight already strict-counted families unless the physical identity changes.
