# L_Ender's Cataclysm 3.33 — semantic action cards

Status: `27/27 EXACT-CURRENT SEMANTIC ROOTS MATERIALIZED`

These cards enumerate discrete supernatural player actions and deliberate summoning rituals in the exact installed Cataclysm 3.33 artifact. Numerical tuning remains provider/config authority and is intentionally not frozen here.

## Item and equipment actions — 24

### 1. Ancient Spear — Sandstorm Launch
- owner: `cataclysm:ancient_spear`;
- trigger: charged/eligible left-click action;
- result: launches the provider sandstorm projectile;
- acquisition: exact provider crafting route;
- state: `COUNTED_EXACT`.

### 2. Astrape — Lightning Spear
- owner: `cataclysm:astrape`;
- trigger: charged use then release;
- result: launches the provider lightning-spear attack and settles the provider cooldown;
- acquisition: exact provider crafting route;
- state: `COUNTED_EXACT`.

### 3. Bulwark of the Flame — Charge
- owner: `cataclysm:bulwark_of_the_flame`;
- trigger: sneaking charged release;
- result: starts the provider charge movement/attack state;
- acquisition: exact provider crafting route;
- state: `COUNTED_EXACT`.

### 4. Ceraunus — Wave Fan
- owner: `cataclysm:ceraunus`;
- trigger: charged release while sneaking;
- result: creates the provider wave fan and settles its cooldown;
- acquisition: exact provider crafting route;
- state: `COUNTED_EXACT`.

The non-sneaking anchor throw is an ordinary primary weapon throw mode and is excluded.

### 5. Gauntlet of Bulwark — Blazing Push
- owner: `cataclysm:gauntlet_of_bulwark`;
- trigger: sustained use to the provider threshold;
- result: resolves the nearby push/control burst and Blazing Brand application;
- acquisition: exact weapon-infusion route;
- state: `COUNTED_EXACT`.

### 6. Gauntlet of Bulwark — Charge
- owner: `cataclysm:gauntlet_of_bulwark`;
- trigger: charged non-sneaking release;
- result: starts the distinct provider charge attack state;
- acquisition: exact weapon-infusion route;
- state: `COUNTED_EXACT`.

### 7. Gauntlet of Guard — Pull Field
- owner: `cataclysm:gauntlet_of_guard`;
- trigger: sustained use;
- result: pulls nearby eligible living entities toward the user;
- acquisition: exact Ender Guardian loot route;
- state: `COUNTED_EXACT`.

### 8. Gauntlet of Maelstrom — Void Vortex
- owner: `cataclysm:gauntlet_of_maelstrom`;
- trigger: use/release against a valid block target;
- result: spawns the provider Void Vortex and settles cooldown;
- acquisition: exact weapon-infusion route;
- state: `COUNTED_EXACT`.

### 9. Infernal Forge — Earthquake
- owner: `cataclysm:infernal_forge`;
- trigger: main-hand use on a block;
- result: resolves the provider area earthquake attack and cooldown;
- acquisition: exact Netherite Monstrosity loot route;
- state: `COUNTED_EXACT`.

Ordinary melee/tool behavior remains excluded.

### 10. Sandstorm in a Bottle — Orbiting Sandstorms
- owner: `cataclysm:sandstorm_in_a_bottle`;
- trigger: direct use;
- result: summons two provider sandstorm entities orbiting the user and settles cooldown;
- acquisition: exact Ancient Remnant loot route;
- state: `COUNTED_EXACT`.

### 11. Soul Render — Render Rush
- owner: `cataclysm:soul_render`;
- trigger: charged non-sneaking release;
- result: starts the provider Render Rush movement/attack state;
- acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

### 12. Soul Render — Phantom Halberd Spiral
- owner: `cataclysm:soul_render`;
- trigger: release while sneaking;
- result: resolves the provider radial/spiral Phantom Halberd sequence;
- acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

Individual halberds are downstream substeps, not extra identities.

### 13. The Annihilator — Dual-Wield Burst
- owner: `cataclysm:the_annihilator`;
- trigger: wield the paired owner in both hands and complete the charge;
- result: resolves the provider area burst and cooldown;
- acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

### 14. The Immolator — Flame Strike
- owner: `cataclysm:the_immolator`;
- trigger: dual-wield charged release;
- result: summons the provider Flame Strike and settles cooldown;
- acquisition: exact weapon-infusion route;
- state: `COUNTED_EXACT`.

### 15. The Incinerator — Flame Strike Line
- owner: `cataclysm:the_incinerator`;
- trigger: fully charged release;
- result: creates the provider forward sequence of Flame Strikes and settles cooldown;
- acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

Individual spawned strikes are downstream substeps.

### 16. Tidal Claws — Tentacle Attack
- owner: `cataclysm:tidal_claws`;
- trigger: eligible left-click action;
- result: launches the provider tentacle link/attack toward an eligible target;
- acquisition: exact Leviathan loot route;
- state: `COUNTED_EXACT`.

### 17. Tidal Claws — Grappling Hook
- owner: `cataclysm:tidal_claws`;
- trigger: direct use;
- result: launches the provider grappling hook traversal action;
- acquisition: exact Leviathan loot route;
- state: `COUNTED_EXACT`.

### 18. Void Core — Void Rune Formation
- owner: `cataclysm:void_core`;
- trigger: direct use;
- result: creates the provider Void Rune formation; geometry varies with aim but remains one causal action;
- acquisition: exact Ender Golem loot route;
- state: `COUNTED_EXACT`.

### 19. Void Forge — Void Rune Fan
- owner: `cataclysm:void_forge`;
- trigger: main-hand use on a block;
- result: creates the provider fan of Void Runes and settles cooldown;
- acquisition: exact weapon-infusion route;
- state: `COUNTED_EXACT`.

### 20. Wrath of the Desert — Cursed Sandstorm Volley
- owner: `cataclysm:wrath_of_the_desert`;
- trigger: charged release;
- result: launches the three-part provider cursed-sandstorm volley, optionally homing when a valid target is resolved;
- acquisition: exact weapon-infusion route;
- state: `COUNTED_EXACT`.

The three projectiles are one action result, not three identities.

### 21. Ignitium Helmet — Gaze of Heat
- owner: `cataclysm:ignitium_helmet`;
- trigger: provider helmet ability key;
- result: applies the provider Blazing Brand area ability and settles helmet cooldown;
- acquisition: exact smithing route;
- state: `COUNTED_EXACT`.

### 22. Cursium Helmet — Ghost Vision
- owner: `cataclysm:cursium_helmet`;
- trigger: provider helmet ability key;
- result: reveals nearby living entities through the provider glowing/reveal action and settles cooldown;
- acquisition: exact smithing route;
- state: `COUNTED_EXACT`.

### 23. Cursium Boots — Back-Step
- owner: `cataclysm:cursium_boots`;
- trigger: provider boots ability key while grounded;
- result: performs the provider backward evasive movement and settles cooldown;
- acquisition: exact smithing route;
- state: `COUNTED_EXACT`.

Passive fall-damage behavior is not counted again.

### 24. Bloom Stone Pauldrons — Amethyst Cluster Burst
- owner: `cataclysm:bloom_stone_pauldrons`;
- trigger: provider chest ability key;
- result: launches the provider radial amethyst-cluster burst and settles cooldown;
- acquisition: exact provider recipe;
- state: `COUNTED_EXACT`.

## Deliberate summoning rituals — 3

### 25. Ignis Summoning
- owner: Cataclysm Altar of Fire encounter surface;
- trigger: player inserts `cataclysm:burning_ashes`;
- result: timed altar sequence culminates in provider-owned Ignis spawn;
- world reachability: exact Burning Arena structure NBT;
- offering reachability: exact provider recipe/loot references;
- state: `COUNTED_EXACT`.

### 26. Leviathan Summoning
- owner: Cataclysm Altar of Abyss encounter surface;
- trigger: player inserts `cataclysm:abyssal_sacrifice`;
- result: timed altar sequence culminates in provider-owned Leviathan spawn;
- world reachability: exact Sunken City structure NBT;
- offering reachability: two exact provider crafting recipes;
- state: `COUNTED_EXACT`.

### 27. Maledictus Summoning
- owner: Cataclysm Cursed Tombstone encounter surface;
- trigger: deliberate player interaction after the provider cooldown powers the tombstone;
- result: timed sequence culminates in provider-owned Maledictus spawn;
- world reachability: exact Frosted Prison structure NBT;
- state: `COUNTED_EXACT`.

## Explicit exclusions

The following remain cataloged provider gameplay but add zero semantic identities under the current metric:

- ordinary Ceraunus/Brontes/Coral weapon throws;
- primary Cursed Bow, Laser Gatling, Meat Shredder and shoulder-weapon firing modes;
- Dungeon Eye locator use;
- skull/effigy/bucket entity materialization;
- passive armor/Curios/on-hit effects;
- Altar of Void proximity auto-spawn;
- Altar of Amethyst recipe processing;
- the generic post-defeat Boss Respawner and its five boss/Eye parameterizations.

## Result

**27/27 exact-current semantic roots materialized: 24 item/equipment actions + 3 deliberate summoning rituals.**
