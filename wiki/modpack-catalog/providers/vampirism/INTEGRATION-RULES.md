# Black Arcana ↔ Vampirism 1.10.13 — Integration Rules

Status: `CONTRATO SOURCE-PINNED / PROVIDER-NATIVE FIRST / VAMPIRE SPELLS 0.0.9 INTEROP SOURCE-CATALOGADO / FAIL-CLOSED / RUNTIME QA PENDENTE`

Canonical provider source: `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`.

## 1. Core principle

Vampirism already owns faction, level, Lord progression, skill trees, actions, blood, refinements, minions, tasks and village warfare. Black Arcana may observe, gate, augment or transact with those systems through supported provider surfaces, but must not create parallel authorities with the same meaning.

Prohibited by default:

- second Vampire/Hunter faction level;
- second Lord level or Lord XP track that impersonates provider progression;
- second Vampirism skill-point wallet;
- duplicated action cooldown/duration timers;
- second player blood bar representing the same Vampirism blood state;
- direct NBT mutation of provider state;
- reimplementation of Bat/Teleport/Freeze/etc. as generic spells merely to integrate them;
- generic stat/effect heuristics when an exact provider API/event exists.

## 2. Dependency and version gate

An integration that requires Vampirism must first confirm the mod is loaded.

Version-sensitive code must be written against the verified 1.10.13 API contract. If the installed artifact changes and the touched API/behavior has not been revalidated, the integration must fail closed for the affected feature rather than guessing compatibility.

Registry ids should be resolved through provider registries/API where runtime enumeration is useful. If an exact id required by the contract is absent, disable only that integration path and emit a clear diagnostic.

## 3. Authority matrix

| Domain | Provider authority | Preferred Black Arcana integration surface |
|---|---|---|
| faction membership | `IFactionPlayerHandler` | read current faction; `CanJoinFaction`/faction events for policy |
| normal faction level | `FactionPlayerHandler` | `FactionLevelChangePre` / `FactionLevelChanged` |
| Lord level | `FactionPlayerHandler` + provider Task/LordLevelReward | authoritative task reward/state transition; no fake `FactionLevelChanged` assumption |
| native skills | `ISkillHandler` | `isSkillEnabled`, tree state, `canSkillBeEnabled` for intentional native mutation |
| player actions | `IActionHandler` | `ActionEvent` lifecycle + handler read state |
| blood intake | `IVampire.drinkBlood` + `BloodStats` | `BloodDrinkEvent.PlayerDrinkBloodEvent` |
| blood spending | `IVampire.useBlood` + provider consumers | provider transaction itself; no thematic precharge |
| blood exhaustion | `BloodStats` + `vampirism:blood_exhaustion` | provider attribute / `addExhaustion` only when semantically correct |
| fluid blood | NeoForge fluid capability + Vampirism blood conversion registry | actual `vampirism:blood` FluidStack / data-map conversion |
| refinements | `ISkillHandler` + refinement registry | read equipped provider refinement state |
| tasks | provider Task registry/TaskManager | observe provider task state/reward; do not duplicate reward authority |
| minions | provider minion controller + Minion Tasks | observe/augment specific task lifecycle only with explicit contract |
| villages/capture | provider Totem/village system | `VampirismVillageEvent`, especially completion Post |
| sundamage/garlic | provider Vampire API/registries | read provider state/attributes/registries; do not infer only from daylight/effects |

## 4. Faction and level integration

### Read-only gate

For perks/quests requiring Vampire or Hunter status:

1. obtain `VampirismAPI.factionPlayerHandler(player)`;
2. compare actual provider faction;
3. read provider level;
4. fail closed if the expected faction is not active.

Do not infer faction from:

- appearance;
- effects;
- possession of blood items;
- presence of Vampire skills in old cached Black Arcana data.

### Completed normal-level transition

Use `PlayerFactionEvent.FactionLevelChanged` for completion-sensitive external rewards.

Recommended idempotency identity:

`vampirism-level:<playerUUID>:<factionId>:<oldLevel>-><newLevel>`

A pre-event or altar/trainer activation must not settle a reward that requires successful level-up.

### Intentional mutation

If a future Black Arcana feature is explicitly designed to grant a native faction level, use `IFactionPlayerHandler` provider methods and require their success result. Never write attachment/NBT/cache fields directly.

## 5. Lord-level integration

There is no dedicated public Lord-level event in the audited 1.10.13 API package, and normal `FactionLevelChanged` is not emitted by the Lord-only setter.

Therefore:

- do not subscribe to `FactionLevelChanged` and claim Lord coverage;
- prefer the provider Task/LordLevelReward path where the external system is reacting to native Lord progression;
- if state reconciliation is needed, compare previous authoritative Lord state with current state at bounded lifecycle points and edge-trigger exactly once;
- persist an idempotency key for external rewards.

Suggested identity:

`vampirism-lord:<playerUUID>:<factionId>:<oldLord>-><newLord>`

Do not poll `lordLevel == N` every tick and award repeatedly.

## 6. Native skill integration

### Gate a Black Arcana perk by a Vampirism skill

Use provider skill state:

`factionPlayer.getSkillHandler().isSkillEnabled(expectedSkill)`

Do not replace this with an attribute threshold or action presence heuristic when the exact skill is known.

### Intentionally enable a native skill

Only if design explicitly delegates this power:

1. resolve exact native skill;
2. call `canSkillBeEnabled`;
3. require `Result.OK`;
4. call provider `enableSkill`;
5. verify enabled state;
6. fail closed on any other result.

This preserves parents, skill points, node exclusivity and tree locks.

### Shared Lord skills

`lord_speed`, `lord_attack_speed` and `minion_recovery` are shared provider definitions referenced by both faction Lord trees. Count them once in provider capability coverage.

## 7. Action integration

### Canonical pre-effect hook

`ActionActivatedEvent` is appropriate for:

- cross-mod activation denial;
- explicit cooldown modifiers;
- explicit duration modifiers;
- telemetry that distinguishes attempted provider-approved activation.

Because the event occurs before `onActivated`, it is not sufficient evidence for an effect-success reward.

### Effect completion/success

For a reward that requires an action to actually take effect, correlate with the provider result/state rather than assuming event emission equals success.

Examples:

- Teleport: provider-approved activation plus actual successful action settlement/displacement under its own path;
- Infect: provider `tryInfect` succeeds and action returns true;
- Lord range actions: activation returns false if no eligible ally exists.

### Lasting actions

Use `ActionUpdateEvent`/`ActionDeactivatedEvent` when integration truly depends on lifecycle. Do not keep a Black Arcana duplicate timer.

### Downstream deduplication

One action activation is one causal action identity.

Do not separately count as additional casts:

- Dark Blood Projectile entity spawn;
- Summon Bats entity spawns;
- Rage potion refreshes;
- Sunscreen effect refreshes;
- Teleport displacement;
- Invisibility state reassertion.

## 8. Blood intake integration

For a perk that changes how much blood a Vampire gains, prefer `BloodDrinkEvent.PlayerDrinkBloodEvent`.

The hook is pre-settlement and exposes:

- amount;
- saturation;
- `useRemaining`;
- source context.

Rules:

1. modify the provider event once;
2. retain source context;
3. do not separately apply another blood delta after provider settlement;
4. clamp/validate any Black Arcana modifier according to the approved perk contract;
5. never award twice from event + resulting blood-level increase.

## 9. Blood expenditure integration

### Direct costs

Use `IVampire.useBlood(amount, allowPartial)` only when the Black Arcana mechanic is explicitly spending the provider's player-blood resource.

A transactional feature should:

1. validate faction/state/gate;
2. reserve/attempt provider blood at the correct causal stage;
3. only settle the external effect if payment succeeds;
4. avoid duplicate payment on retries/duplicate events.

### Native actions

Never add a thematic blood cost to a native action unless the design intentionally changes provider balance.

Examples:

- Bat: native cost path is exhaustion, not immediate blood debit;
- Half Invulnerable: default 4 blood is paid only when a qualifying hit is blocked;
- Teleport/Dark Blood Projectile/Freeze/etc.: no direct source-level player-blood debit was found in the audited action classes.

## 10. Blood exhaustion integration

When a perk is meant to improve Vampire resource efficiency under activity, the canonical domain is often `vampirism:blood_exhaustion`, not direct blood refunds.

Advantages:

- preserves saturation-first settlement;
- preserves Vampire-biome exhaustion threshold;
- preserves Peaceful rules;
- preserves native activity → exhaustion causality.

Do not listen for a blood decrement and refund it generically; that can refund unrelated legitimate costs.

## 11. Large blood reservoir contract

A large Black Arcana structure may safely use actual provider fluid blood if it has a distinct design purpose.

### Allowed baseline

- store `vampirism:blood` as a NeoForge fluid;
- expose normal fluid capabilities as designed;
- use `VampirismAPI.bloodConversionRegistry()` for approved foreign-fluid conversions;
- track structure capacity independently from player `BloodStats`;
- display structure fluid separately from player blood.

### Feeding a player from the reservoir

If designed:

1. calculate exact required mB using `FOOD_TO_FLUID_BLOOD = 100`;
2. atomically confirm/drain reservoir fluid;
3. call provider `drinkBlood` with an explicit context/transaction identity;
4. handle overflow according to the chosen contract;
5. make retry/idempotency behavior explicit.

### Forbidden implicit synchronization

Do not make a 70,000 mB reservoir turn the player's native maximum into `700/700` or similar simply by existing.

The provider player bar is a separate 20-point food-like state with saturation/exhaustion. Increasing its maximum would be a distinct design change requiring a verified provider-compatible implementation, not a UI derivation from tank size.

### If reservoir fluid also powers magic

The magic transaction must reserve/settle actual fluid independently. Do not spend the same mB simultaneously as:

- fluid magic fuel;
- player blood refill;
- another subsystem resource.

Use atomic reservation/settlement and one canonical transaction id.

## 12. Natural regeneration and lifesteal deduplication

Vampirism naturally heals players from its blood/saturation loop. That heal is **not automatically lifesteal**.

For Black Arcana concepts such as “Vampirismo Universal”, “Vampirismo Mágico” or “Vampirismo de Arma”:

- require a causal damage/source pipeline that explicitly proves lifesteal;
- do not observe `LivingHealEvent` alone and classify provider natural regeneration as vampirism/lifesteal;
- do not use current blood level as proof that a heal came from blood drain;
- maintain origin identity from damage/cast/weapon source through heal settlement.

The older Notion consumer designs that still mention Vampirism 1.10.12 must be revalidated separately when their perk contracts are revisited. This provider audit does not silently approve them.

## 13. Minion integration

Vampirism already owns minion task selection and resource generation.

### `collect_blood`

Do not add a second “servant collects blood” system without a separate purpose. If Black Arcana adds bonuses to this task, they should attach to the provider task/output transaction rather than create an independent periodic generator.

### `collect_hunter_items`

Likewise, use the native collection task as the causal source for Hunter servant resource production.

### Idempotency

One provider resource-generation settlement = one external telemetry/reward event. Save/reload/offline replay must not duplicate Black Arcana rewards.

## 14. Refinement integration

Use `ISkillHandler.isRefinementEquipped(...)` for exact refinement gates.

Do not infer refinement presence from:

- final Armor/Speed/Health/Damage numbers;
- action cooldown alone;
- effect amplifier alone.

This is particularly important because detrimental refinements are legitimate provider state and specialized refinements can change action semantics without a generic attribute signature.

## 15. Village/capture integration

Use provider village events.

### Gate or policy

`VampirismVillageEvent.InitiateCapture` can disallow capture and provide a message.

### Completed capture reward

Prefer `VillagerCaptureFinish.Post` for completion-sensitive Black Arcana credit.

Do not award completed-capture rewards on `InitiateCapture`.

### Raid modification

`DefineRaidStrength` is the provider hook for modifying attack/defend strength. Do not independently rescale spawned faction mobs after the provider has built the raid unless the design explicitly requires another layer.

## 16. Cross-provider gates

### Bloodlines 3.0.9

Bloodlines is installed and overlays specialization/progression on Vampirism. Until its exact source/runtime surface is audited:

- do not assume a base Vampirism skill/faction gate fully describes a bloodline-specific build;
- do not mutate Bloodlines state from this base integration;
- fail closed for bloodline-specific perks.

### Vampire Spells Addon 0.0.9

The installed bridge is source-pinned to official release `1.21.1-0.0.9`, commit `2d36e94e67611a316b7311b11e4574b499025580`. Its authority is the **cross-provider transaction policy** for Iron's Blood/Holy spells involving Vampirism; it does not own native Vampirism Actions.

Confirmed rules:

- native Vampirism Actions remain actions and do not inherit Iron's mana/cast/cooldown semantics;
- eligible Vampire casts of Iron's Blood School may replace the **current cast's** mana payment with an atomic Vampirism blood payment;
- default mode uses blood only when mana cannot cover the full current price; forced blood-only mode is configurable;
- Ray of Siphoning is explicitly excluded from resource substitution and remains mana-paid;
- Devour's Vampire mana multiplier is applied before any blood fallback calculation;
- all Vampire Blood-school casts receive the addon's provider-event cooldown multiplier;
- Ray/Devour blood restoration is settled from correlated delivered health damage through Vampirism's real blood API;
- Holy damage/heal/utility overlays are owned by the addon and must not be reapplied by Black Arcana.

Deduplication rule:

`one Iron's cast -> one resource settlement -> one downstream addon settlement`

Black Arcana must not:

- precharge the same blood before the addon;
- refund blood after the addon based only on observed bar delta;
- run a second generic mana↔blood converter for the same cast;
- count pre-cast, blood debit, damage pulse and blood restoration as independent casts/actions;
- generalize this bridge into a global unification of Vampirism blood with Iron's mana.

Runtime caveat: the addon's own compatibility audit explicitly pinned Iron's 3.16.2 while the pack currently installs 3.16.3. The declared metadata range includes 3.16.3, but Black Arcana consumers that depend on the addon's reflection/mixin internals remain fail-closed until the installed combination passes runtime QA.

Canonical addon documentation: [`../vampire-spells-addon/README.md`](../vampire-spells-addon/README.md) and [`../vampire-spells-addon/TECHNICAL-AUDIT.md`](../vampire-spells-addon/TECHNICAL-AUDIT.md).

### Vampiric Ageing 1.4.21

Age Rank is an independent progression layer. Normal level 14/Lord level 5 does not imply an Age Rank.

### Werewolves 2.0.3.3

Werewolf state is another faction/provider surface and must not be treated as a Vampire/Hunter subtype.

### Vampirism Integrations 1.10.2

Compatibility supplied by the dedicated integration addon should be audited before Black Arcana recreates the same bridge.

## 17. Client/server rule

All authoritative mutation and reward settlement occurs from server-authoritative evidence.

Client-only information may drive UI/preflight but not:

- faction/level rewards;
- blood debit/refill;
- skill unlock;
- action success rewards;
- task rewards;
- minion resource production;
- village capture completion.

## 18. Fail-closed matrix

| Failure | Required behavior |
|---|---|
| Vampirism missing | disable Vampirism-dependent integration |
| expected registry id absent | disable affected feature; log diagnostic |
| wrong faction | reject provider-specific effect |
| required native skill missing/disabled | reject |
| action not unlocked/allowed | provider rejects; do not bypass |
| native mutation returns false | no external settlement |
| installed version changed without revalidation | disable version-sensitive path |
| only client evidence exists | no authoritative reward/mutation |
| Bloodlines-specific state unknown | no bloodline-specific integration |
| Vampire Spells reflection/mixin contract unverified on installed Iron's | no Black Arcana dependency on that internal bridge path |
| duplicate causal id | no second settlement |

## 19. Canonical test matrix for implementation/validation

### Faction/level

- Vampire and Hunter join/leave;
- normal 1→14 transitions;
- canceled `FactionLevelChangePre`;
- exactly-once external reward on `FactionLevelChanged`.

### Lord

- Lord task reward 0→1→...→5;
- invalid Lord mutation below normal cap fails;
- no duplicate external reward after save/reload/reconciliation.

### Skills

- parent gate;
- sibling exclusion;
- insufficient points;
- Lord tree lock;
- reset/respec;
- addon-injected state after Bloodlines audit.

### Actions

- ActionActivated cancellation;
- cooldown/duration mutation;
- failed `onActivated` does not become success credit;
- early lasting-action deactivation;
- timeout;
- ActionWheel persistence after reconnect.

### Blood

- drink-event mutation;
- saturation-first exhaustion;
- 4/6 exhaustion gates;
- natural regeneration provenance;
- zero-blood state;
- Half Invulnerable late cost;
- Bat indirect exhaustion;
- reservoir fluid transaction/idempotency.

### Minions

- task skill gates;
- collect outputs;
- online/offline cooldown;
- save/reload persistence;
- exactly-once external telemetry/reward.

### Villages

- disallowed capture;
- Pre/Post ordering;
- completed capture credit only on completion;
- raid-strength modification.

### Pack interoperability

- Bat + Epic Fight/stamina/movement;
- Jump Boost + movement systems;
- Teleport + dimensions/portals;
- Vampire Spells Addon 0.0.9 load/reflection/mixins with Iron's 3.16.3;
- Vampire Spells resource fallback/deduplication + Ray/Devour + Holy matrix;
- Bloodlines coexistence;
- Vampiric Ageing coexistence.

## 20. Closure condition

This integration contract is source-approved for the Vampirism base provider when:

- exact installed 1.10.13 remains the target;
- provider APIs/registries above resolve as expected;
- Black Arcana uses the stated authority boundary;
- runtime tests still pending are not represented as passed.

Vampire Spells Addon 0.0.9 now has a separate source-pinned contract and may be referenced only within that documented boundary. Its installed Iron's 3.16.3 runtime/mixin QA remains pending. Bloodlines semantics remain separate audit work and cannot be inferred from this base-provider contract.