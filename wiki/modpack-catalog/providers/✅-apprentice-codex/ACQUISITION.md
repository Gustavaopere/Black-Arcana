# Apprentice's Codex 0.9.7.1 — acquisition and learning

Source checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

## Principle

Apprentice's Codex is Iron's-native. Spell learning/acquisition must preserve the provider's own `DefaultConfig`, `allowLooting()` and crafting flags plus Iron's scroll/spell infrastructure. The catalog must not claim that every registered spell can appear through every generic Iron's acquisition path.

Per-spell pages record any source-confirmed restrictions discovered during numeric audit. Examples include spells with `setAllowCrafting(false)` and/or `allowLooting() == false`, which are deliberately item/provider-gated instead of ordinary scroll content.

## Data-driven acquisition surfaces present in 0.9.7.1

The exact data tree contains distinct acquisition/progression surfaces for:

- advancements;
- Curios data;
- Errand Mage trades;
- Errand Mage village houses;
- Iron's Jewelry integration data;
- global loot modifiers;
- block loot tables;
- recipes, including provider recipe types and optional Create recipes.

This proves acquisition is broader than generic spell scroll drops.

## Isekai Travel Guidebook — exact paths

The provider registers a Global Loot Modifier that targets:

`minecraft:chests/spawn_bonus_chest`

When that loot table is generated, the modifier adds one `apprenticecodex:isekai_travel_guidebook` if one is not already present. This path is deterministic conditional on the bonus-chest loot table being generated; the modifier does not roll an additional chance.

The default Errand Mage trade table also sells the guidebook at villager level 5 for:

- `64 emeralds`;
- `1 writable_book`;

with `max_uses = 3` in the exact default trade data.

These are two separate provider acquisition paths for the same item and must not be collapsed into one heuristic.

## Errand Mage — exact default trade families

The exact `default.json` includes, among other trades:

- buys Comfort Berries from the player;
- buys Rapid Spellcaster Rounds;
- buys selected Iron's materials;
- sells Basic Spellcaster Rounds;
- sells Iron's Arcane Essence;
- sells an Iron's instant-mana potion;
- buys an Iron's Tarnished Helmet;
- sells `spellstained_arcane_ingot`;
- exchanges a generic Iron's scroll + emeralds for common ink;
- sells the Isekai Travel Guidebook at level 5.

Errand Mage trade data is provider-owned and data-driven. A future progression bridge should observe completed trade causality only if a real hook is needed; simply opening the trading UI is not a Mastery event.

## Recipes

The exact provider recipe tree contains both direct JSON recipes and grouped/custom recipe families. Source-visible examples include:

- Alchemist Cauldron recipes;
- Alchemist's Flask tipped-arrow handling;
- Create-specific recipes;
- Explorer's Cane lodestone binding;
- Explorer's Codex guidebook transfer;
- Magi Compressor Gadget;
- spell-bullet / spell-casing molds;
- Spellcaster Flask extraction;
- additional provider crafting/processing recipes beyond these examples.

Recipe presence proves a provider acquisition/crafting path only for the associated item/output. It does not prove ordinary spell-scroll craftability; that remains controlled per spell by Iron's/Apprentice config.

## Spell acquisition classification

For each `apprenticecodex:*` spell, use this order:

1. exact spell class/default config;
2. explicit `allowLooting()` override;
3. explicit ordinary-crafting flag;
4. provider item that embeds/forces the spell, when present;
5. Iron's native scroll/inscription mechanics only when the spell remains eligible;
6. runtime/config QA for pack-specific datapack/config overrides.

### Known item/provider-gated examples from the exact audit

The 0.9.7.1 audit already confirms non-ordinary paths for spells such as:

- `manifestation_grimoire` — crafting disabled and ordinary looting disabled;
- `mana_slash` — crafting disabled and ordinary looting disabled; tied to provider cast/catalyst context;
- `long_stride` — crafting disabled and ordinary looting disabled;
- `anchor_blink` — crafting disabled and ordinary looting disabled, with provider mirror requirement;
- `edge_dancer` — crafting disabled and ordinary looting disabled, requiring Spell Side Edge for first activation;
- `call_broom` — crafting disabled and ordinary looting disabled, requiring an equipped provider broom.

Other per-spell pages remain authoritative for restrictions found in their exact classes. Do not extrapolate this list by thematic similarity.

## Learning semantics

Apprentice's Codex does not establish a second Black Arcana learning ledger. When a spell is learned/equipped through Iron's/provider mechanics, that identity remains `apprenticecodex:<spell>` in the Iron's registry.

Black Arcana may catalog overlap and future gates, but must not:

- clone the spell into the Black Arcana registry merely to make it learnable;
- charge a second learning currency;
- grant a duplicate spell when the provider already owns the scroll/item;
- treat an item-only spell as ordinary world-loot because another spell of the same school is lootable.

## Pack-specific override caveat

This page audits the exact upstream 0.9.7.1 source/data. User/config/datapack overrides in the full pack can alter effective recipes, trades or spell config. Runtime QA is therefore still required before treating an exact acquisition probability or final pack economy as frozen.

## Confidence

`SOURCE-PINNED ACQUISITION SURFACES / BONUS-CHEST+ERRAND-MAGE PATHS EXACT / SPELL ELIGIBILITY RULES EXACT / FULL PACK OVERRIDE+ECONOMY QA PENDING`