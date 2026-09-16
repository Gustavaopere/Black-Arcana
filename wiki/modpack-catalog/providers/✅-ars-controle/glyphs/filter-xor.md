# Filter: XOR

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_xor`
- Kind: adaptive binary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `minecraft:comparator` + `minecraft:redstone_torch`

## Behavior

Evaluates the next two valid filters and resolves only when their boolean results differ. Nested Y-level and Random filters receive provider-specific preparation before evaluation.

Malformed nested structure fails closed rather than treating missing filters as true.
