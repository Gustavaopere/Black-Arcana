# Ars Controle 1.6.15 — exact registry surface

Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.

## Blocks — 4

- `ars_controle:warping_spell_prism`
- `ars_controle:scryers_linkage`
- `ars_controle:scroll_holder`
- `ars_controle:temporal_stability_sensor`

## Items — 6

Block items:

- `ars_controle:warping_spell_prism`
- `ars_controle:scryers_linkage`
- `ars_controle:scroll_holder`
- `ars_controle:temporal_stability_sensor`

Standalone items:

- `ars_controle:remote`
- `ars_controle:portable_brazier_relay`

## BlockEntityTypes — 3

- `ars_controle:warping_spell_prism` -> `WarpingSpellPrismTile`
- `ars_controle:scryers_linkage` -> `ScryersLinkageTile`
- `ars_controle:scroll_holder` -> `ScrollHolderTile`

There is no registered Temporal Stability Sensor BlockEntityType in the exact `ACRegistry.Tiles` source.

## Data components — 2

- `ars_controle:remote_data` -> persistent + network-synchronized `RemoteData`
- `ars_controle:portable_brazier` -> persistent + network-synchronized `PortableBrazierRelayData`

## Attachments — 4

- `ars_controle:relay_uuid` -> UUID
- `ars_controle:association` -> UUID
- `ars_controle:block_target` -> `GlobalPos`
- `ars_controle:entity_target` -> UUID

## Ars spell parts — 9

Effect:

- `ars_controle:glyph_precise_delay`

Filters:

- `ars_controle:glyph_filter_above`
- `ars_controle:glyph_filter_below`
- `ars_controle:glyph_filter_level`
- `ars_controle:glyph_filter_or`
- `ars_controle:glyph_filter_xor`
- `ars_controle:glyph_filter_xnor`
- `ars_controle:glyph_filter_not`
- `ars_controle:glyph_filter_random`

All nine are registered through `GlyphRegistry.registerSpell` in `ACRegistry.Glyphs.registerAll()`.

## Creative tab — 1

`ars_controle:general`, displaying all entries from the provider item registry.

## Editorial-count reconciliation

The Notion dossier's "31 components" is not a registry count for this release. The exact source tree contains validators, mixins, blocks, routing utilities and integration code in addition to the nine registered spell parts. Phase 2R keeps those internal/runtime surfaces separate from the player-facing glyph registry.
