# Filter: XNOR

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_xnor`
- Kind: adaptive binary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `minecraft:comparator` + `minecraft:redstone` + `minecraft:redstone_torch`

## Behavior

Evaluates the next two valid filters and resolves when both boolean results are equal: both true or both false.

Like the other adaptive binary filters, it consumes nested filter grammar and fails closed when the expected filter structure cannot be resolved.
