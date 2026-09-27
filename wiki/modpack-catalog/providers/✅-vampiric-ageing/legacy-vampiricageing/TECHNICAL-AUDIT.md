# Vampiric Ageing 1.21-1.4.21 — technical audit

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

Status: **source-level audit complete enough for catalog/integration design; runtime QA pending**.

The findings below are static source observations. They are not promoted to runtime-confirmed bugs until reproduced in the exact Black Arcana stack.

## TA-01 — Hunter Wise Eye ignores its own duration config

`HunterAgeingConfig.wiseEyeDuration` defaults to 120, but `HunterEyeAction.getDuration()` reads `HunterAgeingConfig.stepAssistDuration`, clamps it and multiplies by 20.

Default `stepAssistDuration=Integer.MAX_VALUE`, so the source path does not correspond to the advertised Wise Eye duration.

**Integration consequence:** exact Wise Eye timing is fail-closed until runtime QA.

## TA-02 — Step Assist cooldown unit mismatch

Both `StepAssistAction` and `StepAssistHunterAction` return their configured cooldown directly. Other Actions whose config is documented/implemented in seconds normally return `config * 20` ticks.

Defaults are 0, hiding the issue unless the server config is changed.

**QA:** set a non-zero Step Assist cooldown and measure effective cooldown ticks/seconds.

## TA-03 — Wise Eye / Improved Senses cooldown unit asymmetry

`HunterEyeAction.getCooldown()` and `WerewolfEyeAction.getCooldown()` return the numeric config directly; their durations use explicit `*20` conversion. Default cooldown is 10 for both.

**QA:** determine whether the Action framework expects ticks here and document actual 10-tick vs 10-second behavior.

## TA-04 — Celerity multiplier semantics

Default `celerityActionMultiplier=1.025`. `CelerityAction` passes that whole value as the amount of an `ADD_MULTIPLIED_TOTAL` Movement Speed modifier.

That is statically different from a conventional 1.025× total multiplier represented as +0.025.

**QA:** measure effective movement speed during Celerity and confirm upstream intent before exposing exact percentage in gameplay-facing Black Arcana text.

## TA-05 — Limited Bat Mode dimension control-flow mismatch

`canBeUsedBy(...)` rejects:

- The End;
- any dimension in Vampirism's bat blacklist.

`onUpdate(...)` first branch uses `blacklist.contains(currentDimension) && currentDimension == END` before returning true with the dimension warning. The conditions are therefore stricter in update than in activation.

**QA:** test activation/deactivation after teleporting an already-active Hunter Bat Mode player into a blacklisted non-End dimension and into End.

## TA-06 — Werewolf faction-level config mismatch

`WerewolvesAgeingConfig.levelToBeginAgeMechanic` exists and defaults to 14. However, `WerewolfAgeingType.minFactionRank()` returns `CommonConfig.levelToBeginAgeMechanic`, the Vampire/common setting, instead of the Werewolf-specific value.

Defaults coincide, so normal configuration hides the mismatch.

**QA:** configure different Vampire/Werewolf start levels and verify actual gate.

## TA-07 — Blood Tap settlement is per incoming-damage event

`DrainBloodAction.activate()` itself does no blood transfer. `AgeingEventHandler.onHurt(...)` checks whether the Action is active on each qualifying Vampire attack, derives Vampirism `BITE_TYPE`, invokes target bite settlement and calls `VampirePlayer.drinkBlood(...)` plus the provider event.

This is not a bug, but it is a high-risk deduplication point.

**Integration rule:** never add a second Black Arcana blood-on-hit payout while Blood Tap is active.

## TA-08 — Tainted cumulative Age is discontinuous

`CapabilityHelper.getCumulativeTaintedAge(...)` returns 0 when there is no active temporary tainted bonus and no permanent transformation, even if base Hunter Age > 0. While transformed it substitutes fixed bonus 6.

This is provider semantics, not a simple `baseAge + persistentTaintedRank` progression.

**Integration rule:** always call/bridge the provider-derived state; never infer cumulative age from base Age alone.

## TA-09 — Age rank-up discards overflow

`AgeingManager.increaseRankPoints(...)` sets `rankProgress=0` after one rank increase. Excess points over the current threshold are not carried forward by this method.

**Integration rule:** external progression awards must not pre-compute multi-rank carry-over unless upstream is intentionally changed.

## TA-10 — Hunter permanent transformation has independent death policy

Global age death reset and Hunter permanent-transformation death reset are separate controls. `permanentTransformationDeathReset=false` by default, while global `deathReset=true`.

Hunter handler clears temporary Tainted state on death and only clears `transformed` when the dedicated config is enabled.

**QA:** test combinations of global Age loss/reset + permanent Hunter transformation to ensure desired Black Arcana progression semantics.

## TA-11 — Advanced Vampire Age is independently seeded on spawned advanced Vampire entities

With `advancedVampireAge=true`, advanced Vampire entities receive provider Age based on configured probabilities and provider-owned permanent attribute modifiers. This is entity-side ageing state, not player progression.

**Integration rule:** do not treat an advanced NPC Vampire's age as a player Age Rank or award player perks merely because the target has an AgeingManager.

## TA-12 — config-dependent immortality is disabled by default

`shouldOnlyDieFromKillingSources=false` and `immortalBloodLoss=false` by default. If enabled at/above the configured Age rank (default 4), the provider can intercept lethal damage from non-killing sources, optionally consuming blood.

**Integration rule:** death-sensitive perks must not assume ordinary lethal-damage semantics when this provider feature is enabled.

## Mandatory runtime QA matrix

Before promoting sensitive integrations to runtime-confirmed:

1. exact installed `Vampiric Ageing 1.21-1.4.21` + `Vampirism 1.10.13` startup;
2. Werewolves 2.0.3.3 conditional registration;
3. player login/relog attachment persistence and sync;
4. faction change and Age reset reconciliation;
5. each Age method progress event and threshold reset;
6. Blood Tap settlement and no duplicate blood event;
7. Celerity actual speed;
8. Water Walking lifecycle;
9. both Step Assist cooldown units;
10. Hunter Teleport collision/riding/dedicated-server behavior;
11. Limited Bat Mode flight, dimension transitions, water and sun gates;
12. Wise Eye effective duration/cooldown and invisibility bypass;
13. Improved Senses effective cooldown, duration and Werewolves `SENSE` gate;
14. Tainted temporary bonus, cumulative Age 8/10/11 gates and permanent transformation;
15. death handling for base Age and Hunter transformation;
16. Werewolf configured start-level mismatch reproduction;
17. dedicated-server smoke with movement/flight-related mods in the Black Arcana pack.

Until these pass, documentation may say **source-confirmed** but not **runtime-confirmed** for the affected behavior.
