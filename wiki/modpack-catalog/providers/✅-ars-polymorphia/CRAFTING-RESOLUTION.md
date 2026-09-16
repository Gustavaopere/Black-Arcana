# Ars Polymorphia — crafting resolution

Status: `EXACT 1.0.3 SOURCE CATALOGED / CURRENT HOST QA OPEN`

Exact source: `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`.

## Server-side matrix observation

The exact 1.0.3 source injects at the head of Ars Nouveau `CraftingLecternTile.onCraftingMatrixChanged(UUID)`.

The provider resolves the server/player context, obtains that player's lectern crafting inventory and Polymorph selection state, asks the server recipe manager for matching crafting recipes, excludes empty results, preserves a previously selected recipe when it remains valid, and synchronizes the resulting conflict set through Polymorph-owned payloads.

Candidate outputs are therefore derived from the server recipe manager rather than invented by Ars Polymorphia.

## Player-scoped intent

The lectern inventory is queried with the player UUID and Polymorph selection state is read from that player. The source intent is player-scoped even when the underlying Ars storage infrastructure is shared.

This source fact does not replace multiplayer runtime QA. Two-player same-lectern isolation under the current Ars/Polymorph+ host versions remains unverified.

## Provider reset payload

Ars Polymorphia owns one serverbound unit payload: `ars_polymorphia:reset_crafting_result`.

The payload contains no client-supplied output stack and no arbitrary recipe-id field. Its server handler proceeds only when the sender currently has an Ars `CraftingTerminalMenu` backed by a `CraftingLecternTile`.

The handler then asks Polymorph's recipe manager for the player's valid crafting recipe against the current matrix and level. An unresolved recipe is a no-op. On success the provider updates Ars `currentRecipe`, invokes the Ars crafting-matrix refresh, and records the selected recipe through Polymorph player data.

## Authority / deduplication consequence

The authoritative result remains provider-side recipe re-resolution. Black Arcana has no legitimate second settlement path here.

A future Black Arcana progression hook, if ever justified, should consume a completed craft or another provider-owned postcondition. It should not:

- trust the client selector as gameplay authority;
- replay the reset payload;
- run a parallel recipe matcher;
- persist a duplicate recipe selection ledger.
