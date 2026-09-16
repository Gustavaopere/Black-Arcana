# Arcane Slice

- ID: `firesenderexpansion:arcane_slice`
- School: `irons_spellbooks:ender`
- Levels: 1–3
- Min rarity: Rare
- Cast: Instant
- Mana neutral: 75 / 90 / 105
- Spell power neutral: 12 / 17 / 22
- Cooldown: 35 s
- Target acquisition: Iron's pre-cast target helper, 32 blocks
- Base direct damage: `0.77 × spellPower`
- PvP mana scaling: `0.77 × spellPower × (1.5 - currentMana/maxMana/2)` when target is a player with positive Max Mana

## Contract

Single-target Ender hit. Against a player, the hit becomes stronger as the target's current-mana percentage falls: full mana yields the base `0.77×` coefficient and zero mana reaches `1.155× spellPower`. Non-player targets use the base coefficient.

## Dedup / authority

Do not add a second low-mana execute multiplier. The provider owns target selection and damage application through Iron's `DamageSources`.

## Acquisition

Default Iron's spell eligibility is not overridden in this class. Exact scroll loot/crafting weights: **NÃO VERIFICADO**.

## Source

`ArcaneSliceSpell.java` @ `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`.