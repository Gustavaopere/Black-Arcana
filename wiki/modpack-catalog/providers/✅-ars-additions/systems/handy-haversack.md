# Handy Haversack

Status: `SOURCE-PINNED 21.3.0 / STATE+TRANSFER AUDITED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:handy_haversack`.

## Acquisition

The shaped 21.3.0 recipe is:

`sgs / mem / mmm`

where:

- `s` = String;
- `g` = Gold Ingot;
- `m` = Purple Wool;
- `e` = Ender Pearl.

A shapeless clear recipe also exists for the item itself and resets provider-carried configuration according to the recipe output path.

## Persisted state

`HaversackData` stores:

- bound `GlobalPos`;
- target face/direction;
- active flag;
- item filter list;
- cached loaded-state flag.

Shift-use on a block with an item-handler capability binds the Haversack to that container. The filter list is edited through the provider's scribing/use paths. When active, matching picked-up items can be inserted into the bound container.

## No-force-load behavior

`HaversackData.getItemHandler` fails closed unless:

- the player's server exists;
- the stored dimension exists;
- the stored block position is loaded;
- a compatible item-handler capability can be resolved there.

The inventory tick merely observes and records loaded-state changes every 10 game ticks; it does not force-load the target.

## Authority / deduplication

Ars Additions owns the binding, filter and insertion result. Black Arcana must not run a second pickup-transfer path, infer successful remote storage from client state, or force-load the destination to make the provider feature succeed.
