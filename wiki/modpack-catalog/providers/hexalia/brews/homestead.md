# Brew of Homestead

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+RECIPE+TELEPORT PATH VERIFIED / ONE-SHOT CONSUMABLE / INSTALLED-RUNTIME EQUIVALENCE PENDING`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_homestead`
- Acquisition: Small Cauldron
- Type: one-shot custom consumable; **not** a 240-second MobEffect brew
- Return container: `hexalia:rustic_bottle`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `hexalia:tree_resin`
2. `minecraft:ender_pearl`
3. `hexalia:spirit_powder`
4. `hexalia:galeberries`

Result: `hexalia:brew_of_homestead`.

## Teleport behavior 1.3.6

The item uses Hexalia's provider-owned `TeleportUtil.teleportPlayerToSpawn(..., true)`.

### Target dimension

`allowInterdimensional=true`, so the path resolves the player's respawn dimension and may return across dimensions.

### Preferred destination

If the player has a respawn position, Hexalia searches that block position plus vertical offsets `0..2` for a position where both the candidate block and the block above have empty collision shapes.

If found, the player is sent to that position centered on X/Z (`+0.5`).

### Fallback

If no suitable personal respawn position is found, Hexalia falls back to the target level's shared world spawn.

### Player-state handling

Before teleport:

- riding is stopped;
- sleeping is stopped when applicable.

After/around teleport:

- cross-dimension teleport uses the server-player path;
- positive fall distance is reset to `0`;
- the provider plays chorus-fruit teleport audio at the target path.

### Post-use effect

After attempting the provider teleport, the player receives vanilla `Confusion`/Nausea:

- duration: `600 ticks = 30 s`;
- amplifier: `0`.

## Deduplication

Homestead occupies a prepared witch-consumable return-home/respawn teleport niche. Black Arcana should not create an equivalent “witch return potion” merely under another name.

This does **not** eliminate distinct portal/domain/anchor mechanics whose identity is based on persistent targeting, bidirectional topology, typed bindings or other contracts beyond a one-shot return to respawn.

## Authority and world safety

The teleport is Hexalia-owned. Black Arcana must not reroute the same use through its canonical cast pipeline or charge an additional cost.

If Black Arcana later initiates its own cross-provider teleport operation, its own server validation/world-safety rules remain mandatory; that does not grant authority to rewrite Hexalia's native Homestead settlement.
