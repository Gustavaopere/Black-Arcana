# Vampiric Ageing 1.4.21 — technical audit

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Loader/dependency contract

Official metadata for the exact source line declares:

- Minecraft: 1.21.1 build line;
- NeoForge required;
- Vampirism required in range `[1.10-beta.2,1.11.0)`;
- Werewolves optional in range `[1.2.0.0-beta.2, )`;
- Java/mixin compatibility level: Java 21.

Current pack:

- Vampirism `1.10.13` — inside the declared range;
- Werewolves `2.0.3.3` — installed and above the declared minimum;
- Java 21 / NeoForge 1.21.1 — aligned with the provider build.

Declared dependency compatibility does not prove every mixin target behaves as expected in the exact installed combination; runtime QA remains required.

## Persistent state

### Attachment

`ModAttachments.AGEING_MANAGER` registers `AgeingManager` as a serialized NeoForge attachment and calls `.copyOnDeath()`.

`AgeingManager` is therefore the canonical persistent/synchronized authority for Age progression.

Player NBT/update fields include:

- `ageing_rank`;
- `ageing_type`;
- `ageing_rank_progress`;
- serialized TypeState fields where applicable.

The manager also stores runtime references to:

- selected `IAgeType`;
- selected `IAgeMethod`;
- current entity;
- optional `TypeState`.

### Hunter TypeState

`HunterAgeingType.HunterState` is serialized within the manager and owns:

- temporary Tainted Age bonus;
- temporary Tainted ticks;
- accumulated sun ticks;
- permanent Tainted transformation.

Black Arcana must not treat the `tainted_blood_effect` MobEffect as the complete state.

## Registration topology

### Internal Age registry

`AgeingRegistry` is a provider-local static registry/list, not a NeoForge synced custom registry.

Current pack registration order:

Age Types:

1. Vampire;
2. Hunter;
3. Werewolf — only when Werewolves is loaded.

Age Methods:

1. `BitingMethod`;
2. `TimeMethod`;
3. `VampHuntingMethod`;
4. `HunterHuntingMethod`;
5. `DrinkBloodMethod`;
6. `DevourMethod` — Werewolves condition;
7. `WerewolfHuntingMethod` — Werewolves condition;
8. `WerewolfMixedHuntingMethod` — Werewolves condition.

`CapabilityHelper.setDefaultAgeTypeAndMethod` iterates these registrations and selects the enabled type matching current faction plus the enabled method whose valid type is the selected type.

### Vampirism registries

The provider registers through Vampirism registries:

- 9 `IAction` entries in the current pack;
- 10 `ISkill` entries in the current pack;
- 1 `IOil` (`seniority_oil`).

Eight actions and nine skills are in the main VampiricAgeing register sets. Werewolf Improved Senses contributes the ninth action/tenth skill only when Werewolves is loaded.

### Vanilla/NeoForge registries

Own registrations also include:

- four Items;
- one MobEffect: `vampiricageing:tainted_blood_effect`;
- data components/datamaps used by provider content.

## Action/skill authority

Ageing does not create a parallel action handler. Its actions are real entries in `VampirismRegistries.Keys.ACTION`, and ActionSkills are inserted into native Vampirism/Werewolves skill trees.

The Age Type lifecycle enables/disables these zero-cost native skills according to Age Rank and, for Improved Senses, Werewolves SENSE dependency.

Integration consequence: an external UI may expose the provider action state, but it must not run another cooldown/duration counter or independently grant the same native action.

## Event authority and causal settlement

Major event surfaces include:

### `LivingDeathEvent`

- selected Hunting methods route qualifying kills into exactly one provider Age-progress method;
- player death can reset/reduce Age according to provider config;
- Hunter death clears temporary Tainted state and sun exposure;
- optional Sire mechanics can produce age-bearing blood provenance.

### `BloodDrinkEvent.PlayerDrinkBloodEvent`

When the selected Vampire Age Method is `DRAINING`, entity-backed canonical Vampirism blood settlements add the final event amount to Age progress.

This event is the Age-progress boundary for that method. Observers must not also credit the bite/attack precursor as a second Age transaction.

### `LivingIncomingDamageEvent`

Used by multiple provider overlays:

- Blood Tap attack→bite→blood transaction;
- Vampire damage-source ageing modifiers;
- Hunter Tainted fire weakness;
- Werewolf Bite heal/nourishment;
- Werewolf Silver weakness.

A single damage event can therefore be a trigger for downstream native settlements. Black Arcana hooks must preserve causal provenance and deduplicate by the authoritative provider outcome.

### `LivingDamageEvent.Pre` at LOWEST

Optional old-Vampire lethal-damage interception runs late and can convert a non-killing-source lethal hit into survival at 1 HP. Optional blood requirement debits the real Vampirism blood pool.

This is a late settlement path. Never pre-charge or independently resurrect on attack start.

### Tick handlers

Provider ticks settle:

- `TIME` progression every 100 ticks;
- Tainted Blood duration/sun accumulation;
- Hunter Faster Regeneration;
- Vampire ageing side effects and resource/exhaustion mechanics;
- synchronized state refreshes.

## Mixin surface

`vampiricageing.mixins.json` is `required=true` and declares **18 common mixins + 2 client mixins**.

Common list:

1. `BlockBehaviourMixin`
2. `BloodStatsMixin`
3. `CoffinBlockMixin`
4. `DamageHandlerMixin`
5. `FoodStatsAccessor`
6. `HowlActionMixin`
7. `HunterPlayerSpecialAttributesMixin`
8. `InfectActionMixin`
9. `ModPlayerEventHandlerMixin`
10. `PlayerMixin`
11. `PowderSnowBlockMixin`
12. `SilverOilMixin`
13. `VampirePlayerMixin`
14. `VampirePlayerSpecialAttributesMixin`
15. `VampirismItemBloodFoodItemMixin`
16. `VillagerMixin`
17. `WerewolfFormActionMixin`
18. `WWModPlayerEventHandlerMixin`

Client:

19. `client.LivingEntityRendererMixin`
20. `client.RenderHandlerMixin`

### Conditional Werewolves mixins

`VampiricAgeingMixinPlugin` prevents four Werewolves-targeted mixins from applying unless Werewolves is actually present:

- `HowlActionMixin`;
- `SilverOilMixin`;
- `WerewolfFormActionMixin`;
- `WWModPlayerEventHandlerMixin`.

Other Werewolf integration classes/registrations are also guarded by explicit ModList checks in provider initialization.

## Movement/client authority risk

High-risk runtime surfaces:

### Limited Hunter Bat Mode

Touches:

- player dimensions and pose;
- `mayfly`, `flying`, flying speed;
- Hunter special attributes;
- Vampirism bat attachment cleanup;
- attack/mount/block/item restrictions;
- block placement cancellation and server inventory/player-info synchronization;
- client rendering dimensions.

This cannot be safely proxied with a generic flight attribute.

### Hunter Teleport

Owns:

- look-target selection;
- candidate-position calculation;
- collision/liquid validation;
- rollback on failure;
- ServerPlayer teleport;
- provider sounds/particles;
- native action cooldown.

External teleport hooks should observe success after provider settlement, not move the player again.

### Wise Eye / Improved Senses

The authoritative semantic flag is `AgeingPlayerCache.hasBypassInvisibility`, with client rendering mixins consuming that state. It is not equivalent to Night Vision or Glowing.

## Resource authority

### Vampirism blood

Ageing frequently modifies or observes real Vampirism blood behavior:

- default `DRAINING` Age progress listens to BloodDrinkEvent;
- Blood Tap uses native bite/blood APIs then `VampirePlayer.drinkBlood`;
- high-age optional immortality can call `VampirePlayer.useBlood`;
- ageing modifies Vampirism Blood Exhaustion attributes;
- optional Sire mechanics attach Age provenance to Vampire Blood Bottle flows.

It does **not** own a second Vampire blood wallet.

### Hunter food/exhaustion

Hunter Faster Regeneration and Age penalties use the real vanilla FoodData/exhaustion lifecycle. Werewolf Bite nourishment also settles into native FoodData.

### Tainted Blood

Tainted Blood is an `AgeingManager` Hunter TypeState progression/transformation domain. It must remain separate from Vampirism blood, Bloodlines Gravebound Souls and any Black Arcana reservoir.

## Data-driven surfaces

The exact source includes:

- entity tags for petty/common/greater/exquisite hunt/devour classifications;
- `infected_blacklist`;
- `tainted_food` item tag;
- `age_item_restriction` data map and example datapack material.

A generated resource filename is visibly misspelled as `graeter_hunt_vampire.json`; integrations must use the registry/tag constants/source contract rather than hand-normalizing resource paths from prose.

## Static discrepancies requiring runtime QA

### A. Celerity modifier magnitude

Config default: `1.025`.

Operation: `ADD_MULTIPLIED_TOTAL`.

This executable amount does not mean the same thing as an intuitive 1.025× multiplier or +2.5% modifier. Measure runtime attribute output before presenting it as a percentage.

### B. DBNO/neonatal modifiers

Provider config comments describe values below 1 as decreasing duration, while Age Type source uses the positive values directly as `ADD_MULTIPLIED_BASE` modifier amounts. Treat source execution as authoritative and behavior as runtime-QA-gated; do not rewrite the amounts from comments.

### C. Step Assist cooldown unit

Both Vampire and Hunter Step Assist `getCooldown()` implementations return their config integers directly rather than multiplying by 20. Default 0 hides the discrepancy; non-zero custom configs are ambiguous relative to comments/UI expectations.

### D. Hunter Wise Eye duration/cooldown

- `wiseEyeDuration=120` exists in config;
- action `getDuration()` instead reads `stepAssistDuration`;
- action `getCooldown()` returns raw `wiseEyeCooldown=10`.

Do not substitute the dedicated config field externally.

### E. Werewolf Improved Senses cooldown

Duration converts to ticks; cooldown returns raw config `10`.

### F. Rank progress overflow

Threshold overflow is discarded. This is executable source semantics, not a mathematical carry-forward system.

### G. Config/source semantic surfaces

Several provider comments describe high-level intent while implementation routes through attributes/mixins whose exact output depends on Vampirism/Werewolves internals. For Black Arcana, comments are not stronger authority than the executable path.

## Runtime QA matrix

Minimum exact-pack validation:

1. Celerity observed movement-speed value before/during/after action.
2. Vampire DBNO/neonatal duration at Age 0 vs 3/4/5.
3. non-zero test config for Step Assist cooldown unit.
4. Wise Eye actual duration and cooldown under defaults.
5. Werewolf Improved Senses actual cooldown under defaults.
6. Blood Tap: target debit + attacker blood/saturation credit + BloodDrinkEvent exactly once.
7. DRAINING method: one Age-progress credit from Blood Tap resulting blood event.
8. normal rank threshold with excess points: verify overflow reset.
9. death reset and partial-loss configs.
10. faction switch: Age Type/Rank/TypeState cleanup.
11. Tainted bottle rank 1 and rank 5 acquisition/use/duration.
12. Garlic Injection clears temporary + transformed state exactly once.
13. Tainted sun thresholds and decay.
14. permanent transformation survives death by default.
15. Hunter Teleport valid, MISS, liquid and obstructed targets on dedicated server.
16. Limited Hunter Bat enter/exit/reconnect/death + attack/item/block/mount restrictions.
17. Werewolf DEVOUR vs W_HUNTING/W_MIXED progression exactly once.
18. Werewolf Bite heal/nourishment exactly once.
19. Howl wolf modifiers exactly once.
20. Werewolf Form duration scaling and Improved Senses invisibility bypass.
21. mixin startup against exact Vampirism 1.10.13 + Werewolves 2.0.3.3.

Until those validations are recorded, status remains `RUNTIME QA PENDING`.