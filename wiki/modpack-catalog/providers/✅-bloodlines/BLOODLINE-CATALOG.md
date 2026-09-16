# Bloodlines 3.0.9 — bloodline catalog

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

## Shared model

Bloodlines registers five `IBloodline` implementations in a synchronized custom registry. Each bloodline:

- belongs to one Vampirism playable faction;
- has a dedicated Vampirism `ISkillTree`;
- uses four Bloodline ranks;
- can provide rank-based permanent attribute modifiers;
- can declare default/rank skills;
- can listen to damage, critical hit, BloodDrinkEvent and tick hooks;
- may allocate a custom `BloodlineState` inside the player `BloodlineManager` attachment.

The five trees are additionally tagged as `bloodlines:type/bloodline`; the four Vampire trees are tagged in Vampirism's Vampire skill-tree tag and Gravebound in the Hunter tag.

## Noble

ID: `bloodlines:noble`

Faction: Vampire.

Tree: `bloodlines:vampire/noble`.

### Identity

Noble trades raw durability for mobility/social/blood manipulation and reduced exposure to some classic vampire hazards. The source applies rank-dependent modifiers to:

- attack speed;
- max health;
- Vampirism blood exhaustion;
- neonatal duration.

Conditional skills additionally alter:

- DBNO/resurrection duration;
- movement speed.

Noble mobs receive their own movement-speed modifier.

### Damage/event hooks

- incoming damage from non-Noble vampire attackers can be multiplied by the configured rank value;
- Vampirism fire damage types are multiplied by Noble's configured fire multiplier;
- `Intrigue` increases outgoing damage when the victim cannot really see the Noble;
- `Leeching` uses the Vampirism blood pipeline and may exhaust a target, apply Weakness to mobs, give blood to the Noble and, with Enhanced Leeching, heal the Noble;
- a configured rain weakness can apply Weakness while exposed to rain/sky outside artificial vampire fog after the relevant rank/default gate.

### Blood hook

`PlayerDrinkBloodEvent` remains canonical:

- stack-based sources are reduced by Noble's configured amount/saturation multiplier;
- direct entity sources can be increased when Better Blood Drain is enabled;
- direct drinking feeds the Bloodlines `ENTITY_BLOOD_DRUNK` task stat using Vampirism's food→fluid conversion constant.

### Join

The unique source-level route is implemented by `LordslayerInjectionItem` and can be disabled by config.

Requirements:

- attacker is a Player;
- target is a Vampire Baron;
- player is Vampire;
- player has no bloodline;
- Vampirism Lord level >= configured minimum;
- Baron has Weakness;
- Baron health percentage <= configured threshold;
- Lordslayer Injection attack.

On success the Baron is killed, one injection is consumed and `BloodlineHelper.joinBloodlineGeneric(...NOBLE...)` performs the join.

The public README describes the default intended gate as Vampire Lord Rank 2 and Baron below 30% health; because the implementation is config-driven, those values must be treated as defaults, not hardcoded integration constants, until the exact installed config is inspected at runtime.

## Zealot

ID: `bloodlines:zealot`

Faction: Vampire.

Tree: `bloodlines:vampire/zealot`.

### Identity

Zealot is a darkness/underground specialization. Rank modifies:

- Vampirism sun damage;
- Vampirism blood exhaustion.

Player skills provide stone movement/mining behavior, sneaking speed, shadow armor, magic protection, wall climbing, tunneling, shadow mobility and other darkness bonuses. Zealot mobs receive rank-based attack-damage modification.

### Environmental/combat hooks

- Shadow Armour modifies incoming damage in low light and emits particles;
- sufficiently bright areas can multiply incoming damage from a configured rank onward;
- Hex Protection modifies magic and indirect-magic damage;
- Poisoned Strike poisons non-undead targets on qualifying critical hits;
- `ZEALOT_STONE` includes common stone/cobblestone/deepslate/dripstone categories and drives fall/mining/movement behavior;
- Shadow Mastery can alter action cooldowns when light-level conditions match.

### Join

Unique route:

1. find/use a `bloodlines:zealot_altar`;
2. player must be Vampire and have no current bloodline;
3. `zealotUniqueUnlock` must be enabled;
4. use a Zealot Ritual Catalyst;
5. catalyst is consumed and a server-backed 700-tick ritual begins.

The ritual immobilizes/controls vertical movement, applies darkness/blindness phases and audio/particle effects. At `currentTick == 50` it joins the player to Zealot and applies Regeneration amplifier 2 and Damage Boost amplifier 2 for 400 ticks. If the current player is missing/dead the ritual is forced to terminate instead of granting the bloodline.

## Ectotherm

ID: `bloodlines:ectotherm`

Faction: Vampire.

Tree: `bloodlines:vampire/ectotherm`.

### Identity

Ectotherm is the cold/water specialization.

Provider-native mechanics include:

- base water resistance enabled by the rank-1 parent skill;
- rank-based swim-speed modifier;
- optional Hydrodynamic Form multiplier;
- underwater mining speed skill;
- Tentacles block-interaction-range bonus;
- non-player knockback resistance;
- hot-biome max-health/movement penalties after configured rank gates;
- cold-biome movement bonus;
- fire-damage multiplier;
- Holy Water Diffusion modifier;
- freezing immunity behavior (`setTicksFrozen(0)` every five ticks).

Rank 2 parent skill exposes the `Lord of Frost` action. Frozen Attack/Slowness Attack augment critical hits while Lord of Frost is active.

Static discrepancy: `BloodlineFrost.onCrit` also tests `ZEALOT_POISONED_STRIKE` and can apply poison to a non-undead target. Because the Zealot implementation independently contains the intended Poisoned Strike hook, this cross-reference is a runtime QA finding, not something Black Arcana should compensate for.

### Join

The Freezing Elixir gives the neutral `bloodlines:cold_blooded` effect for a config-driven duration.

At LOWEST incoming-damage priority, Bloodlines intercepts a lethal hit when:

- `ectothermUniqueUnlock` is enabled;
- player is Vampire;
- player has no bloodline;
- damage source is Vampirism `SUN_DAMAGE`;
- player has `Cold Blooded`;
- player is in water.

On success:

- `Cold Blooded` is removed;
- Vampirism Sunscreen is applied for 600 ticks at amplifier 2;
- Ectotherm is granted;
- the lethal damage event is canceled.

## Bloodknight

ID: `bloodlines:bloodknight`

Faction: Vampire.

Tree: `bloodlines:vampire/bloodknight`.

### Identity

Bloodknight specializes in consuming vampire blood.

Rank modifies:

- Vampirism blood exhaustion;
- attack damage.

Provider behavior includes:

- reduced nourishment from most non-vampire sources;
- bonuses/frenzy from Vampire Blood Bottles and vampire entities;
- damage multiplier against vampire victims;
- incoming Hunter-source damage multiplier;
- Sapping Strike transfer of blood from vampire targets into the attacker;
- Feeding Frenzy/Blood Frenzy effects;
- Blood Hunt + Hidden Strike interaction;
- Blood Extraction, Daywalker, Crimson Leap and Sanguine Infusion actions.

All blood debit/credit routes observed in the implementation use Vampirism `useBlood`, ExtendedCreature blood or `VampirePlayer.drinkBlood`; Black Arcana must not append a second settlement.

### Join

`bloodlines:heinous_curse` is a harmful ticking effect. Every ten ticks it deals 3 magic damage and reapplies Blindness/Weakness/Wither effects.

When the curse ends, `HeinousCurseEffect.handleHeinousEnding(player)` grants Bloodknight only if:

- player is still Vampire;
- no current bloodline;
- `bloodknightUniqueUnlock` is enabled.

The public README describes the intended Heinous Elixir window as 30 seconds. Exact duration is config/item-driven and must remain provider-owned.

## Gravebound

ID: `bloodlines:gravebound`

Faction: Hunter.

Tree: `bloodlines:hunter/gravebound`.

### Identity

Gravebound is a Hunter bloodline with a persistent Soul resource and Phylactery.

The player's normal food-level display/behavior is coerced from Soul state on tick:

- base proxy food level 10;
- above configured slow-regen Soul threshold → 18;
- below configured no-sprint Soul threshold → 6;
- air supply is forced to 300.

Bloodlines also applies a rank-based XP multiplier in `PlayerXpEvent.XpChange`.

### Soul state

Persistent `BloodlineGravebound.State` includes:

- Souls;
- max Souls;
- total Souls devoured;
- Phylactery BlockPos and dimension;
- Mist Form state;
- possession state and possessed entity identifiers.

Without a bound Phylactery the player max is hard-clamped to 4 Souls. With one, max Souls use rank-indexed config. Total Souls devoured can increase Phylactery capacity.

### Devour

Devour eligibility is determined from `EntitySoulData` data maps plus target health percentage, distance, entity type and player-alive-time anti-abuse gate. Successful devour can kill the target with 1000 `devour_soul` damage, credit Soul state/stats, heal via Regen Devour and transfer overflow to the Phylactery via Soul Transfer.

### Near-immortality / Mist Form

From the config-defined immortality rank, the provider forcibly enables `GRAVEBOUND_MIST_FORM` as a default/non-manual skill.

A qualifying lethal hit can be replaced by Mist Form if:

- damage is not excluded by vulnerable/bypass rules;
- Mist Form action is neither active nor on cooldown;
- required Souls are available.

The provider sets health to 1, zeroes the hit and activates its own action. Full death sets Souls to 3. Disconnecting while Mist Form is cached reapplies the last damage source or kills the player, preventing logout abuse.

### Join

The lethal-event join route requires:

- `graveboundUniqueUnlock` enabled;
- player is Hunter;
- no existing bloodline;
- `Soul Rending` active;
- `Heinous Curse` active;
- a nearby Phylactery found within the provider's ±2 search volume;
- that Phylactery has no owner.

On success:

- Gravebound is granted;
- Phylactery owner becomes the player;
- both join effects are removed;
- state is bound to that Phylactery/dimension;
- player starts with 10 Souls;
- Regeneration amplifier 2 is applied for 100 ticks;
- lethal damage is canceled.

## Leaving any bloodline

The source README calls Purity Injection the canonical removal item. Runtime implementation is more specific: `InjectionChairMixin` extends Vampirism's `MedChairBlock.handleInjections`.

Requirements:

- item is `bloodlines:purity_injection`;
- player is at a Vampirism Med Chair;
- BloodlineManager currently has a bloodline.

Settlement:

1. capture old bloodline/rank;
2. `setBloodline(null)`;
3. `setRank(0)`;
4. `onBloodlineChange(oldBloodline, oldRank)`;
5. clear provider skills/points/custom state through BloodlineManager lifecycle;
6. apply Blindness amplifier 2 + Slowness amplifier 3 for 80 ticks;
7. consume one Purity Injection.

Changing/losing the base Vampirism faction also removes the bloodline automatically through `PlayerFactionEvent.FactionLevelChanged`.

## Integration rule

Joining/leaving is lifecycle-sensitive. Black Arcana may observe these transitions, but must not emulate them by writing only a string/id. The canonical provider path also owns skill removal/default unlocks, attribute modifiers, Phylactery ownership, possession cleanup, points, rank and sync.
