# Apothic Spawners — 1.4.0

Status: `EXACT PHYSICAL ARTIFACT + EXACT CURSEFORGE RELEASE + EXACT OFFICIAL 1.4.0 RELEASE COMMIT / SPAWNER LIFECYCLE+MODIFIER PROVIDER / 0 SPELLS+GLYPHS+RITUALS / 16 SPAWNER STATS / 32 STOCK MODIFIER RECIPES / 2 MIXINS / PERSISTENT TILE STATE / 1 CLIENTBOUND CONFIG PAYLOAD / NUCLEAR-SPAWNER CASCADE / BYTE+FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `ApothicSpawners-1.21.1-1.4.0.jar`
- mod id: `apothic_spawners`
- version: `1.4.0`
- physical SHA-1: `b3be29751daea738e691db8949cce079e5aae3be`
- Minecraft: `1.21.1`
- loader: NeoForge
- physical NeoForge: `21.1.248`
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`

Apothic Spawners is a spawner lifecycle/modification provider. It is cataloged because it touches progression-adjacent acquisition, mob lifecycle, enchantment-driven drops and destructive world behavior, not because it owns a spell system.

## Publisher and exact source identity

- CurseForge project: `986583`
- exact 1.4.0 file id: `8469405`
- release date: 2026-07-20
- official repository: `Shadows-of-Fire/Apothic-Spawners`
- official maintenance branch: `1.21`
- exact release commit: `d3bc0b40d46bee476fc770f8e4e44a1c35ecddd3`, message `1.4.0`
- exact release tree: `7cd127fe22a9810b22bd8203cb2286d53b840e25`
- direct parent: `9b144c0ed58a7c0a83635b9a52653b1228844f55`, `The Nuclear Spawner`, backport of the upstream 26.1 feature
- preceding compatibility fix: `af8b7c4f8a5dd7915b18a0cdab7549f12b4f4ea2`, `Fix float comparisons`

The `1.21` branch later advanced five commits to `fa52d69e86817a377116b669383703f8b6838f8a`. Comparing the release commit to that head shows only translation changes plus schema-documentation additions; no Java, registry or gameplay datapack file changed. The exact 1.4.0 release commit is therefore the semantic source pin used here.

Exact source metadata declares:

- version `1.4.0`;
- Minecraft `1.21.1`;
- Java `21`;
- NeoForge baseline/range `[21.1.187,)`;
- Placebo `[9.9.0,)`;
- generated mod license `MIT License`.

The physical pack uses NeoForge 21.1.248 and Placebo 9.9.2.

## Magic identity result

At the exact 1.4.0 source ceiling:

- **0 standalone spells**;
- **0 glyphs**;
- **0 rituals**;
- **0 provider mana/cast resource**;
- **0 provider C2S cast-intent/network pipeline**.

The source package contains 27 Java files. No spell/glyph/ritual registry surface exists. The only provider payload is a clientbound configuration synchronization payload and is unrelated to casting.

Capturing is an enchantment/effect path attached to weapon kills. Echoing is a spawner stat that affects loot/XP of entities produced by that spawner. Neither becomes a Black Arcana spell identity.

## Canonical spawner-stat registry

The custom `apothic_spawners:spawner_stat` registry closes exactly 16 IDs:

1. `min_delay`
2. `max_delay`
3. `spawn_count`
4. `max_nearby_entities`
5. `req_player_range`
6. `spawn_range`
7. `initial_health`
8. `ignore_players`
9. `ignore_conditions`
10. `redstone_control`
11. `ignore_light`
12. `no_ai`
13. `silent`
14. `youthful`
15. `burning`
16. `echoing`

These are provider-owned spawner semantics. Black Arcana and RPG Skill Tree must not implement a second per-tick throughput controller for them.

## Modifier recipe surface

The exact release tree contains 32 stock `spawner_modifier` recipe JSONs:

- 16 forward recipes;
- 16 matching `_inverse` recipes.

The 16 semantic families are:

- `burning`
- `echoing`
- `ignore_conditions`
- `ignore_light`
- `ignore_players`
- `initial_health`
- `max_delay`
- `max_nearby`
- `min_delay`
- `no_ai`
- `player_range`
- `redstone_control`
- `silent`
- `spawn_count`
- `spawn_range`
- `youthful`

`StatModifier` exposes exactly two operation modes: `add` and `set`. `SpawnerModifier` resolves the first matching recipe, prioritizes offhand-constrained recipes, applies its stat modifiers and marks the tile changed.

Provider registry/data surfaces also include:

- recipe type/serializer `apothic_spawners:spawner_modifier`;
- enchantment effect component `apothic_spawners:capturing`;
- advancement trigger `apothic_spawners:spawner_modifier`;
- item sub-predicate `apothic_spawners:spawn_egg`;
- entity-type tag `apothic_spawners:blacklisted_from_spawners`;
- loot table key `apothic_spawners:gameplay/unstable_spawner`.

## Vanilla-spawner replacement boundary

The exact mixin manifest contains exactly two common mixins and no client mixins:

- `BlocksMixin`
- `ItemsMixin`

They substitute the vanilla `minecraft:spawner` block/item implementation with Apothic behavior rather than registering a parallel spawner identity. Common setup also replaces the `BlockEntityType.MOB_SPAWNER` factory with `ApothSpawnerTile`.

Therefore Black Arcana must treat the loaded vanilla spawner path as provider-owned when Apothic Spawners is present. It must not assume vanilla block/tile implementation details are authoritative.

## Config and network surface

Five common config values are source-closed:

- `spawnerSilkLevel` — default 1;
- `spawnerSilkDamage` — default 100;
- `capturingDropChance` — default 0.005;
- `spawnersDropEmpty` — default false;
- `entityDespawnDelay` — default 600 ticks.

One PLAY payload exists:

- type/id: `apothic_spawners:config`;
- flow: CLIENTBOUND;
- protocol/version string: `2`;
- synchronized fields: Silk level and Capturing base chance only.

This is provider config sync, not cast authorization or a Black Arcana networking seam.

## Persistence and mob-lifecycle surface

`ApothSpawnerTile` explicitly persists:

- custom stat map under `stats`;
- player-modified marker `modified`;
- instability countdown `unstable_ticks`;
- captured next-spawn snapshot `captured_spawn_data`.

Relevant event semantics include:

- Capturing rolls a spawn-egg drop from the killer weapon's Capturing level, respecting the provider blacklist;
- Echoing rerolls loot and multiplies XP according to the provider echo count stored on spawned entities;
- spawn-egg application is denied for blacklisted entity types;
- provider No-AI/movable-mob handling prevents movement-side breakage while retaining the stat semantics;
- despawn delay applies only when `MobSpawnType.isSpawner(...)` identifies the mob as spawner-generated.

These are provider-owned lifecycle rules. BA must not duplicate them through generic mob-spawn or loot hooks.

## 1.4.0 Nuclear Spawner boundary

When an Apothic spawner is affected by the provider explosion path, `ApothSpawnerBlock` begins instability rather than immediately following the ordinary destruction path.

The exact 1.4.0 constants are bounded:

- instability duration: **60 ticks**;
- explosion radius: **8.0**;
- unstable mob spawn attempts: **12**;
- unstable loot table: `apothic_spawners:gameplay/unstable_spawner`.

The tile snapshots its next spawn data, counts down server-side, removes the block, creates the provider explosion, attempts bounded entity spawning and rolls the unstable-spawner loot table.

This is a critical Black Arcana world-safety boundary:

- BA-originated destructive world changes still require `WorldEffectPolicy` before the BA effect is applied;
- if a permitted BA world effect legitimately causes an explosion and Apothic Spawners reacts through its own block/provider hooks, that resulting instability/detonation is provider-owned causality;
- BA must not additionally invoke provider instability/detonation helpers as a second processing pass;
- no adapter may bypass `WorldEffectPolicy` by treating the provider's destruction path as a surrogate BA world mutation API.

## Authority result

- Apothic Spawners owns spawner stats, modifier recipes, spawner collection, tile persistence, Capturing/Echoing spawner interactions, spawner-specific mob lifecycle and the Nuclear Spawner instability path.
- Vanilla Minecraft supplies the base `minecraft:spawner` identity consumed/replaced by the provider runtime.
- Placebo owns the shared infrastructure it provides, including payload helper plumbing.
- Other machine/summon/spawner providers keep authority over their own spawn systems; thematic similarity does not create an adapter.
- Black Arcana retains canonical casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- RPG Skill Tree remains progression-only through explicit contracts and must not directly multiply provider tick loops or spawn throughput without a bounded causal contract.

## Remaining QA / fail-closed boundaries

- source↔physical-JAR byte reproducibility is not proven;
- CurseForge file bytes were not directly compared with the physical artifact;
- full-modpack modifier reload, blacklist interactions, explosion event ordering and external-spawner interoperability remain runtime QA;
- exact behavior when other mods alter vanilla spawner block/tile factories remains integration QA;
- provider explosion/loot interactions with protection/world-policy mods remain runtime QA;
- future provider versions require re-audit.

## License / clean-room

The exact source code/root license and generated 1.4.0 metadata state MIT for code, while `LICENSE_ASSETS` is All Rights Reserved and the current CurseForge project surface labels the project All Rights Reserved. This discrepancy is preserved as a reuse boundary. The Black Arcana catalog performs factual, read-only inspection only and does not copy source implementation or assets.