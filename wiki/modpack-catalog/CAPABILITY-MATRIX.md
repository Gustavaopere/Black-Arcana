# Capability Coverage Matrix

Status: `PHASE 2 — ACTIVE DEDUPLICATION`

This matrix is not a wish list. A row only becomes a Phase 3 candidate after every relevant installed provider has been cataloged sufficiently to prove a real semantic gap.

| Capability family | Providers currently known to touch it | Coverage state | Phase 3 decision |
|---|---|---|---|
| Healing / regeneration / life transfer | Iron's Holy/Blood; Ars Nouveau Heal; Ars Elemental Life Link/Phantom Grasp; Paladin defensive kit; **Eidolon 0.5.0.2 Lay on Hands + Cure Zombie source-pinned**; **Vampirism native blood/saturation regeneration + Regen action**; **Bloodlines 3.0.9 Noble Leeching + Gravebound Regen Devour/Soul Infusion source-pinned**; **Vampiric Ageing 1.4.21 rank-based health/regen and Werewolf heal-on-bite surfaces source-pinned, with several healing knobs config-dependent**; **Werewolves 2.0.3.3 Health Reg + Health After Kill source-pinned, but exact effective tuning is runtime-QA blocked by static config/timing mismatches**; **Vampire Spells Addon 0.0.9 Ray/Devour delivered-damage→blood restoration + Holy-heal inversion for Vampires**; Malum candidates | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Teleport / portals / displacement | Iron's Ender/Eldritch; Ars Nouveau Blink/Exchange/Rewind; Asterism Astral Echo/Gateway concept; Leyline; **Vampirism Teleport action (1.10.13 source-pinned, 50-block default)**; **Bloodlines Noble Flank + Zealot Shadowwalk + Gravebound Phylactery Teleport source-pinned**; **Vampiric Ageing 1.4.21 Hunter Teleport (cumulative Tainted Age gate, 35-block default) + Limited Bat Mode movement/flight lifecycle source-pinned; dedicated-server QA pending**; Immersive Portal bridge; Black Arcana 07.04 | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Telekinesis / forced movement / gravity | Iron's Telekinesis/Black Hole/Gravity Fissure/Gust; Ars Nouveau Pull/Knockback/Launch/Gravity; Ars Elemental Geyser; Ars Zero Push/Anchor/Remove Gravity; Black Arcana Vector Reversal | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Summons / familiars / servants | Iron's summons; Ars Nouveau Animate Block/Summon Decoy/Steed/Undead/Vex/Wolves; Ars Elemental Bee/Slime; Asterism Lunar Moth; **Eidolon 0.5.0.2 has 11 official summon ritual recipes; provider spawn path does not itself prove player ownership/taming**; Goety; Alshanex; Mobstein; **Vampirism Lord minions + 7 Minion Tasks + Summon Bats**; **Werewolves 2.0.3.3 Lord minions reuse Vampirism ownership/task infrastructure and add `collect_werewolf_items`; Wolf Pack is a provider skill tied to Howling, runtime QA pending**; Black Arcana 07.07 pending | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Blood / sacrifice / life-cost casting | Iron's Blood; Apprentice's Codex Blood Brand (mechanics pending); **Eidolon 0.5.0.2 Dark sacrifice prayers + two official brazier crafting rituals with provider health requirements 20/40; do not double-charge health**; **Vampirism 1.10.13 blood bar/saturation/exhaustion + `vampirism:blood` fluid + 100 mB/unit conversion + storage/conversion API**; **Bloodlines 3.0.9 source-pinned: Noble/Bloodknight mutate or consume the canonical Vampirism blood pipeline; Flesh Eating/Fishmonger feed it; no second Bloodlines blood bar**; **Vampiric Ageing 1.4.21 source-pinned: Blood Tap settles through Vampirism bite/`drinkBlood` and `DRAINING` progression consumes the provider BloodDrinkEvent amount; no second Ageing blood pool**; **Werewolves 2.0.3.3 Bite/Bleeding are blood-adjacent provider combat mechanics; Bleeding may drain Vampirism blood but Werewolves does not expose a second player blood pool**; **Vampire Spells Addon 0.0.9 source-pinned: eligible Vampire Blood-school casts atomically replace insufficient mana with real Vampirism blood; Ray remains mana-paid; Ray/Devour restore blood from delivered health damage**; Black Arcana 07.01 | **MULTIPLE DISTINCT BLOOD/LIFE-COST SEMANTICS PROVEN; RESOURCE/HEALTH SETTLEMENT MUST REMAIN PROVIDER-NATIVE; RUNTIME QA INCOMPLETE** | BLOCKED |
| Soul / spirit / death economy | Goety; Malum; **Eidolon 0.5.0.2 own Soul capability + Soul Shards + Crystal/Absorption/summoning surfaces source-pinned; entity-master semantics and serialized Absorption capture remain provider-owned**; Ars Hex Soul Shatter; Ars Elemental Phantom Grasp; **Bloodlines 3.0.9 Gravebound Souls + Devour + Phylactery storage + Mist Form/Possession costs source-pinned and explicitly separate from generic soul resources**; Black Arcana 07.02; Soul Fire'd related content | **SUBSTANTIAL PARTIAL COVERAGE PROVEN / CROSS-PROVIDER SOUL SEMANTICS MUST REMAIN DISTINCT** | BLOCKED |
| Holy / divine / celestial | Iron's Holy; Paladin Spells (5-spell public kit); Asterism Astral school (11 public entries, one creative-only gateway); **Eidolon 0.5.0.2 Light Prayer, Holy Touch, Lay on Hands, Cure Zombie and Smite source-pinned; Smite settlement remains runtime-QA blocked**; **Bloodlines Ectotherm Holy Water Diffusion and Gravebound vulnerable-damage tags**; **Vampiric Ageing 1.4.21 source-pinned age-based Holy Water weakness/divisor pipeline for Vampires**; **Vampire Spells Addon 0.0.9 source-pinned Vampire overlay: NPC Vampire Holy damage ×2, delivered Holy damage reflects to Vampire caster, Holy heals damage/suppress, six Holy utilities cancel with self-damage** | **SUBSTANTIAL PARTIAL COVERAGE PROVEN; EIDOLON THEURGY + VAMPIRE HOLY INTEROP SOURCE-PINNED / RUNTIME QA PENDING** | BLOCKED |
| Fire / infernal / soul fire | Iron's Fire; Ars Nouveau Ignite/Flare; Ars Elemental fire interactions; Ars Zero Fire Voxel; **Eidolon Fire Chant source-pinned**; Somake 1.0.8 Soul/Infernal Fire ritual path; Ignis Soulfires addons; Soul Fire'd; Cataclysm integrations; **Vampiric Ageing 1.4.21 age-based fire/sun weakness divisors for Vampires source-pinned** | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Poison / toxicity / blight / mutagen | Iron's Nature; Ars Nouveau Harm/Hex; Ars Elemental Envenom/Poison Spores; Ars Zero Conjure Blight; **Bloodlines Zealot Poisoned Strike + Gravebound poison immunity/healing source-pinned**; Toxony; Hexalia | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Countermagic / dispel / negation | Iron's Counterspell; Ars Nouveau Dispel; Ars Elemental Nullify Defense; Dreamless | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Shields / wards / barriers | Iron's Shield/Fang Ward; Ars Elemental Bubble Shield; Paladin Bulwark/Bedrock Skin; Asterism Celestial Tether/Silvery Barbs; Ypsilon Saeptum provider-native spherical barrier/domain; **Vampirism Half Invulnerable (late blood settlement)**; **Werewolves form-specific damage reduction + Thick Fur are provider defensive mechanics, not generic ward spells**; Black Arcana fields | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Time / haste / slow / recurrence | Iron's Haste/Slow; Ars Nouveau Delay/Rewind/Extend/Reduce Time; Ars Controle Precise Delay; Ars Zero Temporal Context; Not Enough Glyphs Contingencies; Leyline; Somake candidates; **Eidolon Daylight/Moonlight rituals advance provider world time toward day/night**; **Bloodlines Celerity/Shadow Mastery/Obscured Power/Underwater Duration modify provider action timing or movement speed**; **Vampiric Ageing 1.4.21 Celerity + long-lived Step Assist/Water Walking action surfaces source-pinned; Celerity effective multiplier and several cooldown-unit semantics remain runtime-QA blocked**; Black Arcana recurrence mechanics | PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Reality / domain / localized rules | Black Arcana 07.06; Iron's Pocket Dimension; Ars Nouveau Intangible/Rewind/Wall/Linger; Ars Zero multi-phase/voxel/geometry primitives; Ypsilon Saeptum (20-block provider-native domain with sphere barrier, block restoration, entity return and clash lifecycle); other providers TBD | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Chaos / probability / entropy | Ars Nouveau Randomize; **Ars Controle Filter: Random with documented probability formula**; Not Enough Glyphs Randomize Binder thread; broad elemental/state effects across Iron's/Ars/Somake | **GENERIC RANDOMNESS/PROBABILITY PARTIAL COVERAGE PROVEN; ENTROPY/REALITY DELTA NOT YET PROVEN** | BLOCKED |
| Order / seals / imposed laws | Iron's control/countermagic; Ars Nouveau Rune/Wall/Snare/Dispel/Gravity; Ars Controle boolean filters/Precise Delay; Not Enough Glyphs Plane; Ars Zero Geometrize + geometry augments; Asterism Tether/Echo; Paladin defensive contracts | **LOGIC/GEOMETRY/CONSTRAINT PARTIAL COVERAGE PROVEN; AUTHORITATIVE LAW DELTA NOT YET PROVEN** | BLOCKED |
| Typed binding / external resource routing | **Ars Elemental Life Link directly covers damage/healing linkage**; Paladin Sworn Protector covers ally damage interception; Iron's/Goety/Ars summons; **Vampirism exposes real Blood fluid/storage/conversion and player-blood transactions but keeps tank fluid distinct from player BloodStats**; **Bloodlines Gravebound binds player state to a dimension+BlockPos+owner Phylactery and conservatively transfers Souls between provider stores**; **Eidolon entity Soul master assignment and Absorption serialized capture are provider-owned bindings, not generic cross-provider resource routing**; Black Arcana 07.01/07.02 and planned resource contracts | **GENERIC LIFE/DAMAGE LINK + EXTERNAL BLOOD STORAGE + PROVIDER-NATIVE SOUL/PHYLACTERY/CAPTURE BINDINGS PROVEN; PERSISTENT MULTI-PROVIDER RESOURCE-ROUTING DELTA STILL POSSIBLE BUT UNPROVEN** | BLOCKED |
| Divination / remote sight / detection | Iron's Planar Sight; Ars Nouveau Sense Magic; Apprentice's Codex remote vision/structure/treasure locating; **Eidolon 0.5.0.2 Catacombs locator ritual source-pinned**; **Vampirism Night Vision/Blood Vision/Hunter Awareness**; **Vampiric Ageing 1.4.21 Hunter Wise Eye + Werewolf Improved Senses invisibility-bypass source-pinned; exact Wise Eye duration and eye-action cooldown units runtime-QA blocked**; **Werewolves 2.0.3.3 Sense is tree-reachable but exact cooldown/radius semantics are static-QA blocked; `sixth_sense` has a consumer but no generated-tree path**; Black Arcana 07.07 pending | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Aggro / protector / damage interception | Paladin Taunt/Sworn Protector; Ars Nouveau Summon Decoy; Asterism protection; **Eidolon Allure/Repelling/Enthrall provide provider-native attraction, repulsion and undead control; Undead Lure remains runtime-unproven/inert at inspected source path**; **Vampirism Hissing, Lord/minion protect/defend tasks, Half Invulnerable**; **Werewolves Fear + Lord minion Protect/Defend task surface source-pinned**; other providers pending | SUBSTANTIAL PARTIAL COVERAGE PROVEN / AUDIT INCOMPLETE | BLOCKED |
| Transformation / shapeshifting / alternate body state | **Vampirism Bat action**; **Bloodlines Gravebound Mist Form**; **Vampiric Ageing Limited Bat Mode**; **Werewolves 2.0.3.3 Human/Beast/Survivalist player forms with provider transformation-time/full-moon/form lifecycle; `beast4l` is Alpha-Werewolf entity form, not a player action**; Identity/morph providers outside this magic queue | **SUBSTANTIAL PROVIDER-NATIVE TRANSFORMATION COVERAGE PROVEN / LIFECYCLES MUST NOT BE FLATTENED INTO GENERIC BUFFS** | BLOCKED |
| Supernatural environmental adaptation / weaknesses | **Vampirism/ageing sunlight-fire-Holy weaknesses**; **Werewolves Silver and Wolfsbane weaknesses, water Weakness unless Water Lover, form-native protections**; **Vampirism Integrations 1.10.2 Cold Sweat bridge is target/version eligible and default-enabled but runtime activation is unconfirmed; Cold Sweat remains body-temperature authority** | **DISTINCT PROVIDER WEAKNESSES/ADAPTATIONS PROVEN; COLD SWEAT COMPAT MUST REMAIN FAIL-CLOSED UNTIL EXACT RUNTIME ACTIVATION IS VERIFIED** | BLOCKED |
| Geometry / patterned spell placement | Ars Zero Geometrize + Cube/Sphere/Flatten/Hollow history; Not Enough Glyphs Plane/Flatten-related coverage; Ars forms/fields; Ypsilon Saeptum provider-native spherical barrier/domain; Black Arcana domain geometry | SUBSTANTIAL COVERAGE PROVEN / FULL PROVIDER AUDIT INCOMPLETE | BLOCKED |
| Conditional / contingency / event-triggered casting | Not Enough Glyphs Contingencies; Ars Additions Retaliate; Ars Zero begin/tick/end containers + Temporal Context | **GENERIC CONDITION-TRIGGERED EXECUTION PARTIAL COVERAGE PROVEN** | BLOCKED |
| Stored-reference / remote-target casting | Ars Additions Mark + Reliquary + Recall; Ars remote-access infrastructure; other divination/portal providers pending | **PERSISTENT TARGET-REFERENCE PRIMITIVE PROVEN / BROADER AUDIT INCOMPLETE** | BLOCKED |
| Spell containers / cross-engine spellbook casting | Not Enough Glyphs SpellBinder; Ars 'n' Spells Spellbook Binding/Transcription + Ars spells in Iron's spellbooks/native wheel; native Iron's/Ars containers | **CROSS-CONTAINER AND CROSS-ENGINE CASTING PARTIAL COVERAGE PROVEN; VAMPIRE SPELLS 0.0.9 AUDITED AS RESOURCE/HOLY OVERLAY, NOT A CONTAINER PROVIDER** | BLOCKED |
| Mana/resource unification across magic engines | Ars 'n' Spells Ars Nouveau ↔ Iron's mana/progression bridge; native Ars Source remains separate infrastructure; provider-specific resources such as Goety Soul Energy/Malum spirits/**Eidolon mana + Soul capability + deity reputation/research**, **Vampirism BloodStats + Blood fluid/Bloodlines perk points/Gravebound Souls**, and **Werewolves faction level/action/form/bite state** remain independent; **Vampiric Ageing adds Age Rank/progress/Tainted state but no interchangeable mana/blood/soul pool**; **Vampire Spells Addon 0.0.9 provides a narrow atomic mana→Vampirism-blood substitution only for eligible Vampire casts of Iron's Blood School, not global resource unification**; **Vampirism Integrations adds no new resource pool** | **ARS↔IRON'S GENERIC UNIFICATION PROVEN; NARROW VAMPIRE SPELLS CAST TRANSACTION PROVEN; EIDOLON/VAMPIRISM/BLOODLINES/AGEING/WEREWOLVES STATES EXPLICITLY DISTINCT; OTHER RESOURCE TYPES MUST NOT BE COLLAPSED** | BLOCKED |
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

A large Black Arcana blood reservoir therefore may reuse actual `vampirism:blood`, but **tank capacity must not be silently mapped to player max blood**, and the same mB cannot be settled simultaneously as player blood and magical fuel. Likewise Eidolon Soul state, Gravebound Souls/Phylactery storage, Goety Soul Energy and Malum spirits must not become a generic shared soul reservoir without an explicit conversion contract.

### Eidolon 0.5.0.2 resource and ritual boundaries

The source-pinned Eidolon audit proves multiple distinct native state channels: mana, Light/Dark deity reputation, Soul capability, research/knowledge, chants and rituals. Black Arcana must not collapse them into one occult resource.

Important consequences:

- `StaticSpell` validation does not centrally guarantee settlement; concrete spell paths differ, so Black Arcana must not externally “fix” Smite, Sunder/Reinforce, Create Water container branch or Undead Lure by charging a guessed cost;
- Enthrall's actual default cost is dynamic (`100 × target health ratio`), not the declared base 50;
- Dark/Holy Touch conversion must defer to the provider RecipeManager and recipe override/fallback semantics;
- 24 official ritual recipes are built from 10 generic prototypes plus dynamic summon/item/location ritual classes; hardcoded prototype count is not the recipe count;
- 11 summon rituals use provider spawn semantics but do not themselves prove player ownership/taming;
- Absorption serializes/removes eligible entities into Summoning Staff charges and must not automatically produce ordinary kill/progression credit;
- Daylight/Moonlight mutate world time provider-side and require deduplication against any external time integration;
- command-chant recipe support is a privileged datapack extension surface; Black Arcana must never synthesize/re-execute arbitrary provider command lists or infer them safe;
- `undead_lure` is registered but its inspected 0.5.0.2 `cast()` is empty; keep it runtime-unproven rather than advertising a working lure.

### Vampirism-native actions, Bloodlines, Vampiric Ageing and blood

The 1.10.13 base provider audit proves that native Vampire/Hunter/Lord actions are not Iron's spells and have their own action handler, cooldown/duration, skill gates and event lifecycle. The blood economy is also food-like: vanilla exhaustion is routed into Vampirism exhaustion, saturation is consumed before blood, and natural blood-based regeneration is provider-owned.

Bloodlines 3.0.9 is source-pinned as a separate structural layer over this base provider: five Bloodlines, 101 skills, 29 actions, 22 tasks, Bloodline perk points and Gravebound Souls/Phylactery are cataloged. Its actions still use the Vampirism ActionHandler and its Vampire-blood mechanics still settle through Vampirism blood APIs/events.

Vampiric Ageing 1.4.21 is source-pinned as another provider-owned layer over the TeamLapen faction/action/skill stack: the installed combination exposes 3 Age Types, 8 Age Methods, 9 Actions and 10 Skills plus a synchronized `AgeingManager`. Hunter Tainted state and cumulative Tainted Age are provider-derived; Blood Tap settles through the native Vampirism bite/`drinkBlood` pipeline; Werewolf Improved Senses remains conditional on the Werewolves provider. Static mismatches affecting exact timings/multipliers and movement lifecycle are documented and remain runtime-QA blocked.

Consequences:

- generic `LivingHealEvent` is insufficient to classify Vampirism natural regeneration or Noble/Gravebound/Ageing healing surfaces as generic lifesteal;
- Bat must not receive an inferred immediate blood cost because its native path adds exhaustion;
- Half Invulnerable must not be pre-charged because its blood settlement occurs only on a qualifying blocked hit;
- `collect_blood` already provides servant-driven automated Blood Bottle production;
- Bloodknight action costs/upkeep must not be charged twice by Black Arcana;
- Gravebound Souls, Bloodline perk points and Vampirism blood are distinct resource domains;
- Gravebound Devour action activation alone is not sufficient proof that a Soul was acquired;
- Mist Form must retain its lethal-hit/Soul/cooldown/logout lifecycle rather than being flattened into generic invulnerability;
- Vampiric Ageing Age Rank, current Age Method, rank progress and Hunter Tainted state must not be mirrored as Black Arcana scoreboards/tags;
- Vampiric Ageing Blood Tap must not receive a second blood-on-hit payout because the provider already settles bite blood and fires the provider drink event;
- Hunter Teleport and Limited Bat Mode must retain provider Action/movement/flight lifecycle and require dedicated-server QA before integration claims;
- Wise Eye exact duration and Wise Eye/Improved Senses/Step Assist cooldown units remain fail-closed for exact-timing contracts until runtime QA;
- Werewolf Improved Senses must preserve its Age + optional Werewolves `SENSE` compound gate;
- **Vampire Spells Addon 0.0.9 is source-pinned as an Iron's Blood/Holy bridge only; it does not convert native Vampirism/Bloodlines/Vampiric Ageing Actions into spells or apply Iron's mana/cooldown semantics to them**.

### Werewolves 2.0.3.3 provider-native lifecycle

Werewolves is a Vampirism-hosted supernatural faction provider, not a mana/spell engine. The source-pinned 2.0.3.3 audit proves Human/Beast/Survivalist player form actions, provider bite/infection/cure, Stone Altar normal leveling, Vampirism-backed Lord progression/minions/refinements, Silver/Wolfsbane/Bleeding and generated skill trees.

Consequences:

- do not mirror Werewolf faction level, form state, transformation time, bite cooldown, Silver/Wolfsbane state or provider skill wallet in Black Arcana;
- `beast4l` is an Alpha-Werewolf entity form, not a fourth player transformation action;
- `resistance` and `sixth_sense` are registered but have no generated-tree path in the audited source; `no_leap_cooldown` has a consumer but no normal acquisition/RefinementSet path was found;
- exact Howling aura radius/attack-speed tuning, Sense radius/cooldown, Health Reg tuning, armor-toughness config and short Health After Kill regeneration remain runtime-QA blocked because source/config paths disagree;
- provider bite settlement, Stun/Bleeding and Lupus Sanguinem infection must happen exactly once; a Black Arcana observer may consume causal outcomes but must not replay the bite transaction;
- Bleeding can interact with Vampirism blood and is not a generic untyped DoT;
- Epic Fight form/render/animation compatibility remains an explicit client/runtime QA gate, not a source-level compatibility claim.

### Vampirism Integrations 1.10.2 eligibility is not runtime activation

The exact source pin proves that Cold Sweat 2.4.2 satisfies the declared version range and that the generated compat option is enabled by default. That is **eligibility evidence only**. `ModCompatLoader` also depends on the user's generated config and successful setup; `/vampirism-integrations loaded` is the direct runtime confirmation gate.

Jade 15.10.6 is target-present and its plugin is independently discoverable through `@WailaPlugin`, but exact registration/rendering is likewise not inferred as PASS without runtime QA.

Consequences:

- Cold Sweat remains the authority for body/world temperature and consequences; Black Arcana must not install a second Vampire thermal model;
- consumers that require the Vampirism↔Cold Sweat compat specifically fail closed until runtime activation is proven;
- Jade remains informational/presentational and never authorizes blood/faction/altar mutation;
- MineColonies presence does not create a Vampirism Integrations bridge: no current Java compat/central-loader registration was found at the exact 1.10.2 source pin;
- supported-but-inactive conditional blood/conversion data maps remain dormant while their external targets are absent.

### Cross-engine casting and mana

Ars 'n' Spells **3.3.0 is the installed bridge** and current official release material continues to cover generic Ars Nouveau ↔ Iron's mana/progression interoperability, inscription/transcription and casting Ars spells from Iron's spellbooks/native wheel. The 3.3.0 release also reports reworked resource payment, long-cast handling and protection against stale/repeated cross-cast requests. A Black Arcana feature that only repeats that bridge is not a gap. Any integration must preserve one causal cast and one canonical provider settlement rather than process the same action once per host engine.

Vampirism's Blood resource remains an independent provider resource. **Vampire Spells Addon 0.0.9 defines one specific exception:** for an eligible Vampire cast of an Iron's Blood School spell, the addon can atomically replace the current mana payment with a Vampirism blood payment. Ray of Siphoning is explicitly excluded, and the bridge does not unify the pools globally. Bloodlines does not broaden this exception: its own perk wallet and Gravebound Souls remain separate. Vampiric Ageing likewise adds Age/progress/Tainted state without making those values convertible into mana, blood or souls. Werewolves adds faction/form/bite/progression state, not a new interchangeable mana resource. Eidolon mana/Soul/reputation and Vampirism Integrations compatibility state remain independent. Black Arcana must not generalize any narrow bridge into a universal mana↔blood↔soul↔age converter or process the same cast once in each resource engine.

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