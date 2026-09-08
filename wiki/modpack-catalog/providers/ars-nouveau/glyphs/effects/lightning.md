# Lightning

- Registry ID: `ars_nouveau:glyph_lightning`
- Source class: `EffectLightning`
- School: Elemental Air
- Default tier: **3**
- Default mana: **100**
- Default source config: damage **5.0**, amplification scalar **3.0**, wet-target bonus **2.0**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Spawns Ars Nouveau's custom LightningEntity at the resolved location and transfers spell amplification/duration data into that entity. The provider documents Shocked stacking and bonus lightning interactions, including wet targets; the exact class sets the wet bonus from config and the lightning's source damage state.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time. Amplify is limited to 2 by default.

## Boundary

Ars owns LightningEntity, Shocked and provider damage semantics. Black Arcana must preserve causal identity and avoid duplicate lightning damage/proc/mastery processing.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.