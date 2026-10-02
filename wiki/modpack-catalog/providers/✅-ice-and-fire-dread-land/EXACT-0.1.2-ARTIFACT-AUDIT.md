# Ice And Fire: Dread Land 0.1.2 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / PLAYER-ACTIVATION + PORTAL-PROGRESSION DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `iceandfire_dreadland-0.1.2.jar`;
- mod id: `iceandfire_dreadland`;
- runtime: `0.1.2`;
- physical SHA-1: `1790b22e21c69485d582b9da50174339a9dc994c`.

NON-MERGE PR #513 audits CurseForge File `1664091 / 8708824` and hard-fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Final exact audit:

- HEAD: `f5e95a4b7c7095e0c10e8998ca33346593201ad3`;
- run: `36953394134` — SUCCESS;
- artifact: `11204564418`;
- artifact digest: `sha256:60f2af0bc1ae7eaa44e30372eaeb3ce9a834bb3789c80d6efafed116031048af`;
- publisher SHA-1: `1790b22e21c69485d582b9da50174339a9dc994c`;
- publisher SHA-256: `110090646adbda8d5dc5f6cdd1cef17ea6b5c37a01e05d93909c9e5a600a8db4`;
- bytes: `680,235`.

Result: exact publisher/physical equality is proven.

## Bounded archive inventory

- archive entries: **303**;
- classes: **32**;
- non-class resources: **271**;
- top-level item classes: **3**;
- block classes: **3**;
- provider/data paths: **197**.

## Exhaustive player-activation surface

Exact signature inspection finds only two item classes with player activation: `DreadQueenPortraitItem.useOn` and `DreadlandKeyItem.useOn`. Plain `KeyItem` only contributes tooltip presentation, so Fireland/Iceland/Lightning keys do not expose independent player-action roots.

### Dread Queen Portrait

The exact use path validates placement space, places a 3×3 portrait block surface server-side, emits ordinary placement feedback and consumes the item. It is decorative placement and is excluded.

### Dreadland Key

The exact use path:

- requires the clicked block to match `iceandfire_dreadland:dreadland_portal_frame`;
- resolves a valid empty `DreadPortalShape` adjacent to the clicked face;
- server-side creates the provider portal blocks;
- consumes one Dreadland Key outside creative instabuild;
- settles as one successful portal activation.

The portal data lifecycle subsequently handles delayed dimension transition between Overworld and `iceandfire_dreadland:dreadland`. Travel is downstream settlement of the same action, not a second identity.

## Exact key progression / reachability

The exact artifact closes normal owner acquisition:

- Fire Dragon trial reward guarantees `iceandfire_dreadland:fireland_key`;
- Ice Dragon trial reward guarantees `iceandfire_dreadland:iceland_key`;
- Lightning Dragon trial reward guarantees `iceandfire_dreadland:lightning_key`;
- ominous variants also guarantee their corresponding realm key;
- exact shapeless recipe combines all three into `iceandfire_dreadland:dreadland_key`.

## Exact frame contract

The portal-frame tag accepts seven host-owned Ice And Fire blocks: `dread_stone`, `dread_stone_bricks`, `dread_stone_bricks_chiseled`, `dread_stone_bricks_cracked`, `dread_stone_bricks_mossy`, `dread_stone_tile` and `dread_stone_face`.

These are frame parameters supplied by the Ice And Fire host; they are not seven additional Dread Land actions.

## Config boundary

Exact common config exposes portal teleport delay and destructive-lightning behavior. No boolean registration/activation gate removing Dread Portal creation was identified. Teleport delay changes timing only and does not remove the action identity.

## Semantic disposition

- Dreadland Key — Dread Portal Activation: **1 `COUNTED_EXACT`**;
- Dread Queen Portrait: **EXCLUDED**;
- realm keys: **SETUP / PROGRESSION EXCLUDED**;
- portal blocks, shape validation, transition ticks, exit structure, particles and rendering: **INFRASTRUCTURE / CONSEQUENCE EXCLUDED**.

Strict semantic contribution: **+1**.

## Clean-room boundary

The durable catalog retains hashes, identifiers, counts, resource IDs, control-flow seam facts and behavior-level classification needed for cataloging. It does not redistribute the third-party JAR or assets.
