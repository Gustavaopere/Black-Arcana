# Randomize

- Registry ID: `ars_nouveau:glyph_randomize`
- Source class: `AugmentRandomize`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1**
- Default mana: **0**

## Source-pinned behavior

Marks Ars Nouveau spell stats as randomized. Compatible glyphs define the resulting behavior. The exact provider description specifically identifies block-selection randomization for glyphs such as Place Block and Exchange, using blocks available through the provider's spell context/hotbar behavior.

## Boundary

Ars Nouveau owns the randomization algorithm and compatible-glyph interpretation. Black Arcana randomness must remain server-owned, deterministic where required for replay/tests, and bounded independently.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.