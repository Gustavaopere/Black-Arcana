# Capability Matrix Delta — Dis-Enchanting Table 5.0.2

Status: `✅ ENCHANTMENT-ECONOMY UTILITY / +0 SEMANTIC MAGIC ACTIONS`

| Capability | Authority | Black Arcana consequence |
|---|---|---|
| disenchant transaction | Dis-Enchanting Table | never replay after provider settlement |
| XP cost | provider server config/runtime | do not charge a second time |
| enchantment identity/effect | original registry/provider | do not reclassify as Black Arcana spell |
| book output | provider transaction result | do not duplicate output |
| hopper I/O | provider block inventory contract | do not bypass with guessed slot mutation |
| automatic output | provider config/runtime | exactly-once requirement |
| shift-click/menu | provider UI/inventory | presentation/interaction only |
| sound/particles | provider presentation | +0 |

## Semantic boundary

Dis-Enchanting Table owns an enchantment extraction transaction, not a spell/glyph/ritual registry.

Strict semantic delta: **+0**.

## Runtime boundary

Config, hopper automation, XP settlement, lifecycle and overlapping enchantment-economy mods remain runtime QA.
