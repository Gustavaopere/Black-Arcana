# Somake Spells — progressão e equipamento públicos

## Authority

Somake owns its own addon-specific tier-book, grimoire, Upgrade Forge, ritual and equipment progression. Black Arcana may recognize provider-native state only through a proven boundary; it must not maintain a parallel Somake progression ledger.

## Tier books — 1.0.6 lineage

Publisher changelog 1.0.6 documents:

- objectives per tier and quest-style advancement;
- Upgrade Forge for book recipe upgrades;
- rebuilt books with final identities;
- adjusted tier-book stats;
- Tier 3 affinity bonus for specific spells.

The release also warns that the books were completely remade, creating migration risk for already-held books/spells.

Exact current 1.0.8-fix book registry IDs, tier names, objective IDs, advancement IDs, recipes and affinity values remain `NÃO VERIFICADO`.

## Grimoires — 1.0.8 lineage

The publisher describes Grimoires as off-hand staff-like equipment with evolution/progression. The player chooses a path between:

- Blood — `Profane`;
- Holy — `Sanctum`.

The current project page also describes grimoire evolution for all elements, including elements from other addons.

Unknown until registry/runtime audit:

- exact grimoire IDs;
- path-selection storage;
- upgrade recipes/objectives;
- stats/slots/affinity values;
- external-school detection mechanism;
- whether path state is item NBT/data component/advancement/capability.

## Ritual progression — 1.0.8

The 1.0.8 changelog moves Soul Fire and Infernal Fire necklaces into a ritual progression performed at Cataclysm's **Altar of Ignis** with pedestals.

Publisher compatibility rule:

- Born in Chaos present → progression extends to Infernal Fire;
- Born in Chaos absent → progression stops at Soul Fire.

The current pack contains Born in Chaos `1.7.6`, so the public eligibility condition for the Infernal branch is satisfied. Runtime completion, recipe ingredients and exact ritual state are not yet validated.

`Ritual Flame` is directly associated with triggering the new fire-pedestal rituals and evolving elemental blaze variants.

## Staffs / ritual items publicly named in 1.0.8

- Ignitium Staff — can be upgraded via ritual system toward Soul Fire / Infernal Fire;
- Archangel's Staff — Holy;
- Withered Rose Staff — Blood and described as carrying a unique spell;
- Soul Fire Rune;
- Infernal Fire Rune;
- Upgrade Orb;
- Rod;
- powder.

The public text does not provide enough information to equate the Withered Rose Staff's `unique spell` with any particular named spell. No such mapping is inferred here.

## Fragmented equipment

1.0.8 introduces:

- Fragmented Sword I;
- Fragmented Sword II;
- Fragmented Sword III;

with evolution through the Upgrade Forge.

`Copper Glove` is explicitly described in 1.0.8 as a simple craftable sword-like item for now; the publisher's planned future progression integration is not current behavior.

## Current project-page equipment families

The current public description names examples:

### Weapons

- Glacium Greataxe;
- Core Splitter;
- Witherite Glaive;
- Ruined Blade;
- Clef Sword;
- Hallow Sword;
- Rock Sword;
- Boltcutter (Dagger).

### Armor

- Dark Metal Battlemage;
- Ceranium Armor;
- Aquamancer Armor;
- Abyssium Armor.

These are current publisher-facing examples, not a complete equipment registry.

## Historical 1.0.5 weapon surface

With crafts at that release:

- Trumpet Axe — Sound;
- Totem Dagger — Evocation;
- Tide Piercer — Aqua;
- Sculkborn Axe — Eldritch;
- Scorn — Blood;
- Centuri — Blood;
- Radiant Judgment — Holy;
- Monolith Swrod — Geo, publisher spelling;
- Mirrored Edge — Symmetry;
- Last Mourning — Evocation.

Without craft at that release:

- Plague Light Saber;
- Exo Light Saber;
- FrostFlow Light Saber;
- Flare Light Saber;
- Plague Dual Saber;
- Exo Dual Saber;
- FrostFlow Dual Saber;
- Flare Dual Saber.

Current craftability/availability is not inferred.

## Other historical items

1.0.2 publicly names:

- Lightning Dagger;
- Storm Scriptures Spell Book (`Simple`);
- Aquamancer Spell Book recipe;
- various ingots/plates/cores.

1.0.1 publicly names:

- Rock Sword;
- Hollow Sword.

Again, historical introduction does not prove exact current registry or recipe.

## Elemental Charges

The current project page says Somake has one `charge` for each element and references addon elements including Sound, Symmetry, Spirit and Geo. The exact installed fix specifically repairs Symmetry and Spirit charge buffs.

Provider authority includes, at minimum, Somake's charge generation/application semantics. Black Arcana must not create a second charge resource or write guessed charge state.

Unverified fields:

- registry IDs;
- charge acquisition/generation;
- max stacks/caps;
- expiry/persistence;
- exact buffs;
- spell-power/damage formula;
- cross-addon school detection;
- server synchronization.

## Deduplication consequences

- Black Arcana Infernal content must not clone Somake's Soul Fire→Infernal Fire ritual progression.
- Black Arcana Blood/Holy progression must not imitate Profane/Sanctum grimoire branching without a distinct system contract.
- Equipment perks in RPG Skill Tree may gate or modify progression only through real provider contracts; they do not own Somake item evolution.
- Elemental Charges remain Somake/provider-owned state, not a second Black Arcana resource.