# Weapons of Miracles 2.0.178 — supernatural action cards

Status: `13/13 SUPERNATURAL SEMANTIC ROOTS MATERIALIZED / 12 COUNTED_EXACT + 1 CONDITIONAL`

These cards retain the causal action identity only. Numerical tuning, animation frames, resource values and downstream effects remain WOM/Epic Fight authority.

## Exact current skill-tree actions — 6

### 1. Ender Step
- id: `wom:ender_step`;
- trigger: provider Dodge-skill activation;
- semantic root: Ender-themed instantaneous evasive relocation with provider defensive window;
- acquisition: exact WOM Epic Skills tree;
- state: `COUNTED_EXACT`.

### 2. Ender Obscuris
- id: `wom:ender_obscuris`;
- trigger: provider Dodge-skill activation with a valid recent target;
- semantic root: relocates the player behind the provider-resolved target;
- acquisition: exact WOM Epic Skills tree;
- state: `COUNTED_EXACT`.

### 3. Shadow Step
- id: `wom:shadow_step`;
- trigger: provider Dodge-skill activation;
- semantic root: provider shadow-state evasive action, distinct from an ordinary roll;
- acquisition: exact WOM Epic Skills tree;
- state: `COUNTED_EXACT`.

### 4. Time Travel
- id: `wom:time_travel`;
- trigger: provider Dodge-skill activation;
- semantic root: creates the provider temporal checkpoint using player position/health state;
- acquisition: exact WOM Epic Skills tree;
- state: `COUNTED_EXACT`.

### 5. Voodoo Magic
- id: `wom:voodoo_magic`;
- trigger: deliberate provider input/state while the player is crouching and eligible for the conversion;
- semantic root: provider-owned health↔stamina conversion lifecycle;
- acquisition: exact WOM Epic Skills tree;
- state: `COUNTED_EXACT`.

`Voodoo Magic` is not collapsed into a passive: exact control flow reads deliberate player input/state and performs the conversion. This differs from WOM's registered `PassiveSkill` family and automatic proc identities.

### 6. Avatar of Might
- id: `wom:avatar_of_might`;
- trigger: sustained sneak according to the provider skill;
- semantic root: releases a provider shockwave and grants a temporary defensive/stun-immunity state;
- acquisition: exact WOM Epic Skills tree;
- state: `COUNTED_EXACT`.

## Exact weapon-bound supernatural actions — 6 strict

### 7. Sky Dive
- id: `wom:agony_plunge`;
- owner: `wom:agony`;
- trigger: weapon-innate activation;
- semantic root: provider aerial disappearance/reposition/levitation and dive sequence;
- acquisition: exact provider chest-loot injection for Agony;
- state: `COUNTED_EXACT`.

### 8. True Wrath
- id: `wom:true_berserk`;
- owner: `wom:tormented_mind`;
- trigger: weapon-innate activation;
- semantic root: provider wrath/transformation-style state with its own health/effect/combat lifecycle;
- acquisition: exact provider chest-loot injection for Tormented Mind;
- state: `COUNTED_EXACT`.

### 9. Demonic Ascension
- id: `wom:demonic_ascension`;
- owner: `wom:antitheus`;
- trigger: weapon-innate activation;
- semantic root: provider demonic possession/ascension state with teleport/effect/entity lifecycle;
- acquisition: exact `wom:antitheus` smithing recipe;
- state: `COUNTED_EXACT`.

### 10. Ender Ritual
- id: `wom:plunder_perdition`;
- owner: `wom:ruine`;
- trigger: weapon-innate activation;
- semantic root: provider Ender-arcane ritual action;
- acquisition: exact provider chest-loot injection for Ruine;
- state: `COUNTED_EXACT`.

### 11. Lunar Eclipse
- id: `wom:lunar_eclipse`;
- owner: `wom:moonless`;
- trigger: weapon-innate activation;
- semantic root: lunar supernatural action with provider visibility/status/teleport-style state;
- acquisition: exact provider chest-loot injection for Moonless;
- state: `COUNTED_EXACT`.

### 12. Solar Arcano
- id: `wom:solar_arcano`;
- owner: `wom:solar`;
- trigger: weapon-innate activation;
- semantic root: stellar/solar supernatural action with provider effect/fire-state settlement;
- acquisition: exact `wom:solar` crafting recipe;
- state: `COUNTED_EXACT`.

## Exact identity, reachability still open — 1

### 13. Flash Mutilation
- id: `wom:flash_mutilation`;
- owner: `wom:nova`;
- trigger: weapon-innate activation;
- semantic root: teleport sequence around a target followed by the provider attack settlement;
- identity/binding: exact-current;
- normal acquisition: not closed by the audited exact recipe/chest/drop surfaces;
- state: `CONDITIONAL`.

## Deduplication boundary

Individual teleports, particles, effects, spawned entities, damage events, animation phases and follow-up hits caused by one card are downstream consequences and do not create additional semantic identities.

Ordinary WOM combat techniques and all 10 weapon-passive IDs remain outside this file; their exact dispositions are recorded in [`../skills/SKILL-DISPOSITION-2.0.178.md`](../skills/SKILL-DISPOSITION-2.0.178.md).

## Result

**13 supernatural roots materialized: 12 strict exact-current + 1 reachability-conditional.**
