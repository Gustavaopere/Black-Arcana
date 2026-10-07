# Legendary Monsters 2.2.2 — supernatural action cards

Status: `22/22 COUNTED_EXACT ACTION ROOTS MATERIALIZED`

Individual files:

- [Annihilator Helmet — Targeted Teleport](annihilator-helmet-targeted-teleport.md)
- [Axe of Lightning — Lightning Strike](axe-lightning-strike.md)
- [Axe of Lightning — Electric Burst](axe-electric-burst.md)
- [Buckler of Annihilation — Sweep + Bombs](buckler-annihilation-sweep-bombs.md)
- [Chorus Blade — Random Teleport](chorus-blade-random-teleport.md)
- [Dinosaur Bone Club — Circular Shockwaves](dinosaur-bone-club-shockwaves.md)
- [Entity Warper — Radius Entity Warp](entity-warper-radius-warp.md)
- [Fiery Boots — Fire Trail](fiery-boots-fire-trail.md)
- [Fiery Jaw — Fire Breath + Repulsion](fiery-jaw-fire-breath-repulsion.md)
- [The Great Frost — Directed Ice Spikes](great-frost-directed-ice-spikes.md)
- [The Great Frost — Radial Ice Spikes](great-frost-radial-ice-spikes.md)
- [Guard Summoner — Guard Summon](guard-summoner.md)
- [Knight Summoner — Knight Summon](knight-summoner.md)
- [Monstrous Anchor — Launch + Stun Burst](monstrous-anchor-launch-stun.md)
- [Mossy Chestplate — Poison Cloud Field](mossy-chestplate-poison-field.md)
- [Mossy Hammer — Poison/Moss Shockwave](mossy-hammer-shockwave.md)
- [Soul Great Sword — Phantom Daggers](soul-great-sword-phantom-daggers.md)
- [The Tesseract — Annihilation Portal Star](tesseract-portal-star.md)
- [Totem of Moss — Mossy Golem Summon](totem-moss-golem-summon.md)
- [Void Entity Warper — Targeted Entity Warp](void-entity-warper-targeted-warp.md)
- [Wand of Clouds — Explosive Cloud Summon](wand-clouds-explosive-cloud.md)
- [Teleport Machine + Eye Crystal — Obliterator Summon](teleport-machine-obliterator-summon.md)

These files materialize the existing 22-root denominator and do not change the +22 strict accounting.

Each card represents one player-owned causal supernatural action. Repeated projectiles, particles, waves, summoned-entity attacks, cooldown ticks and other downstream consequences remain provider-owned settlement details rather than additional identities.

## 1. Annihilator Helmet — Targeted Teleport

- owner: `legendary_monsters:annihilator_helmet`;
- trigger: armor ability input;
- semantic settlement: teleports the player to the provider-resolved target/location;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 2. Axe of Lightning — Lightning Strike

- owner: `legendary_monsters:axe_of_lightning`;
- trigger: right-click use;
- semantic settlement: summons the provider lightning-strike settlement;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 3. Axe of Lightning — Electric Burst

- owner: `legendary_monsters:axe_of_lightning`;
- trigger: use on block;
- semantic settlement: launches the provider electric shockwave in the look direction;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 4. Buckler of Annihilation — Sweep + Bombs

- owner: `legendary_monsters:buckler_of_annihilation`;
- trigger: shift + charged use;
- semantic settlement: settles one area sweep and its three annihilation bombs;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 5. Chorus Blade — Random Teleport

- owner: `legendary_monsters:chorus_blade`;
- trigger: right-click use;
- semantic settlement: teleports the player to a provider-selected nearby location;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 6. Dinosaur Bone Club — Circular Shockwaves

- owner: `legendary_monsters:dinosaur_bone_club`;
- trigger: use on block;
- semantic settlement: spawns the provider shockwave action around the user/impact area;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 7. Entity Warper — Radius Entity Warp

- owner: `legendary_monsters:entity_warper`;
- trigger: right-click use;
- semantic settlement: teleports eligible nearby entities to the player;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 8. Fiery Boots — Fire Trail

- owner: `legendary_monsters:fiery_boots`;
- trigger: provider boots ability key;
- semantic settlement: creates the provider fire-column/trail action while moving;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 9. Fiery Jaw — Fire Breath + Repulsion

- owner: `legendary_monsters:fiery_jaw`;
- trigger: right-click use;
- semantic settlement: one activation pushes nearby entities and starts the provider fire-breath settlement;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 10. The Great Frost — Directed Ice Spikes

- owner: `legendary_monsters:the_great_frost`;
- trigger: direct use;
- semantic settlement: creates the directed provider Ice Spike action;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 11. The Great Frost — Radial Ice Spikes

- owner: `legendary_monsters:the_great_frost`;
- trigger: alternate shift/block use;
- semantic settlement: creates the separate radial/surrounding Ice Spike action;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 12. Guard Summoner — Guard Summon

- owner: `legendary_monsters:guard_summoner`;
- trigger: use on block;
- semantic settlement: creates the provider owner-bound/tamed Guard companion;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 13. Knight Summoner — Knight Summon

- owner: `legendary_monsters:knight_summoner`;
- trigger: use on block;
- semantic settlement: creates the provider owner-bound/tamed Knight companion;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 14. Monstrous Anchor — Launch + Stun Burst

- owner: `legendary_monsters:monstrous_anchor`;
- trigger: charged active use;
- semantic settlement: launches/stuns nearby entities as one provider action;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 15. Mossy Chestplate — Poison Cloud Field

- owner: `legendary_monsters:mossy_chestplate`;
- trigger: provider chestplate ability key;
- semantic settlement: spawns the provider poison/shockwave field around the player;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 16. Mossy Hammer — Poison/Moss Shockwave

- owner: `legendary_monsters:mossy_hammer`;
- trigger: use on block;
- semantic settlement: settles provider AoE damage/poison plus moss placement branch;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 17. Soul Great Sword — Phantom Daggers

- owner: `legendary_monsters:soul_great_sword`;
- trigger: shift + charged targeted use;
- semantic settlement: releases the provider homing Phantom Daggers;
- catalog acquisition: exact Possessed Paladin loot;
- state: `COUNTED_EXACT`.

## 18. The Tesseract — Annihilation Portal Star

- owner: `legendary_monsters:the_tesseract`;
- trigger: charged use;
- semantic settlement: summons the provider portal-star/gravity-pull action;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 19. Totem of Moss — Mossy Golem Summon

- owner: `legendary_monsters:totem_of_moss`;
- trigger: use on block;
- semantic settlement: creates the provider owner-bound/tamed Mossy Golem;
- catalog acquisition: exact provider recipe; also appears in exact Mossy Golem loot;
- state: `COUNTED_EXACT`.

## 20. Void Entity Warper — Targeted Entity Warp

- owner: `legendary_monsters:void_entity_warper`;
- trigger: targeted right-click interaction;
- semantic settlement: teleports the selected eligible entity to the player;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 21. Wand of Clouds — Explosive Cloud Summon

- owner: `legendary_monsters:wand_of_clouds`;
- trigger: right-click on entity;
- semantic settlement: summons the provider explosive cloud set above the target;
- catalog acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## 22. Teleport Machine + Eye Crystal — Obliterator Summon

- owner: `legendary_monsters:teleport_machine` + `legendary_monsters:eye_crystal`;
- trigger: Eye Crystal use on inactive Teleport Machine;
- semantic settlement: activates the provider BlockEntity lifecycle and server-spawns `THE_OBLITERATOR`;
- catalog acquisition: Eye Crystal from exact Annihilation Pursuer loot; machine is provider world/structure surface;
- state: `COUNTED_EXACT`.

## Excluded neighboring surfaces

- Atom Splitter beam/bomb modes: primary charged firing modes, not separate magic roots;
- Bottle of Annihilation, Chorus Cannon, Sand Cannon / Hand Cannon and Resurrected Javelin: primary throw/fire modes;
- Withered Scythe forward charge: martial movement/weapon technique;
- Soul Great Sword parry: guard technique;
- Eyes: locators;
- shield/armor/on-hit/on-hurt effects: passive/reactive;
- summon recolor/stand-still/respawn management: management of the already-counted summon, not a second summon;
- `heart_of_tornado`: residual localization/model surface without an exact registered action owner;
- mob-native abilities and all downstream entities/effects: excluded.

## Accounting

- action cards: **22**;
- state: **22 `COUNTED_EXACT`**;
- strict semantic contribution: **+22**.
