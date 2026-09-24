# Corail Tombstone 9.5.6 — publisher-bounded magic surface

## Evidence boundary

Physical authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Physical artifact identity:

`tombstone-neoforge-1.21.1-9.5.6.jar` / mod id `tombstone` / runtime `9.5.6`.

Exact publisher artifact:

`https://www.curseforge.com/minecraft/mc-mods/corail-tombstone/files/8842741`

Publisher project description:

`https://www.curseforge.com/minecraft/mc-mods/corail-tombstone`

This is a publisher-bounded clean-room catalog. No current proprietary implementation body is copied or reconstructed.

## Exact 1.21.1 release lineage relevant to magic

| Version | Publisher-reported change relevant to this catalog |
|---|---|
| 9.5.6 | fixes high-level XP restoration overflow on death |
| 9.5.5 | Create Aeronautics vehicle-respawn compatibility |
| 9.5.4 | learned Ritual Flute melodies auto-play on the correct block; old flute screen removed; lore stories rewritten |
| 9.5.3 | adds "The Nights of Nour" lore sequence |
| 9.5.2 | Grave Guardian trades become data-driven; readable scrolls adjusted |
| 9.5.0 | adds Bone Scepter; adds spellcasting animation for tamed undeads and Grave Guardian |

The release history establishes that Ritual Flute/rite and readable-scroll systems belong to the installed 1.21.1 lineage before 9.5.6.

## Publicly confirmed magical mechanics

| Surface | Publicly documented role | Counting disposition |
|---|---|---|
| Grave Soul | powers enchanting of magic scroll/tablet and Grave's Key upgrade | resource/support; +0 by itself |
| Magic scroll/tablet | enchantable magical item family | action cardinality unresolved |
| Forgotten Knowledge scrolls | readable clues/objectives unlocking special knowledge | lore/progression object unless a discrete action is established |
| Ritual Flute | lootable instrument used to begin/support some rite flows; learned melodies auto-play on correct block in 9.5.4+ | support surface; exact rite identities unresolved |
| Elyra's Diary | unlocks enhanced prayers on graves | confirms prayer action family; exact action cardinality unresolved |
| Rite of Silent Bound | named forgotten-knowledge archive associated with undead affinity under conditions | named rite/knowledge surface; exact runtime action semantics unresolved |
| Ankh of Pray | prayer interaction near Decorative Grave grants Knowledge of Death under documented cooldown rules | confirmed prayer interaction; deployed config unresolved |
| Knowledge of Death | provider progression/perk system connected to Soul use, prayer and advancements | provider progression; not a spell identity |
| Bone Scepter | controls sitting behavior for tamed undeads | item action; not promoted to spell identity |
| Tombstone enchantments | 13 provider gear enchantments publicly listed | gear; metric-excluded |
| Tombstone effects | 24 provider status effects publicly listed | status; metric-excluded |

## Enchantments — public list

The publisher page names 13:

- Soulbound
- Shadow Step
- Magic Siphon
- Plague Bringer
- Blessing
- Curse of Bones
- Frostbite
- Spectral Bite
- Spectral Conjurer
- Incurable Wounds
- Decrepitude
- Sanctified
- Ruthless Strike

Disposition: `GEAR_ENCHANTMENT / +0 SEMANTIC ACTIONS`.

## Effects — public list

The publisher page names 24:

- `tombstone:ghostly_shape`
- `tombstone:diversion`
- `tombstone:preservation`
- `tombstone:unstable_intangibility`
- `tombstone:feather_fall`
- `tombstone:purification`
- `tombstone:true_sight`
- `tombstone:reach`
- `tombstone:lightning_resistance`
- `tombstone:frost_resistance`
- `tombstone:bait`
- `tombstone:bone_shield`
- `tombstone:aquatic_life`
- `tombstone:frostbite`
- `tombstone:earthly_garden` / publisher display "earthly garden"
- `tombstone:discretion`
- `tombstone:mercy`
- `tombstone:restoration`
- `tombstone:incurable`
- `tombstone:decrepitude`
- `tombstone:weaver_walk`
- `tombstone:giant_strength`
- `tombstone:little_world`
- `tombstone:beyond_the_grave_bond`

The publisher text displays the Earthly Garden identifier with a space; the normalized underscore form above is **not asserted as an exact registry ID without artifact evidence**. Treat that row as display/documentation normalization only.

Disposition for all effects: `STATUS_EFFECT / +0 SEMANTIC ACTIONS`.

## Why semantic cardinality remains pending

The user-facing metric counts spells, glyphs/spell-parts, rituals/rites and equivalent discrete magic actions.

The public evidence proves Tombstone has such magic, but does not provide:

- a complete 9.5.6 prayer registry;
- a complete 9.5.6 rite registry;
- a complete magic scroll/tablet action list;
- exact survival reachability of each action;
- exact config enablement of each action;
- a public implementation source pin matching 9.5.6.

Therefore:

`SEMANTIC_DELTA = PENDING`

No `+0` closure and no invented positive count are permitted.

## Clean-room boundary

Allowed use here:

- publisher-provided names;
- release/version identity;
- user-facing behavior summaries;
- public IDs where explicitly printed by the publisher;
- high-level interoperability/authority facts.

Not used:

- copied proprietary implementation code;
- decompiled method bodies;
- proprietary assets;
- inferred registry names/classes not publicly evidenced.

## Next closure evidence

Any of the following could advance this provider:

1. exact installed resource-only artifact inventory showing action/localization/data identities;
2. official API/source publication covering the exact 9.5.6 action registry;
3. provider-native runtime registry observation in the exact pack;
4. deployed config plus reachability evidence for the identified actions.

Until then: **⚠️ partial / conditioned**.
