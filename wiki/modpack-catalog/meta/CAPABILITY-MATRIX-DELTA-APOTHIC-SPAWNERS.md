# Capability Matrix Delta — Apothic Spawners

Phase 2AT candidate provider: `apothic_spawners` 1.4.0.

## Evidence layers

- Physical artifact: `ApothicSpawners-1.21.1-1.4.0.jar`, SHA-1 `b3be29751daea738e691db8949cce079e5aae3be`.
- Physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`, NeoForge 21.1.248.
- Exact publisher release: CurseForge project/file `986583 / 8469405`, 2026-07-20.
- Exact official source release commit: `Shadows-of-Fire/Apothic-Spawners@d3bc0b40d46bee476fc770f8e4e44a1c35ecddd3`.
- Exact release tree: `7cd127fe22a9810b22bd8203cb2286d53b840e25`.
- Source metadata: 1.4.0, Minecraft 1.21.1, Java 21, NeoForge 21.1.187+, Placebo 9.9.0+.

No source↔physical-JAR byte equivalence is asserted.

## Capability delta

| Capability family | Provider surface | Black Arcana action |
|---|---|---|
| standalone spells | 0 | do not invent spell identities from Capturing/Echoing or destructive spawner behavior |
| glyphs / rituals | 0 / 0 | no BA registry identities or Mastery mapping |
| mana / cast resource | none | no resource settlement bridge |
| cast networking | none observed | no C2S cast-intent path; do not infer casting authority |
| config networking | 1 clientbound PLAY payload `apothic_spawners:config`, protocol/version `2` | provider config sync only; not a BA networking seam |
| spawner stats | 16 `apothic_spawners:spawner_stat` entries | provider is authority; no duplicate BA/RPG throughput controller |
| modifier recipes | 32 stock recipes = 16 direct + 16 inverse; operations `add` and `set` | provider/data-pack authority; no duplicate modifier engine |
| vanilla spawner runtime | 2 common mixins + block-entity factory replacement | treat loaded `minecraft:spawner` behavior as provider-owned when installed |
| persistence | NBT `stats`, `modified`, `unstable_ticks`, `captured_spawn_data` | do not mirror provider state in BA persistence |
| Capturing | kill-driven spawn-egg drop with blacklist gate | provider enchantment/drop causality; not a spell proc |
| Echoing | duplicates loot and XP according to provider spawn state | provider loot/XP causality; BA Backlash must not synthesize this path |
| mob lifecycle | blacklist, No-AI/movable handling, spawner-only despawn delay | do not double-process generic mobs based on thematic similarity |
| unstable spawner | 60-tick instability, radius 8 explosion, 12 spawn attempts, provider loot | BA uses `WorldEffectPolicy` for BA-originated world changes; provider owns reaction once legitimately triggered |
| Silk Touch / collection | provider-owned block/item/tile preservation and config | no duplicate collection/persistence settlement |
| external spawner systems | no generic authority over third-party machine/summon providers | separate provider evidence required; fail closed |

## Exact stat identities

1. `apothic_spawners:min_delay`
2. `apothic_spawners:max_delay`
3. `apothic_spawners:spawn_count`
4. `apothic_spawners:max_nearby_entities`
5. `apothic_spawners:req_player_range`
6. `apothic_spawners:spawn_range`
7. `apothic_spawners:initial_health`
8. `apothic_spawners:ignore_players`
9. `apothic_spawners:ignore_conditions`
10. `apothic_spawners:redstone_control`
11. `apothic_spawners:ignore_light`
12. `apothic_spawners:no_ai`
13. `apothic_spawners:silent`
14. `apothic_spawners:youthful`
15. `apothic_spawners:burning`
16. `apothic_spawners:echoing`

## World-effect causality rule

The provider's Nuclear Spawner path must not become a backdoor around Black Arcana world safety.

Correct causal ordering:

1. BA decides whether its own destructive action is allowed through `WorldEffectPolicy`.
2. If allowed, the world/provider receives the normal consequence.
3. If Apothic Spawners reacts to that consequence through its own hooks, the resulting instability/detonation remains provider-owned.
4. BA does not separately trigger, duplicate, suppress or re-settle that provider reaction unless a future explicit adapter contract requires it.

This preserves one cause, one provider reaction and no double processing.

## Progression boundary

RPG Skill Tree may gate or describe progression only through an explicit contract. It must not directly modify raw spawner tick loops, spawn count, delays, Echoing repetition or unstable-spawner spawn count from generic perk hooks. Any future progression integration requires bounded semantics and a causal ledger so one provider action yields one progression event.

## Authority boundary

- Apothic Spawners: spawner stats/modifiers, collection, tile persistence, Capturing/Echoing interaction, spawner-specific mob lifecycle and instability.
- Vanilla Minecraft: base `minecraft:spawner` identity, with implementation interception by the installed provider.
- Placebo: shared helper/infrastructure consumed by the provider.
- Black Arcana: canonical casting, targeting, costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and `WorldEffectPolicy`.
- RPG Skill Tree: progression only through explicit contracts.

## Fail-closed boundaries

- source/JAR byte reproducibility;
- direct publisher-file hash comparison;
- full-modpack event ordering and datapack reload;
- alternate spawner implementation compatibility;
- protection/world-policy interaction with provider explosion;
- third-party machine-spawner or summon integration;
- future provider-version changes.