# Capability Coverage Matrix

Status: `PHASE 2 — ACTIVE DEDUPLICATION`

This matrix is not a wish list. A row only becomes a Phase 3 candidate after every relevant installed provider has been cataloged sufficiently to prove a real semantic gap.

| Capability family | Providers currently known to touch it | Coverage state | Phase 3 decision |
|---|---|---|---|
| Healing / regeneration / life transfer | Iron's Holy/Blood; Ars Nouveau Heal; Ars Elemental Life Link/Phantom Grasp; Paladin defensive kit; Vampirism; Malum/Eidolon candidates | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Teleport / portals / displacement | Iron's Ender/Eldritch; Ars Nouveau Blink/Exchange/Rewind; Asterism Astral Echo/Gateway concept; Leyline; Immersive Portal bridge; Black Arcana 07.04 | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Telekinesis / forced movement / gravity | Iron's Telekinesis/Black Hole/Gravity Fissure/Gust; Ars Nouveau Pull/Knockback/Launch/Gravity; Ars Elemental Geyser; Black Arcana Vector Reversal | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Summons / familiars / servants | Iron's summons; Ars Nouveau Animate Block/Summon Decoy/Steed/Undead/Vex/Wolves; Ars Elemental Bee/Slime; Asterism Lunar Moth; Goety; Alshanex; Mobstein; Black Arcana pending 07.07 | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Blood / sacrifice / life-cost casting | Iron's Blood; Apprentice's Codex Blood Brand (mechanics pending); Vampirism/Bloodlines; Black Arcana 07.01; Vampire Spells bridge | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Soul / spirit / death economy | Goety; Malum; Eidolon; Ars Hex Soul Shatter; Ars Elemental Phantom Grasp; Black Arcana 07.02; Soul Fire'd related content | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Holy / divine / celestial | Iron's Holy; Paladin Spells (5-spell public kit); Asterism Astral school (11 public entries, one creative-only gateway); Eidolon theurgy candidates | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Fire / infernal / soul fire | Iron's Fire; Ars Nouveau Ignite/Flare; Ars Elemental fire interactions; Somake 1.0.8 Soul/Infernal Fire ritual path; Ignis Soulfires addons; Soul Fire'd; Cataclysm integrations | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Poison / toxicity / blight / mutagen | Iron's Nature; Ars Nouveau Harm/Hex; Ars Elemental Envenom/Poison Spores; Toxony; Hexalia | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Countermagic / dispel / negation | Iron's Counterspell; Ars Nouveau Dispel; Ars Elemental Nullify Defense; Dreamless | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Shields / wards / barriers | Iron's Shield/Fang Ward; Ars Elemental Bubble Shield; Paladin Bulwark/Bedrock Skin; Asterism Celestial Tether/Silvery Barbs; Black Arcana fields | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Time / haste / slow / recurrence | Iron's Haste/Slow; Ars Nouveau Delay/Rewind/Extend/Reduce Time; Ars Controle Precise Delay; Leyline; Somake candidates; Black Arcana recurrence mechanics | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Reality / domain / localized rules | Black Arcana 07.06; Iron's Pocket Dimension; Ars Nouveau Intangible/Rewind/Wall/Linger; Ars Zero geometry candidates; other providers TBD | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Chaos / probability / entropy | Ars Nouveau Randomize; **Ars Controle Filter: Random with documented probability formula**; broad elemental/state effects across Iron's/Ars/Somake | **PROBABILITY PARTIAL COVERAGE PROVEN; ENTROPY/REALITY DELTA NOT YET PROVEN** | BLOCKED |
| Order / seals / imposed laws | Iron's control/countermagic; Ars Nouveau Rune/Wall/Snare/Dispel/Gravity; Ars Controle boolean filters/Precise Delay; Ars Zero Geometrize + geometry augments; Asterism Tether/Echo; Paladin defensive contracts | **LOGIC/GEOMETRY/CONSTRAINT PARTIAL COVERAGE PROVEN; AUTHORITATIVE LAW DELTA NOT YET PROVEN** | BLOCKED |
| Typed binding / external resource routing | **Ars Elemental Life Link directly covers damage/healing linkage**; Paladin Sworn Protector covers ally damage interception; Iron's/Goety/Ars summons; Black Arcana 07.01/07.02 and planned resource contracts | **GENERIC LIFE/DAMAGE LINK COVERAGE PROVEN; PERSISTENT TYPED RESOURCE-ROUTING DELTA STILL POSSIBLE BUT UNPROVEN** | BLOCKED |
| Divination / remote sight / detection | Iron's Planar Sight; Ars Nouveau Sense Magic; Apprentice's Codex remote vision/structure/treasure locating; Black Arcana 07.07 pending | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Aggro / protector / damage interception | Paladin Taunt/Sworn Protector; Ars Nouveau Summon Decoy; Asterism protection; other providers pending | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Geometry / patterned spell placement | Ars Zero Geometrize + Cube/Sphere/Flatten/Hollow; Ars forms/fields; Black Arcana domain geometry | COVERAGE PROVEN / FULL PROVIDER AUDIT INCOMPLETE | BLOCKED |

## Proven Phase 2 constraints on new schools

### Chaos

`Randomize` and `Filter: Random` mean that generic randomness and tunable binary probability are **not gaps**. A future Chaos candidate must prove a stronger semantic delta such as persistent entropy, weighted outcome families, probability debt/compensation, bounded law corruption or another mechanic that cannot already be composed by the installed providers.

### Order

Boolean logic, runes, walls, immobilization, geometric spell placement, counters, shields and anchor-like effects are all already represented somewhere in the pack. Order must prove an **authoritative imposed-law/seal system**, not a visual geometry rename.

### Arcana Vincular

A simple damage/healing link is **not a gap** because Ars Elemental `Life Link` already does it, and Paladin `Sworn Protector` already performs ally damage interception. The remaining candidate delta is the larger typed persistent relationship/resource-routing architecture: blood reservoir, spirit source, familiar/servant, ritual artifact or living donor, with reserve/commit/refund, lifecycle, consent/protection, recursion prevention and fail-closed behavior.

## Gate

No row may be changed from `BLOCKED` to an implementation candidate until the involved provider pages carry enough evidence to distinguish:

1. same mechanic with different visuals/name;
2. partial overlap;
3. distinct mechanic with a real gameplay delta;
4. unsupported/unverifiable behavior that must remain fail-closed.
