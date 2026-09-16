# Filter: OR

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_or`
- Kind: adaptive binary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `minecraft:comparator` + `minecraft:redstone`

## Behavior

Consumes/interprets the next two valid filters in the spell grammar and resolves when either one is true. It accounts for augments attached to the first nested filter when locating the second filter and advances the spell context past the consumed nested filter sequence.

Malformed or failing nested-filter evaluation fails closed and can emit a provider error to the casting player.
