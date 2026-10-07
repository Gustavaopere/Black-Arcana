# Ice And Fire: Dread Land 0.1.2 — Dread Portal Activation

Status: `1/1 COUNTED_EXACT`

Individual file:

- [Dreadland Key — Dread Portal Activation](dreadland-key-dread-portal-activation.md)

This file materializes the existing one-root denominator and does not change the +1 strict accounting.

## Identity

**Dread Portal Activation**

- owner item: `iceandfire_dreadland:dreadland_key`;
- provider: `iceandfire_dreadland`;
- semantic class: deliberate supernatural dimensional-portal activation;
- state: `COUNTED_EXACT`.

## Trigger

The player uses the Dreadland Key on a block accepted by the provider `iceandfire_dreadland:dreadland_portal_frame` tag.

## Exact server-side settlement

The exact physical/publisher-matched 0.1.2 artifact closes one causal activation root:

1. validate the clicked frame block;
2. resolve an adjacent valid empty Dread Portal shape;
3. fill the validated shape with provider Dread Portal blocks on the server;
4. consume one Dreadland Key outside creative instabuild;
5. leave later portal collision/delay/dimension transfer to the provider portal lifecycle.

The later Overworld ↔ `iceandfire_dreadland:dreadland` transition is a consequence of the already-created portal and is not counted as a second action.

## Normal acquisition

Normal catalog-level acquisition is closed by exact provider data:

- Fire Dragon trial reward -> `iceandfire_dreadland:fireland_key`;
- Ice Dragon trial reward -> `iceandfire_dreadland:iceland_key`;
- Lightning Dragon trial reward -> `iceandfire_dreadland:lightning_key`;
- ominous trial variants also guarantee the corresponding realm key;
- exact shapeless recipe combines the three realm keys into `iceandfire_dreadland:dreadland_key`.

## Frame contract

The exact provider frame tag accepts seven host-owned Ice And Fire Dread Stone variants. Those blocks are parameters of this activation and do not create seven separate ritual identities.

## Config boundary

Exact common config exposes portal teleport delay and destructive-lightning behavior. No boolean gate removing Dread Portal creation was identified in the exact artifact. Timing configuration does not alter semantic identity count.

## Deduplication boundary

Portal-shape scanning, portal block placement, particle/render feedback, delayed collision handling, exit-portal generation and individual dimension-transfer ticks are infrastructure or downstream consequences of this single activation root.

## Result

**1 exact-current supernatural portal-activation identity.**
