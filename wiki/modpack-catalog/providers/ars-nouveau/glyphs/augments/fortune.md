# Fortune / Luck

- Registry ID: `ars_nouveau:glyph_fortune`
- Source class: `AugmentFortune`
- Source display name: `Luck`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **80**

## Source-pinned behavior

Increases relevant drop chances for compatible provider behavior, including mobs killed through the provider damage path and blocks broken through Break. It is declared incompatible with Extract.

## Boundary

Ars Nouveau owns its loot/fortune calculations and compatible-glyph semantics. Black Arcana must preserve provider causal identity and must not double-apply external Fortune/Looting-style rewards.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.