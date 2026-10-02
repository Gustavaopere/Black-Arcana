# Alex's Mobs Continued 2.1.13 — supernatural action cards

Status: `3/3 ROOTS MATERIALIZED / 1 COUNTED_EXACT + 2 CONDITIONAL`

These cards retain only the player-owned causal identity. Numerical tuning, entity AI, particles, sounds, costs, config and settlement remain Alex's Mobs Continued authority.

## 1. Transmutation Table — Item Transmutation

- owner surface: `alexsmobs:transmutation_table`;
- trigger: player inserts an eligible item and chooses one of the provider-generated transmutation possibilities in the table menu;
- semantic root: provider replaces the input with the selected transmuted result, charges the configured XP-level cost and rerolls provider result state;
- acquisition: exact shaped provider recipe;
- state: `COUNTED_EXACT`.

Individual input items, displayed candidates, rarity pools, XP amounts, rerolls and result items are parameters of this one transmutation action.

## 2. Mysterious Worm — Void Worm Summoning

- owner: `alexsmobs:mysterious_worm`;
- trigger: deliberate dropped-item summon setup satisfying the provider dimension/depth conditions;
- semantic root: provider consumes the item and server-spawns/configures the Void Worm, crediting the summon advancement to the owner when applicable;
- acquisition: exact Capsid recipe from `alexsmobs:mosquito_larva`; Capsid has exact Enderiophage loot;
- gate: `AMConfig.voidWormSummonable` + `AMConfig.voidWormSpawnDimensions` + provider depth condition;
- state: `CONDITIONAL`.

The identity is exact-current. It contributes +0 strict until deployed effective summon/dimension config is captured.

## 3. Dimensional Carver — Void Portal / Dimensional Passage

- owner: `alexsmobs:dimensional_carver`;
- trigger: deliberate channel/use of the Carver;
- semantic root: provider creates/configures an `EntityVoidPortal` with destination/dimension/lifespan and settles owner durability;
- acquisition: exact shaped recipe using Void Worm Eye + Void Worm Mandible + Netherite;
- dependency: exact Eye/Mandible loot is owned by the Void Worm, whose normal summon path is currently config-conditioned;
- state: `CONDITIONAL`.

Portal entity ticks, particles, portal lifetime, destination coordinates and teleport events are downstream consequences/parameters rather than extra spell identities.

## Explicit non-counted processing

Capsid has four exact transformations, including Mysterious Worm creation, but its interaction is recipe-based timed processing. It is setup/acquisition infrastructure for counted/conditional owners and not a separate player-cast identity.

## Accounting

- supernatural roots: **3**;
- `COUNTED_EXACT`: **1**;
- `CONDITIONAL`: **2**;
- strict semantic contribution: **+1**.
