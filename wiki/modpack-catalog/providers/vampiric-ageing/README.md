# Vampiric Ageing 1.4.21 — provider audit

Status: `SOURCE-PINNED 1.4.21 / CORE AGEING + ACTIONS + TAINTED BLOOD + WEREWOLF INTEROP CATALOGED / RUNTIME QA PENDING`

## Version authority

- mod id: `vampiricageing`
- installed JAR: `vampiricageing-1.21-1.4.21.jar`
- installed/runtime version: `1.21-1.4.21`
- Minecraft: `1.21.1`
- loader: NeoForge
- base provider: Vampirism `1.10.13` in the current pack
- optional provider active in the current pack: Werewolves `2.0.3.3`
- official source: `TheDrOfDoctoring/Vampiric-Ageing`
- exact source pin: `16049e9aeadc47b2307995901c373521cef5fd76`

The selected commit is the exact 1.4.21 source line: its `gradle.properties` declares `mod_version=1.21-1.4.21`, and the official NeoForge 1.21.1 release artifact is the installed build.

## What this provider is

Vampiric Ageing is a progression/RPG addon over Vampirism, with optional Werewolves integration. It does not introduce a spell engine. Its primary authority is an `AgeingManager` attachment that tracks an Age Type, Age Rank, rank progress and optional type-specific state, then grants/modifies provider-native Vampirism/Werewolves skills, actions, attributes and faction mechanics.

In the current pack, three Age Types are registered:

| Age Type | Base faction | Max normal Age Rank | Default starting faction level |
|---|---|---:|---:|
| `VAMPIRE` | Vampirism Vampire | 5 | 14 |
| `HUNTER` | Vampirism Hunter | 5 | 14 |
| `WEREWOLF` | Werewolves | 5 | 14 |

Werewolf registration is conditional on the `werewolves` mod being loaded; that condition is satisfied by the current modlist.

## Source inventory confirmed

| Surface | Confirmed current count |
|---|---:|
| Age Types active in this pack | **3** |
| Ageing Methods registered in this pack | **8** |
| `IAction` registrations | **9** |
| `ISkill` registrations | **10** |
| Own item registrations | **4** |
| Own mob-effect registrations | **1** (`tainted_blood`) |
| Own oil registrations | **1** (`seniority`) |
| Serialized AgeingManager attachment | **1** |

The 9 actions are eight entries in `VampiricAgeingActions` plus `improved_senses_action`, which is registered through `WerewolfAgeingSkills` only when Werewolves support is active.

## Provider-native authority

### AgeingManager

`AgeingManager` is a serialized NeoForge attachment registered with `copyOnDeath()` and synchronized through TeamLapen's attachment sync infrastructure. It persists, for players:

- `ageing_rank`;
- `ageing_type`;
- `ageing_rank_progress`;
- type-specific serialized state when the Age Type exposes one.

Hunter adds `HunterState`, which persists temporary Tainted Age, Tainted duration, accumulated sun exposure and permanent-transformation state.

Black Arcana must not persist a second authoritative age/rank/progress state.

### Rank settlement

Normal Age Rank is capped at 5 by `AgeingManager.canAge()`. A rank-up is provider-owned:

1. the selected `IAgeMethod` credits rank progress;
2. the player must satisfy faction-level and optional Lord-level gates;
3. reaching the configured threshold increments Age Rank by exactly one;
4. rank progress is reset to zero rather than carrying overflow;
5. the manager synchronizes state;
6. Age Type lifecycle reapplies attributes and enables/disables the provider's age-granted skills.

### Faction lifecycle

Age Type follows the current playable faction. Losing/changing faction clears the old type/rank/progress and reselects the valid Age Type/method. Hunter Tainted Blood state is additionally cleaned when leaving Hunter faction.

This lifecycle must be observed, not emulated by changing only a number or tag.

## Default progression methods

### Vampire

Default method: `DRAINING` (`DrinkBloodMethod`).

Default BloodDrink progress thresholds: **150 / 300 / 600 / 900 / 1250** for Age 0→1 through Age 4→5. Only entity-backed `PlayerDrinkBloodEvent` settlements are credited by the audited handler.

Alternative provider-native methods available through config:

- `BITING`: successful eligible Infect/Biting progression, thresholds **30 / 45 / 70 / 100 / 200**;
- `TIME`: **72,000 / 144,000 / 288,000 / 576,000 / 1,152,000 ticks**;
- `V_HUNTING`: tagged kills, thresholds **20 / 40 / 80 / 160 / 250 points**, with default petty/common/greater values 1/3/5.

Optional Sire progression is a separate provider mechanic and is disabled by default.

### Hunter

Default method: `HUNTING`.

Default thresholds: **20 / 40 / 80 / 160 / 250 points**. Tagged kills award default petty/common/greater values **1 / 3 / 5**.

### Werewolf

Default method: `DEVOUR`, which only credits qualifying kills through the Werewolves Bite damage path. Default thresholds: **30 / 60 / 100 / 250 / 500 points**. Petty/common/greater/exquisite devour values are **1 / 2 / 5 / 10**.

Alternatives:

- `W_HUNTING`: any qualifying tagged kill, thresholds 20/40/80/160/250, worth 1/3/5;
- `W_MIXED`: bite kills use devour categories and other qualifying kills use hunting categories.

## Default age-granted actions/skills

### Vampire

- Age 1: Celerity action/skill;
- Age 2: Step Assist action/skill;
- Age 3: Blood Tap action/skill;
- Age 4: Water Walking action/skill.

### Hunter

- Age 2: Tainted Blood skill / crafting-use gate;
- Age 4: Hunter Step Assist;
- Age 5: Wise Eye;
- cumulative Tainted Age 8: Hunter Teleport;
- cumulative Tainted Age 10: Limited Bat Mode.

### Werewolf

- Age 5: Improved Senses action/skill, by default also requiring Werewolves' native `SENSE` skill.

## High-impact source findings / QA gates

1. **Celerity's configured amount is `1.025` with `ADD_MULTIPLIED_TOTAL`.** Under vanilla attribute operation semantics this is not merely a +2.5% amount; runtime behavior must be verified before Black Arcana displays or balances it as such.
2. **Vampire DBNO and neonatal modifiers use `ADD_MULTIPLIED_BASE` with positive config values whose comments describe shorter durations.** Treat the resulting runtime direction/magnitude as QA-gated rather than normalizing the prose.
3. **Step Assist Vampire/Hunter cooldown getters return the config value without `×20`.** Defaults are zero, so non-zero custom values have an unresolved unit contract.
4. **Hunter Wise Eye returns `wiseEyeCooldown` without `×20` and uses `stepAssistDuration`, not `wiseEyeDuration`, for its duration.** Default `wiseEyeDuration=120` exists in config but is not used by the audited action implementation.
5. **Werewolf Improved Senses returns `improvedSensesCooldown` without `×20`; duration does convert to ticks.**
6. **Age rank progress overflow is discarded on rank-up.** External systems must not independently retain or settle overflow unless deliberately redesigned.
7. **Blood Tap performs its blood settlement from the incoming-damage hook, not from action activation.** It calls Vampirism bite/blood APIs and `VampirePlayer.drinkBlood`; no second Black Arcana blood credit is allowed.
8. **Tainted Blood is Hunter state, not Vampirism Vampire blood.** Its cumulative age is `Hunter Age + temporary bottle bonus`, or `Hunter Age + 6` after permanent transformation.
9. **Garlic Injection clears both temporary Tainted Blood and permanent transformation in the audited handler.**
10. **Limited Hunter Bat Mode directly mutates flight/pose/dimensions and blocks attacks, mounting, block interaction, item use and block placement while active.** Dedicated-server/client reconciliation is mandatory before any integration relies on this state.
11. **Werewolf mechanics are provider overlays on Werewolves' Bite/Howl/Form/Sense pipelines.** Do not duplicate the underlying action or food settlement.
12. **Death reset is enabled by default.** With default `ageLostOnDeath=0`, normal player death resets Age to 0; optional partial rank loss is config-driven. Permanent Tainted transformation has a separate death-reset toggle, default false.
13. **Optional high-age vampire immortality is disabled by default.** It intercepts lethal non-killing-source damage at LOWEST priority and can optionally settle blood loss through the real Vampirism blood bar; it must not be pre-charged or independently resurrected by Black Arcana.

## Documents

- [`PROGRESSION-CATALOG.md`](./PROGRESSION-CATALOG.md) — Age Types, methods, ranks, attributes and progression settlement.
- [`ACTION-CATALOG.md`](./ACTION-CATALOG.md) — all 9 registered actions and their gates/default contracts.
- [`TAINTED-BLOOD-AND-WEREWOLVES.md`](./TAINTED-BLOOD-AND-WEREWOLVES.md) — Hunter cumulative Tainted Age and Werewolves overlays.
- [`TECHNICAL-AUDIT.md`](./TECHNICAL-AUDIT.md) — attachment, lifecycle, event/mixin surfaces and static discrepancies.
- [`INTEGRATION-RULES.md`](./INTEGRATION-RULES.md) — Black Arcana authority/settlement contract.

## Closure state

The installed 1.4.21 source line is pinned and the provider's core Age Types, Ageing Methods, registered actions/skills, Tainted Blood system, Werewolves overlays, major config defaults and integration boundaries are cataloged.

Do **not** mark `RUNTIME QA CONFIRMED`. Runtime validation remains required for action timing units, Celerity magnitude, DBNO/neonatal modifier direction, Bat Mode synchronization, Tainted state lifecycle and mixin compatibility against the exact installed Vampirism/Werewolves versions.