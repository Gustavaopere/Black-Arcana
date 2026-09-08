# Precision Jack

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:precision_jack`
- **School:** Evocation
- **Levels:** 1–4
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 1 s
- **Interruptible:** no
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 60`
- `manaCostPerLevel = 30`
- `castTime = 40 ticks / 2 s`
- fixed base damage: `6 * PRECISION_JACK damage multiplier`

Looting bonus:

`min(5, max(1, round(spellPower / 100)))`

Duplicate-loot-roll chance:

`min(30, max(0, round(spellPower / 10)))%`

## Attack-time snapshot

The provider writes damage, looting bonus and duplicate-drop chance into the summoned knife when it is created, and refreshes all three at the initial weapon cast. These values therefore belong to the attack context and are not recomputed by an external loot observer.

A successful completion triggers the provider knife slice; cancellation releases the weapon.

## Provider-owned drop settlement

`PrecisionJackLootingEvent` only acts when all causal checks match:

- the damage source is the provider `PRECISION_JACK` damage type;
- the victim is not a player;
- the direct damage entity is the provider `PrecisionJackKnifeEntity`.

If the duplicate chance triggers, the provider performs **one additional loot-table roll** using the target/entity damage context and player luck when kill credit is a player. Separately, the looting bonus can grow each resulting non-empty drop by a random `0..lootingBonus` amount.

Both caps are enforced again inside the event path: looting at 5 and duplicate chance at 30%.

## Authority / anti-double-processing

Precision Jack's loot mutation is provider-owned. Black Arcana or RPG integrations must not add a second looting pass, second loot-table roll or duplicate-drop chance from the same kill.

One successful Precision Jack kill remains one causal spell outcome even if several item entities result from the provider's loot settlement.

## Confidence

`SOURCE-PINNED SPELL + ATTACK SNAPSHOT + LIVING-DROPS SETTLEMENT / FULL MODPACK LOOT-TABLE COMPAT QA PENDING`