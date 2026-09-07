# Capability Coverage Matrix

Status: `PHASE 2 — ACTIVE DEDUPLICATION`

This matrix is not a wish list. A row only becomes a Phase 3 candidate after every relevant installed provider has been cataloged sufficiently to prove a real semantic gap.

| Capability family | Providers currently known to touch it | Coverage state | Phase 3 decision |
|---|---|---|---|
| Healing / regeneration / life transfer | Iron's Holy/Blood; Ars Nouveau Heal; Ars Elemental Life Link/Phantom Grasp; Paladin defensive kit; **Vampirism native blood/saturation regeneration + Regen action**; **Bloodlines 3.0.9 Noble Leeching + Gravebound Regen Devour/Soul Infusion source-pinned**; **Vampire Spells Addon 0.0.9 Ray/Devour delivered-damage→blood restoration + Holy-heal inversion for Vampires**; Malum/Eidolon candidates | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Teleport / portals / displacement | Iron's Ender/Eldritch; Ars Nouveau Blink/Exchange/Rewind; Asterism Astral Echo/Gateway concept; Leyline; **Vampirism Teleport action (1.10.13 source-pinned, 50-block default)**; **Bloodlines Noble Flank + Zealot Shadowwalk + Gravebound Phylactery Teleport source-pinned**; Immersive Portal bridge; Black Arcana 07.04 | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Telekinesis / forced movement / gravity | Iron's Telekinesis/Black Hole/Gravity Fissure/Gust; Ars Nouveau Pull/Knockback/Launch/Gravity; Ars Elemental Geyser; Ars Zero Push/Anchor/Remove Gravity; Black Arcana Vector Reversal | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Summons / familiars / servants | Iron's summons; Ars Nouveau Animate Block/Summon Decoy/Steed/Undead/Vex/Wolves; Ars Elemental Bee/Slime; Asterism Lunar Moth; Goety; Alshanex; Mobstein; **Vampirism Lord minions + 7 Minion Tasks + Summon Bats**; Black Arcana pending 07.07 | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Blood / sacrifice / life-cost casting | Iron's Blood; Apprentice's Codex Blood Brand (mechanics pending); **Vampirism 1.10.13 blood bar/saturation/exhaustion + `vampirism:blood` fluid + 100 mB/unit conversion + storage/conversion API**; **Bloodlines 3.0.9 source-pinned: Noble/Bloodknight mutate or consume the canonical Vampirism blood pipeline; Flesh Eating/Fishmonger feed it; no second Bloodlines blood bar**; **Vampire Spells Addon 0.0.9 source-pinned: eligible Vampire Blood-school casts atomically replace insufficient mana with real Vampirism blood; Ray remains mana-paid; Ray/Devour restore blood from delivered health damage**; Black Arcana 07.01 | **VAMPIRISM BASE BLOOD ECONOMY + BLOODLINES SPECIALIZATION + VAMPIRE SPELLS 0.0.9 CAST BRIDGE SOURCE-PINNED; RUNTIME QA INCOMPLETE** | BLOCKED |
| Soul / spirit / death economy | Goety; Malum; Eidolon; Ars Hex Soul Shatter; Ars Elemental Phantom Grasp; **Bloodlines 3.0.9 Gravebound Souls + Devour + Phylactery storage + Mist Form/Possession costs source-pinned and explicitly separate from generic soul resources**; Black Arcana 07.02; Soul Fire'd related content | **SUBSTANTIAL PARTIAL COVERAGE PROVEN / CROSS-PROVIDER SOUL SEMANTICS MUST REMAIN DISTINCT** | BLOCKED |
| Holy / divine / celestial | Iron's Holy; Paladin Spells (5-spell public kit); Asterism Astral school (11 public entries, one creative-only gateway); Eidolon theurgy candidates; **Bloodlines Ectotherm Holy Water Diffusion and Gravebound vulnerable-damage tags**; **Vampire Spells Addon 0.0.9 source-pinned Vampire overlay: NPC Vampire Holy damage ×2, delivered Holy damage reflects to Vampire caster, Holy heals damage/suppress, six Holy utilities cancel with self-damage** | **SUBSTANTIAL PARTIAL COVERAGE PROVEN; VAMPIRE HOLY INTEROP SOURCE-PINNED / RUNTIME QA PENDING** | BLOCKED |
| Fire / infernal / soul fire | Iron's Fire; Ars Nouveau Ignite/Flare; Ars Elemental fire interactions; Ars Zero Fire Voxel; Somake 1.0.8 Soul/Infernal Fire ritual path; Ignis Soulfires addons; Soul Fire'd; Cataclysm integrations | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Poison / toxicity / blight / mutagen | Iron's Nature; Ars Nouveau Harm/Hex; Ars Elemental Envenom/Poison Spores; Ars Zero Conjure Blight; **Bloodlines Zealot Poisoned Strike + Gravebound poison immunity/healing source-pinned**; Toxony; Hexalia | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Countermagic / dispel / negation | Iron's Counterspell; Ars Nouveau Dispel; Ars Elemental Nullify Defense; Dreamless | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Shields / wards / barriers | Iron's Shield/Fang Ward; Ars Elemental Bubble Shield; Paladin Bulwark/Bedrock Skin; Asterism Celestial Tether/Silvery Barbs; Ypsilon Saeptum provider-native spherical barrier/domain; **Vampirism Half Invulnerable (late blood settlement)**; Black Arcana fields | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Time / haste / slow / recurrence | Iron's Haste/Slow; Ars Nouveau Delay/Rewind/Extend/Reduce Time; Ars Controle Precise Delay; Ars Zero Temporal Context; Not Enough Glyphs Contingencies; Leyline; Somake candidates; **Bloodlines Celerity/Shadow Mastery/Obscured Power/Underwater Duration modify provider action timing or movement speed**; Black Arcana recurrence mechanics | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Reality / domain / localized rules | Black Arcana 07.06; Iron's Pocket Dimension; Ars Nouveau Intangible/Rewind/Wall/Linger; Ars Zero multi-phase/voxel/geometry primitives; Ypsilon Saeptum (20-block provider-native domain with sphere barrier, block restoration, entity return and clash lifecycle); other providers TBD | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Chaos / probability / entropy | Ars Nouveau Randomize; **Ars Controle Filter: Random with documented probability formula**; Not Enough Glyphs Randomize Binder thread; broad elemental/state effects across Iron's/Ars/Somake | **GENERIC RANDOMNESS/PROBABILITY PARTIAL COVERAGE PROVEN; ENTROPY/REALITY DELTA NOT YET PROVEN** | BLOCKED |
| Order / seals / imposed laws | Iron's control/countermagic; Ars Nouveau Rune/Wall/Snare/Dispel/Gravity; Ars Controle boolean filters/Precise Delay; Not Enough Glyphs Plane; Ars Zero Geometrize + geometry augments; Asterism Tether/Echo; Paladin defensive contracts | **LOGIC/GEOMETRY/CONSTRAINT PARTIAL COVERAGE PROVEN; AUTHORITATIVE LAW DELTA NOT YET PROVEN** | BLOCKED |
| Typed binding / external resource routing | **Ars Elemental Life Link directly covers damage/healing linkage**; Paladin Sworn Protector covers ally damage interception; Iron's/Goety/Ars summons; **Vampirism exposes real Blood fluid/storage/conversion and player-blood transactions but keeps tank fluid distinct from player BloodStats**; **Bloodlines Gravebound binds player state to a dimension+BlockPos+owner Phylactery and conservatively transfers Souls between provider stores**; Black Arcana 07.01/07.02 and planned resource contracts | **GENERIC LIFE/DAMAGE LINK + EXTERNAL BLOOD STORAGE + PROVIDER-NATIVE SOUL/PHYLACTERY BINDING PROVEN; PERSISTENT MULTI-PROVIDER RESOURCE-ROUTING DELTA STILL POSSIBLE BUT UNPROVEN** | BLOCKED |
| Divination / remote sight / detection | Iron's Planar Sight; Ars Nouveau Sense Magic; Apprentice's Codex remote vision/structure/treasure locating; **Vampirism Night Vision/Blood Vision/Hunter Awareness**; Black Arcana 07.07 pending | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Aggro / protector / damage interception | Paladin Taunt/Sworn Protector; Ars Nouveau Summon Decoy; Asterism protection; **Vampirism Hissing, Lord/minion protect/defend tasks, Half Invulnerable**; other providers pending | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Geometry / patterned spell placement | Ars Zero Geometrize + Cube/Sphere/Flatten/Hollow history; Not Enough Glyphs Plane/Flatten-related coverage; Ars forms/fields; Ypsilon Saeptum provider-native spherical barrier/domain; Black Arcana domain geometry | SUBSTANTIAL COVERAGE PROVEN / FULL PROVIDER AUDIT INCOMPLETE | BLOCKED |
| Conditional / contingency / event-triggered casting | Not Enough Glyphs Contingencies; Ars Additions Retaliate; Ars Zero begin/tick/end containers + Temporal Context | **GENERIC CONDITION-TRIGGERED EXECUTION PARTIAL COVERAGE PROVEN** | BLOCKED |
| Stored-reference / remote-target casting | Ars Additions Mark + Reliquary + Recall; Ars remote-access infrastructure; other divination/portal providers pending | **PERSISTENT TARGET-REFERENCE PRIMITIVE PROVEN / BROADER AUDIT INCOMPLETE** | BLOCKED |
| Spell containers / cross-engine spellbook casting | Not Enough Glyphs SpellBinder; Ars 'n' Spells Spellbook Binding/Transcription + Ars spells in Iron's spellbooks/native wheel; native Iron's/Ars containers | **CROSS-CONTAINER AND CROSS-ENGINE CASTING PARTIAL COVERAGE PROVEN; VAMPIRE SPELLS 0.0.9 AUDITED AS RESOURCE/HOLY OVERLAY, NOT A CONTAINER PROVIDER** | BLOCKED |
| Mana/resource unification across magic engines | Ars 'n' Spells Ars Nouveau ↔ Iron's mana/progression bridge; native Ars Source remains separate infrastructure; provider-specific resources such as Goety Soul Energy/Malum spirits/**Vampirism BloodStats + Blood fluid/Bloodlines perk points/Gravebound Souls** remain independent; **Vampire Spells Addon 0.0.9 provides a narrow atomic mana→Vampirism-blood substitution only for eligible Vampire casts of Iron's Blood School, not global resource unification** | **ARS↔IRON'S GENERIC UNIFICATION PROVEN; VAMPIRE SPELLS NARROW CAST TRANSACTION PROVEN; BLOODLINES RESOURCES EXPLICITLY DISTINCT; OTHER RESOURCE TYPES MUST NOT BE COLLAPSED** | BLOCKED |
| Create-integrated magic automation / moving magic infrastructure | Ars Creo contraption turrets/Source Jars/ritual support + Starbuncle Wheel; Ars Technica processing glyphs, Source Motor, logistics/transmutation; Create: Wizardry and other bridges pending | **SUBSTANTIAL PARTIAL COVERAGE PROVEN / FULL TECHNOMAGIC AUDIT INCOMPLETE** | BLOCKED |

## Proven Phase 2 constraints on new schools

### Chaos

`Randomize`, Ars Controle `Filter: Random`, and the Not Enough Glyphs `Randomize` Binder thread mean that generic randomness and tunable probability are **not gaps**. Current NEG migration evidence also establishes that the generic `Random` filter moved to Ars Controle in the current 4.6.1 line, so it must not be double-counted as a second NEG-owned filter.

A future Chaos candidate must prove a stronger semantic delta such as persistent entropy, weighted outcome families, probability debt/compensation, bounded law corruption or another mechanic that cannot already be composed by the installed providers.

### Order

Boolean logic, runes, walls, immobilization, geometric spell placement, counters, shields, Not Enough Glyphs Plane and Ars Zero Geometrize/shape composition are already represented somewhere in the pack. Order must prove an **authoritative imposed-law/seal system**, not a visual geometry rename.

### Arcana Vincular

A simple damage/healing link is **not a gap** because Ars Elemental `Life Link` already does it, and Paladin `Sworn Protector` already performs ally damage interception. Vampirism additionally proves a native external Blood-fluid storage/conversion surface, while Bloodlines proves a provider-native Gravebound Soul↔Phylactery binding/transfer surface. These stores remain semantically independent.

The remaining candidate delta is the larger typed persistent relationship/resource-routing architecture: blood reservoir, spirit source, familiar/servant, ritual artifact or living donor, with reserve/commit/refund, lifecycle, consent/protection, recursion prevention and fail-closed behavior.

A large Black Arcana blood reservoir therefore may reuse actual `vampirism:blood`, but **tank capacity must not be silently mapped to player max blood**, and the same mB cannot be settled simultaneously as player blood and magical fuel. Likewise Gravebound Souls/Phylactery storage must not become a generic soul reservoir for Goety, Malum or Black Arcana without an explicit conversion contract.

### Vampirism-native actions, Bloodlines and blood

The 1.10.13 base provider audit proves that native Vampire/Hunter/Lord actions are not Iron's spells and have their own action handler, cooldown/duration, skill gates and event lifecycle. The blood economy is also food-like: vanilla exhaustion is routed into Vampirism exhaustion, saturation is consumed before blood, and natural blood-based regeneration is provider-owned.

Bloodlines 3.0.9 is now source-pinned as a separate structural layer over this base provider: five Bloodlines, 101 skills, 29 actions, 22 tasks, Bloodline perk points and Gravebound Souls/Phylactery are cataloged. Its actions still use the Vampirism ActionHandler and its Vampire-blood mechanics still settle through Vampirism blood APIs/events.

Consequences:

- generic `LivingHealEvent` is insufficient to classify Vampirism natural regeneration or Noble/Gravebound healing as generic lifesteal;
- Bat must not receive an inferred immediate blood cost because its native path adds exhaustion;
- Half Invulnerable must not be pre-charged because its blood settlement occurs only on a qualifying blocked hit;
- `collect_blood` already provides servant-driven automated Blood Bottle production;
- Bloodknight action costs/upkeep must not be charged twice by Black Arcana;
- Gravebound Souls, Bloodline perk points and Vampirism blood are distinct resource domains;
- Gravebound Devour action activation alone is not sufficient proof that a Soul was acquired;
- Mist Form must retain its lethal-hit/Soul/cooldown/logout lifecycle rather than being flattened into generic invulnerability;
- **Vampire Spells Addon 0.0.9 is source-pinned as an Iron's Blood/Holy bridge only; it does not convert native Vampirism/Bloodlines Actions into spells or apply Iron's mana/cooldown semantics to them**.

### Cross-engine casting and mana

Ars 'n' Spells **3.3.0 is the installed bridge** and current official release material continues to cover generic Ars Nouveau ↔ Iron's mana/progression interoperability, inscription/transcription and casting Ars spells from Iron's spellbooks/native wheel. The 3.3.0 release also reports reworked resource payment, long-cast handling and protection against stale/repeated cross-cast requests. A Black Arcana feature that only repeats that bridge is not a gap. Any integration must preserve one causal cast and one canonical provider settlement rather than process the same action once per host engine.

Vampirism's Blood resource remains an independent provider resource. **Vampire Spells Addon 0.0.9 defines one specific exception:** for an eligible Vampire cast of an Iron's Blood School spell, the addon can atomically replace the current mana payment with a Vampirism blood payment. Ray of Siphoning is explicitly excluded, and the bridge does not unify the pools globally. Bloodlines does not broaden this exception: its own perk wallet and Gravebound Souls remain separate. Black Arcana must not generalize the narrow cast transaction into a universal mana↔blood↔soul converter or process the same cast once in each resource engine.

### Conditional casting

Not Enough Glyphs Contingencies already stores a spell for later condition-triggered execution, while Ars Additions Retaliate and Ars Zero phase/context primitives provide other conditional execution patterns. Therefore “automatically cast a stored spell when X happens” alone is not a new Black Arcana mechanic.

### Create-integrated magic

Ars Creo already allows Ars systems on Create contraptions and Ars Technica already maps magical actions/resources into Create-style processing/kinetics. A dark-themed turret, processing spell or moving-contraption cast is not automatically a Phase 3 gap.

## Gate

No row may be changed from `BLOCKED` to an implementation candidate until the involved provider pages carry enough evidence to distinguish:

1. same mechanic with different visuals/name;
2. partial overlap;
3. distinct mechanic with a real gameplay delta;
4. unsupported/unverifiable behavior that must remain fail-closed.