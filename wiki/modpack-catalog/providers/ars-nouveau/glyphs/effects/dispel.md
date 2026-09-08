# Dispel

- Registry ID: `ars_nouveau:glyph_dispel`
- Source class: `EffectDispel`
- School: Abjuration
- Default tier: **1**
- Default mana: **30**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Posts Ars Nouveau `DispelEvent.Pre` and honors cancellation before resolution. On living entities it removes milk-curable effects except provider-tagged deny entries, plus explicitly provider-tagged allow entries; it then invokes `IDispellable` where supported and posts `DispelEvent.Post`. Blocks/block entities implementing `IDispellable` receive the same provider dispel callback/event framing.

Compatible augments: none in the exact 5.13.1 class.

## Boundary

This is a real Ars-supported event/interface surface, but it remains Ars authority. A future Black Arcana adapter may observe/use a supported seam only after exact API-contract review; it must not reinterpret Dispel as authority over Black Arcana state, Corruption, Strain or arbitrary third-party effects.

Status: `SOURCE-PINNED 5.13.1 / API CANDIDATE SEAM IDENTIFIED / RUNTIME QA PENDING`.