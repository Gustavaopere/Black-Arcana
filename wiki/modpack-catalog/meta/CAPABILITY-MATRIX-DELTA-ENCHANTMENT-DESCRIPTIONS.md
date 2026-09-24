# Capability Matrix Delta — Enchantment Descriptions 21.1.11

Status: `CATALOGED / CLIENT PRESENTATION LAYER / +0 SEMANTIC ACTIONS`

| Capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| enchantment description tooltip | explanatory text for an existing enchantment | presentation only; never treat as runtime authority |
| modded-enchantment localization | resolves provider namespaces/IDs into description keys | consumes external identity; does not mint one |
| Shift/`require_keybind` | client display condition | not a gameplay cast/input boundary |
| only-on-books | presentation filter | no semantic action |
| enchanting-table-only | presentation filter | no enchanting mechanic ownership |
| prefix/suffix/style | text formatting | UI only |
| level-specific description | alternate localized text by existing enchantment level | does not change level/effect |
| Apothic coexistence | possible tooltip/keybind composition issue | smoke-test UI; do not alter enchantment authority |

## Semantic boundary

Enchantment Descriptions does not register or execute magic.

The existing enchantment provider remains authority for:

- identity;
- level;
- applicability;
- conflicts;
- effects;
- enchanting mechanics.

Therefore:

- spells: **0**;
- rituals/rites: **0**;
- provider enchantments: **0**;
- equivalent discrete magical actions: **0**.

Strict semantic delta: **+0**.

## Runtime boundary

The catalog closure does not imply UI compatibility PASS. Config, localization, tooltip composition and Apothic coexistence remain direct runtime/UI QA.
