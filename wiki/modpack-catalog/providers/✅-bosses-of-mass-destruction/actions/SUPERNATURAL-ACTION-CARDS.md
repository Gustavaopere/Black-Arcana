# Bosses of Mass Destruction 1.3.3 — supernatural action cards

Status: `5/5 ROOTS MATERIALIZED / 3 COUNTED_EXACT + 2 CONDITIONAL`

## 1. Obsidilith Summoning

- provider trigger: Eye of Ender used on the provider Obsidian Altar / `obsidilith_end_frame`;
- server settlement: consumes the eye, schedules the summon event, removes/replaces the frame and creates the Obsidilith entity;
- packaged reachability: exact Obsidilith arena/worldgen resources;
- state: `COUNTED_EXACT`.

## 2. Earthdive Wall Teleport

- owner: Earthdive Spear;
- trigger: charge and release provider item use;
- settlement: provider `WallTeleport` attempts short-range teleport through solid geometry;
- exact acquisition: shaped recipe using Obsidian Heart + Void Thorn + Stick; exact provider data supplies Obsidian Heart in the Obsidilith arena chest and Void Thorn from Void Blossom loot;
- state: `COUNTED_EXACT`.

## 3. Brimstone Structure Restoration

- owner: Brimstone Nectar;
- trigger: deliberate item use near an eligible BOMD structure;
- settlement: resolves damaged/resettable provider structures and schedules their provider-owned repair operation, with cooldown and item consumption;
- exact acquisition: shapeless Netherite Scrap + Dragon's Breath + Ghast Tear;
- state: `COUNTED_EXACT`.

## 4. Night Lich Summoning

- owner/setup item: Soul Star;
- trigger: Soul Star used on the provider Chiseled Stone Altar network;
- settlement: consumes/activates altar state and schedules Night Lich spawning after the required altar arrangement is filled;
- config gate: exact provider config exposes `lichConfig.summonMechanic.isEnabled`; binary default is true, but deployed effective value is not captured;
- normal Soul Star production is tied to that summon mechanic;
- state: `CONDITIONAL`.

## 5. Charged Ender Pearl Teleport

- owner: Charged Ender Pearl;
- trigger: deliberate item throw/use;
- settlement on impact: teleports owner, resets fall distance, grants provider Resistance/Slow Falling effects and applies nearby knockback;
- exact recipe: Void Thorn + vanilla Ender Pearl + Ancient Anima;
- reachability gate: exact normal Ancient Anima source is Lich entity loot, so current normal acquisition inherits the unresolved Night Lich summon gate;
- state: `CONDITIONAL`.

## Explicit exclusions

- Soul Star locator launch toward the Lich tower is navigation, not a second magical action;
- Void Blossom spawning from its arena block is proximity-triggered automatically, not a deliberate player summon;
- Levitation Block, Mob Ward and Monolith are passive/environmental infrastructure;
- boss attacks/projectiles and downstream teleport/effect/particle events do not mint additional roots.

## Accounting

- supernatural roots: **5**;
- `COUNTED_EXACT`: **3**;
- `CONDITIONAL`: **2**;
- strict semantic delta: **+3**.
