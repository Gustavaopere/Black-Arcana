# Goety 3.1.4 — Focus catalog

Status: `OFFICIAL PUBLIC-WIKI INVENTORY 110/110 NAMES / EXACT 3.1.4 JAR REGISTRY RECONCILIATION PENDING`

## Evidence boundary

This file catalogs the **current public official Goety Focus inventory** for semantic coverage and deduplication. It does **not** claim that every listed name has been independently proven in the installed `goety-3.1.4.jar` registry.

Installed authority:

- mod id: `goety`;
- JAR: `goety-3.1.4.jar`;
- runtime version: `3.1.4`;
- NeoForge 1.21.1;
- exact public release pinned separately in the provider README.

Current exact 3.1.4 source/API internals are unavailable through an auditable official 1.21.1 source pin. Registry IDs, costs, cooldowns, damage, duration, range and settlement hooks therefore remain `UNVERIFIED FOR EXACT 3.1.4` unless separately evidenced.

## Casting authority

Goety Focuses are provider-owned spell units used through compatible Wands/Staffs. Black Arcana must not:

- translate one Focus activation into a second Black Arcana cast;
- externally charge Soul Energy for a Goety cast;
- invent registry ids from English display names;
- grant a Focus merely because an RPG mastery or Black Arcana domain has similar semantics;
- treat a specialized Staff modifier as an independent spell event.

## Public inventory by provider category

### Magic — 25

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
25. Order Focus

The earlier preparatory count of 24 Magic Focuses omitted **Order Focus**. The corrected public-family count is 25.

### Necromancy — 11

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

### Geomancy — 8

1. Barricade Focus
2. Quaking Focus
3. Pulverize Focus
4. Rotation Focus
5. Burrowing Focus
6. Sensing Focus
7. Scatter Focus
8. Eruption Focus

### Frost — 9

1. Frost Breath Focus
2. Ice Spike Focus
3. Ice Storm Focus
4. Hail Focus
5. Iceology Focus
6. Blizzard Focus
7. Chilling Focus
8. Frost Nova Focus
9. Frostborn Focus

### Wild — 11

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

### Wind — 8

1. Launching Focus
2. Flight Focus
3. Cushion Focus
4. Whirlwind Focus
5. Cyclone Focus
6. Updraft Focus
7. Wind Blast Focus
8. Trembling Focus

### Storm — 8

1. Charge Focus
2. Shocking Focus
3. Thunderbolt Focus
4. Electrocute Focus
5. Monsoon Focus
6. Discharge Focus
7. Bolting Focus
8. Lighting Focus

### Abyss — 8

1. Bubble Stream Focus
2. Bouncy Bubble Focus
3. Steaming Focus
4. Trident Storm Focus
5. Prisma Beam Focus
6. Guardian Focus
7. Biomine Focus
8. Tidal Focus

### Nether — 10

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

### Void — 12

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

## Count reconciliation

| Category | Public count |
|---|---:|
| Magic | 25 |
| Necromancy | 11 |
| Geomancy | 8 |
| Frost | 9 |
| Wild | 11 |
| Wind | 8 |
| Storm | 8 |
| Abyss | 8 |
| Nether | 10 |
| Void | 12 |
| **Total** | **110** |

## Semantic overlap constraints

The public inventory is already sufficient to prove broad overlap families that Phase 3 must not ignore:

- **defense:** Iron Hide, Bulwark;
- **healing/sustain:** Soul Heal, Leeching;
- **telekinesis/control:** Telekinesis, Command, Weakening, Banish, Snaring;
- **mobility:** Grapple, Leaping, Launching, Flight, Updraft, Blink, End Walk;
- **summoning/servants:** Vexing, Rotting, Osseous, Vanguard, Blackguard, Guardian, Call, Troop and related families;
- **fire/nether:** Ignite, Fire Breath and the full Nether family;
- **cold:** the full Frost family;
- **storm/lightning:** the full Storm family;
- **earth/terrain-facing magic:** Geomancy family;
- **void/displacement:** Void family;
- **projectile/area offense:** Arrow Rain, Sonic Boom, Eruption, Blizzard, Meteor Shower and others.

This proves semantic coverage, not exact implementation equivalence. Final disposition still needs behavior-level evidence before declaring a Black Arcana idea duplicate or genuinely distinct.

## Individual-file policy

Do not create one `.md` per Focus from this public-name list alone. Individual Focus pages become appropriate when at least one of the following is available for the exact installed line:

1. exact official 3.1.4 registry/artifact evidence;
2. current official documentation giving enough per-Focus mechanics to satisfy the catalog contract;
3. direct runtime QA with reproducible evidence.

Until then, unknown numeric/mechanical fields remain fail-closed instead of being copied from older Goety branches or forks.

## Addon exclusion

The base 110 inventory excludes content owned by separately installed addons such as:

- Goety Iron `3.1`;
- Goety Cataclysm `1.21.1-1.8.2`.

Their Focuses/effects must be cataloged under their own provider folders so base Goety coverage is not inflated.
