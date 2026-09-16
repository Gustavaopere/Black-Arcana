# Ars Additions 21.3.0 — Rituals

Status: `2/2 SOURCE-PINNED / RUNTIME+CONFIG QA PENDING`

`ArsNouveauRegistry.registerRituals()` registers exactly two rituals at source checkpoint `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`:

1. [Arcane Permanence](arcane-permanence.md) — registry `ars_additions:ritual_chunk_loading`; configurable provider force-loading.
2. [Locate Structure](locate-structure.md) — registry `ars_additions:ritual_locate_structure`; asynchronous provider structure lookup producing a Wayfinder.

Both remain Ars/Ars Additions ritual authority. Neither grants Black Arcana permission to force-load chunks or perform unbounded structure scans.
