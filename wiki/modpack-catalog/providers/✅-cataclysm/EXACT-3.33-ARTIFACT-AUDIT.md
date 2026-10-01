# L_Ender's Cataclysm 3.33 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / EXHAUSTIVE 67-ITEM-CLASS ACTIVATION INDEX / 27 SEMANTIC ACTION-RITUAL ROOTS`

## Evidence packet

- NON-MERGE audit PR: **#495**;
- final audit HEAD: `b72fc9ff0ffd23da7bccc11363e3fb8c94f8283a`;
- exact-artifact workflow run: `36893767327` — **SUCCESS**;
- same-head Black Arcana CI: `36893767138` — **SUCCESS**;
- evidence artifact: `11178651951`;
- artifact digest: `sha256:7dcec77b436265c83e30481227fc5effc53bc789cb646bcbbf26f1760d5984b7`.

| Field | Value |
|---|---|
| physical SHA-1 | `5ff39c0eddfa08ea0e921bdcb17da7f32f0b00ce` |
| publisher File | CurseForge `551586 / 8706841` |
| publisher SHA-1 | `5ff39c0eddfa08ea0e921bdcb17da7f32f0b00ce` |
| publisher SHA-256 | `23921a268acc8b695291f12e89c5e4c261ee5f59a3b6d763793461efb3e7e1d6` |
| bytes | `73,375,661` |
| equality | **EXACT** |

A later publisher file sharing the 3.33 version label was also tested and failed the physical hash gate. It is excluded from this catalog.

## Exact archive inventory

The exact installed artifact contains:

- **4,236** archive entries;
- **1,313** class files;
- **2,923** non-class resources;
- **67** top-level classes under the provider item package;
- **63** combat projectile/effect classes;
- **899** provider data paths.

The audit ran `javap` across every exact top-level item class and generated an activation index for `use`, `releaseUsing`, `onUseTick`, `finishUsingItem`, `useOn`, `onLeftClick`, `hurtEnemy`, `inventoryTick` and related entrypoints.

Exactly **36 item classes** expose at least one indexed activation/passive surface. That number is structural evidence only; it is not the semantic count.

## Semantic classification rule

The Black Arcana semantic ledger counts discrete provider-owned supernatural player actions and rituals. It excludes:

- item containers by themselves;
- ordinary primary weapon fire/throw modes;
- passive gear and generic on-hit procs;
- pets/familiars/entity containers;
- locators;
- ordinary recipe/process machinery;
- downstream projectiles/statuses/effects;
- parameterizations of one generic infrastructure mechanism.

Applying that rule to every activation-bearing exact class closes **24 item/equipment supernatural action identities**.

## Counted exact item/equipment roots

The exact action roster contains:

1. Ancient Spear — Sandstorm launch;
2. Astrape — Lightning Spear;
3. Bulwark of the Flame — charge;
4. Ceraunus — wave fan;
5. Gauntlet of Bulwark — Blazing push/burst;
6. Gauntlet of Bulwark — charge;
7. Gauntlet of Guard — pull field;
8. Gauntlet of Maelstrom — Void Vortex;
9. Infernal Forge — earthquake;
10. Sandstorm in a Bottle — orbiting sandstorms;
11. Soul Render — Render Rush;
12. Soul Render — Phantom Halberd spiral;
13. The Annihilator — dual-wield charged burst;
14. The Immolator — charged Flame Strike;
15. The Incinerator — Flame Strike line;
16. Tidal Claws — tentacle attack;
17. Tidal Claws — grappling hook;
18. Void Core — Void Rune formation;
19. Void Forge — Void Rune fan;
20. Wrath of the Desert — cursed sandstorm volley;
21. Ignitium Helmet — Blazing Brand key ability;
22. Cursium Helmet — reveal/glowing key ability;
23. Cursium Boots — back-step key ability;
24. Bloom Stone Pauldrons — radial amethyst-cluster key ability.

The exact artifact also exposes the armor input/network seams needed to distinguish the three equipment key actions from passive armor state.

## Acquisition closure

Exact provider data references close catalog-level acquisition for every action-hosting owner:

- crafting/smithing/weapon-infusion routes cover Ancient Spear, Astrape, Bulwark, Ceraunus, both upgraded gauntlets, Soul Render, Annihilator/Immolator, Incinerator, Void Forge, Wrath of the Desert and the three counted armor owners;
- exact boss loot covers Gauntlet of Guard, Infernal Forge, Sandstorm in a Bottle, Tidal Claws and Void Core;
- Bloom Stone Pauldrons has an exact provider recipe.

A provider-data reference to an owner is not automatically treated as acquisition; the audit separately classified recipe output/ingredient and loot-table roles.

## Exact ritual closure

The exact artifact plus release-correlated source close three deliberate ritual-like boss summoning identities:

### Ignis Summoning

- structure reachability: `data/cataclysm/structure/burning_arena2.nbt`;
- altar: provider Altar of Fire;
- deliberate trigger: player inserts Burning Ashes;
- result: timed server-side Ignis spawn;
- offering reachability: exact recipe and Ignited Revenant loot references.

### Leviathan Summoning

- structure reachability: `data/cataclysm/structure/sunken_city_lower.nbt`;
- altar: provider Altar of Abyss;
- deliberate trigger: player inserts Abyssal Sacrifice;
- result: timed server-side Leviathan spawn;
- offering reachability: two exact provider crafting recipes.

### Maledictus Summoning

- structure reachability: `data/cataclysm/structure/frosted_prison_bottom_7.nbt`;
- trigger surface: provider Cursed Tombstone;
- deliberate trigger: player interacts after the tombstone becomes powered by its provider cooldown;
- result: timed server-side Maledictus spawn.

These three add **+3**.

## Boss respawner classification

The provider also has a generic `Boss Respawner` block created after defeated bosses when their respawner config is enabled. Exact release-correlated source closes five parameterizations:

- Ender Guardian + Void Eye;
- The Harbinger + Mech Eye;
- Scylla + Storm Eye;
- Ancient Remnant + Desert Eye;
- Netherite Monstrosity + Monstrous Eye.

The block entity stores a boss EntityType and an item, consumes the matching item on interaction, then re-spawns the configured boss. These are five parameterizations of one generic post-defeat encounter-reset mechanism, not five independent semantic magic identities. They are cataloged as provider progression/world infrastructure and contribute **+0**.

## Other exact-current exclusions

Metric-excluded exact surfaces include conventional projectile/throw/fire behavior, ordinary tool attacks, pet/entity summon containers, Dungeon Eyes, passive equipment, Altar of Void proximity auto-spawn and Altar of Amethyst recipe processing.

Ceraunus illustrates the distinction: its ordinary anchor throw is excluded, while its separate sneaking wave-fan branch is counted.

## Release-correlated source

Source checkpoint used for bounded semantic corroboration:

`lender544/new1.20.1@fe6d06e79d98fcbf22fbd8aee153c65a1d9eb3cd`

This checkpoint is on the official 1.21 line and declares the installed 3.33 release. Later moving-branch changes are not projected backward.

## Clean-room boundary

The durable catalog stores factual identifiers, hashes, counts, semantic classifications and concise behavior summaries. It does not redistribute the third-party JAR, implementation bodies, assets or localization text.

## Result

- exact current item-class surface: **67/67 audited**;
- activation-bearing item classes: **36**;
- counted item/equipment actions: **24**;
- counted deliberate summoning rituals: **3**;
- semantic total: **27 `COUNTED_EXACT`**;
- runtime/integration QA: separate.
