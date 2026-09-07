# Mobstein 5.4.4 — resurrection and experiment catalog

## Evidence boundary

This inventory is derived from the publisher-maintained CurseForge guide for the exact 1.21.1 release line plus the current installed modlist. It is a player-facing semantic catalog, not a source-code/API inventory.

The following remain `UNVERIFIED` unless the publisher explicitly states them: registry IDs, exact attributes, AI internals, internal cooldowns, event classes, persistence schemas, damage formulas and external API hooks.

## 1. Clinical Stretch resurrection

Publisher flow:

1. craft/place the Clinical Stretch;
2. perform the normal full-body resurrection route at night;
3. place a supported full body in the middle;
4. remain at the apparatus for approximately 15 seconds;
5. the documented lightning event completes the resurrection.

The separate Lightningbolt Syringe is documented as allowing a stretcher resurrection during daytime. These routes remain Mobstein-owned; Black Arcana must not synthesize a parallel resurrection transaction around them.

### 1.1 Resurrected forms

| Form | Public tame/input | Public behavior |
|---|---|---|
| Axolotl Resucited | Tropical Fish | can sit; bucket transport; nearby regeneration and night vision |
| Dolphin Resucited | any uncooked fish | rideable; water breathing; fast water movement |
| Bat Resucited | Pumpkin Pie | flying attack behavior; can sit |
| Putrid Horse | Rotten Flesh | fast/high-jump mount; approximately five cosmetic decay stages; own interface; no armor |
| Ocelot Resucited | Raw Salmon | very fast; can sit; dyeable collar |
| Villager Resucited | Rotten Flesh | kills may drop one of the provider's three organs |
| Silver fish Resucited | Stone Block | nearby cave-mining speed utility; can sit |
| Warden Resucited | Echo Shard | powerful stationary bodyguard; no vanilla sonic boom; excluded from Reviver Syringe resurrection |
| Frankenstein Resucited | Iron Ingot | stationary bodyguard; nearby `Blacksmithstrength` is described as granting speed; excluded from Reviver Syringe resurrection |
| Rabbit Resucited | Carrots | nearby jump boost; can sit |

### 1.2 Authority notes

- Taming, sit/follow/bodyguard state are Mobstein-owned.
- Do not infer exact owner UUID storage or event hooks from the guide.
- Companion auras are provider effects. A Black Arcana adapter must not reapply the same regeneration/night vision/water-breathing/mining/jump effect.
- Warden/Frankenstein revive exclusions are provider rules and must not be bypassed by a generic Black Arcana resurrection fallback.

## 2. Mob parts, full bodies and organs

Publisher-documented material/interactions include:

| Source | Public material/interation |
|---|---|
| Piglin | Piglin Chop; cookable into Cooked Piglin Chop |
| Polar Bear | Polar Bear Leather |
| Panda | Panda Leather |
| Villager | nose harvested with shears |
| Spider / Cave Spider | legs harvested with shears |
| Dolphin | Dolphin Tail |
| Horse | Horse Leather |
| Axolotl | Axolotl Gill |
| Bat | Bat Wings and Bat Fangs |

Additional documented system behavior:

- normal leather is cooked for some body recipes;
- Full Body Support stores/hangs full bodies; shears remove them;
- Organ Extractor consumes/interacts with a full body using tweezers and randomly provides one of three organs;
- Resurrected Villager provides an alternate kill-driven organ route;
- Jar stores organs.

The exact three organ item names/registry IDs are not asserted here because the publisher guide only establishes the three-organ cardinality in the relevant passages.

## 3. Surgery Stretch construction

The Surgery Stretch is a separate provider construction flow from Clinical Stretch resurrection.

### 3.1 Mobstein construction perks

The official guide calls four construction inputs `perks`:

| Provider perk | Public value/role |
|---|---|
| Health | `20–40` |
| Attack | `0.8–2` |
| Speed | `0.3–0.5` |
| Template | used to create the other perks |

These values belong to Mobstein's own constructed-creature system. They are not RPG Skill Tree ranks and must not be imported as general player attributes.

### 3.2 Constructed types

| Type | Public tame/input | Public capability |
|---|---|---|
| Turtle | Seagrass | regeneration, luck and water breathing |
| Panda | Bamboo | strength and resistance |
| Polar Bear | uncooked fish | Dolphin's Grace |
| Spider | Egg | rideable; wall climbing; may place web when hit |
| Enderman | Grass Block | random teleport; night vision |
| SnowGolem | not specified in guide | strong defensive creature; public warning that spawning can break the Surgery Stretch |

Publisher constraints:

- player heads cannot be used on Surgery Stretch;
- torsos and pants cannot be used there.

Exact construction formulas, internal attribute application and persistence remain unverified.

## 4. Subject Assembly Machine

The publisher distinguishes this from Surgery Stretch:

- it creates a mannequin rather than an ability-bearing experiment;
- any game head may be used;
- the Head Creator accepts a player head + brain and a typed player name to produce the selected player head;
- head + torso + pants are then used for mannequin assembly;
- the guide states this route has **no abilities**.

This is a body-assembly/content system. No FE, SU, network-power or machine API contract is established by the public documentation.

## 5. Failed experiments

The guide describes seven public failed-experiment variants.

| Experiment | Public tame/input | Public behavior / route |
|---|---|---|
| 097 | Slime Balls | passive Endermite/Frog mix; random jumps; wanders; found in Frankenstein Castle |
| 062 | Cocoa Beans | passive Cod/Cocoa-block mix; wanders; found in Frankenstein Castle |
| 067 | Seeds | passive Chicken/Enderman mix; random teleport including when hit; Igor's table route |
| 077 | Seeds | Allay/Parrot mix; flies; melee attack; no item pickup/shoulder behavior; Igor's table route |
| 091 | Strawberries | partially passive Fox/Dragon mix; attacks chickens; cannot jump; Igor's table route |
| 012 | Wheat | passive Llama/Mooshroom mix; bowl/bucket interaction; no llama spit; Igor's table route |
| 007 | any Flower | passive Villager/Bee mix; does not lose a stinger; guide says it wanders rather than behaving like a normal bee; Igor's table route |

The guide characterizes the failed experiments as useful bodyguards. Exact target-selection, faction, friendly-fire and ownership semantics remain runtime QA items.

## 6. Dr. Mobstenio and Igor

### Dr. Mobstenio

Public progression:

- found in Frankenstein Castle;
- revived with Mobstenio Blood Syringe;
- tamed with Wither Spores obtained after defeating Witherstein;
- revived/tamed NPC wanders and does not follow.

### Igor

Public progression:

- summoned from Igor Spawner;
- not tameable;
- requires Igor's table;
- creates random failed experiments after Suspicious Syringes are thrown at him;
- first attempt is described as always failing;
- must be near the table;
- 062 and 097 are excluded from Igor's creation route;
- the guide states several Suspicious Syringes are needed, up to a maximum of four.

Do not infer a stable event/API for either NPC from these public gameplay rules.

## 7. Syringe catalog

| Syringe | Publisher-documented role |
|---|---|
| Empty Syringe | base/empty item |
| Reviver Syringe | resurrects mobs subject to provider exclusions; also awakens Witherstein from its skeleton |
| Mobstenio Blood Syringe | revives Dr. Mobstenio in Frankenstein Castle |
| Lightningbolt Syringe | allows stretcher resurrection during daytime |
| Suspicious Syringe | thrown at Igor to drive random-experiment creation |

The phrase “any mob” in the public Reviver description is bounded by the same guide's explicit Warden/Frankenstein exclusions and must not be expanded by Black Arcana into unsupported provider targets.

## 8. Structures and Witherstein

### Structures

- Frankenstein Castle — Swamp;
- Witherstein Ruins — Jungle;
- Old Ruins — Jungle.

### Witherstein

Publisher flow:

1. locate the skeleton at the center of Witherstein Ruins;
2. use Reviver Syringe;
3. encounter progresses through three stated stages;
4. later stages spawn Wither Skeletons.

Wither Spores are part of the documented Dr. Mobstenio taming path after defeating Witherstein.

Exact boss attributes, attack cadence, stage thresholds, spawn counts, loot tables and repeatability are not public contracts in the audited material and remain `UNVERIFIED`.

## 9. Deduplication consequences

Mobstein already provides concrete semantics for:

- full-body resurrection;
- corpse/body-part processing;
- organ harvesting;
- constructed undead/experimental companions;
- tameable bodyguards and utility pets;
- daytime/nighttime resurrection variants;
- resurrection exclusions;
- resurrection-triggered boss activation.

Therefore a Black Arcana concept in the same fantasy space requires a demonstrable semantic delta, not merely a different particle/color/name. Integration must preserve Mobstein as causal owner of its bodies, companions, organ drops, experiments and encounter lifecycle.