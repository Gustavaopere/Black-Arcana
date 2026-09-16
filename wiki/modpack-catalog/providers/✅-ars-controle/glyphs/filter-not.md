# Filter: NOT

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_not`
- Kind: adaptive unary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:redstone_torch`

## Behavior

Evaluates the next valid filter and negates its result. Augments belonging to that nested filter are accounted for when advancing the spell context.

Missing/non-filter nested parts fail closed. Nested Y-level/Random filters receive provider-specific setup before evaluation.
