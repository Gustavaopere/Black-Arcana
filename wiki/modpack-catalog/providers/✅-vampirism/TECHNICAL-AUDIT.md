# Vampirism 1.10.13 — Technical Audit

Status: `SOURCE-PINNED 1.10.13 / PUBLIC API + REGISTRIES + EVENTS + AUTHORITY AUDITADOS / RUNTIME QA PENDENTE`

## Version pin

- installed artifact: `Vampirism-1.21-1.10.13.jar`
- mod id: `vampirism`
- Minecraft: 1.21.1
- loader: NeoForge
- official source: `TeamLapen/Vampirism`
- exact source pin: `e1ed095713cef5e9eb151d0ee58908fa830d6bb7`
- pin date: 2026-09-05

At this pin the build still declares 1.10.13. The subsequent source line advances toward 1.10.14, so later behavior is not silently imported into this audit.

## Provider classification

Vampirism is a **stateful progression provider**, not a cosmetic addon. It owns authoritative state for:

- faction membership;
- normal faction level;
- Lord level;
- skill-tree unlocks and skill points;
- action unlocks, cooldowns and active timers;
- Vampire blood/saturation/exhaustion;
- sundamage and garlic interaction;
- tasks/rewards;
- minions and minion tasks;
- refinements;
- faction village warfare.

Any Black Arcana integration touching these domains must be provider-native first.

## Public registry surface

`VampirismRegistries` exposes API registry access for:

### Built-in/custom registries

- `skills`
- `actions`
- `entityactions`
- `miniontasks`
- `refinement`
- `refinement_set`
- `oil`
- `task_reward`
- `task_unlocker`
- `task_requirement`
- `task_reward_instance`
- `converting_handler`

### Data-pack registries

- `tasks`
- `skill_node`
- `skill_tree`

Integration consequence: registry enumeration is preferable to maintaining hard-coded copies when runtime completeness matters. Hard-coded ids remain useful for an exact version-pinned contract, but the provider registry should remain the authority for existence.

## `VampirismAPI` public accessors

Confirmed API managers/registries:

- `skillManager()`
- `actionManager()`
- `entityActionManager()`
- `vampireVisionRegistry()`
- `factionRegistry()`
- `sundamageRegistry()`
- `entityRegistry()`
- `extendedBrewingRecipeRegistry()`
- `settings()`
- `bloodConversionRegistry()`

Confirmed attachment accessors:

- `factionPlayerHandler(Player)`
- `vampirePlayer(Player)`
- `hunterPlayer(Player)`
- `extendedCreatureVampirism(PathfinderMob)`
- `garlicHandler(Level)`
- `fogHandler(Level)`

Deprecated Optional-returning accessors exist, but integrations should use the current non-deprecated API where possible.

## Public events

The API event package at this pin contains:

- `ActionEvent`
- `BloodDrinkEvent`
- `PlayerFactionEvent`
- `VampireFogEvent`
- `VampirismVillageEvent`

There is no public `SkillEvent`, `TaskEvent` or dedicated Lord-level event in this API package.

### Action lifecycle

`ActionActivatedEvent`:

- emitted after action cooldown/unlock/permission/`canUse` gates;
- emitted before `action.onActivated(...)`;
- cancellable;
- may mutate cooldown and duration.

Important: event emission is **not proof that the effect succeeded**. The provider only stores timers/stat after `onActivated(...)` returns success.

`ActionUpdateEvent`:

- carries remaining duration;
- can force deactivation;
- can skip provider `onUpdate` for that tick.

`ActionDeactivatedEvent`:

- carries remaining duration and cooldown;
- permits cooldown mutation;
- represents lasting-action deactivation.

### Blood intake lifecycle

`BloodDrinkEvent.PlayerDrinkBloodEvent` is fired immediately before player `BloodStats.addBlood(...)`.

Mutable inputs:

- amount;
- saturation modifier;
- useRemaining.

Source context is retained through `IDrinkBloodContext`.

This is a pre-settlement hook.

### Faction/normal-level lifecycle

`PlayerFactionEvent.FactionLevelChangePre`:

- server side;
- cancellable;
- contains current/new faction and current/new normal level.

`PlayerFactionEvent.FactionLevelChanged`:

- emitted after the successful faction/normal-level mutation;
- contains old/new faction and old/new normal level.

`CanJoinFaction` can return provider behaviors `ONLY_WHEN_NO_FACTION`, `ALLOW` or `DENY`.

### Lord-level lifecycle gap

`FactionPlayerHandler.setLordLevel(...)` validates:

- active faction exists for positive Lord level;
- normal level equals the faction maximum;
- target Lord level does not exceed faction Lord cap.

It then:

- updates Lord level;
- reconciles skill-tree locks;
- updates cached player attributes;
- updates max minions;
- manages advancement state;
- synchronizes attachment state.

At this source pin it does **not** emit the normal `PlayerFactionEvent` pair for the Lord-only mutation. No dedicated public Lord event was found in `api/event`.

Integration consequence: completion-sensitive Lord mirroring must use a verified provider state transition/task-reward path or another stable observable surface. Do not pretend `FactionLevelChanged` covers Lord levels.

### Village warfare hooks

`VampirismVillageEvent` provides explicit surfaces for:

- `InitiateCapture` — can disallow capture and attach a message;
- `VillagerCaptureFinish.Pre` — can disable provider entity conversion;
- `VillagerCaptureFinish.Post` — post-capture observation;
- `DefineRaidStrength` — mutable attack/defend strength and trigger classification;
- `SpawnNewVillager` — replace spawned Villager object;
- `MakeAggressive` — cancellable villager-aggression conversion.

These hooks are preferable to scanning totems/villagers after the fact when Black Arcana needs a village-war integration.

## Faction authority

`IFactionPlayerHandler` exposes:

### Read

- current faction;
- current faction player;
- current level;
- faction-relative level;
- Lord level through `ILordPlayer` inheritance;
- faction predicates/state.

### Write

- `joinFaction(...)`;
- `setFactionAndLevel(...)`;
- `setFactionLevel(...)`;
- `setLordLevel(...)`;
- `leaveFaction(...)`;
- `checkSkillTreeLocks()`.

These writes are legitimate API but are **high-authority operations**. Black Arcana should not call them merely to make its own mirror state match. Use them only where design intentionally delegates progression mutation to an integration.

## Skill authority

`ISkillHandler` controls:

- point balance;
- parent lookup;
- sibling/node locks;
- enable/disable;
- reset/respec;
- refinement equipment;
- skill-tree lock state.

`canSkillBeEnabled(...)` must be honored before intentional native enablement.

Because no Skill event was found, safe read integration uses `isSkillEnabled(...)`, `unlockedSkillTrees()` and provider state reconciliation. Polling/caching should be bounded to meaningful lifecycle moments rather than every tick when not necessary.

## Action authority

`IActionHandler` exposes provider-native operations for:

- available/unlocked actions;
- active/cooldown state;
- timer percentage;
- toggle/deactivate;
- timer extension/reset;
- explicit action unlock/relock.

The handler persists timers by registry `ResourceLocation`. This is important after the 1.10.13 persistence-related fixes: Black Arcana should never maintain a competing timer for the same provider action.

## Blood authority

### Read

`IVampirePlayer` exposes:

- `getBloodLevel()`;
- `getBloodStats()`;
- `getTicksInSun()`;
- DBNO state;
- active vision;
- provider ActionHandler.

### Write

`IVampire` exposes `drinkBlood(...)` and `useBlood(...)` in blood food units.

`IVampirePlayer.addExhaustion(...)` is also public.

These methods must be used semantically:

- `drinkBlood` for a true blood-intake transaction;
- `useBlood` for a true provider blood cost;
- `addExhaustion` when the intended effect is provider blood exhaustion.

Do not use `drinkBlood` as a generic mana refill or `useBlood` as a thematic tax where the provider action itself does not consume blood.

## Blood fluid/interoperability authority

`VampirismAPI.bloodConversionRegistry()` exposes NeoForge data-map-driven conversion rather than forcing integrations to hard-code foreign fluids.

This gives Black Arcana a stable route for:

- checking whether a fluid has a provider blood conversion;
- converting a `FluidStack` to provider Blood;
- querying item → impure-blood behavior.

## Dedicated-server authority

Provider-changing integrations should settle on server-side state. Client-visible action updates, HUD state, vision and model data do not authorize progression/resource mutation.

Critical server-authoritative examples:

- faction/level changes;
- Lord rewards;
- altar settlement;
- task claims;
- blood consumption;
- minion resource output;
- action activation after packet handling.

## Causal event recommendations

### Provider action

Suggested identity:

`vampirism-action:<playerUUID>:<actionId>:<activationSequence>`

Do not derive a second cast identity from spawned projectiles, potion effects, teleport displacement or bats caused by that action.

### Blood intake

Suggested identity:

`vampirism-blood-drink:<playerUUID>:<sourceContext>:<sequence>`

The resulting blood-level delta is settlement, not another intake.

### Faction level

Suggested idempotency key:

`vampirism-level:<playerUUID>:<factionId>:<oldLevel>-><newLevel>`

### Lord level

Because no dedicated public event is confirmed, use a state-transition/idempotency model only after observing an authoritative task reward or verified old/new Lord state. Never award repeatedly from “current Lord level == N” polling.

### Village capture

Prefer `VillagerCaptureFinish.Post` for completed capture credit, not `InitiateCapture`.

## Fail-closed rules

Fail closed if any of these are true:

- Vampirism is not loaded when an integration requires it;
- expected registry id does not exist;
- player is not in the required provider faction;
- native skill/action is not actually unlocked when the design requires it;
- source/installed version diverges from the contract and the relevant API was not revalidated;
- Bloodlines or another addon overrides/injects semantics that make a base-only assumption unsafe;
- an attempted native mutation returns failure;
- client-only observation is the only evidence available for a server-side reward.

Do not substitute a generic Strength/Speed/Regeneration effect for a missing Vampirism hook.

## Compatibility gates for the Black Arcana pack

### Epic Fight / stamina / movement

High-risk actions:

- Bat;
- Teleport;
- Jump Boost;
- Rage.

They manipulate flight, forced pose/dimensions, movement attributes, teleport state or movement effects. These need integration/runtime tests rather than static “compatible” claims.

### Iron's Spells

Vampirism player actions are not Iron's spells. `Vampire Spells Addon 0.0.9` is the designated bridge/provider and must be audited separately before any action↔spell equivalence is accepted.

### Bloodlines

Bloodlines 3.0.9 is a progression addon on top of Vampirism. Base skills/faction state remain important, but addon-injected bloodline state must be audited before Black Arcana assumes base-only eligibility.

### Vampiric Ageing

Age ranks are an additional progression layer. Do not infer Age from normal faction/Lord level.

## Regression-sensitive 1.10.13 areas

Runtime QA should specifically exercise areas touched by this release line and already relevant to the pack:

- ActionWheel/action persistence;
- MinionTask persistence;
- village totems/capture;
- Teleport/dimension transition behavior.

## Test contract for later validation

1. dedicated server joins and faction level transitions;
2. all four skill-tree lock predicates;
3. representative sibling skill exclusivity;
4. ActionActivated cancel/mutate and successful-vs-failed activation;
5. lasting action early deactivation/timeout timers;
6. BloodDrink pre-settlement mutation;
7. exhaustion → saturation → blood settlement;
8. Half Invulnerable late payment;
9. altar Inspiration/Infusion completion and interruption;
10. Hunter Table/Trainer transaction;
11. Lord Task reward progression and no duplicate settlement;
12. minion collect tasks, save/reload/offline behavior;
13. village capture pre/post hooks;
14. Bat/Teleport/Epic Fight/movement interoperability;
15. Bloodlines and Vampire Spells addon coexistence.
