# Warp Scroll Holder

State: `SOURCE-PINNED 1.6.15 / ARS PORTAL WRAPPER / RUNTIME QA PENDING`

Registry id: `ars_controle:scroll_holder`
Block entity: `ars_controle:scroll_holder` -> `ScrollHolderTile`
Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

## Acquisition

Vanilla shaped crafting:

`sss / s s / sss`

where `s = ars_nouveau:sourcestone_slab`.

Result: 1 × `ars_controle:scroll_holder`.

## Accepted item

The single-slot holder accepts only an item carrying Ars Nouveau `WARP_SCROLL` data that exists and reports valid. Ars Controle exposes that slot as a NeoForge item handler.

The destination data remains Ars Nouveau Warp Scroll data; Ars Controle does not invent a parallel destination format.

## Portal construction

If Ars Nouveau `ENABLE_WARP_PORTALS` is disabled, holder updates do not create the portal.

The tile searches provider-defined frame orderings built from another Scroll Holder and/or Ars decorative blocks. Each scanned edge is bounded by `22` steps; accepted dimensions must also fall between `2` and `22` blocks for the checked spans.

When a valid frame contains a scroll, empty interior cells become Ars Nouveau `PortalBlock` instances. Each new `PortalTile` receives the original Warp Scroll data, optional custom display name and horizontal/orientation state.

Removing the scroll causes existing Ars Portal blocks in the interior to be removed by the holder update path.

## Source settlement

Default `scroll_holder.cost = 1000` Source.

When a non-empty scroll would create a fresh portal interior, the code determines whether Source is needed and attempts the provider Source withdrawal once before filling the remaining interior cells. Existing portal cells can suppress the new activation charge for that update.

This Source settlement is Ars/Ars Controle-owned and must not be duplicated.

## Optional ComputerCraft surface

When `computercraft` is loaded, a peripheral exposes the stored Warp Scroll target as provider data including stability/cross-dimension flag, dimension, position and rotation.

ComputerCraft is absent from the current physical modlist, so this is not an active pack surface at this checkpoint.

## Boundary

- Ars Nouveau owns Warp Scroll destination semantics and PortalBlock/PortalTile behavior.
- Ars Controle owns holder/frame assembly and its activation Source charge.
- Black Arcana Stage 07.04 keeps independent safe-destination, consent, throughput and no-force-load contracts.
- The presence of an Ars portal is not permission to bypass `WorldEffectPolicy` or Black Arcana teleport admission.

## QA pending

1. Validate frame shapes/orientations and the 2–22/22-step bounds in the installed JAR.
2. Validate Source charging when reopening partially existing portals.
3. Validate portal cleanup after scroll removal/chunk reload.
4. Test interaction with Ars Two-Way Portals and other installed portal addons separately; thematic proximity is not compatibility evidence.
