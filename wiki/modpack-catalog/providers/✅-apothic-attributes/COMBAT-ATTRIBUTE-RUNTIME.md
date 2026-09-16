# Combat and attribute runtime — Apothic Attributes 2.10.1

## Event runtime

`AttributeEvents` owns the provider's main gameplay handlers.

| Surface | Provider behavior | Black Arcana boundary |
|---|---|---|
| Draw speed | adjusts use-duration ticks for projectile weapons/tridents | do not reinterpret as BA cast/channel speed |
| Life steal | heals attacker from physical post-damage health loss | BA Backlash must not enter normal offensive lifesteal proc chains |
| Overheal | converts eligible physical damage to absorption, capped by provider logic | do not duplicate settlement |
| Current-HP auxiliary damage | additional provider damage on physical hits | provider-owned damage identity |
| Fire auxiliary damage | provider damage + remaining fire ticks | provider-owned proc; no BA Black Flame identity transfer |
| Cold auxiliary damage | provider damage + movement slowdown | provider-owned proc; no BA Ice/domain identity transfer |
| Crit chance/damage | provider multi-crit loop; extra crit damage diminishes 15% per additional roll | no second BA crit pass |
| Vanilla criticals | provider `crit_damage` may raise vanilla crit multiplier | observe resulting damage, do not recompute |
| Mining speed | multiplies BreakSpeed | non-casting authority |
| Experience gained | multiplies block/mob XP | RPG progression remains separate authority |
| Healing received | multiplies LivingHealEvent amount | provider combat stat authority |
| Arrow damage/velocity | modifies AbstractArrow at spawn | no duplicate projectile scaling |
| Projectile damage | multiplies projectile-owned incoming damage | no duplicate damage multiplier |
| Dodge | cancels eligible melee/projectile hit and supplies sound/particles | provider owns dodge result |
| Item modifiers | bridges vanilla item modifiers into StackAttributeModifiersEvent | attribute composition only |
| Elytra flight | injects provider elytra attribute modifier where applicable | not BA flight/cast authority |
| Aux tracker tick | ticks only entities carrying the attachment | no global BA scan needed |

The auxiliary-damage handler has its own recursion guard. Black Arcana must not route its own terminal Backlash through this offensive provider pipeline.

## Armor and protection authority

`CombatRulesMixin` and `ALCombatRules` replace/redirect core armor and protection calculations.

Default provider rules include:

- protection: 2.5% reduction per effective protection point, capped at 85%;
- protection bypass: `prot_shred` then `prot_pierce`;
- armor bypass: `armor_shred` then `armor_pierce`, with armor toughness reducing bypass effectiveness;
- armor reduction: provider A-value / armor formula;
- negative effective armor: increases incoming damage by `negativeArmorFactor * -armor * amount`;
- armor/protection/toughness formulas are configurable.

These are provider-owned combat rules. BA should consume final server combat facts rather than re-running Apothic formulas.

## Mixins — 7 common + 1 client

1. `CombatRulesMixin` — custom armor/protection formula path.
2. `EntityMixin` — gravity-aware fall-damage motion adjustment.
3. `IItemExtensionMixin` — `elytra_flight` controls elytra capability defaults.
4. `LivingEntityMixin` — Sundering/protection-penetration integration and internal absorption access.
5. `NearestAttackableTargetGoalMixin` — refreshes dynamic follow range before targeting.
6. `PlayerMixin` — aux-damage attack continuation, sweep marker and sneak edge drop cap.
7. `ThrownTridentMixin` — derives trident hit damage from base arrow damage.
8. `client.AbstractContainerScreenMixin` — inventory mouse-drag client shim.

## Sundering

The effect class itself carries no tick implementation; `LivingEntityMixin` applies it inside resistance calculation. When the damage source does not bypass resistance, Sundering adds 20% of initial damage per effect level and participates against Resistance according to provider logic.

## BA authority result

Apothic Attributes is not a safe substitute for BA Arcane Danger or WorldEffectPolicy. It owns generic combat math; BA owns causal forbidden-magic hazards and its no-proc Backlash semantics. Double-processing either side would violate both providers' authority boundaries.
