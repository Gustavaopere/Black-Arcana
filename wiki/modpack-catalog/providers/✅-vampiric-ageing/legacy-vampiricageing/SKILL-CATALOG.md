# Vampiric Ageing 1.21-1.4.21 — skill catalog

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

All entries below are registered in `VampirismRegistries.Keys.SKILL`. They are not a separate purchasable Vampiric Ageing skill tree: the Age Types call the provider skill handlers and enable/disable these nodes according to Age Rank / cumulative Tainted Age and optional provider gates.

## Inventory — 10/10 with Werewolves installed

### Vampire — 4

| Skill ID | Action | Default unlock authority |
|---|---|---|
| `vampiricageing:celerity_skill` | `vampiricageing:celerity_action` | Vampire Age >= 1 |
| `vampiricageing:blood_drain_skill` | `vampiricageing:drain_blood_action` | Vampire Age >= 3 |
| `vampiricageing:water_walking_skill` | `vampiricageing:water_walking_action` | Vampire Age >= 4 |
| `vampiricageing:step_assist_skill` | `vampiricageing:step_assist_action` | Vampire Age >= 2 |

All four are registered against `VampireSkills.Trees.LEVEL` with zero skill cost / provider-controlled enablement semantics.

### Hunter — 5

| Skill ID | Action | Default unlock authority |
|---|---|---|
| `vampiricageing:hunter_teleport_skill` | `vampiricageing:hunter_teleport_action` | cumulative Tainted Age >= 8 |
| `vampiricageing:limited_bat_mode_skill` | `vampiricageing:limited_hunter_batmode_action` | cumulative Tainted Age >= 10 |
| `vampiricageing:tainted_blood_skill` | none; `SimpleHunterSkill` | base Hunter Age >= 2 |
| `vampiricageing:step_assist_hunter_skill` | `vampiricageing:step_assist_hunter_action` | base Hunter Age >= 4 |
| `vampiricageing:wise_eye_skill` | `vampiricageing:hunter_wise_eye_action` | base Hunter Age >= 5 |

Hunter Teleport and Limited Bat Mode are intentionally gated by `CapabilityHelper.getCumulativeTaintedAge(...)`, not by base age alone. Step Assist, Wise Eye and access to Tainted Blood use base Hunter Age.

### Werewolf — 1 conditional skill

| Skill ID | Action | Default unlock authority |
|---|---|---|
| `vampiricageing:improved_senses_skill` | `vampiricageing:improved_senses_action` | Werewolf Age >= 5 **and**, by default, Werewolves `SENSE` skill enabled |

The skill/action registry exists only when the `werewolves` mod is loaded. Black Arcana currently has Werewolves installed, so this surface is present.

## Provider-owned reconciliation

`AgeingManager.onAgeChange(...)` invokes the current `IAgeType.handleSkills(...)`. Each type directly reconciles the corresponding Vampirism/Werewolves `ISkillHandler` by enabling or disabling these nodes. Black Arcana must therefore treat the provider skill handler as the enabled-state authority and must not grant equivalent parallel abilities when the provider skill is disabled.

## Integration rule

A Black Arcana perk may use one of these skills as a gate/observation point only when the provider relationship is preserved:

- base faction must be valid;
- Age Type/Rank or cumulative Tainted Age must be provider-derived;
- compound Werewolf `SENSE` gate must remain intact;
- Action settlement remains provider-owned;
- no extra skill point must be charged by Black Arcana for an Ageing skill that the provider unlocks automatically.
