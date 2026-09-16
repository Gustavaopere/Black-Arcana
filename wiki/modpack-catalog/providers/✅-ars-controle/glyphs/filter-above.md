# Filter: Above

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_above`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:feather`

## Behavior

The filter snapshots its comparison Y from `caster position Y - 1`, cast to integer, then permits block/entity resolution only when the target's integer Y compares as greater than that stored value.

This is provider spell-grammar filtering, not a Black Arcana targeting authorization. A target rejected or admitted by this glyph does not bypass Black Arcana's own server-side target rules for Black Arcana spells.
