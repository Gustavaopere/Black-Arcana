# Werewolves 2.0.3.3 — effects, weaknesses and combat state

Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.

## Registered mob effects — 8/8

| ID | Type | Source semantics |
|---|---|---|
| `lupus_sanguinem` | harmful | infection precursor; eligible player joins Werewolf faction when effect resolves |
| `howling` | beneficial | +50% attack speed via hard-coded attribute modifier in exact source |
| `silver` | harmful Werewolf weakening | level-scaled movement-speed and attack-damage penalties; also amplifies incoming damage through player handler |
| `wolfsbane` | harmful Werewolf weakening | level-scaled movement-speed penalty; refreshed from provider wolfsbane world influence |
| `bleeding` | harmful | blood-loss damage over time; may additionally drain Vampirism blood state |
| `un_werewolf` | neutral | on final tick, removes Werewolf faction/level through Vampirism faction handler |
| `bad_omen_werewolf` | faction omen | Vampirism Bad Omen specialization for Werewolf faction |
| `stun` | harmful | zeros horizontal velocity and prevents positive vertical movement each tick |

Werewolves also references Vampirism `poison`; it is not Werewolves-owned.

## Infection — Lupus Sanguinem

Provider flow:

1. player/mob bite can call provider infection roll;
2. infection chance comes from Werewolves server config and differs for player-bite vs mob-bite paths;
3. only targets accepted by `Helper.canBecomeWerewolf` receive the persistent effect;
4. sleep/wake provider hooks resolve the effect;
5. `applyEffectTick` joins `WReference.WEREWOLF_FACTION` through Vampirism `FactionPlayerHandler`.

Black Arcana must treat the provider faction transition as authority, not the mere presence of the icon/effect as proof that the transition has completed.

## Cure — Un Werewolf

The provider cure effect only commits the faction removal on its final tick:

- if target is still Werewolf, call `FactionPlayerHandler.setFactionAndLevel(null, 0)`;
- show provider message;
- provider state/skills are then reconciled through faction-level lifecycle.

Do not emit a second faction-leave transaction.

## Silver weakness

`SilverEffect` is a `WerewolfWeakeningEffect` with source-level templates for:

- movement speed: max modifier basis 0.15;
- attack damage: max modifier basis 0.10.

The generic weakening-effect implementation computes level-scaled negative `ADD_MULTIPLIED_TOTAL` modifiers based on Werewolf level/max level and effect amplifier.

Additional player rule: while a Werewolf has `SILVER`, incoming damage is multiplied by:

`1 + (amplifier + 1) × 0.1`

Examples from that direct formula:

- amplifier 0 → ×1.1 incoming damage;
- amplifier 1 → ×1.2;
- amplifier 3 → ×1.4.

### Silver Blooded

When player is in a **human-like form** and has `silver_blooded`:

- if incoming Silver effect amplifier >0, provider lowers amplifier by one;
- otherwise, for a non-continuous application, provider halves duration.

The skill does not make the player globally silver-immune.

### Silver application paths observed

- silver tool attacks against Werewolves;
- a Werewolf attacks a target wearing silver armor;
- Werewolf holds silver item(s);
- Werewolf wears silver armor.

Provider continuously refreshes some equipment-derived Silver applications, so external systems must deduplicate effect application observations.

## Wolfsbane weakness

`WOLFSBANE` is another Werewolf-only weakening effect, reducing movement speed through the same level-scaled modifier architecture. `WerewolfPlayer` periodically queries provider world wolfsbane state and refreshes the effect when affected.

This is a spatial/provider-world mechanic, not a generic potion-only weakness.

## Bleeding

`BleedingEffect`:

- does not damage inverted-heal/harm entities;
- damaging-tick frequency is `20 >> amplifier` ticks while positive;
- each damaging tick applies provider `bloodLoss` damage;
- default configured damage per damaging tick: **0.4**;
- independently, on a 1-in-8 random roll per effect tick, it can drain one Vampirism blood unit:
  - Vampirism player: `VampirePlayer.useBlood(1, true)`;
  - Vampirism vampire entity: `IVampire.useBlood(1, true)`;
  - other PathfinderMob with Vampirism extended-creature blood: decrements that blood state by one.

Therefore Black Arcana must not replace Bleeding with a generic DOT if it needs compatibility with Vampirism blood economy.

## Stun

Every active tick:

`setDeltaMovement(0, min(0,currentY), 0)`

This removes horizontal movement and clamps upward motion. It is movement control rather than a generic AI-disable flag.

## Howling

`HowlingEffect` hard-codes:

- `Attributes.ATTACK_SPEED` modifier;
- +0.5 `ADD_MULTIPLIED_TOTAL`.

The exact 2.0.3.3 config separately declares `howling_attackspeed_amount = 2.0`, but the inspected `HowlingEffect` constructor does not consume that setting. Runtime-effective behavior should follow the class/JAR and be QA-verified; Black Arcana must not silently use the apparently intended config value.

`HowlingAction` creates the effect for `(howling_duration + howling_disabled_duration)` seconds — defaults 10 + 10 = 20 seconds — while the effect itself carries the attack-speed modifier for the active instance. The source does not split the final 10 seconds into a no-buff lockout in this class. Treat effective 20-second buff/lock semantics as QA-required.

## Form-native damage reduction

`WerewolfForm` declares base damage reduction:

- `none`: 0%;
- `human`: 5%;
- `beast`: 20%;
- `beast4l`: 30%;
- `survivalist`: 40%.

`ModEntityEventHandler` applies this reduction for Werewolves unless source damage is tagged `WITCH_RESISTANT_TO`.

Additional rules:

- player outside a transformed form + Thick Fur multiplies the provider reduction by default **1.5**;
- if attacker is a Vampire, the reduction is multiplied by **0.3**;
- selected Werewolf attack damage types reduce the target's armor contribution according to attacker level/max level:
  - Werewolf bite path: level ratio ×0.8;
  - other tagged Werewolf armor-reduction path: level ratio ×0.3.

Do not convert this to one unconditional RPG damage-resistance stat.

## Survivalist dodges

While `WerewolfForm.SURVIVALIST`:

- **Arrow Awareness:** if player is moving, provider source gives 40% chance to cancel arrow damage;
- **Movement Tactics:** while sprinting and damage has an entity source, provider default dodge chance is 0.30; Greater Dodge Chance refinement can add provider-configured chance.

These are cancellation mechanics, not armor/resistance amounts.

## Custom attributes — 4/4

| ID | Default | Role |
|---|---:|---|
| `werewolves:bite_damage` | 4 | bite transaction damage basis |
| `werewolves:time_regain` | 0.01 | recovery of transformation-time state |
| `werewolves:food_consumption` | 1 | form/provider food-cost multiplier basis |
| `werewolves:food_gain` | 1 | form/provider food-gain multiplier basis |

Keep these as provider state. Do not merge them into mana, Vampirism blood, stamina or generic RPG attributes without an explicit bridge contract.

## Runtime QA priorities

1. effective Howling radius and attack-speed duration;
2. Howling config-vs-hardcoded amount mismatch;
3. Silver level-scaling and amplifier behavior with installed combat stack;
4. Bleeding tick cadence under high amplifiers and Vampirism blood drain;
5. form damage reduction ordering with Epic Fight and other damage modifiers;
6. Survivalist damage-cancel ordering;
7. infection and cure authority exactly once.