# Capability Coverage Matrix — Apprentice's Codex 0.9.7.1 delta

Date: `2026-09-07`

This delta supplements the global capability matrix with the exact installed/source-pinned Apprentice's Codex checkpoint. It does not override unrelated provider rows.

Source authority for this delta: installed `apprentice_codex-0.9.7.1+mc1.21.1.jar` plus `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

| Capability family | Apprentice's Codex evidence | Deduplication consequence | Phase 3 posture |
|---|---|---|---|
| Iron's-native spellcasting | 83 registered spells across the 9 canonical Iron's schools; provider uses Iron's mana, schools, cooldown/cast lifecycle and spell power | A provider cast is settled once by Iron's/Apprentice. Black Arcana must not charge second mana, replay damage/healing/world effects or manufacture duplicate cooldown/recast state | `PROVIDER NATIVE / OBSERVE ONLY` |
| Remote vision / scrying | `Remote Eye` creates provider-owned remote-view state; `Otherworld Lens` exposes another remote/alternate viewing surface | Generic remote sight is already occupied. Borrowed Sight/Black Arcana divination must prove materially different contract or integrate rather than clone | `DEDUP REQUIRED` |
| Detection / divination | `Sense Evil`, `Deep Sensor`, `Treasure Divination`, `Search Beacon`, `Terra Resonance` and related provider utilities cover entity, vibration, treasure/structure and material-location workflows | Do not add generic detect-evil, through-wall sensor, treasure locator, structure finder or gem detector under new VFX. A Black Arcana divination spell needs distinct information contract/cost/risk | `BLOCKED / DELTA REQUIRED` |
| Persistent pet/summon storage | `Tamer's Pocket` stores multiple owned pets and safely redeploys them; `Companion Trunk` toggles provider companion state | These are Binding-adjacent but remain provider pet/companion lifecycles. Black Arcana Binding may exist only as typed metaphysical/persistent contracts materially distinct from generic pet storage/recall | `DEDUP REQUIRED` |
| Autonomous constructs / summoned weapons | Archer Multiple, Servant Gaze, Auto Turret and many summoned firearm/blade spells create autonomous or retained provider entities | Persistent/retained attack entities remain children of their originating provider cast. No Mastery/proc per autonomous tick/projectile; no conversion into Black Arcana summon ownership | `PROVIDER OWNERSHIP` |
| Temporary bound equipment | Bound Sword, Bound Bow, Edge Dancer and provider casting gear create timed/equipment-like sessions with recast/deactivation behavior | Activation is one provider spell lifecycle; later melee/projectile actions must be causally separated from the cast and deduplicated against ordinary combat progression | `OBSERVE / NO DOUBLE CREDIT` |
| Barriers / guard / defensive magic | Force Field, Mystic Shield, Phalanx/guard surfaces, protection items and Mana Shield-related content occupy generic magical defense | Black Arcana Order cannot be another generic barrier/guard package. Order must preserve imposed-law, seal, constraint or deterministic-rule identity | `BLOCKED / ORDER DELTA REQUIRED` |
| High-energy barrages / weapons | Commence Fire, Quick Arms, Breaching Enemy, Bullet Stream, Dual Acrobat, Tiro Volley, Feather Rush, Silent Assassin, Lethal Assault and others cover firearm/barrage/high-output combat | Volatile visuals or rapid projectiles do not make a spell Black Arcana Chaos. Chaos requires its own instability/risk/cost semantics rather than reskinned provider firepower | `BLOCKED / CHAOS DELTA REQUIRED` |
| Mobility / evasion / flight | Assist Wings, Mantis Leap, Mirage Avoidance, Long Stride, Spectral Wing, Combustion Jet and broom interactions cover multi-jump, dash/evasion, movement buffs, wings/flight-adjacent and vehicle mobility | Do not add generic dash/double-jump/wing/flight spells unless Black Arcana's version has a distinct forbidden-magic contract and does not duplicate provider state | `DEDUP REQUIRED` |
| World placement / excavation / construction | Rift Hole, Linear Build, World Flatter, Earth Forge, Frost Rune, Mage Light, Wizardlamp, Healing Bloom, Catch Flame and related spells place/replace/temporarily mutate world blocks | Provider world effects remain provider-owned. Do not invoke Black Arcana `WorldEffectPolicy` as a second settlement layer after an Apprentice cast. Black Arcana-originated destructive effects still require its policy | `PROVIDER SETTLEMENT / BA POLICY FOR BA ONLY` |
| Harvest / processing / utility | Tiny Lumberjack, Harvest Moon, Extract, Thermal Process, Compound Phial, Linear Build and provider infrastructure overlap automated harvesting, processing, potion/flask and construction utility | Black Arcana should not mirror general-purpose automation. Forbidden magic utility needs a domain-specific risk/resource/ritual identity | `OVERLAP SUBSTANTIAL` |
| Healing / mana support | Mana Charge, Mana Mending, Healing Bloom, Graced Rain, provider mana-regeneration foods/effects and support gear cover recovery channels | Never create a second settlement for Iron's mana or provider healing. Black Arcana costs/recovery remain its own transaction only for Black Arcana casts/resources | `RESOURCE BOUNDARY` |
| School power specialization | School Affinity reserves 25 slots: 9 fixed Iron's schools + up to 16 eligible extra schools; temporary effects grant +10% school spell power per effect level using `ADD_MULTIPLIED_TOTAL` | School Affinity is provider state, not RPG Mastery, class affinity, Arcane Resistance or Corruption/Strain state. Do not duplicate its modifier | `PROVIDER ATTRIBUTE EFFECT` |
| Alternate casting equipment | Spellcaster guns, staffs, Focus Staffbow, Swingcast/Freecast/Revolvercast surfaces, shields, gauntlet, catalystbook, flasks and Curios modify or trigger provider casting | Alternative input/equipment surfaces do not create a second cast identity. A future RPG hook must deduplicate equipment-triggered callbacks back to the canonical provider cast | `CAUSAL DEDUP REQUIRED` |
| Loot/drop modification | Precision Jack applies provider-owned Looting bonus and duplicate-drop chance; provider trade/recipe/loot systems also own acquisition economy | Do not stack an equivalent RPG loot bonus by interpreting Precision Jack as ordinary melee looting; provider attack settlement owns the spell-specific drop modifier | `PROVIDER LOOT AUTHORITY` |
| Acquisition / learning | Per-spell crafting/looting flags, Iron's registry semantics, item-only spells, Errand Mage trades, recipes and a bonus-chest guidebook modifier form multiple acquisition paths | No generic assumption that all 83 spells are random scrolls/craftable. Preserve explicit item-only/no-loot flags and provider economy | `SOURCE-SPECIFIC / FAIL-CLOSED` |
| Optional cross-mod compatibility | Exact source packages exist for Ars Nouveau, Create, Sable, Epic Fight, Malum, Lootr, Iron's Jewelry, Jade, JEI, Patchouli, EMF and others; Better Combat/Botania are absent in pack; `sodiumdynamiclights` mod ID absent | A compat package is not a Black Arcana bridge. Activate only when exact provider/mod identity and runtime seam are proven; absent/mismatched surfaces fail closed | `VERSION-ELIGIBLE ≠ QA-PROVEN` |

## Domain consequences for Black Arcana

### Chaos

Apprentice's Codex already occupies broad high-output projectile, firearm, summoned-weapon and explosive/thermal combat fantasy. Black Arcana Chaos therefore needs mechanically explicit instability: unpredictable but bounded transformation of outcomes, self-risk, environmental consequence, transactional danger or other domain law. Pure projectile randomness, colorful barrages or large damage are insufficient.

### Order

Generic barriers, shields and stance defenses are already provider territory. Black Arcana Order should remain about constraints, seals, imposed rules, deterministic enforcement and rule-bound control rather than another shield spell.

### Binding

Provider pet storage/recall and autonomous companions are adjacent to Binding. Black Arcana Binding remains viable when it represents typed, persistent metaphysical contracts with identity/ownership/cost semantics that cannot be reduced to `store pet / summon pet`.

### Familiars & Divination

This is the highest direct collision area. The provider already has remote sight, evil/entity sensing, vibration sensing, treasure/structure finding, gemstone detection and alternate-view surfaces. Stage 07.07 design must consume this matrix before promoting any Black Arcana divination spell to canonical content.

## Current gap decision

Apprentice's Codex removes a large amount of generic combat, mobility, defense, utility and divination design space from Black Arcana. Remaining Black Arcana features should be justified by its own forbidden-magic domains, Arcane Danger, transactional costs, rituals, persistent contracts and world-safety semantics—not by recreating one of the 83 provider spells with different naming.