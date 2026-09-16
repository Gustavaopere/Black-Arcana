# Vampirism 1.10.13 — Skill Catalog

Status: `VAMPIRE 31/31 + HUNTER 32/32 + SHARED LORD 3/3 REGISTRY ENTRIES INVENTORIADAS / TOPOLOGIA SOURCE-PINNED / RUNTIME QA PENDENTE`

Canonical source: `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`.

## Authority

`ISkillHandler` is the provider authority for:

- skill-point balance;
- parent requirements;
- sibling exclusivity inside a node;
- explicit node locks;
- tree locks;
- enable/disable;
- refinements;
- unlocked skill-tree state.

The provider exposes `canSkillBeEnabled(...)` with explicit outcomes such as `PARENT_NOT_ENABLED`, `NO_POINTS`, `OTHER_NODE_SKILL`, `LOCKED_BY_OTHER_NODE` and `LOCKED_BY_PLAYER_STATE`. Black Arcana must not reconstruct this decision tree from UI assumptions.

The first numeric argument used by the concrete `VampirismSkill` constructors is confirmed by source to be `skillPointCost`.

## Tree set

The installed provider defines four native trees:

- `vampirism:vampire/level`
- `vampirism:vampire/lord`
- `vampirism:hunter/level`
- `vampirism:hunter/lord`

The normal trees unlock from faction membership. The Lord trees unlock from the provider's Lord predicate. `FactionPlayerHandler.checkSkillTreeLocks()` is responsible for reconciling which trees are currently unlocked after level/Lord changes or respawn.

## Vampire normal tree — 29 non-root skills + root

Registry root: `vampirism:vampire` — cost 0.

The source topology is:

```text
level_root
└─ skill2: night_vision
   └─ skill3: vampire_regeneration
      └─ skill4: fledgling
         ├─ offensive1 → offensive2 → offensive3 → offensive4 → offensive5 → offensive6
         ├─ defensive1 → defensive2 → defensive3
         │                              ├─ defensive4
         │                              └─ defensive5 → defensive6 → defensive7
         └─ util1
            ├─ util2 → util3 → util4 → util5 → util6
            └─ util15
```

A `SkillNode` can contain more than one skill. Those entries are alternatives controlled by the provider's node/sibling logic; they are not automatically cumulative.

### Core chain

| Node | Skill | Cost | Provider behavior |
|---|---|---:|---|
| `level_root` | `vampire` | 0 | normal-tree root |
| `skill2` | `night_vision` | 2 | unlocks + activates provider night vision; disabling relocks it |
| `skill3` | `vampire_regeneration` | 2 | unlocks `vampirism:regen` action |
| `skill4` | `fledgling` | 2 | unlocks Bat and Infect actions |

### Offensive branch

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `offensive1` | `vampire_rage` | 2 | unlocks Rage |
| `offensive2` | `advanced_biter` | 1 | toggles provider `advanced_biter` state |
| `offensive3` | `sword_finisher` | 2 | unlocks vampire-sword finisher semantics; threshold config-driven |
| `offensive4` | `dark_blood_projectile` | 2 | unlocks Dark Blood Projectile |
| `offensive5` | `blood_charge` | 1 | provider vampire-sword/blood-charge skill gate |
| `offensive6` | `freeze` | 2 | unlocks Freeze |

### Defensive branch

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `defensive1` | `sunscreen` | 2 | unlocks Sunscreen action |
| `defensive2` | `vampire_attack_speed` **or** `vampire_speed` | 2 each | provider attribute modifier; sibling choice |
| `defensive3` | `blood_vision` | 2 | unlocks Blood Vision |
| `defensive4` | `blood_vision_garlic` | 1 | toggles garlic visibility in Blood Vision |
| `defensive5` | `vampire_attack_damage` **or** `vampire_jump` | 2 each | attack modifier or Jump action; sibling choice |
| `defensive6` | `neonatal_decrease` **or** `dbno_duration` | 2 each | modifies provider Neonatal or DBNO duration attribute; sibling choice |
| `defensive7` | `teleport` | 3 | unlocks Teleport |

### Utility branch

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `util1` | `summon_bats` | 2 | unlocks Summon Bats |
| `util2` | `less_sundamage` **or** `water_resistance` | 3 / 2 | sundamage modifier or provider water-resistance state; sibling choice |
| `util3` | `less_blood_thirst` | 1 | modifies provider `blood_exhaustion` attribute |
| `util4` | `vampire_disguise` | 1 | unlocks Vampire Disguise |
| `util5` | `half_invulnerable` | 2 | unlocks Half Invulnerable |
| `util6` | `vampire_invisibility` | 3 | unlocks Vampire Invisibility |
| `util15` | `hissing` | 1 | unlocks Hissing; direct child of `util1`, parallel to `util2→...→util6` |

### Remaining registry entries accounted for

The Vampire registry contains two roots plus all normal/Lord skills. The two Lord-only vampire-specific skills are:

- `vampire_minion_collect` — cost 2;
- `vampire_minion_stats_increase` — cost 3.

Together with the normal-tree entries above, this closes **31/31 Vampire registry entries** including roots.

## Vampire Lord tree

Registry root: `vampirism:vampire_lord` — cost 0.

Topology:

```text
lord_root
├─ lord_skill2: vampire_minion_stats_increase
├─ lord_skill3: lord_speed OR lord_attack_speed
├─ lord_skill4: vampire_minion_collect
└─ lord_skill5: minion_recovery
```

This tree is intentionally broad from the root rather than a single linear chain in `SkillTreeProvider`.

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `lord_skill2` | `vampire_minion_stats_increase` | 3 | calls `updateMinionAttributes(true/false)` on enable/disable |
| `lord_skill3` | `lord_speed` **or** `lord_attack_speed` | 1 each | shared Lord action unlock; sibling choice |
| `lord_skill4` | `vampire_minion_collect` | 2 | gates Vampire resource-collection minion behavior |
| `lord_skill5` | `minion_recovery` | 2 | shared Lord minion-recovery skill |

## Hunter normal tree — 29 non-root skills + root

Registry root: `vampirism:hunter` — cost 0.

Topology:

```text
level_root
└─ skill2: stake1
   └─ skill3: weapon_table
      └─ skill4: hunter_disguise
         ├─ alchemy1 → alchemy2 → alchemy3 → alchemy4 → alchemy5 → alchemy6
         ├─ potion1 → potion2 → potion3 → potion4 → potion5 → potion6
         └─ weapon1 → weapon2 → weapon3 → weapon4 → weapon5 → weapon6
```

### Core chain

| Node | Skill | Cost | Provider behavior |
|---|---|---:|---|
| `level_root` | `hunter` | 0 | normal-tree root |
| `skill2` | `stake1` | 2 | first stake instant-kill rule; exact eligibility config-driven |
| `skill3` | `weapon_table` | 2 | Hunter weapon-table progression gate |
| `skill4` | `hunter_disguise` | 1 | unlocks Hunter Disguise action |

### Alchemy branch

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `alchemy1` | `basic_alchemy` | 2 | base alchemy gate |
| `alchemy2` | `garlic_diffuser` | 2 | garlic-diffuser gate |
| `alchemy3` | `crucifix_wielder` | 1 | crucifix gate |
| `alchemy4` | `purified_garlic` **or** `enhanced_blessing` | 2 / 3 | sibling choice |
| `alchemy5` | `garlic_diffuser_improved` **or** `ultimate_crucifix` | 2 each | sibling choice |
| `alchemy6` | `hunter_awareness` | 2 | unlocks Awareness |

### Potion/Brewing branch

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `potion1` | `multitask_brewing` | 2 | brewing behavior gate |
| `potion2` | `durable_brewing` **or** `concentrated_brewing` | 2 each | sibling choice |
| `potion3` | `swift_brewing` **or** `efficient_brewing` | 2 each | sibling choice |
| `potion4` | `master_brewer` | 3 | advanced brewing gate |
| `potion5` | `potion_resistance` | 2 | unlocks Hunter Potion Resistance action |
| `potion6` | `concentrated_durable_brewing` | 2 | combined advanced brewing gate |

### Weapon branch

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `weapon1` | `hunter_attack_speed` **or** `hunter_attack_damage` | 2 each | vanilla attribute modifier; sibling choice |
| `weapon2` | `double_crossbow` | 1 | double-crossbow gate |
| `weapon3` | `hunter_attack_speed_advanced` **or** `enhanced_weapons` | 2 each | advanced attack-speed modifier or enhanced-weapons gate; sibling choice |
| `weapon4` | `enhanced_armor` | 2 | enhanced armor gate |
| `weapon5` | `tech_weapons` | 3 | tech weapons gate |
| `weapon6` | `stake2` | 2 | second stake instant-kill rule; exact NPC/player threshold config-driven |

### Remaining Hunter registry entries accounted for

Hunter Lord-specific skills:

- `hunter_minion_collect` — cost 2;
- `hunter_minion_stats_increase` — cost 3;
- `minion_tech_crossbows` — cost 1.

Together with roots and normal-tree entries, this closes **32/32 Hunter registry entries**.

## Hunter Lord tree

Registry root: `vampirism:hunter_lord` — cost 0.

Topology:

```text
lord_root
├─ lord_2: hunter_minion_stats_increase
│  └─ lord_6: minion_tech_crossbows
├─ lord_3: lord_speed OR lord_attack_speed
├─ lord_4: hunter_minion_collect
└─ lord_5: minion_recovery
```

| Node | Skill(s) | Cost | Provider behavior |
|---|---|---:|---|
| `lord_2` | `hunter_minion_stats_increase` | 3 | updates provider minion attributes |
| `lord_6` | `minion_tech_crossbows` | 1 | child of `lord_2`; Hunter minion equipment gate |
| `lord_3` | `lord_speed` **or** `lord_attack_speed` | 1 each | shared Lord action unlock; sibling choice |
| `lord_4` | `hunter_minion_collect` | 2 | gates Hunter collection minion behavior |
| `lord_5` | `minion_recovery` | 2 | shared Lord minion-recovery skill |

## Shared Lord skills — 3/3

The separate `LordSkills` registry contributes three shared skills usable by Lord-tagged trees:

| Registry id | Cost | Effect |
|---|---:|---|
| `vampirism:lord_speed` | 1 | unlocks shared Lord Speed action |
| `vampirism:lord_attack_speed` | 1 | unlocks shared Lord Attack Speed action |
| `vampirism:minion_recovery` | 2 | shared minion recovery skill |

These entries must not be double-counted as new faction-specific definitions merely because both Vampire and Hunter Lord trees reference them.

## Skill points

`BalanceConfig.skillPointsPerLevel` default is **2 skill points per normal level-up**. `skillPointsPerLordLevel` is a separate provider balance setting for Lord progression. The skill handler calculates current spend/availability and applies node/parent/tree gates.

Black Arcana must not create a second provider-skill point wallet unless explicitly designed as an external meta-currency that never impersonates Vampirism skill points.

## Action ↔ skill mapping

The API callback `SkillCallbacks` constructs an official action→skill map at registry-add time. `ActionSkill` contributes directly; `DefaultSkill` may also expose actions.

Important mappings in 1.10.13:

- Fledgling → Bat + Infect;
- Vampire Regeneration → Regen;
- Sunscreen → Sunscreen;
- Summon Bats → Summon Bats;
- Teleport → Teleport;
- Vampire Disguise → Disguise;
- Vampire Invisibility → Invisibility;
- Vampire Jump → Jump Boost;
- Vampire Rage → Rage;
- Dark Blood Projectile → Dark Blood Projectile;
- Freeze → Freeze;
- Half Invulnerable → Half Invulnerable;
- Hissing → Hissing;
- Hunter Awareness → Awareness;
- Hunter Disguise → Hunter Disguise;
- Potion Resistance → Hunter Potion Resistance;
- shared Lord Speed/Attack Speed skills → corresponding Lord actions.

## Integration rules

1. Read `ISkillHandler.isSkillEnabled(...)` or the provider action↔skill mapping when a perk needs a native skill gate.
2. Do not award a native skill by merely observing its downstream attribute/effect.
3. Do not infer that every skill registry entry is simultaneously obtainable; multi-skill nodes are provider-managed choices.
4. Never bypass `canSkillBeEnabled(...)` when intentionally enabling a native skill.
5. Preserve tree locks. Vampire normal, Vampire Lord, Hunter normal and Hunter Lord are separate provider progression surfaces.
6. Do not count shared Lord skills twice in capability coverage.

## Runtime QA queue

- confirm actual left-skill-point accounting at normal and Lord caps with pack config;
- verify reset/respec behavior and sibling exclusions in-game;
- verify skill-tree lock transitions at faction/Lord changes and respawn;
- verify addon injection by Bloodlines 3.0.9 before freezing any cross-provider topology assumptions;
- verify Vampire Spells Addon 0.0.9 does not add/replace Vampirism skill nodes before declaring ecosystem-wide coverage.
