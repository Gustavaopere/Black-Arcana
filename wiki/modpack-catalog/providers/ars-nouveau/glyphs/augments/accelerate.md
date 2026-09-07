# Accelerate

- Registry ID: `ars_nouveau:glyph_accelerate`
- Source class: `AugmentAccelerate`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's acceleration modifier. Provider glyphs that declare Accelerate compatible interpret that stat; Projectile uses it to increase projectile velocity.

## Boundary

Ars Nouveau owns augment compatibility, acceleration semantics and effective configured cost. Black Arcana must not treat this modifier as a universal projectile-speed API.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.