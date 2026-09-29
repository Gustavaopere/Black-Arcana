# Ice And Fire CE 2.1.2 — Dread Lich Staff exact runtime reachability

Status: `EXACT PHYSICAL PROVIDER + CURRENT-PACK NEOFORGE RUNTIME / SURVIVAL ACQUISITION ROUTE CLOSED / +1 COUNTED_EXACT`

## Evidence checkpoint

- temporary NON-MERGE branch: `audit/iceandfire-dread-lich-staff-runtime-drop-2026-09-27`;
- final audit HEAD: `7fd05fd74dab192f2f3fbfb17dd51e7763df730f`;
- final workflow run: `36327488231` — GREEN;
- text-only artifact: `10934238232`;
- evidence artifact digest: `sha256:12cb50fde9936268bbfb5aeb1cb2d43a2fb87de82dcf1cf815b5b9846bec0aa4`.

The audit intentionally retains only bounded class/field/control-flow facts. It does not redistribute provider or Minecraft implementation bodies.

## Exact provider identity

The audit materialized CurseForge File `8757837` and hard-gated it against the physical pack SHA-1:

- expected physical SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`;
- publisher/audit SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`;
- exact artifact SHA-256: `3ce264a17bc06e5372077f64e80870d6c84ffbd5383aef59faeaa81d297769a6`.

The exact `DreadLichEntity` binary:

- extends `DreadMobEntity`;
- calls the parent equipment-population path;
- references `IafItems.LICH_STAFF`;
- references `EquipmentSlot.MAINHAND`;
- calls `setItemSlot`;
- does **not** call `setDropChance` in that equipment path;
- does not declare its own `dropCustomDeathLoot`;
- its parent `DreadMobEntity` also does not declare `dropCustomDeathLoot`.

This directly corroborates the exact 2.1.2 source-semver observation that spawned Dread Liches equip the Lich Staff in the main hand while inheriting ordinary mob death-loot handling.

## Current-pack runtime identity

The final audit explicitly materialized the Black Arcana modding runtime with:

- Minecraft: `1.21.1`;
- NeoForge override: `21.1.250`, matching the current physical pack loader line;
- Parchment: `2024.11.17` for readable mapped inspection.

The mapped `net.minecraft.world.entity.Mob` class directly proves:

- `DEFAULT_EQUIPMENT_DROP_CHANCE = 0.085f`;
- constructor initialization fills `handDropChances` with `0.085f`;
- `dropCustomDeathLoot` iterates equipment slots;
- it reads the equipped stack via `getItemBySlot`;
- it reads the slot chance via `getEquipmentDropChance`;
- it evaluates the random threshold using `RandomSource.nextFloat`;
- the successful branch calls `spawnAtLocation(ItemStack)`;
- hand-slot chance resolution reads the `handDropChances` array.

This is direct current-runtime evidence, not an inference from generic Minecraft behavior or a different loader line.

## Catalog conclusion

The exact provider equips `iceandfire:lich_staff` into the Dread Lich main hand, does not replace the inherited drop chance/death-loot path, and the exact current-pack runtime provides a non-zero hand-equipment drop route.

Therefore the Dread Lich Staff has an explicit survival acquisition route and is promoted from `CONDITIONAL` to **`COUNTED_EXACT` (+1)**.

The provider remains **⚠️ partial/conditioned** because Ghost Sword / Phantasmal Blade still depends on the unresolved deployed Jupiter value `tools.phantasmalBladeAbility`.

## Runtime QA boundary

This catalog closure does not certify:

- assembled-pack Dread Lich spawn frequency/worldgen;
- realized drop-frequency statistics in a live world;
- Looting/enchantment adjustments to the base equipment chance;
- multiplayer item settlement;
- item durability/cooldown/balance;
- Ghost Sword config state.

Those are runtime/balance QA and do not reopen the now-explicit semantic acquisition route unless the physical provider or loader identity changes.
