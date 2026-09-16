# Bloodlines 3.0.9 — technical audit

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

Installed contract: Minecraft 1.21.1, NeoForge, Bloodlines `1.21-3.0.9`, with Vampirism `1.10.13` as required base provider.

This document records the engineering boundary Black Arcana must preserve. It is a source audit, not runtime-QA confirmation.

## Architecture summary

Bloodlines is tightly layered on Vampirism. It adds its own bloodline identity/state, but deliberately reuses Vampirism's faction-player abstractions, skill/action registries, skill trees, task system, Vampire blood economy and multiple player/entity implementations.

Canonical authority is split as follows:

| Domain | Authority |
|---|---|
| Base Vampire/Hunter faction and normal levels | Vampirism |
| Bloodline identity + Bloodline rank | `BloodlineManager` |
| Bloodline perk wallet | `BloodlineSkillHandler` inside `BloodlineManager` |
| Skill topology/enabled skills | Vampirism `ISkillHandler` + Bloodlines gates/mixins |
| Action timers/activation lifecycle | Vampirism `IActionHandler` + Bloodlines action implementations/mixins |
| Vampire player blood/saturation/exhaustion | Vampirism |
| Gravebound player Souls/state | `BloodlineGravebound.State` |
| Gravebound Phylactery storage/ownership | Bloodlines `PhylacteryBlockEntity` + Gravebound state binding |
| Bloodline mob identity/state | Bloodlines mob attachment/registry logic |

No Black Arcana shadow state should be promoted above these authorities.

# Custom Bloodline registry

Bloodlines creates a synchronized NeoForge custom registry:

- registry key: `bloodlines:bloodlines`;
- `.sync(true)`;
- default key: `bloodlines:empty`;
- five registrations: Noble, Ectotherm, Zealot, Bloodknight, Gravebound.

The source itself documents that a complete Bloodline is expected to integrate:

- an `IBloodline` implementation;
- Bloodline parent/root skills;
- a dedicated skill tree;
- custom skills/events;
- tasks for rank/perk points unless an alternate system exists;
- optional spawn/rank distribution for mobs.

Therefore a Black Arcana integration should resolve a Bloodline by its provider registry identity, not by display-name string matching.

# Player attachment and persistence

`BloodlineManager` is a NeoForge attachment registered under the `bloodline_manager` path.

Attachment properties:

- factory requires a Player holder;
- custom `CompoundTag` serializer;
- `copyOnDeath()` enabled;
- server/client update NBT support through the provider attachment sync layer.

Persistent BloodlineManager fields include:

- bloodline ResourceLocation;
- Bloodline rank;
- Bloodline perk-wallet fields;
- optional bloodline-specific state.

For Gravebound, that state additionally persists Souls, total Souls devoured, Phylactery location/dimension, Mist Form and Possession identifiers.

## Lifecycle behavior

`setBloodline(null)` is not equivalent to clearing an id field. It also:

- resets rank to 0;
- clears custom Bloodline state via its lifecycle hook when present;
- clears Bloodline perk points and enabled-skill accounting.

`onBloodlineChange(oldBloodline, oldRank)` additionally owns:

- disabling skills from the previous Bloodline in the Vampirism SkillHandler;
- recalculating Vampirism skill-tree locks;
- recreating new Bloodline state when applicable;
- invoking old/new Bloodline transition hooks;
- disabling now-ineligible skills on rank decrease;
- updating rank-dependent attributes;
- triggering Bloodline-rank advancement hooks for ServerPlayer;
- syncing the attachment;
- updating cached `BloodlinesPlayerAttributes`.

This lifecycle is the canonical mutation path. Direct NBT/field edits are unsafe.

# Bloodline perk wallet

`BloodlineSkillHandler` is a small provider-owned wallet persisted inside the BloodlineManager tag:

- `blSkillPoints`: task-awarded points;
- `blOtherSkillPoints`: non-task points;
- `blEnabledSkills`: count of charged enabled Bloodline skills.

Definitions:

`total = taskSkillPoints + otherSkillPoints`

`remaining = max(0, total - enabledSkills)`

Leaving the Bloodline clears the two point balances; manager lifecycle also resets enabled-skill accounting.

## SkillHandler mixin boundary

Bloodlines injects directly into Vampirism `SkillHandler`.

At `canSkillBeEnabled` HEAD, Bloodlines adds:

1. `NO_POINTS` when a Bloodline skill requires a Bloodline perk point and none remain;
2. `LOCKED_BY_PLAYER_STATE` when `requiredBloodlineRank()` exceeds current rank;
3. `OTHER_NODE_SKILL` for default/rank skills when manual default unlock is disabled by config.

On a successful non-loading Bloodline skill enable:

- rank-dependent attributes are refreshed;
- if the skill requires Bloodline points, `blEnabledSkills` increments by **1**;
- manager sync follows.

Disable performs the inverse accounting.

### Static dual-gate discrepancy

This mixin does not replace Vampirism's original `SkillHandler.canSkillBeEnabled` checks; it injects extra decisions at HEAD. Bloodline skills can still expose ordinary `getSkillPointCost()` values >0 while Bloodlines separately requires its own wallet.

Observed risk:

- Vampirism normal skill-point check may still apply;
- Bloodlines only checks `remaining > 0` for its own wallet;
- Bloodlines charges its wallet by one enabled skill, even for a skill whose Vampirism cost is 2 or 3.

The public provider intent says Bloodline perks use Bloodline points instead of regular points, but source composition creates an ambiguity that must be tested in the installed runtime. Do not add automatic compensation/refunds from Black Arcana.

# Vampirism registries reused by Bloodlines

Bloodlines registers directly into Vampirism registries for:

- `ISkill`: 101 entries;
- `ISkillTree`: five trees;
- `ISkillNode`: provider nodes/configured trees;
- `IAction`: 29 actions;
- `Task`: 22 provider tasks.

The five skill trees are predicate-gated by current Bloodline identity and faction. Black Arcana must not infer that a registered skill/action is usable simply because its registry entry exists.

# ActionHandler mixin boundary

Bloodlines also injects into Vampirism `ActionHandler.updateActions`.

Every 10 timer units in the audited path it can extend lasting-action timers when:

- Zealot `Obscured Power` is enabled and the light gate matches;
- Ectotherm `Underwater Duration` is enabled and the player is underwater, excluding Dolphin Leap.

The mixin calls the provider ActionHandler's timer-extension path. Therefore Bloodlines action duration is not always a simple fixed countdown from initial config; other provider-native skills can extend it dynamically.

Black Arcana must read/observe actual handler state instead of maintaining its own nominal timer.

# High-value events and hooks

## Vampirism events consumed

### `PlayerFactionEvent.FactionLevelChanged`

Bloodlines clears the Bloodline when:

- new faction level becomes 0; or
- current faction differs from old faction and old faction was non-null.

Base faction therefore remains a hard identity gate.

### `BloodDrinkEvent.PlayerDrinkBloodEvent`

Used by Vampire Bloodlines to mutate blood amount/saturation and record provider stats while preserving Vampirism settlement.

### `ActionEvent.ActionActivatedEvent` / `ActionDeactivatedEvent`

Used to modify native action duration/cooldown in cases such as:

- Noble + base Vampirism Invisibility deduplication;
- Zealot Shadow Mastery cooldown manipulation.

### Vampirism faction/skill/action implementations

Bloodlines subclasses or directly accesses Vampirism implementations such as:

- `DefaultVampireAction`;
- `DefaultHunterAction`;
- `InvisibilityVampireAction`;
- `VampirePlayer` / `HunterPlayer`;
- `FactionPlayerHandler`;
- `SkillHandler` / `ActionHandler`.

That tight dependency is why base-provider version drift is a material compatibility risk.

## NeoForge gameplay events consumed

The provider's event handler uses or modifies behavior at least through:

- `LivingIncomingDamageEvent`;
- `LivingDamageEvent.Pre`;
- `LivingDeathEvent`;
- `CriticalHitEvent`;
- `LivingFallEvent`;
- `LivingEntityUseItemEvent.Finish`;
- `PlayerXpEvent.XpChange`;
- `PlayerEvent.BreakSpeed`;
- player/world join/leave/logout events;
- `PlayerTickEvent.Post`;
- interaction events.

These event stages are causally significant. A Black Arcana reward should bind to the event that proves the intended provider outcome, not merely a nearby earlier signal.

# Join and leave authority

Provider join routes are lifecycle-sensitive and differ per Bloodline. See `BLOODLINE-CATALOG.md`.

All successful joins converge on Bloodlines' canonical helper/manager lifecycle rather than just assigning a registry id.

Leaving uses an explicit mixin into Vampirism's `MedChairBlock.handleInjections` for Purity Injection. The source performs manager lifecycle cleanup and consumes the injection. Therefore a generic right-click listener is not equivalent.

# Mixins: compatibility-sensitive surfaces

Bloodlines relies on mixins against both Minecraft and Vampirism internals. High-impact audited examples include:

- `SkillHandlerMixin`: Bloodline point/rank/default gates and enabled-skill accounting;
- `ActionHandlerMixin`: dynamic action-duration extension;
- `InjectionChairMixin`: Purity Injection Bloodline removal through Vampirism Med Chair;
- `BatVampireActionMixin`: Bloodline/Bat behavior integration;
- `ExtendedCreatureMixin`: Bloodlines extension of Vampirism entity state;
- `BasicVampireEntityMixin` / related entity/AI mixins: Bloodline mob behavior;
- block/entity accessors/invokers used by Ghost Walk/Possession and other mechanics.

The exact mixin target signatures are a version-sensitive boundary. Upgrading Vampirism must trigger a compatibility audit even if the game starts successfully.

# Server/client authority audit

## Primarily server-authoritative surfaces

- Bloodline join/leave/rank mutation;
- persistent BloodlineManager/Gravebound state;
- provider task rewards;
- blood debit/credit settlement;
- Gravebound Soul debit/credit;
- Phylactery ownership/storage;
- damage-event joins and Mist Form lethal interception;
- most action success checks;
- final teleports such as Noble Flank and Gravebound Phylactery Teleport.

## Client-sensitive surfaces requiring runtime QA

### Wall Climb

The audited action changes vertical velocity only when `world.isClientSide` and collision is detected.

### Dolphin Leap / Crimson Leap

Activation originates server-side but sends a custom leap packet to the client for movement behavior.

### Possession

The server changes camera/ownership state, while custom client input/interact packets drive the possessed entity. This is a high-complexity authority surface.

### Mist Form

State and attributes are synchronized, but dimensions/pose/flight and action lifecycle span both sides.

Any Black Arcana movement bridge must fail closed until dedicated-server testing proves that the provider remains authoritative under the installed movement/combat stack.

# Static discrepancies catalog

The following are source findings, not automatically patched bugs:

1. **Bloodline dual skill-point gate:** own wallet plus possible Vampirism normal point gate.
2. **Bloodline wallet charges one per enabled skill** while some base costs are 2–3.
3. **`MaxPerkUnlocker.CODEC` field/getter mapping is inverted** for min/max names.
4. **Non-Gravebound perk tasks have no source-level Bloodline-point cap** analogous to Gravebound's 15 task points.
5. **Ectotherm `onCrit` references `ZEALOT_POISONED_STRIKE`.**
6. **Shadowwalk has a Bloodlines max-distance config that the audited action does not use.**
7. **Bloodknight Sanguine Infusion/Blood Hunt/Daywalker upkeep comments say one blood, implementation debits two.**
8. **Sorcerous Strike has a specific Wither-duration config (8 s) but the hit hook uses the general action duration (10 s default).**
9. **Sorcerous Strike registry/node/action exists but is absent from configured Gravebound tree/default skills.**
10. **Devour Soul can return action success for an invalid LivingEntity that was not devoured.**
11. **Mist Form deactivation requires Souls strictly greater than cost; exact configured cost reaches the death branch.**
12. **Wall Climb movement is client-side in the audited method.**
13. **Heinous Elixir public README and source config differ:** exact 3.0.9 source default is 15 seconds; stale/public prose must not override source for this build.

# Causal settlement requirements

## Blood

Use the Vampirism blood event/`BloodStats`/`useBlood`/`drinkBlood` path as final authority. A Bloodlines modifier changing amount/saturation is still part of one Vampirism settlement.

## Bloodline tasks

`BloodlineRankReward` / `BloodlinePerkReward` are completion settlement. They call the provider/Vampirism task manager lifecycle and can reset unique tasks. Do not award a Black Arcana duplicate from task acceptance/list generation.

## Souls

Only treat a Soul as acquired after `BloodlineGravebound.devour(...)` or another explicit provider state transfer has actually settled. Action activation is insufficient for Devour Soul because of the invalid-target return-true finding.

## Mist Form

The causal resurrection sequence is lethal-hit interception → state/action activation → timed Mist Form → Soul settlement or death. Do not treat action activation alone as a completed resurrection.

# Fail-closed integration rules

If a required provider API/state/event cannot be resolved at runtime:

- do not grant equivalent generic stats;
- do not debit a fallback generic resource;
- do not shadow-set Bloodline rank/skills;
- do not fake action cooldown completion;
- do not broaden a whitelist/tag by semantic similarity;
- log/telemetry the missing provider contract and leave the Black Arcana integration inactive.

# Runtime QA matrix

The source catalog is complete enough for design, but `RUNTIME QA CONFIRMED` is explicitly **not** granted.

Required installed-pack validation:

1. Bloodline join/leave/rank lifecycle and attachment persistence across death/reconnect.
2. Skill enable/disable under both normal Vampirism points and Bloodline points, including costs 2–3.
3. Default/rank skill manual-unlock blocking.
4. All 22 tasks and repeat/reset behavior; Gravebound cap at 15 vs uncapped other Bloodline perk tasks.
5. All 29 action registration/gates/timers and dynamic timer extension.
6. Blood settlement for Noble/Bloodknight/Flesh Eating/Fishmonger exactly once.
7. Bloodknight upkeep actual debit = 2 and timer units.
8. Shadowwalk distance config mismatch.
9. Ectotherm cross-Zealot Poisoned Strike reference.
10. Wall Climb/Dolphin Leap/Crimson Leap with dedicated server, Epic Fight/stamina/movement stack.
11. Devour Soul invalid-target cooldown behavior.
12. Soul/Phylactery conservation, reload, cross-dimension ownership and max clamp.
13. Sorcerous Strike survival reachability and Wither-duration mismatch.
14. Mist Form vulnerable damage, strict Soul threshold, cleanup, logout anti-abuse and reduced cooldown/cost skills.
15. Ghost Walk blacklist/collision behavior with modded blocks.
16. Possession whitelist, network input authority, supported mob behavior, cleanup and swap.
17. Purity Injection through Med Chair after active Gravebound/Mist/Possession states.
18. Compatibility with exact installed Vampirism 1.10.13 mixin targets.
19. Compatibility with Vampire Spells Addon 0.0.9 after its separate audit.

Until those tests pass, Bloodlines is `SOURCE-PINNED / GRANULAR CATALOG COMPLETE`, not runtime-confirmed.