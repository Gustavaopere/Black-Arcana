# Soul Elytra Boost

Status: `PUBLIC_SOURCE_BASELINE / CONFIG_CONDITIONAL / PHYSICAL EXACTNESS OPEN / +0 STRICT`

- Provider: **Deeper and Darker** (`deeperdarker`)
- Version line: `1.4.1`
- Semantic owner: `deeperdarker:soul_elytra`
- Client trigger: BOOST keybind, default key **B**
- Network identity: `deeperdarker:soul_elytra_boost`
- Server seam: `SoulElytraBoostPacket.handle(...)`
- Exact source pin: `KyaniteMods/DeeperAndDarker@f7ba235d078411a1165a8cac184adfe0ccc8cebe`
- Public publisher SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`
- Current physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`
- Semantic type: deliberate supernatural equipment/flight action
- Current strict state: `OPEN_PHYSICAL_ARTIFACT / DEPLOYED_CONFIG_UNKNOWN / +0`

This card describes the **official/public 1.4.1 + exact-source baseline**. It is not projected onto the unmatched physical JAR.

## Input and network path

Exact 1.4.1 client code registers `Keybinds.BOOST` with default GLFW key **B**.

On a consumed BOOST click, the client sends:

`new SoulElytraBoostPacket(true)`

to the server. The payload ID is:

`deeperdarker:soul_elytra_boost`.

The server handler is the provider-owned authority for action admission and settlement.

## Item contract

Exact 1.4.1 item registration defines:

- durability: **956**;
- rarity: **UNCOMMON**;
- chest armor modifier: **+3 armor**;
- repair item: `deeperdarker:soul_crystal`.

## Config contract

Exact 1.4.1 COMMON config key:

- key: `soulElytraCooldown`;
- source default: **600 ticks**;
- valid range: **-1..12000**;
- `-1`: disables the active boost.

The current pack is known to load `config/deeperdarker-common.toml`, but the effective deployed value is not retained. Black Arcana does not substitute the source default for deployed evidence.

See `../DEPLOYED-CONFIG-CHECKPOINT.md`.

## Server admission

If `soulElytraCooldown == -1`, the handler returns without producing the boost and sends the provider's disabled/no-cooldown client message.

Otherwise, the action settles only when all of these are true:

- player is fall-flying;
- chest armor inventory slot contains `deeperdarker:soul_elytra`;
- Soul Elytra is not currently on cooldown.

## Settlement

On admission:

- provider creates a vanilla `FireworkRocketEntity`;
- the rocket uses a plain `minecraft:firework_rocket` item stack;
- the rocket is attached to the player through the vanilla entity constructor used by the provider;
- the rocket entity is added to the level;
- Soul Elytra receives item cooldown equal to the effective `soulElytraCooldown` value.

## Public/source acquisition

Exact generated shaped recipe:

```text
BCB
DED
B B
```

Ingredients:

- `B` = `deeperdarker:sculk_bone`;
- `C` = `deeperdarker:soul_crystal`;
- `D` = `deeperdarker:soul_dust`;
- `E` = `minecraft:elytra`.

Result: **1 `deeperdarker:soul_elytra`**.

This is baseline acquisition evidence only; exact physical reachability is not asserted while the installed JAR remains byte-different.

## Excluded adjacent behavior

`SoulElytraItem.inventoryTick(...)` only reports cooldown state client-side while the item occupies the chest slot. It does not create an additional semantic action.

Ordinary Elytra fall-flying is host behavior; the provider-owned semantic root here is the explicit BOOST input and its server-side settlement.

## Evidence boundary

Two independent gates remain open:

1. the current physical JAR does not hash-match the public artifact or clean source build;
2. the deployed effective `soulElytraCooldown` value is unknown.

Therefore:

- public/source baseline: **present**;
- exact-current physical action: **not proven**;
- deployed enablement: **unknown**;
- strict semantic contribution: **+0**;
- provider remains **⚠️ partial**.

Sources inside this provider folder: `../PUBLIC-1.4.1-BASELINE-AUDIT.md`, `../DEPLOYED-CONFIG-CHECKPOINT.md`, `PUBLIC-BASELINE-ACTIONS.md`.
