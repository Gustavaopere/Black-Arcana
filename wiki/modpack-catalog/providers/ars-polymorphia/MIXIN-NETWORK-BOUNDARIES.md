# Ars Polymorphia — mixin and network boundaries

Status: `EXACT 1.0.3 SOURCE CATALOGED / CURRENT-HOST MIXIN QA OPEN`

## Mixin inventory — 5

`ars_polymorphia.mixins.json` is required, targets Java 21, and declares four common mixins/accessors plus one client mixin:

Common:

1. `CraftingLecternTileAccessor`
2. `CraftingLecternTileMixin`
3. `CraftingTerminalMenuAccessor`
4. `StorageTerminalMenuAccessor`

Client:

5. `CraftingTerminalScreenMixin`

These are direct mixin bindings to Ars Nouveau storage/crafting internals, so exact runtime compatibility is sensitive to Ars version drift.

## Client screen behavior

`CraftingTerminalScreenMixin` injects after `CraftingTerminalScreen.init` and:

- creates the Polymorph recipes widget for the Ars terminal;
- sends the provider's reset/reselection payload to the server so current recipe state is refreshed.

This is presentation/init behavior only.

## Provider networking

The provider registers protocol version `1` and exactly one provider-owned payload type:

- `ars_polymorphia:reset_crafting_result` — play-to-server, unit payload with no arbitrary recipe/output data fields.

The server handler delegates to `PacketResetCraftingResult.onServerReceived`.

The provider also invokes Polymorph's own server-to-client recipe list/player recipe sync payloads when the lectern crafting matrix changes; those payloads are owned by Polymorph, not Ars Polymorphia.

## Server validation boundary

The provider-owned serverbound payload only settles when the sender currently has an Ars `CraftingTerminalMenu` whose associated block entity is a `CraftingLecternTile`. The actual recipe is then re-obtained from Polymorph's server recipe manager using the current crafting matrix.

No client-provided ItemStack or arbitrary recipe id is trusted as the final craft result by this packet.

## Current-host risks

1. Ars Nouveau source host drift: provider was built against Ars 5.4.2.938; physical pack uses Ars 5.13.1.
2. Dependency-id/API drift: provider declares required mod id `polymorph`; physical top-level pack lists `polymorph_plus` 1.3.1+1.21.1.
3. Mixin failure if Ars renamed/changed `CraftingLecternTile`, terminal menus/screens, fields or methods.
4. Recipe selection becoming stale after datapack reload.
5. Multiplayer contamination if shared terminal state escapes intended UUID/player-scoped resolution.
6. Client ghost output if Polymorph sync and Ars terminal refresh diverge.

## Black Arcana boundary

- Do not bind BA to these mixins/accessors.
- Do not mirror Polymorph selection into BA persistence.
- Do not send a second craft/reset packet after provider settlement.
- Any BA progression hook should consume an already authoritative craft/result event, not participate in recipe conflict choice.
