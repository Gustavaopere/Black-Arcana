# Born in Chaos 1.7.6 — supernatural player-action cards

Status: `17/17 EXACT-CURRENT SEMANTIC ROOTS MATERIALIZED`

Numerical tuning, effect duration, damage and entity lifetime remain provider/config authority. These cards record causal identity, trigger/result shape and catalog-level acquisition only.

### 1. Bone Heart — Bone Barrier
- owner: `born_in_chaos_v1:bone_heart`;
- trigger: direct item use;
- result: grants provider `BONE_BARRIER`, a one-hit protective ward;
- acquisition: exact provider recipe `bone_heart_k`;
- state: `COUNTED_EXACT`.

### 2. Charm of Endurance
- owner: `born_in_chaos_v1:charmof_endurance`;
- trigger: direct charm activation with the provider Ethereal Spirit requirement;
- result: provider Endurance buff action (Speed plus provider-side restoration behavior);
- acquisition: exact Missionary/Missionary Raider loot + rare-loot tags;
- state: `COUNTED_EXACT`.

### 3. Charm of Fury
- owner: `born_in_chaos_v1:charmof_fury`;
- trigger: direct charm activation with Ethereal Spirit;
- result: provider Fury/Rampage buff action and associated restoration;
- acquisition: exact Missionary/Missionary Raider loot + rare-loot tags;
- state: `COUNTED_EXACT`.

### 4. Charm of Strength
- owner: `born_in_chaos_v1:charmof_power`;
- trigger: direct charm activation with Ethereal Spirit;
- result: provider Strength buff action;
- acquisition: exact Missionary/Missionary Raider loot + rare-loot tags;
- state: `COUNTED_EXACT`.

### 5. Charm of Resistance
- owner: `born_in_chaos_v1:charmof_resistance`;
- trigger: direct charm activation with Ethereal Spirit;
- result: provider Resistance buff action;
- acquisition: exact Missionary/Missionary Raider loot + rare-loot tags;
- state: `COUNTED_EXACT`.

### 6. Charm of Stealth
- owner: `born_in_chaos_v1:charmof_stealth`;
- trigger: direct charm activation with Ethereal Spirit;
- result: provider Stealth/Invisibility buff action;
- acquisition: exact Missionary/Missionary Raider loot + rare-loot tags;
- state: `COUNTED_EXACT`.

### 7. Dark Atrium — Dark Ward
- owner: `born_in_chaos_v1:dark_atrium`;
- trigger: direct item activation;
- result: grants provider `DARK_WARD`, whose later lethal-damage response is downstream state settlement;
- acquisition: exact provider recipe `dark_atrium_craft`;
- state: `COUNTED_EXACT`.

### 8. Dark Ritual Dagger — Sacrifice
- owner: `born_in_chaos_v1:dark_ritual_dagger`;
- trigger: provider player `EntityInteract` on an eligible animal/minion;
- result: sacrifice settlement applies provider `SACRIFICE`/benefit state and dagger cooldown/durability;
- acquisition: exact provider recipe `dark_ritual_dagger_k`;
- state: `COUNTED_EXACT`.

### 9. Ethereal Spirit — Pumpkin Spirit Animation
- owner: `born_in_chaos_v1:ethereal_spirit`;
- trigger: use on the provider Evil/Flaming Evil Pumpkin structure surface;
- result: consumes the spirit/block preparation and materializes provider `PUMPKIN_SPIRIT`;
- acquisition: exact current loot across multiple provider spirit entities;
- state: `COUNTED_EXACT`.

### 10. Bonescaller Staff — Controlled Summon
- owner: `born_in_chaos_v1:bonescaller_staff`;
- trigger: use on a block while provider admission permits summoning;
- result: summons provider-controlled Baby Skeletons or the Spiritual Assistant variant under provider equipment conditions, then settles Magic Depletion/durability;
- acquisition: exact provider recipe `staffofthe_summoner_k`;
- state: `COUNTED_EXACT`.

Different minion quantity/type branches are parameters/results of the same staff action, not extra spell identities.

### 11. Fel Lamp — Summon Felsteed
- owner: `born_in_chaos_v1:fel_lamp`;
- trigger: use on a block with filled lamp state;
- result: summons provider `RIDING_FELSTEED` and settles lamp/Magic Depletion state;
- acquisition: exact provider recipe plus Pumpkinhead loot;
- state: `COUNTED_EXACT`.

Capturing/refilling a Felsteed spirit into the empty lamp is setup/state preparation, not a second root.

### 12. Lord Pumpkinhead's Lamp — Summon Lord's Felsteed
- owner: `born_in_chaos_v1:lord_pumpkinheads_lamp`;
- trigger: use on a block with filled lamp state;
- result: summons provider `RIDING_LORDS_FELSTEED` and settles lamp/Magic Depletion state;
- acquisition: exact provider recipe plus Lord Pumpkinhead-head loot;
- state: `COUNTED_EXACT`.

This remains distinct from the ordinary Fel Lamp because the owner and summoned provider entity are distinct.

### 13. Icy Splash
- owners: `born_in_chaos_v1:frostbitten_blade` and `born_in_chaos_v1:icy_sweetness`;
- trigger: direct right-click active ability;
- result: shared provider procedure applies the radial Bone Chilling/freeze action and cooldown, with Nightmare-set scaling retained by the provider;
- acquisition: exact provider recipe for both owners;
- state: `COUNTED_EXACT`.

Both items call the same active procedure, so this is one shared semantic root.

### 14. Pumpkin Staff — Arcane Pumpkin Shot
- owner: `born_in_chaos_v1:pumpkinstaffa`;
- trigger: direct staff use;
- result: fires the provider magical pumpkin projectile; entity-hit explosion and block-hit controlled-Mr.-Pumpkin summon are downstream target branches of this single activation;
- acquisition: exact Pumpkinhead loot;
- state: `COUNTED_EXACT`.

### 15. Staff of Magic Arrows — Magic Arrow
- owner: `born_in_chaos_v1:staff_of_magic_arrows`;
- trigger: direct staff use;
- result: fires the provider Magic Arrow projectile; Spiritual Dust and Nightmare-set state modify the same action rather than minting additional identities;
- acquisition: exact Bonescaller/Supreme Bonescaller loot plus provider recipe;
- state: `COUNTED_EXACT`.

### 16. Stormcaller's Horn — Snow Storm
- owner: `born_in_chaos_v1:stormcallers_horn`;
- trigger: item use/release completion;
- result: applies provider `SNOW_STORM`, with Nightmare-set state modifying duration/cooldown;
- acquisition: exact provider recipe `stormcallers_horn_craft`;
- state: `COUNTED_EXACT`.

### 17. Transmuting Elixir — Transmutation
- owner: `born_in_chaos_v1:transmuting_elixir`;
- trigger: right-click a supported provider block or entity;
- result: transforms the target according to the provider's exact block/entity transformation table and consumes the elixir;
- acquisition: exact provider recipe `transmuting_elixirkraft`;
- state: `COUNTED_EXACT`.

The block and entity handlers are two target routes for the same transmutation action, not separate spell identities.

## Explicit non-roots

- `dark_charge` and debug-style `staffof_blindness` share the provider blindness-projectile family; primary projectile firing is excluded as a standalone spell root.
- `pumpkinhandgun` is a magical ranged weapon, but ordinary primary firing remains a weapon mode.
- bombs/Easter Eggs are throwable projectile modes.
- ordinary drink/food buffs and Magic-Depletion removal are consumable/effect delivery.
- Death Totem, Missionary Hat, Nightmare armor and similar equipment are reactive/passive.
- Nightmare Scythe, Soul Saber/Soulbane, Spider Bite and similar weapon effects are on-hit/proc behavior.
- mob-owned spells and summons are not player-owned semantic roots.

## Result

**17/17 exact-current Born in Chaos player-magic roots materialized.**
