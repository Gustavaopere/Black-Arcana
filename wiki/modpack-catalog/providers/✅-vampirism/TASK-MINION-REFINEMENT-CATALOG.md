# Vampirism 1.10.13 — Tasks, Minions and Refinements

Status: `TASK KEYS 46/46 + ENTITY ACTIONS 10/10 + MINION TASKS 7/7 + REFINEMENTS 47/47 SOURCE-PINNED / RUNTIME QA PENDENTE`

Canonical source: `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`.

## Provider Task system

Vampirism registers its own task unlockers, requirement codecs, rewards and reward instances. Task progress/reward is therefore a native progression surface, not a generic quest wrapper.

Registered requirement categories include:

- boolean;
- entity;
- entity tag;
- item;
- stat.

Registered unlocker categories include:

- Lord level;
- faction level;
- parent task.

Registered rewards include:

- item;
- Lord level;
- refinement;
- provider consumer callback.

### 46 task keys inventoried

#### Vampire Lord — 5

- `vampire_lord1`
- `vampire_lord2`
- `vampire_lord3`
- `vampire_lord4`
- `vampire_lord5`

These are the authoritative Vampire Lord 1–5 progression and are detailed in `PROGRESSION.md`.

#### Vampire minion — 4

- `vampire_minion_binding`
- `vampire_minion_upgrade_simple`
- `vampire_minion_upgrade_enhanced`
- `vampire_minion_upgrade_special`

Source requirements:

| Task | Unlock | Requirements | Reward |
|---|---|---|---|
| binding | Lord ≥1 | Advanced Hunter tag ×4; Vampire Baron ×5; Gold ×32 | Vampire Minion Binding |
| simple | Lord ≥2 | Advanced Hunter tag ×8; Gold Block ×16 | Simple Vampire Minion Upgrade |
| enhanced | Lord ≥3 | Vampire Baron ×10; Human Heart ×32; Vampire Book ×1; Diamond Block ×3 | Enhanced Vampire Minion Upgrade |
| special | Lord ≥5 | Vampire Baron ×20; Human Heart ×64; Vampire Book ×1; Diamond Block ×8 | Special Vampire Minion Upgrade |

#### Vampire recurring/utility tasks — 14

- `random_refinement1`
- `random_refinement2`
- `random_refinement3`
- `random_rare_refinement`
- `fire_resistance1`
- `fire_resistance2`
- `feeding_adapter`
- `v_infect1`
- `v_infect2`
- `v_infect3`
- `v_capture1`
- `v_capture2`
- `v_kill1`
- `v_kill2`

Notable exact definitions:

- Feeding Adapter: level ≥4; Advanced Hunter tag ×10 + Gold ×5 → Feeding Adapter.
- Fire Resistance 1: Magma Cream ×3 + Hunter tag ×10 → Vampire Fire Resistance potion.
- Fire Resistance 2: level ≥7; Magma Cream ×5 + Hunter tag ×15 → long Vampire Fire Resistance potion.
- `v_infect1/2/3`: provider infected-creatures stat thresholds 20 / 25 / 15 with Gold 5 / Gold 15 / Iron 5 rewards respectively.
- `v_capture1/2`: provider capture-village stat ×1, rewarding Emerald ×10 / ×5.
- `v_kill1`: Hunter entity-tag requirement ×10 → Human Heart ×5.
- `v_kill2`: Advanced Hunter entity-tag requirement ×4 → Human Heart ×8.
- Random Refinement 1: Advanced Hunter tag ×10 + Gold ×2 → random Vampire refinement.
- Random Refinement 2: Vampire Baron ×3 + Gold ×2 → random Vampire refinement.
- Random Refinement 3: vanilla `TRADED_WITH_VILLAGER` stat ×15 + Gold ×2 → random Vampire refinement.
- Random Rare Refinement: vanilla `RAID_WIN` stat ×1 → random **rare** Vampire refinement.

#### Hunter Lord — 5

- `hunter_lord1`
- `hunter_lord2`
- `hunter_lord3`
- `hunter_lord4`
- `hunter_lord5`

These are the authoritative Hunter Lord 1–5 progression and are detailed in `PROGRESSION.md`.

#### Hunter minion — 4

- `hunter_minion_equipment`
- `hunter_minion_upgrade_simple`
- `hunter_minion_upgrade_enhanced`
- `hunter_minion_upgrade_special`

Source requirements:

| Task | Unlock | Requirements | Reward |
|---|---|---|---|
| equipment | Lord ≥1 | Advanced Vampire tag ×4; Vampire Baron ×5; Gold ×32 | Hunter Minion Equipment |
| simple | Lord ≥2 | Advanced Vampire tag ×8; Gold Block ×16 | Simple Hunter Minion Upgrade |
| enhanced | Lord ≥3 | Vampire Baron ×10; Vampire Blood Bottle ×16; Vampire Book ×1; Diamond Block ×3 | Enhanced Hunter Minion Upgrade |
| special | Lord ≥5 | Vampire Baron ×20; Vampire Blood Bottle ×32; Vampire Book ×1; Diamond Block ×8 | Special Hunter Minion Upgrade |

#### Hunter recurring tasks — 3

- `h_kill1`: Vampire entity-tag requirement ×20 → Diamond ×2.
- `h_kill2`: Vampire entity-tag requirement ×15 → Diamond ×2.
- `h_capture1`: provider capture-village stat ×2 → Vampire Blood Bottle ×10.

#### Cross-faction/general tasks — 11

- `oblivion_potion`
- `oblivion_potion_pure_blood_1`
- `oblivion_potion_pure_blood_2`
- `oblivion_potion_pure_blood_3`
- `oblivion_potion_pure_blood_4`
- `oblivion_potion_pure_blood_5`
- `break_bones1`
- `break_bones2`
- `break_bones3`
- `break_bones4`
- `totem_top`

Exact notable paths:

- base Oblivion Potion: Poison potion + Vampire Blood Bottle → Oblivion Potion;
- level-range Oblivion alternatives use Pure Blood tiers 0–4 for faction level ranges 1–3, 4–6, 7–9, 10–12 and 13–14;
- Break Bones 1–4 use Skeleton entity requirements 20/14/10/10 and reward the four Chainmail armor pieces;
- Totem Top: level ≥5; Obsidian ×32 + Diamond ×1 + Zombies-tag requirement ×32 → crafted Totem Top.

### Task counter caution

The static task definitions identify whether a requirement is an entity/entity-tag/stat/item requirement. Black Arcana must consume the provider task runtime/state rather than inventing its own interpretation of when those counters advance.

## NPC Entity Actions — 10/10

These are actions for Vampirism entities, separate from player `IAction` abilities.

| Registry id | Tier | Entity class affinity | Core semantics |
|---|---|---|---|
| `entity_invisible` | Medium | Assassin | invisibility behavior |
| `entity_heal` | High | Fighter | direct healing; provider comment states healing is preferred over regeneration |
| `entity_regeneration_areaofeffect` | Medium | Support | regeneration AoE |
| `entity_regeneration` | Medium | Fighter | self/target regeneration behavior |
| `entity_speed` | Medium | Assassin, Fighter | speed behavior |
| `entity_bat_spawn` | Medium | Caster | bat spawning |
| `entity_dark_projectile` | High | Caster | dark projectile attack |
| `entity_sunscreen` | Medium | Tank | sunscreen behavior |
| `entity_garlic_areaofeffect` | High | Caster | garlic AoE Hunter behavior |
| `entity_ignoresundamage` | High | Fighter | temporary sun-damage bypass |

These must not be counted as player spell casts merely because some names parallel player actions.

## Minion Tasks — 7/7

Registered ids:

1. `stay`
2. `defend_area`
3. `follow_lord`
4. `collect_hunter_items`
5. `collect_blood`
6. `nothing`
7. `protect_lord`

### `collect_hunter_items`

Faction: Hunter.

Gate: `hunter_minion_collect` skill.

Default base resource cooldown: `miResourceCooldown = 1500 ticks`.

Hunter minion resource efficiency reduces that cooldown by up to 40% at maximum resource-efficiency level.

Weighted output table in source:

| Output stack | Weight |
|---|---:|
| Garlic Bread ×10 | 10 |
| Iron Nugget ×19 | 25 |
| Gold Nugget ×7 | 10 |
| Garlic ×2 | 15 |
| Coal ×5 | 20 |

### `collect_blood`

Faction: Vampire.

Gate: `vampire_minion_collect` skill.

Default resource cooldown: `miResourceCooldown = 1500 ticks`.

Weighted output table:

| Output stack | Weight |
|---|---:|
| provider Blood Bottle filled to `BloodBottleItem.AMOUNT` (9 blood units) | 20 |
| Human Heart ×1 | 5 |
| Iron Nugget ×12 | 12 |
| Gold Nugget ×6 | 10 |

This is a confirmed provider-native automated blood source. A Black Arcana servant/farm feature producing the same resource needs explicit deduplication and balance rationale.

### Offline production

`miResourceCooldownOfflineMult` default is **20×**. Runtime QA is required before making guarantees about exact offline settlement/persistence after the 1.10.13 MinionTask persistence fix.

## Refinements — 47/47

Refinements are a separate provider customization layer. `ISkillHandler` owns equipped refinement items and `isRefinementEquipped(...)` state.

### Attribute refinements — 30

Five stat families, each with three positive and three detrimental variants.

#### Armor

- `armor1`: +0.3 Armor
- `armor2`: +0.5 Armor
- `armor3`: +1 Armor
- `n_armor1`: −1 Armor
- `n_armor2`: −2 Armor
- `n_armor3`: −3 Armor

Operation: `ADD_VALUE`.

#### Movement speed

- `speed1`: +0.025 base multiplier
- `speed2`: +0.05
- `speed3`: +0.075
- `n_speed1`: −0.025
- `n_speed2`: −0.05
- `n_speed3`: −0.075

Operation: `ADD_MULTIPLIED_BASE`.

#### Max health

- `health1`: +0.5
- `health2`: +1
- `health3`: +1.5
- `n_health1`: −1
- `n_health2`: −2
- `n_health3`: −3

Operation: `ADD_VALUE`.

#### Attack damage

- `damage1`: +0.15
- `damage2`: +0.3
- `damage3`: +0.5
- `n_damage1`: −0.15
- `n_damage2`: −0.3
- `n_damage3`: −0.5

Operation: `ADD_VALUE`.

#### Attack speed

- `attack_speed1`: +0.03 base multiplier
- `attack_speed2`: +0.08
- `attack_speed3`: +0.11
- `n_attack_speed1`: −0.05
- `n_attack_speed2`: −0.10
- `n_attack_speed3`: −0.15

Operation: `ADD_MULTIPLIED_BASE`.

### Specialized refinements — 17

1. `half_invulnerable`
2. `teleport_distance`
3. `sword_finisher`
4. `summon_bats`
5. `rage_fury`
6. `regeneration`
7. `sun_screen`
8. `dark_blood_projectile_penetration`
9. `dark_blood_projectile_multi_shot`
10. `dark_blood_projectile_aoe`
11. `dark_blood_projectile_damage`
12. `dark_blood_projectile_speed`
13. `vista`
14. `freeze_duration`
15. `blood_charge_speed`
16. `sword_trained_amount`
17. `crucifix_resistant`

These do not all encode their final numeric effect in the registry declaration; many are queried by the specific action/item/player logic and use balance-config multipliers. Therefore their existence is cataloged here while exact runtime deltas remain tied to the consuming source path/config.

## Refinement causal examples

- `summon_bats` changes Summon Bats targeting/count/cooldown behavior.
- `half_invulnerable` changes the damage threshold used before a hit is blocked.
- `teleport_distance` changes Teleport distance/cooldown calculations.
- `regeneration` increases provider Regen action amplifier.
- `sun_screen` multiplies Sunscreen duration.
- Dark Blood Projectile has separate penetration, multishot, AoE, damage and speed refinements.
- `freeze_duration` modifies Freeze duration.
- `blood_charge_speed` changes Vampire Sword blood-charge behavior.

Black Arcana must read provider refinement state rather than duplicating these as independent passive flags.

## Deduplication and authority rules

1. Provider Task reward and an external quest reward may coexist only if they have different identities; do not re-award the native reward.
2. Lord level remains settled by `LordLevelReward`.
3. Entity Actions are NPC behavior, not player casts.
4. Minion Tasks are provider-owned work orders; generated resources should receive a minion-task causal identity if mirrored into telemetry.
5. `collect_blood` is already a blood automation mechanic.
6. Refinements are provider equipment/progression state and must not be inferred from equivalent attribute values.
7. A negative refinement is intentional provider state; generic stat-normalization code must not silently erase it.

## Runtime QA queue

- task requirement counter semantics for entity/entity-tag requirements;
- task expiration/duration in singleplayer vs dedicated server;
- reward claim idempotency;
- random refinement rarity distribution;
- refinement damage-on-death/equip persistence;
- 1.10.13 MinionTask persistence;
- offline resource production multiplier;
- minion resource-efficiency cooldown reduction;
- NPC Entity Action selection/tier behavior;
- addon injection from Bloodlines into task/minion/refinement registries.
