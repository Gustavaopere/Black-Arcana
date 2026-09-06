# Goety

Status: `PHASE 2 — PROVIDER AUDIT IN PROGRESS`

## Runtime identity

- Provider: **Goety**
- Installed JAR: `goety-3.1.4.jar`
- Runtime version: `3.1.4`
- Loader/game: NeoForge 1.21.1
- Role: `SOUL ENERGY / FOCUS SPELLCASTING / NECROMANCY / SERVANT / RITUAL PROVIDER`
- Addons installed separately: Goety Iron `3.1`, Goety Cataclysm `1.21.1-1.8.2`.

The current modlist and runtime logs are authoritative for the installed `3.1.4` identity.

## Documentation drift warning

Public Goety pages currently visible for Minecraft 1.21.1 are behind the installed runtime in places. CurseForge/public port surfaces prominently expose 3.0.x while the pack is running 3.1.4. Therefore:

- the public Wiki is accepted as a **baseline for capability names, progression concepts and provider identity**;
- public older Wiki values are **not** accepted as exact 3.1.4 numeric authority;
- costs, cooldowns, durations, damage, servant limits and exact acquisition details remain `UNVERIFIED FOR 3.1.4` unless current-artifact/current-version evidence is found.

## Core resource authority — Soul Energy

Goety owns a real **Soul Energy** economy.

Public provider documentation establishes the following loop:

1. obtain/equip a soul totem such as Totem of Roots;
2. kill mobs to generate Soul Energy, with entity type affecting yield;
3. store Soul Energy in provider totems, with Totem of Souls offering greater capacity;
4. spend Soul Energy on spellcasting, artifices, crafting and servant-related systems;
5. use wands/staves equipped with a **Focus** to cast provider spells.

Black Arcana must not synthesize a second generic `Goety Soul Energy` pool from death events. Any integration must read/consume/refund the provider-owned resource through a verified public/runtime-safe surface.

## Focus casting model

Goety spells are represented by **Focuses** inserted into compatible Wands/Staves. The public baseline lists a large focus surface grouped by domain. Current 3.1.4 numeric properties are pending, but these names already establish semantic coverage for deduplication.

### Magic — 24 baseline focuses

1. Vexing Focus
2. Biting Focus
3. Feasting Focus
4. Teeth Focus
5. Shredding Focus
6. Mirror Focus
7. Ignite Focus
8. Fire Breath Focus
9. Soul Bolt Focus
10. Magic Bolt Focus
11. Magic Sword Focus
12. Soul Light Focus
13. Glow Light Focus
14. Crafting Focus
15. Iron Hide Focus
16. Bulwark Focus
17. Soul Heal Focus
18. Shockwave Focus
19. Weakening Focus
20. Arrow Rain Focus
21. Telekinesis Focus
22. Command Focus
23. Sonic Boom Focus
24. Corruption Focus

### Necromancy — 11 baseline focuses

1. Rotting Focus
2. Osseous Focus
3. Ghost Fire Focus
4. Reaping Focus
5. Spooky Focus
6. Phantasm Focus
7. Vanguard Focus
8. Blackguard Focus
9. Leeching Focus
10. Killing Focus
11. Skull Focus

### Geomancy — 8 baseline focuses

1. Barricade Focus
2. Quaking Focus
3. Pulverize Focus
4. Rotation Focus
5. Burrowing Focus
6. Sensing Focus
7. Scatter Focus
8. Eruption Focus

### Frost — 9 baseline focuses

1. Frost Breath Focus
2. Ice Spike Focus
3. Ice Storm Focus
4. Hail Focus
5. Iceology Focus
6. Blizzard Focus
7. Chilling Focus
8. Frost Nova Focus
9. Frostborn Focus

### Wild — 11 baseline focuses

1. Swarm Focus
2. Poison Dart Focus
3. Blossoming Focus
4. Grapple Focus
5. Hunting Focus
6. Mauling Focus
7. Slimy Focus
8. Overgrowth Focus
9. Entangling Focus
10. Whispering Focus
11. Leaping Focus

### Wind — 8 baseline focuses

1. Launching Focus
2. Flight Focus
3. Cushion Focus
4. Whirlwind Focus
5. Cyclone Focus
6. Updraft Focus
7. Wind Blast Focus
8. Trembling Focus

### Storm — 8 baseline focuses

1. Charge Focus
2. Shocking Focus
3. Thunderbolt Focus
4. Electrocute Focus
5. Monsoon Focus
6. Discharge Focus
7. Bolting Focus
8. Lighting Focus

### Abyss — 8 baseline focuses

1. Bubble Stream Focus
2. Bouncy Bubble Focus
3. Steaming Focus
4. Trident Storm Focus
5. Prisma Beam Focus
6. Guardian Focus
7. Biomine Focus
8. Tidal Focus

### Nether — 10 baseline focuses

1. Fireball Focus
2. Lava Bomb Focus
3. Bombardment Focus
4. Meteor Shower Focus
5. Magma Bomb Focus
6. Fire Blast Focus
7. Flame Strike Focus
8. Wither Skull Focus
9. Ghastly Focus
10. Blazing Focus

### Void — 12 baseline focuses

1. Call Focus
2. Troop Focus
3. Recall Focus
4. Ender Chest Focus
5. End Walk Focus
6. Blink Focus
7. Banish Focus
8. Tunnel Focus
9. Rupture Focus
10. Watching Focus
11. Blasting Focus
12. Snaring Focus

**Baseline total: 109 named Focuses.**

This number is a public-Wiki capability baseline, **not a claim that the installed 3.1.4 JAR contains exactly 109 player-usable focuses**. Phase 2 still requires an installed/current-artifact registry reconciliation.

## Wands / staffs — baseline provider casting authorities

Public provider content lists:

- Dark Wand
- Ominous Staff
- Necro Staff
- Geo Staff
- Wind Staff
- Storm Staff
- Frost Staff
- Wild Staff
- Abyss Staff
- Void Staff
- Nether Staff
- Nameless Staff

School/domain staff bonuses, costs and restrictions remain pending for exact 3.1.4 verification.

## Research and acquisition

Goety uses research rather than granting its advanced content as generic spell scrolls.

Public provider documentation establishes that **Research Scrolls** can unlock recipes, rituals, servant systems and Focuses. Examples include:

- Buried/necromancy-related research unlocking necromancer servant rituals and bound-servant content;
- research paths for Vanguard / Blackguard Focuses and servant rituals;
- Bygone research unlocking Blaze and Wildfire rituals plus the Blazing Focus and Nether equipment;
- higher research paths for advanced constructs and Lich-related progression.

Most advanced Focuses are therefore progression-bound and should not be granted by Black Arcana merely because the player has learned a semantically similar school.

## Servants and binding authority

Goety is a major **servant authority** in the pack. Its servant families include undead, wild/natural, Nether, Void and other magical entities. Public provider documentation also establishes that some servant families can be healed using owner Soul Energy under appropriate equipment states and that persistence/limits may depend on provider gear.

Consequences:

- a Goety servant is not automatically a generic Black Arcana familiar;
- Black Arcana may maintain a cross-provider `relationship` record only if it can prove the provider servant identity/owner and lifecycle safely;
- Soul Energy healing/cost stays Goety-owned;
- servant caps/persistence must not be bypassed through Binding.

## Witchcraft surface

Goety already exposes explicit witchcraft/preparation content in addition to Focus spellcasting. Public baseline content includes:

- Taglock Kit;
- Waystone;
- Cauldron Ladle;
- Brew;
- Splash Brew;
- Lingering Brew;
- Gas Brew;
- Refuse Bottle;
- `The Witch's Brews` documentation.

This is a major dedup constraint for the planned integrated Witchcraft system. Black Arcana must not create a second generic taglock or brew-delivery engine if Goety already owns the needed behavior.

### Constantine-style consequence

The planned sympathetic/identity magic must audit **Goety Taglock** before implementing any `true-name`, hair/blood sample or personal-object targeting mechanism. If Taglock already provides the identity proof required for a ritual, Black Arcana should integrate it as a provider-native evidence token rather than create a cosmetically different taglock.

## Infernal / Nether consequences

Goety already has a substantial Nether Focus family: Fireball, Lava Bomb, Bombardment, Meteor Shower, Magma Bomb, Fire Blast, Flame Strike, Wither Skull, Ghastly and Blazing.

Therefore the planned Black Arcana Infernal school cannot justify itself as `stronger fire magic` or `Nether fire spells`. Its real delta must remain the separate **Nether-bound Infernal Lava reservoir + binding/structure/resource economy**, with only spell effects that remain semantically distinct after Goety, Iron's Fire, Cataclysm and Ignis/Soulfire providers are fully cataloged.

## Soul / death consequences

Goety occupies:

- death-derived Soul Energy;
- soul-powered spellcasting;
- soul-powered artifacts;
- necromancy;
- servant summoning/control;
- soul healing/utility;
- ritual progression.

This sharply limits any generic Black Arcana `soul mana` proposal. Black Arcana 07.02 must continue treating provider-native resources distinctly: `Goety Soul Energy` is not interchangeable with Malum spirits, Eidolon Soul Shards, Blood reservoir mB or ordinary Iron's mana.

## Existing overlaps with other installed providers

Several baseline Goety focuses directly overlap broad capabilities already present elsewhere:

- Telekinesis → Iron's Eldritch Telekinesis / Ars movement primitives;
- Soul Heal → Iron's/Ars healing families but with a different resource/provider identity;
- Ignite / Fire Breath / Fireball / Magma Bomb / Wither Skull → Iron's Fire/Blood/Goety Nether and Cataclysm overlap;
- Blink / Recall / Ender Chest / Banish → Iron's Ender + Ars displacement/utility;
- Bulwark → Iron's Shield / Paladin Bulwark / Ars Bubble Shield;
- Sonic Boom → Iron's Eldritch Sonic Boom / Ars ecosystem variants;
- servant summons → Iron's/Ars/Asterism/Mobstein and Black Arcana 07.07 territory.

These overlaps must be resolved semantically before Phase 3 approves any duplicate-looking Black Arcana spell.

## Goety addons in the current pack

### Goety Iron 3.1

Bridge/provider addon between Goety and Iron's. It is cataloged separately because it can change servant/spell integration and authority boundaries.

### Goety Cataclysm 1.21.1-1.8.2

Content addon integrating Cataclysm themes/entities/powers into Goety's Soul Energy / Focus / servant ecosystem. It must be cataloged separately before Infernal, summoning and boss-power gaps are considered final.

## Provenance status

Public 1.21.1 port repositories expose MIT licensing for some 3.0.x source lines, but Phase 2 has **not established that those exact source snapshots correspond to installed Goety 3.1.4**. Therefore no current implementation may be derived from those repositories merely because the older port is MIT.

Current 3.1.4 implementation provenance/API surface remains `PENDING`.

## Open audit items

- reconcile the actual 3.1.4 Focus registry against the 109-name public baseline;
- extract current 3.1.4 costs/cooldowns/damage/duration/range where a current artifact/API/doc source is available;
- catalog every Research Scroll and exact acquisition/gate;
- catalog servant families, owner identity, cap/persistence and Soul Energy healing semantics;
- catalog Goety Witchcraft/taglock behavior;
- catalog Goety Iron 3.1;
- catalog Goety Cataclysm 1.21.1-1.8.2;
- identify public integration/API hooks suitable for Black Arcana without bypassing provider authority.

## Phase 3 gate

Goety-related Black Arcana implementation is `BLOCKED` until the installed 3.1.4 registry and relevant addon surfaces are reconciled.
