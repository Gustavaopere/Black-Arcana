# Warp Index / Stabilized Warp Index / Warp Nexus

Status: `SOURCE-PINNED 21.3.0 / SEMANTICS AUDITED / ACQUISITION PARTIAL / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

## Warp Index

Registry id: `ars_additions:warp_index`.

The Warp Index is a remote-access tool for an Ars Nouveau Crafting/Storage Lectern. Shift-use on a valid lectern stores a `WarpBindData` reference containing dimension and block position. Normal use attempts to activate that lectern remotely.

The source explicitly fails closed when:

- no binding exists;
- the bound dimension is unavailable;
- the bound block position is not loaded;
- the bound block is no longer the expected Crafting Lectern.

The base Warp Index also requires the player to be in the same dimension as the stored binding.

## Stabilized Warp Index

Registry id: `ars_additions:stabilized_warp_index`.

`StabilizedWarpIndex` overrides the same-dimension activation check, so the remote lectern may be addressed across dimensions. It does **not** remove the existing loaded-position and valid-block checks in `WarpIndex.activateTerminal`.

Source acquisition from the 21.3.0 Enchanting Apparatus provider:

- Warp Index result: reagent `ars_nouveau:mundane_belt` plus Scry Caster, Scryer's Crystal, Starbuncle Charm and Bookwyrm Charm on pedestals.
- Stabilized Warp Index result: reagent Warp Index plus Netherite Ingot, Nether Star and Ender Chest on pedestals.

## Warp Nexus

Registry id: `ars_additions:warp_nexus`.

Warp Nexus is a separate teleportation surface. The block owns a provider tile and uses the player's `warp_nexus_inventory` attachment, a serializable **9-slot** item handler. Warp Scrolls selected from that attachment are resolved by the provider's server packet.

`TeleportNexusPacket` validates on the server:

1. sender is a server player;
2. the referenced Warp Nexus tile exists;
3. the player is within their current block-interaction range of the Nexus;
4. the requested inventory index is inside the 9-slot attachment;
5. the selected Warp Scroll data is then resolved through provider teleport utilities.

When the Nexus block state has `requires_source=true`, the provider attempts `SourceUtil.takeSourceMultiple` with radius **5** and amount **1000 Source**. Teleport proceeds only when that provider operation succeeds. Generated structures may deliberately set `requires_source=false` through their worldgen processor.

The exact source audit did not yet prove a normal player crafting recipe for the Warp Nexus itself, so acquisition remains `UNPROVEN IN CURRENT SOURCE PASS` rather than invented.

## Black Arcana boundary

- Warp Index remote access is not a spell cast and must not become one in Black Arcana accounting.
- Warp Nexus teleport settlement is provider-owned and server-validated; Black Arcana must not replay teleportation or charge an additional mana/Source/cooldown transaction.
- Presence of a provider force-loading ritual elsewhere in Ars Additions does not grant Black Arcana permission to force-load destinations.
- Any independent Black Arcana displacement still obeys its canonical already-loaded / safe-destination / world-policy contracts.
