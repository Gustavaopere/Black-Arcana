# Filter: Below

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_below`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:cobbled_deepslate`

## Behavior

The filter snapshots its comparison Y from `caster position Y - 1`, cast to integer, then permits resolution only when the target's integer Y compares below that value.

The exact integer conversion and `-1` offset are source facts; the catalog does not normalize them to a looser geometric interpretation.
