# Mobstein 5.4.4 — corporeal resurrection and resurrected mobs

## Evidence status

`PUBLISHER PUBLIC GUIDE / EXACT 5.4.4 RELEASE LINE / REGISTRY IDS UNVERIFIED / RUNTIME QA PENDING`

This inventory uses the official Mobstein CurseForge guide and exact 5.4.4 release metadata. It does not use decompiled ARR bytecode.

## Clinical Stretch resurrection

The provider's ordinary revival presentation is explicitly body-based:

- a compatible full body is placed on the **Clinical Stretch**;
- the public guide instructs using it at night;
- the guide describes a wait of about **15 seconds**;
- lightning accompanies the resulting resurrection.

The **Lightningbolt Syringe** is separately documented as a daytime resurrection route.

Exact server timing, event ownership, recipe IDs and internal eligibility predicates remain unverified.

## Resurrected Axolotl

Publisher-documented behavior:

- can sit;
- can be carried with a bucket;
- tamed with Tropical Fish;
- when tamed and nearby, grants Regeneration and Night Vision.

Black Arcana consequence: this is an existing resurrection-companion + beneficial-aura capability. Do not add a duplicate generic resurrected familiar whose identity is only “small revived creature that buffs nearby owner.”

## Resurrected Dolphin

Publisher-documented behavior:

- rideable;
- provides Water Breathing while used as documented;
- fast aquatic movement;
- tamed with uncooked fish.

This occupies a revived aquatic mount/utility niche.

## Resurrected Bat

Publisher-documented behavior:

- can attack while flying;
- can sit;
- tamed with Pumpkin Pie.

This occupies a small aerial reconstructed-companion combat niche.

## Putrid Horse

Publisher-documented behavior:

- approximately five visual rotting/decomposition stages;
- those visual stages are explicitly described as giving no gameplay advantage;
- green-particle presentation;
- provider-specific interface controlled through Mobstein keys;
- high jump and high speed;
- cannot equip horse armor;
- tamed with Rotten Flesh.

The visual decomposition stages must not be misrepresented as a hidden stat progression system.

## Resurrected Ocelot

Publisher-documented behavior:

- tamed with Raw Salmon;
- collar can be dyed;
- can sit;
- high movement speed.

## Resurrected Villager

Publisher-documented behavior:

- tamed with Rotten Flesh;
- functions as an organ-farm support creature;
- killed mobs have a chance to yield one of the provider's organ types.

This is an important acquisition authority surface: Black Arcana should not independently duplicate the same organ-drop automation to make Mobstein progression easier unless an explicit compatibility design requires it.

## Resurrected Silverfish

Publisher-documented behavior:

- tamed with Stone;
- can sit;
- grants a nearby fast cave-mining/mining utility effect according to the public guide.

Exact effect registry id/value is not publicly established in this checkpoint.

## Resurrected Warden

Publisher-documented behavior:

- tamed with Echo Shards;
- very strong bodyguard role;
- does not follow the owner in the ordinary companion pattern described by the guide;
- does not use the vanilla Warden sonic-boom behavior;
- cannot be revived with the Reviver Syringe.

The inability to use the Reviver Syringe is a provider-owned exception and should be preserved in any future compatibility design.

## Frankenstein Resucited / Golem

Publisher-documented behavior:

- tamed with Iron Ingots;
- has multiple aesthetic/suit presentations plus a carved-pumpkin easter egg;
- bodyguard role;
- does not follow in the ordinary companion pattern;
- drops Screws and Infested Iron Ingots;
- grants the nearby `Blacksmithstrength` effect according to the publisher guide;
- the guide describes that effect as giving **speed**, despite the strength-like naming/icon presentation;
- cannot be revived with the Reviver Syringe.

Because the public name/presentation and described behavior are internally surprising, Black Arcana records the publisher text rather than “correcting” it to Strength.

## Resurrected Rabbit

Publisher-documented behavior:

- tamed with Carrots;
- grants nearby Jump Boost;
- can sit.

## Authority conclusions

Mobstein owns the lifecycle and gameplay identity of these reconstructed mobs. If Black Arcana later reacts to them, it should do so through an approved provider boundary and preserve Mobstein ownership/taming/lifecycle.

Specifically, Black Arcana must not:

- respawn Mobstein companions from its own soul ledger;
- infer ownership from proximity;
- award repeated mastery from continuous aura ticks;
- clone or replace provider tame state;
- bypass provider exceptions such as Warden/Frankenstein Reviver restrictions;
- create offensive proc chains merely because a Mobstein companion dealt damage, unless a causal integration contract explicitly allows that credit.