# Ars Polymorphia

Status: `PHASE 2BM — EXACT 1.0.3 SOURCE-PINNED / ZERO SEMANTIC MAGIC / CURRENT-HOST RUNTIME QA FAIL-CLOSED`

## Physical identity

- Mod id: `ars_polymorphia`
- JAR: `ars_polymorphia-1.0.3.jar`
- Runtime version: `1.0.3`
- Physical SHA-1: `8cce819e83f6360ab9aa8b44ac841511172a6a79`
- CurseForge hash from the physical modlist: `3576413974`
- Minecraft / loader: 1.21.1 / NeoForge 21.1.248 host
- Provider class: `BRIDGE / COMPAT / PROGRESSION`

The installed pack also exposes Ars Nouveau `5.13.1` and `polymorph_plus` `1.3.1+1.21.1` (`mod id polymorph_plus`).

## Exact source checkpoint

Exact official source used for factual cataloging:

`Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`

The signed commit message is `ver: 1.0.3`, and `gradle.properties` declares mod version `1.0.3`, GNU LGPL 3.0, Minecraft `1.21.1`, NeoForge baseline `21.1.115`, Ars build host `5.4.2.938` with runtime range `[5.4.2,)`, and Polymorph range `[1.0.7,)`.

The generated NeoForge metadata template requires dependency mod id `polymorph`, not `polymorph_plus`.

## Provider-owned surface

The exact source is a narrow Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict adapter. It registers no provider-owned spell, glyph, ritual, school, mana/resource system or independent magical action identity.

Its exact direct integration footprint is:

- four common mixins/accessors plus one client mixin (`5` total), with the mixin config marked `required=true` and Java 21 compatibility;
- protocol registrar version `1`;
- exactly one provider-owned play-to-server payload, `ars_polymorphia:reset_crafting_result`;
- player-specific conflict enumeration/selection around Ars `CraftingLecternTile` / crafting terminal state;
- server-side recipe re-resolution through Polymorph before Ars `currentRecipe` is changed.

The client reset payload carries no arbitrary output stack or arbitrary recipe id. The server handler requires an Ars crafting terminal/lectern context and asks Polymorph to resolve the current valid recipe against the current crafting matrix.

## Semantic disposition

Semantic-magic contribution: **0**.

Ars Nouveau owns the terminal/crafting substrate. Polymorph-compatible infrastructure owns conflict-selection state. Ars Polymorphia is an adapter between those systems and does not mint a second spell identity merely because it changes recipe-selection behavior in a magical terminal.

Black Arcana therefore must not:

- create a second recipe-conflict resolver for the same lectern flow;
- mirror Polymorph player selection into Black Arcana state;
- treat client selector/widget state as authoritative settlement;
- convert this bridge into a spell-domain, casting, Corruption, Strain or Arcane Danger provider.

If Black Arcana later consumes a crafting completion as progression evidence, it should observe the final provider-owned craft outcome rather than replaying selection/reset traffic.

## Current-host runtime blockers

Runtime compatibility is **not** promoted to PASS by the source audit.

1. Exact source metadata requires mod id `polymorph`; the physical pack currently exposes `polymorph_plus`. No dependency alias/API equivalence is assumed.
2. Exact source built against Ars Nouveau `5.4.2.938`; the physical pack uses `5.13.1`. All five direct mixin targets therefore remain runtime-compatibility QA surfaces.
3. Exact source simultaneously declares `minecraft_version=1.21.1` and dependency range `minecraft_version_range=[1.21,1.21.1)`. This source-level metadata inconsistency is recorded, not silently corrected.
4. Client boot, dedicated-server startup, real conflicting-recipe behavior, multiplayer isolation, reload/reconnect persistence and full-pack interop have not been revalidated in this tranche.

## Clean-room / provenance

Source inspection is read-only and limited to factual identity, dependency declarations, registry absence, mixin/network footprint, authority boundaries and compatibility risks. Black Arcana copies/adapts no upstream implementation body, assets, GUI sprites, localization prose or other creative content.

See:

- [`CRAFTING-RESOLUTION.md`](./CRAFTING-RESOLUTION.md)
- [`MIXIN-NETWORK-BOUNDARIES.md`](./MIXIN-NETWORK-BOUNDARIES.md)
- [`../../meta/PHASE2BM-ARS-POLYMORPHIA-CHECKPOINT.md`](../../meta/PHASE2BM-ARS-POLYMORPHIA-CHECKPOINT.md)
- [`../../meta/PROVENANCE-DELTA-PHASE2BM-ARS-POLYMORPHIA.md`](../../meta/PROVENANCE-DELTA-PHASE2BM-ARS-POLYMORPHIA.md)
