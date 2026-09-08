# Filter: Random

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_random`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `ars_nouveau:glyph_randomize`

## Behavior

Base resolution probability is 50%.

For positive amplification `a`:

`chance = 1 - 0.5 / 2^a`

For dampening magnitude `d`:

`chance = 0.5 / 2^d`

The compatible augments are Amplify and Dampen, and Ars Controle overrides their mana contribution on this filter to 0.

The actual roll uses `ThreadLocalRandom.nextDouble() <= chance`. Randomness is provider-owned spell filtering; Black Arcana must not perform a second independent roll for the same Ars filter.
