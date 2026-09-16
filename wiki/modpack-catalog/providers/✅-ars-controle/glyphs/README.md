# Ars Controle 1.6.15 — glyph catalog

Status: `9/9 SOURCE-PINNED / RUNTIME+PACK QA PENDING`

| Glyph | Kind | Tier | Base mana | Scribe XP |
|---|---|---:|---:|---:|
| Precise Delay | Effect | II | 0 | 55 |
| Filter: Above | Filter | I | 0 | 27 |
| Filter: Below | Filter | I | 0 | 27 |
| Filter: Level | Filter | I | 0 | 27 |
| Filter: OR | Filter | I | 0 | 27 |
| Filter: XOR | Filter | I | 0 | 27 |
| Filter: XNOR | Filter | I | 0 | 27 |
| Filter: NOT | Filter | I | 0 | 27 |
| Filter: Random | Filter | I | 0 | 27 |

Precise Delay explicitly returns Tier II and mana 0 in Ars Controle. The filters inherit Ars `AbstractFilter`, whose installed Ars Nouveau 5.13.1 implementation uses base mana 0; `AbstractSpellPart` defaults to Tier I when the addon class does not override the tier. The generated Ars Controle glyph recipes independently encode 55 XP for Precise Delay and 27 XP for the filter family.

These parts belong to the Ars spell grammar. Their use does not create a second Black Arcana cast identity or cost settlement.
