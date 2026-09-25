# Dis-Enchanting Table 5.0.2 — utility surface

## Evidence boundary

Physical artifact:

- `disenchanting_table-merged-1.21.1-5.0.2.jar`;
- mod id `disenchanting_table`;
- runtime `5.0.2`;
- SHA-1 `c054a8bef63addff4d4a9520ec4c7a915c3fc1d1`.

Exact publisher release:

- CurseForge project `933354`;
- file `6581607`;
- 1.21 / 1.21.1;
- Fabric + NeoForge;
- Release;
- uploaded 2025-05-26.

## Provider-owned operation

The provider's meaningful gameplay surface is the disenchanting transaction:

| Surface | Role | Semantic magic disposition |
|---|---|---:|
| Dis-Enchanting Table block | transaction owner | +0 |
| enchanted-item input | external enchantment data input | +0 |
| enchanted-book output | physicalized existing enchantment | +0 |
| item-with-enchants-removed output | transaction result | +0 |
| XP cost | provider economy/resource settlement | +0 |
| hopper automation | inventory automation | +0 |
| automatic output | transaction automation | +0 |
| server config | economy/automation policy | +0 |
| sound/particles/menu | presentation | +0 |

## Enchantment deduplication

Existing enchantments remain owned by:

- Minecraft;
- Apothic/Apotheosis;
- any mod that registered the enchantment.

The table's extraction does not mint a second enchantment identity and does not convert an enchantment into a spell identity.

## Semantic exclusion

Do not count as semantic magic objects:

- the table block;
- the act of placing an item in the table;
- hopper insertion/extraction;
- XP payment;
- book output;
- repair-cost reset;
- auto-output;
- manipulated enchantment registry entries.

## Strict result

- spells: 0;
- glyphs/spell-parts: 0;
- rituals/rites: 0;
- equivalent discrete magic actions: 0.

Strict semantic delta: **+0**.

Status: **✅ zero-semantic enchantment-economy utility closure**.
