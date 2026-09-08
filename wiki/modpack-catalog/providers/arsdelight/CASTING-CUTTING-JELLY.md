# Ars Delight 2.2.2 — Enchanter's Knife, Cutting Board and Jelly spell seams

Status: `SOURCE BEHAVIOR CATALOGED / CURRENT-HOST RUNTIME QA OPEN`

## Enchanter's Knife

`EnchantersKnife` extends Farmer's Delight `KnifeItem` and implements Ars Nouveau `ICasterTool`, GeckoLib `GeoItem` and Ars `IManaDiscountEquipment`.

Source behavior:

- stores Ars `SPELL_CASTER` data on the item;
- only accepts a scribed spell whose recipe contains no `AbstractCastMethod`;
- on scribe, prepends Ars `MethodTouch` to the spell recipe;
- the source has its additional Amplify append disabled/commented;
- on `hurtEnemy`, builds an Ars `SpellContext` and uses `SpellResolver`/`EntitySpellResolver` to resolve the spell on the struck target;
- player casters use `PlayerCaster`; other living users use `LivingCaster`;
- `getManaDiscount` returns Ars `AugmentAmplify.INSTANCE.getCastingCost()`;
- inventory ticking calls Ars `RepairingPerk.attemptRepair`.

### Authority consequence

The knife is a provider-native Ars caster surface layered onto an FD knife. Black Arcana must not:

- treat the same melee hit as a second BA cast by default;
- charge a duplicate resource cost/cooldown around the Ars resolver;
- replay the Ars spell effect in an observer;
- copy the source implementation into Black Arcana.

Any future BA interaction must be an explicit observer/boundary around the settled provider action.

## Enchanter's Knife acquisition

`ADApparatusRecipeGen` creates the knife through the Ars Enchanting Apparatus:

- reagent: Farmer's Delight Diamond Knife;
- pedestal: 1 diamond;
- pedestal: 1 gold storage block;
- pedestal: 1 Ars Source Gem Block;
- output: Enchanter's Knife;
- reagent NBT is preserved (`keepNbtOfReagent(true)`).

Ars apparatus learning/crafting and FD tool identity remain provider authorities.

## Spell-aware Cutting Board

`ArsDelightEffectProcessingHandler` subscribes to `EffectResolveEvent.Pre`.

When the ray trace hits a Farmer's Delight `CuttingBoardBlockEntity` and the spell has **no AOE augment**, the provider maps Ars effects to board tools:

- `EffectCut` → shears when Extract is present; otherwise Amplify selects diamond axe + diamond knife fallback, and the base path uses diamond knife + shears fallback;
- `EffectCrush` → diamond shovel;
- `EffectFell` → diamond axe;
- `EffectBreak` → diamond pickaxe.

`ResolveCutting` asks the board to `processStoredItemUsingTool`. The event is cancelled when the provider path reports handled.

### Dedup rule

Cancellation is part of the provider transaction. A BA observer must not execute the original Ars block effect after the board operation has consumed the event.

## Jelly spell context

`JellyBlock` implements Ars `IPrismaticBlock`. When an Ars `EntityProjectileSpell` hits a Jelly on the server:

1. the provider stores a `JellyAttachment` in the projectile spell context;
2. the attachment records the jelly item registry id;
3. the jelly block entity wiggles for presentation/state feedback.

`EffectInfuseMixin` injects at the head of Ars `EffectInfuse.getPotionData`. If the context has the Jelly attachment and the provider can resolve food effects, it returns provider-generated `PotionContents` instead of the normal path.

`JellyAttachment.getData`:

- resolves the jelly item from the built-in item registry;
- reads its food properties;
- rolls each food-effect probability against level RNG;
- copies successful effects with duration divided by four and the same amplifier;
- returns no override if no effects survive.

This context/potion mutation belongs to Ars + Ars Delight. Black Arcana must not introduce a parallel context attachment or second Infuse result.

## Jelly fall behavior

`JellyMethod` separately applies food effects to living entities falling on a jelly on the server, with source duration divided by four and amplifier decremented by one. The exact amplifier-edge behavior and interaction with current Minecraft/host effect semantics is a runtime QA item rather than an inferred correction.
