# Werewolves 2.0.3.3 — technical audit

## Source authority

- Installed artifact: `Werewolves-1.21-2.0.3.3.jar`.
- Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.
- Source version fields: 2.0.3.3.
- Declared Vampirism range: `[1.10.0-beta.2,1.11.0)`; installed Vampirism 1.10.13 lies inside that range.

This document records static source evidence. It does not claim byte-for-byte installed-JAR validation or runtime confirmation.

## Architecture summary

Werewolves is tightly integrated with Vampirism registries and infrastructure:

- playable faction via `VampirismAPI.factionRegistry()`;
- Vampirism `FactionPlayerHandler` for faction/level authority;
- Vampirism ACTION/SKILL/TASK/REFINEMENT/MINION_TASK registries;
- Vampirism `ActionHandler` and `SkillHandler` for player state;
- Vampirism task/Lord/minion/refinement systems;
- NeoForge player attachment for `WerewolfPlayer`;
- custom provider attributes, effects, packets, events, mixins and world state.

Black Arcana should integrate with provider state rather than creating parallel abstractions where native authority already exists.

## Static mismatches / QA blockers

### WW-QA-01 — Howling AABB inflation result is discarded

`HowlingAction.applyHowling()` constructs an AABB and then calls `bb.inflate(10)` without assigning the returned AABB. Minecraft `AABB` operations are immutable-style and return a new box. The intended 10-block Werewolf buff aura therefore cannot be assumed from source intent alone.

Required QA: measure which nearby Werewolves actually receive `HOWLING` in the installed JAR.

### WW-QA-02 — Howling attack-speed config vs hard-coded effect

Balance config exposes `howling_attackspeed_amount = 2.0`, but `HowlingEffect` hard-codes `+0.5 ADD_MULTIPLIED_TOTAL` and does not read the config in the inspected path.

Required QA: verify effective installed attribute delta; do not silently substitute 2.0.

### WW-QA-03 — Howling duration vs disabled-duration semantics

`HowlingAction` creates one `HOWLING` effect instance for `(howling_duration + howling_disabled_duration)` seconds, default 20 seconds. `HowlingEffect` attaches its attack-speed modifier to the effect itself. No inspected source split removes the buff for the final `disabled_duration` portion.

Required QA: determine whether the effective buff lasts the full 20 seconds or another hook modifies it.

### WW-QA-04 — Sense cooldown unit mismatch

`SenseWerewolfAction.getDuration()` returns `sense_duration * 20`, but `getCooldown()` returns:

`sense_cooldown + sense_duration * 20`

rather than `(sense_cooldown + sense_duration) * 20` or `sense_cooldown * 20`.

With defaults, source returns `90 + 600 = 690` ticks if the action framework expects ticks.

Required QA: measure effective cooldown; do not advertise 90 seconds solely from config label.

### WW-QA-05 — Sense radius config not used by inspected renderer

Config defines `sense_radius = 25`, but `RenderHandler` filters outlined entities using Vampirism `vsBloodVisionDistanceSq` instead. No use of `sense_radius` was located in the inspected vision path.

Required QA: measure effective visual radius and verify whether another hook consumes the Werewolves config.

### WW-QA-06 — level armor-toughness call uses speed config

`WerewolfPlayer.onLevelChanged()` applies its Armor Toughness level modifier using `werewolf_speed_amount`, despite a separate `werewolf_armor_toughness` config field.

Required QA: verify effective toughness scaling and preserve provider result.

### WW-QA-07 — Health Reg config not consumed by active path

`health_reg_modifier = 0.2` exists, but the located `HEALTH_REG` consumer simply advances the internal `FoodData` tick timer by one extra tick. No use of `health_reg_modifier` was found.

Required QA: measure actual health/hunger regeneration acceleration.

### WW-QA-08 — `resistance` registered but not connected

`werewolves:resistance` is registered, has language/config data, but:

- no generated normal/Lord skill-tree node grants it;
- no direct `ModSkills.RESISTANCE` consumer was located.

Status: fail-closed/unreachable until additional runtime/datapack evidence exists.

### WW-QA-09 — `sixth_sense` functional consumer but no generated tree path

`werewolves:sixth_sense` has a real target-change consumer that sends a client packet when mobs acquire the Werewolf player, but no generated normal/Lord tree node grants it.

Status: functional registration, survival reachability unproven.

### WW-QA-10 — `no_leap_cooldown` refinement has no located set/acquisition path

The refinement is registered and consumed by Leap, but exact-source search located no `RefinementSet` or other ordinary acquisition reference.

Status: functional registration, survival reachability unproven.

### WW-QA-11 — refinement-set name/body mismatch

Set ID `damage3_n_armor1` is constructed with Vampirism `N_ARMOR_2` in source.

Required QA: implementation/JAR behavior is authority; do not infer from ID name.

### WW-QA-12 — bite cooldown duplicate configs

Actual `WerewolfPlayer.bite()` sets `biteTicks` from `BALANCE.PLAYER.bite_cooldown` (default 200 ticks). A separate `BALANCE.SKILLS.bite_cooldown` default 5 seconds exists but was not found in that transaction.

Required QA: measure player bite availability and use provider state as source of truth.

### WW-QA-13 — post-bite feeding predicate is narrow/unusual

`eatEntity()` returns immediately unless `Helper.isNoLiving(entity)` is true; that helper is true for inverted-heal/harm entities or Vampires. It then feeds only if the entity is dead. This is much narrower than a generic “bite feeds from victim” interpretation.

Required QA: do not grant food/heal perks from every bite unless provider outcome confirms it.

### WW-QA-14 — Health After Kill timing is unusual

Provider kill handler applies Regeneration amplifier 10 for duration 4 ticks, or 5 ticks with refinement, while also adding 0.5 saturation on eligible kills.

Required QA: measure actual health gain with vanilla effect ticking and installed stack; do not normalize to a conventional long regeneration buff.

### WW-QA-15 — form synchronization deserves runtime verification

Form state is stored/synced through provider attachments/action lifecycle, player dimensions, inventory swaps and client rendering. Because Epic Fight interaction is already a documented pack risk, direct NBT/action/render consistency should be tested through login, dimension change, death and battle/mining mode changes.

## Epic Fight boundary

Notion/current project audit records a known upstream visual incompatibility risk between Werewolves and Epic Fight. Installed Epic Fight includes Werewolves/Vampirism-specific compat mixins, but that is evidence of attempted mitigation, not proof of complete compatibility.

Runtime QA must cover:

- Human/Beast/Survivalist visuals;
- hitboxes/dimensions;
- attack animations;
- bite input;
- Leap/jump;
- battle ↔ mining mode transitions;
- death/respawn;
- full moon forced transformation;
- armor/inventory swaps.

## World boundary

Registry key `werewolves:werewolf_heaven` is an Overworld biome whose display name is Werewolf Forest. Do not document it as a separate dimension.

## Dedicated-server QA matrix

1. join faction through Lupus Sanguinem exactly once;
2. cure through injection + Med Chair and final Un Werewolf tick;
3. levels 2–14: progress, altar gates, start consumption, completion settlement;
4. action registry availability and skill gates;
5. all three player forms day/night/full-moon behavior;
6. transformation-time use/regain/refinements;
7. bite damage/cooldown/stun/bleeding/infection;
8. Silver Blooded and all silver application paths;
9. Wolfsbane world application;
10. form damage reduction ordering;
11. Sense shader/radius/cooldown;
12. Howling aura/buff/Wolf Pack;
13. Fear pathing;
14. Leap state and landing cleanup;
15. Digger/Enhanced Digger tiers/drops;
16. Lord tasks 1–5;
17. minion binding/upgrades/tasks/collection;
18. refinement acquisition including unreachable candidates;
19. Werewolf Forest worldgen;
20. Epic Fight compatibility.

## Audit conclusion

`SOURCE SURFACE SUBSTANTIALLY COMPLETE / STATIC MISMATCHES DOCUMENTED / SURVIVAL REACHABILITY EXCEPTIONS IDENTIFIED / RUNTIME + EXACT-JAR QA PENDING`.