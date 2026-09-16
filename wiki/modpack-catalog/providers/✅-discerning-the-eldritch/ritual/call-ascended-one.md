# Call The Ascended One

- **ID:** `discerning_the_eldritch:call_ascended_one`
- **School:** Ritual
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 100 ticks / 5 s
- **Mana:** 1000
- **Spell power neutral:** 10
- **Cooldown:** 1000 s
- **Complexity:** complex + super-complex

## Cast-source/acquisition gates

By `AbstractRitualSpell`: no crafting, no normal looting, and SPELLBOOK/SWORD cast sources are rejected. Concrete ritual focus/source granting the cast remains provider progression and must not be replaced by a generic scroll.

## Boss settlement

Creates `AscendedOneBoss` near caster, sets attributes from Ritual spell power, calls `finalizeSpawn(... MOB_SUMMONED ...)` and adds it directly to the level.

Neutral stats at power 10:

- attack damage = `2.5*power` = **25**;
- max health = `60.5*power` = **605**;
- spell power = `0.75*power` = **7.5**;
- spell resist = `0.075*power` = **0.75**.

Crucially, the spell does **not** initialize this boss through Iron's `SummonManager` and does not set a caster owner in the spell class. It is a boss-summoning ritual, not a normal controlled minion contract.

## Dedup / safety

Never reinterpret this as a tame summon. Black Arcana boss rituals must preserve boss spawn semantics and not attach normal summon ownership/recast cleanup unless intentionally redesigning the provider.

## Source

`CallAscendedOneSpell.java`, `AbstractRitualSpell.java`, DTE 1.4.4 branch.
