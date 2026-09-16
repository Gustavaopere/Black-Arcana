# Eidolon: Repraised 0.5.0.2 — Progression and Resource Authority

Status: `RESEARCH REGISTRY 16/16 INVENTORIED / KEY DEPENDENCIES PARTIALLY NORMALIZED / FULL SURVIVAL CHAIN + RUNTIME QA PENDING`

Canonical source: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Provider-owned progression axes

The installed version exposes multiple independent progression/resource axes that must not be collapsed into a single generic magic level:

- mana;
- Light deity reputation/devotion;
- Dark deity reputation/devotion;
- research/knowledge;
- soul capability;
- altar power/capacity state;
- prayer cooldown state;
- Sign/chant knowledge and recipe availability.

## Research registry 16/16

`Researches.java` registers exactly these 16 research keys in 0.5.0.2:

| # | Research key |
|---:|---|
| 1 | `core` |
| 2 | `pewter_crucible` |
| 3 | `soul_enchanter` |
| 4 | `arcane_gold` |
| 5 | `shadow_gem` |
| 6 | `improved_crucible` |
| 7 | `candle` |
| 8 | `wooden_altar` |
| 9 | `deity_altar` |
| 10 | `chants` |
| 11 | `frost_spell` |
| 12 | `fire_spell` |
| 13 | `necrotic_touch` |
| 14 | `soulfire_wand` |
| 15 | `prestigious_palm` |
| 16 | `soulfire_ritual` |

This is the registered research surface, not yet a proof that every key is reachable in survival under the current full modpack.

## Dependency examples verified from source

### Chants

`CHANTS` depends on the earlier Pewter Crucible path and introduces sign/chant knowledge, including the Light/Dark chant branch. The provider, not Black Arcana, determines when the player actually knows the required sign/spell knowledge.

### Frost Spell

`FROST_SPELL` is downstream of Chants and includes water/frost knowledge plus prior chant/deity requirements in the provider research-task graph. `FrostSpell.canCast()` independently checks this research at runtime.

### Fire Spell

`FIRE_SPELL` is likewise downstream of Chants and fire knowledge. `FireTouchSpell.canCast()` independently checks this research at runtime.

### Necrotic Touch

`NECROTIC_TOUCH` depends on the chant path plus soul/wicked rune knowledge, prior Dark trade progression and a Dark-deity reputation/devotion task at 10. This aligns with `DarkTouchSpell` also requiring at least 10 Dark reputation at cast time.

### Soulfire Wand

`SOULFIRE_WAND` depends on `NECROTIC_TOUCH`, soul/fire rune knowledge and additional provider progression including Dark-deity reputation at 20 and required spell/use tasks.

### Prestigious Palm

`PRESTIGIOUS_PALM` depends on the Soul Enchanter branch.

### Soulfire Ritual

`SOULFIRE_RITUAL` is downstream of both `NECROTIC_TOUCH` and `SOULFIRE_WAND`.

These examples prove that Eidolon progression is a graph of provider-specific knowledge, tasks and deity requirements rather than a flat spell-level ladder.

## Prayer progression

Prayer requires a nearby ready Effigy. On successful prayer the provider:

1. marks the prayer time in the reputation capability;
2. adds deity reputation based on base reputation plus altar power scaling;
3. recalculates/increases max mana using current reputation and altar capacity;
4. increases current mana using reputation and altar power.

Default `PrayerSpell` parameters:

- base reputation: 1;
- power multiplier: 0.25;
- cooldown: 21000 ticks.

All are provider/server-config surfaces.

### Prayer-derived special cases

- Dark Animal Sacrifice: base Dark reputation gain 3 + `0.5 × altarPower`; zero generic mana cost in its registered constructor.
- Dark Villager Sacrifice: requires Dark reputation ≥15; gain 6 + `altarPower`; grants sacrifice-related provider knowledge on a successful ritual kill.
- Zombify Villager: requires Dark reputation ≥20 and spends 20 mana; gain 8 + `1.25 × altarPower`.
- Cure Zombie: requires Light reputation ≥20 and spends 20 mana; gain 8 + `1.25 × altarPower`.

These transactions must not be reduced to “mana spell casts”: devotion, effigy readiness, altar state and prayer cooldown are part of provider authority.

## Runtime spell gates already proven

- Fire Chant -> `Researches.FIRE_SPELL`;
- Frost Touch -> `Researches.FROST_SPELL`;
- Darklight Chant -> Dark reputation ≥3;
- Light Chant -> Light reputation ≥3;
- Dark Touch -> Dark reputation ≥10;
- Holy Touch -> Light reputation ≥10;
- Dark Villager Sacrifice -> Dark reputation ≥15 plus prayer/target gates;
- Zombify Villager -> Dark reputation ≥20 plus prayer/target gates;
- Cure Zombie -> Light reputation ≥20 plus prayer/target gates;
- Lay on Hands can grant `DeityLocks.HEAL_VILLAGER` when healing another damaged entity;
- Smite can grant `DeityLocks.SMITE_UNDEAD` on successful undead damage.

## Soul capability

`SoulImpl` proves a separate provider-owned soul state:

- integer soul count;
- increment/decrement/set operations;
- optional master entity UUID or master block position;
- provider validation around entity-master ownership, including Summon Staff semantics;
- synchronization to server players when soul state changes;
- serialized soul count plus optional master identity/location.

This capability is distinct from physical Soul Shard items produced by the Crystal ritual. Black Arcana must not assume that an item drop, the capability count and another mod's “soul” resource are interchangeable.

## Black Arcana rule

Perks may react to provider-confirmed progression state, but must not manufacture equivalent Eidolon progress. No generic perk should silently:

- add Light/Dark reputation;
- mark Eidolon research complete;
- refresh prayer cooldown;
- increase Eidolon max mana;
- mutate Eidolon soul state;
- bypass effigy/altar requirements;
- synthesize missing research prerequisites;
- map Eidolon soul/reputation to another provider's resource without an explicit contract.

## Remaining progression work

The research registry itself is 16/16 inventoried. Still pending:

1. normalize the complete task/prerequisite graph for all 16 researches;
2. connect each active chant/ritual to its actual survival acquisition path;
3. inventory data-driven chant and ritual recipes in the exact 0.5.0.2 resources;
4. verify survival reachability in the full pack;
5. runtime-test prayer cooldown, reputation, mana and soul synchronization on dedicated server.

Any explicit future integration that changes one of these progression axes requires a dedicated provider contract and runtime test.