# Wayfinder

Status: `SOURCE-PINNED 21.3.0 / ITEM+RITUAL ROLE AUDITED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:wayfinder`.

## Acquisition

Shaped crafting recipe:

` g `
`gag`
` g `

where:

- `g` = Gold Ingot;
- `a` = Amethyst Shard.

## Provider-native role

Wayfinder can carry provider `wayfinder_data` and vanilla `LODESTONE_TRACKER` data. When bound data is present it displays the provider bound form/name. If the lodestone target is in the player's current dimension, the tooltip reports Manhattan distance to the target.

Wayfinder is also an explicit ingredient in the Ars Additions Locate Structure ritual tablet recipe, alongside Vexing Log, Compass and a Source Gem-tag item.

The actual structure selection/binding lifecycle is owned by the Locate Structure ritual and related provider locate data; the Wayfinder item itself does not perform an unrestricted structure scan in its class.

## Black Arcana boundary

Do not interpret Wayfinder tooltip/location data as general divination authority. A future Black Arcana divination mechanic must use its own bounded server contract and must not copy provider target data or silently trigger provider locate operations.
