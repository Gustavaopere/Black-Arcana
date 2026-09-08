# Ars Portals on moving contraptions

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Ars Creo registers movement + collision behavior for the existing Ars Nouveau Portal Block and marks Portal/Ritual blocks movement-allowed through Create's movement check.

Portal destination data is reconstructed from stored NBT (`warp`, dimension id, rotation/display/horizontal fields). Entity transfer delegates to Ars `PortalTile.teleportEntityTo` rather than implementing a second teleport engine.

The behavior ignores the contraption entity itself and processes entities occupying the moving portal cell through tick/new-position and moving-collision paths.

This proves moving Ars portal support, not Black Arcana displacement authorization. Cross-dimensional safety, claims and full-pack portal-addon interaction remain runtime QA.