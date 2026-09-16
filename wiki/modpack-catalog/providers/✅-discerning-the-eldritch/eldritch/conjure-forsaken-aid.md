# Conjure: Forsaken Aid

- **ID:** `discerning_the_eldritch:conjure_forsaken_aid`
- **School:** Eldritch
- **Levels:** 1–8
- **Rarity:** Legendary
- **Cast:** Long, 30 ticks
- **Mana neutral:** 100–170
- **Spell power neutral:** 10–45
- **Cooldown:** 100 s
- **Summon count:** exactly `spellLevel`
- **Recast count:** 2

## Contract

On first cast without an existing recast, spawns `spellLevel` allies near the caster from the provider pool:

- `SightlessMawEntity`;
- `UntoldBehemothEntity`;
- `TheApostleEntity`.

Each candidate is posted through NeoForge `SpellSummonEvent` before insertion, then initialized with Iron's `SummonManager` and stored in `SummonedEntitiesCastData`.

Summon lifetime/recast timer = `20 * (20 * getSpellPower)` ticks = `20*spellPower` seconds. Neutral range: 200–900 s.

The random-selection implementation uses independent booleans; the exact resulting distribution should be treated provider-native rather than recreated externally.

## Dedup / authority

- `SpellSummonEvent` can replace/alter the creature; use the event result.
- `SummonManager` owns lifecycle/removal/recast semantics.
- Never spawn a second companion set from a bridge observing the cast.
- Exact AI, friendly-fire and target priorities are entity-native / `NÃO VERIFICADO` here.
- acquisition route: `NÃO VERIFICADO`.

## Source

`ConjureForsakenAidSpell.java`, branch `1.21@7bbd81f...`.
