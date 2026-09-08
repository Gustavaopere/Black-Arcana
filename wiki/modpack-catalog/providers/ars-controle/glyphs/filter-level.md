# Filter: Level

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_level`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:short_grass`

## Behavior

The filter snapshots its comparison Y from `caster position Y - 1`, cast to integer, then permits resolution only when the target's integer Y is equal to that stored value.

This is discrete integer-Y comparison rather than an arbitrary vertical tolerance band.
