# Ender Source

Status: `SOURCE-PINNED 21.3.0 / PERSISTENCE+AUTHORITY AUDITED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

## Ender Source Jar

Registry id: `ars_additions:ender_source_jar`.

Source acquisition from the 21.3.0 Enchanting Apparatus provider:

- reagent: `ars_nouveau:source_jar`;
- pedestal items: Ender Pearl ×4 and Popped Chorus Fruit ×4.

Placement assigns the placing entity UUID as owner when available.

## Provider-owned ledger

`EnderSourceData` is Minecraft `SavedData` stored through the overworld data storage under the id `ender_source_data`.

Its canonical provider state is a map:

`owner UUID -> integer Source amount`

Every owned Ender Source Jar reads/writes that same server-side owner pool. The tile stores the owner UUID in block-entity NBT, synchronizes the shared Source value and refuses Source acceptance while owner is absent.

This is **Source**, not player mana and not a Black Arcana resource. Multiple jars for one owner are views into the same provider-owned balance rather than independent tanks.

## Black Arcana boundary

- Do not mirror `EnderSourceData` into Black Arcana persistence.
- Do not convert this Source pool into mana, Corruption, Strain, blood, soul or RPG progression resources.
- Do not settle a second cost when Ars Additions already changes the owner Source balance.
- A future adapter must use a verified provider seam; item/block observation alone is insufficient authority to mutate the ledger.
