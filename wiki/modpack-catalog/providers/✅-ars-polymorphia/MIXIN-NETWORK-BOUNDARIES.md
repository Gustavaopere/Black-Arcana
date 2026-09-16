# Ars Polymorphia — mixin and network boundaries

Status: `EXACT 1.0.3 SOURCE CATALOGED / RUNTIME COMPATIBILITY FAIL-CLOSED`

Exact source: `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`.

## Direct mixin footprint

`ars_polymorphia.mixins.json` is required, targets Java 21 and declares exactly five direct integration classes:

Common:

1. `CraftingLecternTileAccessor`
2. `CraftingLecternTileMixin`
3. `CraftingTerminalMenuAccessor`
4. `StorageTerminalMenuAccessor`

Client:

5. `CraftingTerminalScreenMixin`

Because these target Ars Nouveau storage/crafting internals directly, permissive dependency ranges are not treated as proof that the physical Ars `5.13.1` host remains ABI/mixin compatible with a provider built against Ars `5.4.2.938`.

## Provider networking

The exact source registers payload protocol version `1` and exactly one provider-owned payload:

- `ars_polymorphia:reset_crafting_result` — play-to-server, unit codec.

The server handler delegates to provider logic after resolving the server-side player. Polymorph-owned recipe-list/player-selection sync payloads used elsewhere remain Polymorph infrastructure and are not counted as Ars Polymorphia-owned payload identities.

## Server validation boundary

The provider reset packet does not carry a client-chosen ItemStack or arbitrary recipe id. Settlement requires an Ars crafting terminal backed by an Ars crafting lectern, then re-resolves the valid recipe through Polymorph against the current crafting matrix.

That is sufficient to classify the source architecture, but not to certify current-host runtime behavior.

## Current physical-host risks

- source metadata requires dependency mod id `polymorph`; physical modlist exposes `polymorph_plus` `1.3.1+1.21.1`;
- source build host Ars Nouveau `5.4.2.938`; physical Ars Nouveau `5.13.1`;
- source declares `minecraft_version=1.21.1` while its declared range is `[1.21,1.21.1)`;
- five required mixin targets make host drift materially relevant.

No dependency alias, mixin compatibility, client startup or dedicated-server startup PASS is inferred without direct current-host evidence.
