# Unstable Reliquary

Status: `SOURCE-PINNED 21.3.0 / MARK+RECALL STATE AUDITED / RUNTIME CONFIG QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:unstable_reliquary`.

## Acquisition

Enchanting Apparatus recipe in the exact pin:

- reagent: Ars Nouveau Mob Jar;
- pedestal items: Conjuration Essence, Manipulation Essence and Ender Pearl.

## Item state

The item has durability **1000** and is not enchantable. Its `mark_data` component may hold Entity, Location, Empty or Broken mark data through the provider custom registry.

Mark/Recall uses this item from a Tile Caster inventory when the provider caster is a tile, otherwise only from the caster's main/off hand.

## Entity marks

`EntityMarkData` stores entity UUID, entity type and optional display name. On server inventory tick, the provider breaks the Reliquary mark when:

- the target entity cannot be found in the current `ServerLevel`;
- the target is no longer alive;
- the target is a player who no longer has the Ars Additions `marked` effect.

Recall resolves the stored entity with `ServerLevel.getEntity(uuid)`, so the exact execution path audited here does not establish arbitrary cross-dimension entity resolution.

Default durability cost is config-owned:

- player target: **1000**;
- other entity target: **250**.

## Location marks

`LocationMarkData` stores a `GlobalPos`. Recall fails when the stored dimension differs from the execution level dimension. Default durability cost: **50**.

## Marked duration

Server config default for player Mark duration is **300 seconds**, bounded by the config to 0–900 seconds.

## Black Arcana boundary

The Reliquary is an Ars Additions reference/state ledger. Black Arcana must not copy its mark data into Black Arcana persistence, infer a global target handle from the UUID, or settle a second remote cast when Recall already routes the provider spell resolver to the stored target.
