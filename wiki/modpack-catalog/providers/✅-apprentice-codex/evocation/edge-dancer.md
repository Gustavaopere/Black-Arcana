# Edge Dancer

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:edge_dancer`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Ordinary crafting:** disabled
- **Ordinary looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 40 ticks`
- duration: `round(20 * 60 * spellPower / 100)` ticks
- recast count: `2`
- first activation requires a provider `SpellSideEdge` in the main hand

## Provider lifecycle

The initial server cast activates `EdgeDancerManager`; recasting while provider recast state is active deactivates it. The spell is deliberately unavailable through ordinary crafting and loot and requires its provider-specific weapon surface.

Greater Conjurer's Talisman can alter provider cooldown behavior on deactivation/timeout. That remains Iron's/Apprentice authority.

## Causality and progression

The stance/equipment session is one spell activation. Weapon strikes performed while Edge Dancer is active are not automatically additional spell casts. A combat bridge must attribute them through a real provider/combat seam and deduplicate against ordinary melee progression.

## Deduplication

Occupies the **Spell Side Edge-gated timed Evocation weapon/stance session with recast deactivation** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DURATION FORMULA+ITEM GATE+RECAST / EDGE DANCER MANAGER COMBAT MODIFIERS REQUIRE MANAGER AUDIT`