# Vampiric Ageing 1.21-1.4.21 — Black Arcana integration rules

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## 1. Provider-native first

Vampiric Ageing owns Age Type, Age Method, Age Rank, progress, Hunter Tainted state and all registered Ageing Actions/Skills. Black Arcana must bridge these surfaces rather than substitute equivalent scoreboards, tags, attributes or custom counters.

## 2. Faction is a hard gate

Age Types are selected from the real Vampirism/Werewolves faction state. A Vampire-age perk must not activate for Hunter/Werewolf merely because a stale Black Arcana unlock exists. The same applies to Hunter/Werewolf-specific effects after faction loss or conversion.

Revalidate on login/relog, faction-level change, death/reset and any provider sync transition relevant to the perk.

## 3. Rank and progression use `AgeingManager`

Use provider Age Rank and current Age Method. Do not reconstruct them from faction level, played time, kill count, blood-bar changes, visible attributes or titles.

Do not carry progression overflow across provider rank-ups: the audited provider resets progress to zero.

## 4. Tainted Age is provider-derived

Hunter cumulative Tainted Age must use the provider semantics. It is not equivalent to base Hunter Age while Tainted state is inactive. Teleport and Limited Bat Mode specifically use cumulative Tainted Age; Tainted access, Step Assist and Wise Eye use base Hunter Age.

## 5. Skill gates remain provider-owned

The 10 Ageing Skills are enabled/disabled by the provider's faction Skill handlers. Black Arcana must not charge its own extra provider-skill points for them or force-enable them independently.

Werewolf Improved Senses preserves the compound default gate: Age >= 5 plus Werewolves `SENSE` when the config requires it.

## 6. Action lifecycle remains provider-owned

For all nine Actions, the TeamLapen Action handler remains authority for:

- availability;
- activation success/failure;
- active state;
- duration;
- cooldown;
- deactivation/cleanup.

A Black Arcana perk may observe an Action or require it as a prerequisite, but should not duplicate provider lifecycle.

## 7. Settlement deduplication

### Blood Tap

Do not award blood in a second hit hook. The provider settles target bite state and invokes `VampirePlayer.drinkBlood(...)` itself.

### Movement/flight

Do not apply a second teleport, flight permission, Step Height bonus, Water Walking state or movement-speed modifier for the same provider Action.

### Invisibility bypass

Wise Eye / Improved Senses set the provider cache flag and own slowdown cleanup. Do not maintain another invisibility-bypass flag for the same Action.

## 8. Damage hooks must preserve provider ordering

Vampiric Ageing can alter incoming Vampire weaknesses, hunter-mob damage, starvation damage and optional lethal-damage handling. A Black Arcana damage perk must operate in a clearly defined pipeline stage and must not blindly recompute damage from pre-provider values.

For optional immortality, a perk depending on an actual death event should only settle after the provider has allowed death to occur.

## 9. Attribute modifiers are provider-owned

Age Types reconcile transient rank-based attributes. Several Actions add/remove their own modifier IDs. Black Arcana should not clone those modifiers under new IDs, because that creates stacking and cleanup divergence.

## 10. Configuration is server authority

Thresholds, unlock Age, cooldowns, durations and multipliers are configurable. The defaults recorded in this catalog are not immutable protocol constants.

If a perk contract requires a threshold, resolve the current provider config/state through a supported hook or fail closed. Do not hardcode default Age 4, 35 blocks, 150 s, etc. as if they were universal.

## 11. Static mismatches are fail-closed for exact-timing contracts

The known source mismatches in `TECHNICAL-AUDIT.md` prevent exact-timing or exact-multiplier claims for affected Actions until runtime QA:

- Wise Eye duration;
- Step Assist cooldown units;
- Wise Eye / Improved Senses cooldown units;
- Celerity effective speed;
- Limited Bat dimension transition behavior;
- Werewolf start-level config divergence.

## 12. Optional Werewolves dependency

Code touching Werewolves classes/surfaces must remain loader-gated. Black Arcana currently installs Werewolves, but the bridge should not cause classloading failure if that optional dependency is absent in another environment unless Black Arcana explicitly makes it required.

## 13. Dedicated-server authority

Movement/teleport/flight integrations must be tested on dedicated server before approval. Client-visible success is insufficient evidence for Hunter Teleport or Limited Bat Mode compatibility with the broader Black Arcana movement stack.

## 14. Perk contract checklist

Before approving a perk that uses Vampiric Ageing, record:

- required faction/Age Type;
- base Age vs cumulative Tainted Age;
- required Age Method, if any;
- required provider Skill/Action;
- current-config gate source;
- settlement authority;
- damage/movement pipeline position;
- dedup key/source event;
- death/faction-change invalidation;
- optional Werewolves gate;
- fallback/fail-closed behavior;
- exact runtime tests from `TECHNICAL-AUDIT.md` that must pass.
