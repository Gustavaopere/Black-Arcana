# Soul Fire'd 6.1.0 — enchantments, loot and data

The exact 6.1.0 source registers its enchantment content through a Cobweb `StaticDataPack` named `soul_fire_d:enchantments` at top pack position. This document records the exact bundled definitions rather than inferring behavior from names.

## Enchantment registry identities

The static datapack places exactly two definitions under `data/minecraft/enchantment/`:

- `minecraft:soul_fire_aspect`;
- `minecraft:soul_flame`.

They are vanilla enchantment-registry entries supplied by Soul Fire'd's bundled datapack. They are **not** Black Arcana spells and are not evidence of a Soul Fire'd spell registry.

## `minecraft:soul_fire_aspect`

Exact data:

- max level: `2`;
- anvil cost: `4`;
- weight: `2`;
- supported items: `#minecraft:enchantable/fire_aspect`;
- primary items: `#minecraft:enchantable/sword`;
- slot: `mainhand`;
- exclusive set: `#prometheus:exclusive_set/fire_aspect`.

Effect:

- event: `minecraft:post_attack`;
- enchanted party: attacker;
- affected party: victim;
- requires a direct damage source;
- effect type: `prometheus:ignite`;
- fire type: `soul`;
- duration expression: linear, base `4.0`, plus `4.0` per level above first.

The exact source data therefore delegates actual Soul Fire ignition semantics to Prometheus rather than implementing a second ignition runtime in Soul Fire'd.

## `minecraft:soul_flame`

Exact data:

- max level: `1`;
- anvil cost: `4`;
- weight: `2`;
- supported items: `#minecraft:enchantable/bow`;
- slot: `mainhand`;
- exclusive set: `#prometheus:exclusive_set/flame`.

Effect:

- event: `minecraft:projectile_spawned`;
- effect type: `prometheus:ignite`;
- fire type: `soul`;
- exact data value for duration: `100.0`.

No unit is inferred here beyond the provider data/API contract. Runtime interpretation belongs to Prometheus/Minecraft's enchantment effect system.

## Enchantment tags

The bundled datapack also supplies tag contributions for the new enchantments, including:

- `minecraft:in_enchanting_table`;
- `minecraft:tradeable`;
- `minecraft:treasure`;
- `minecraft:smelts_loot`;
- Prometheus exclusive sets for Fire Aspect and Flame families.

The exact 6.1.0 changelog specifically records a fix for unwanted override of tags in this enchantments datapack. This is a release-relevant data-pack correction, not a new gameplay subsystem.

## NeoForge loot serializer

Soul Fire'd registers one `NeoForgeRegistries.GLOBAL_LOOT_MODIFIER_SERIALIZERS` entry:

- `soul_fire_d:chest_loot_modifier`.

Its codec accepts a list of additions with:

- enchantment holder;
- float chance;
- requested level.

At application time, each addition:

1. verifies the enchantment supports at least one item;
2. rolls the configured chance independently;
3. creates an enchanted book;
4. clamps requested level to the enchantment's current maximum.

## Bundled Bastion acquisition

The exact bundled modifier data targets:

- loot table `minecraft:chests/bastion_other`.

It contains exactly two additions:

| Enchantment | Level | Chance |
|---|---:|---:|
| `minecraft:soul_fire_aspect` | 1 | 0.05 |
| `minecraft:soul_flame` | 1 | 0.05 |

These are independent rolls in the implementation loop. This acquisition surface belongs to Soul Fire'd/NeoForge loot processing and should not be duplicated by Black Arcana progression or spell rewards.

## Soul Fire Charge recipe

The exact common data includes a shapeless recipe producing:

- `16x minecraft:soul_fire_charge`.

Inputs:

- `minecraft:gunpowder`;
- `minecraft:ghast_tear`;
- either `minecraft:coal` or `minecraft:charcoal`.

A matching recipe advancement/resource family is bundled under the `minecraft` namespace.

## Deduplication result

Black Arcana should not:

- register duplicate Soul Fire Aspect/Flame enchantments;
- repeat the Bastion loot injection;
- treat provider enchantment ignition as a BA spell cast;
- award or settle the same provider loot through a second progression pipeline;
- infer that `minecraft` namespace means vanilla authorship — these exact entries are supplied by Soul Fire'd's bundled datapack.

If future BA content intentionally references these enchantments, it should reference the real registry identities and preserve provider ownership rather than cloning semantics under BA names.
