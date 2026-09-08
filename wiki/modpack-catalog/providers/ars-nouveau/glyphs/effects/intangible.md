# Ars Nouveau — Intangible

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_intangible`
- Display name: Intangible
- School: Manipulation
- Default tier: 3
- Default mana cost: 30
- Compatible augments: Amplify, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), Pierce, AOE
- Source default duration: 3 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Intangible replaces eligible non-air blocks with Ars `Intangible Air`, storing the original block-state id in the tile so the block can later return. Blocks with block entities, blacklisted blocks, unharvestable blocks and claim-denied positions are skipped. AOE/Pierce expand coverage; Amplify/Dampen change harvest hardness eligibility.

## Authority / deduplication

Ars Nouveau owns this temporary block-phasing/restoration ledger. Black Arcana must not reuse Ars' temporary-block storage as its own rollback authority or duplicate restoration. Independent Black Arcana phasing remains governed by `WorldEffectPolicy` and Black Arcana-owned persistence/compare-and-set restoration.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectIntangible`).
