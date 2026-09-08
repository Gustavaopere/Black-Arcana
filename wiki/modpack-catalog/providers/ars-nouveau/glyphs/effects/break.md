# Break

- Registry ID: `ars_nouveau:glyph_break`
- Source class: `EffectBreak`
- School: Elemental Earth
- Default tier: **1**
- Default mana: **10**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Break destroys harvestable blocks in provider-calculated AOE/depth geometry. It checks Ars Nouveau's claim-respect helper and a provider break blacklist before mutation. Amplify/Dampen change harvest capability; Fortune and Extract synthesize Fortune/Silk Touch levels for the provider break operation; Sensitive switches the simulated tool to shears; Randomize may skip candidate blocks.

Compatible augments: Amplify, Dampen, Pierce, AOE, Extract, Fortune, Sensitive, Randomize. Default Fortune limit is 4 and Sensitive limit is 1. It is explicitly a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:iron_pickaxe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, Break is considered known without consuming a Glyph item.
- The generated recipe still exists; provider Glyph learning rejects the item while Break is currently configured as a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns its break/loot/claim semantics. Any Black Arcana block destruction still requires `WorldEffectPolicy`, loaded-chunk/budget controls and Black Arcana causal ownership; Ars Break is not a world-policy bypass.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.