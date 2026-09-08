# Ars Nouveau — Spell Books & Glyph Learning

State: `SOURCE-PINNED 5.13.1 / LEARNING FLOW VERIFIED`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

## Spell-book tiers

The exact 5.13.1 item registry binds:

- `ars_nouveau:novice_spell_book` -> `SpellTier.ONE` (value 1)
- `ars_nouveau:apprentice_spell_book` -> `SpellTier.TWO` (value 2)
- `ars_nouveau:archmage_spell_book` -> `SpellTier.THREE` (value 3)
- `ars_nouveau:creative_spell_book` -> `SpellTier.CREATIVE` (value 99)

The normal progression surface is Tier I/II/III; Creative is a distinct provider tier for creative tooling.

Using a non-Creative `SpellBook` on the server updates the player's Ars mana capability so `bookTier` is at least the book's tier, and updates `glyphBonus` to at least the number of known glyphs, then syncs mana data to the client when changed.

## Learning a glyph

Each registered spell part exposes a provider Glyph item. `Glyph#use` is server-side authoritative for learning:

1. reject if the glyph is disabled by Ars config;
2. read the Ars player-data capability;
3. reject if already known or if it belongs to the default-starting glyph set;
4. call `unlockGlyph(spellPart)` on the Ars player capability;
5. sync player capability;
6. raise mana `glyphBonus` to the new known-glyph count when required and sync it;
7. consume one Glyph item in non-infinite-material mode;
8. report the learned glyph to the player.

Known glyphs are therefore persistent Ars player progression, not merely possession of an item or a client-side book state.

## Glyph crafting / XP

`GlyphRecipeProvider` generates the provider-native glyph recipes. The generated recipe XP requirement is based on the spell part's default tier:

- Tier 1 -> 27 XP
- Tier 2 -> 55 XP
- Tier 3 -> 160 XP

Each individual spell-part page is being linked to its exact generated ingredient recipe. This XP is Ars glyph-recipe progression; it is not RPG Skill Tree XP/Mastery unless a real bridge explicitly says so.

## Authority boundary

- Ars owns known-glyph state, spell-book tier and glyph-learning consumption.
- RPG Skill Tree may gate progression only through a real provider contract; it must not write Ars known-glyph capability by inference.
- Black Arcana must not auto-learn Ars glyphs because a thematically similar Black Arcana spell was unlocked.
- Registry namespace remains decisive for addon glyph ownership: Ars' guide/UI may display addon entries, but `ars_elemental:*`, `ars_controle:*`, `ars_zero:*`, etc. remain their own providers.
