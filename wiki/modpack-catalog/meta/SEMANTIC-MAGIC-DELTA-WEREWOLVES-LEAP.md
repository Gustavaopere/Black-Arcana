# Semantic Magic Delta — Werewolves Leap

Physical/current provider: `Werewolves-1.21-2.0.3.3.jar`
Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`

## Correction

The previous semantic ledger treated `werewolves:leap` as `CONDITIONAL`, reasoning that the action is hidden from the normal action selector and that its enabling path was not proven.

That exclusion is too conservative. The exact installed-version source proves a complete survival enabling path:

1. `ModSkills.LEAP` is registered as an `ActionSkill` bound to `ModActions.LEAP` on the normal Werewolf level tree.
2. `ModSkills.Nodes.SURVIVAL31` is explicitly constructed as `new SkillNode(ModSkills.LEAP)`.
3. `SkillTreeProvider` connects `SURVIVAL31` into the generated `werewolf_level` tree as a child of `SURVIVAL3`.
4. The generated configured skill tree contains `werewolves:werewolf/survival31` in that branch.
5. The player has a dedicated Leap input path; the server receives `ServerboundSimpleInputEventPacket.Action.LEAP` and delegates activation to the provider-owned `ActionHandler` for `ModActions.LEAP`.
6. Provider source implements the Leap action lifecycle and server/player event handling. Being hidden from the generic action selector therefore does not make the ability unreachable; it is deliberately key-driven.

The separate `no_leap_cooldown` refinement remains reachability-unproven. That refinement is not the semantic identity being counted here and must not be conflated with the reachable Leap action itself.

## Semantic disposition

- previous Werewolves counted semantic actions: **7**;
- corrected Werewolves counted semantic actions: **8**;
- delta: **+1**;
- previous strict global minimum: **796**;
- corrected strict global minimum: **797**.

`hide_name` remains excluded as presentation-only. `no_leap_cooldown` remains fail-closed as an acquisition/reachability question for a modifier of Leap, not as a separate spell/action identity.

## Authority boundary

Werewolves/Vampirism remain authority for the skill tree, action activation, cooldown and Leap settlement. Black Arcana may observe a validated provider event/state transition for progression or integration, but must not activate Leap by bypassing provider gates, duplicate its cooldown, or reapply movement settlement.

## Evidence

Exact source files at the pinned revision:

- `src/main/java/de/teamlapen/werewolves/core/ModSkills.java`
- `src/main/java/de/teamlapen/werewolves/data/SkillTreeProvider.java`
- `src/generated/resources/data/werewolves/vampirism/configured_skill_tree/werewolf_level.json`
- `src/main/java/de/teamlapen/werewolves/server/ServerPayloadHandler.java`
- `src/main/java/de/teamlapen/werewolves/entities/player/werewolf/actions/LeapAction.java`

No Werewolves source code or assets are copied into Black Arcana runtime. This document records read-only factual registry/reachability evidence under the existing LGPLv3 source-audit posture.