# GTBC's Geomancy Plus — 1.1.0-1.21.1

Status: `EXACT RELEASE ARTIFACT CLOSED / COUNTED-EXACT-RELEASE CANDIDATE +12 / COMPONENT #66 CANDIDATE / CURRENT-HOST RUNTIME QA FAIL-CLOSED`

## Current physical/release identity

The current physical modlist line identifies GTBC's Geomancy Plus as present on Minecraft 1.21.1 with runtime/version line `1.1.0-1.21.1` and mod id `gtbcs_geomancy_plus`.

The matching publisher release inspected for Phase 2BR is:

- CurseForge project: `1352485`;
- CurseForge file: `7041615`;
- published filename: `gtbcs_geomancy_plus-1.1.0-1.21.1.jar`;
- loader/game line: NeoForge / Minecraft 1.21.1;
- exact release artifact SHA-1: `67e9652799f35f1fbd09968da6f400d0229f5599`;
- exact release artifact SHA-256: `b645cf8852b3453f2d7ccc10cd4b4f897edcc6f857f912042dc9f4d96c8e8bf7`.

Important evidence boundary: the current repository does not preserve a cryptographic hash of the user's local physical GTBC Geomancy Plus JAR. The exact publisher release therefore aligns to the installed filename/version/mod-id authority, but Phase 2BR does **not** claim byte-for-byte hash equivalence to a separately hashed local physical artifact.

Exact artifact metadata declares:

- `modId="gtbcs_geomancy_plus"`;
- `version="1.1.0-1.21.1"`;
- license `All Rights Reserved`;
- NeoForge `[21.1.0,)`;
- Minecraft `[1.21.1,1.22)`;
- required GTBC SpellLib `[1.3.1-1.21.1,)`.

The physical pack's previously reconciled GTBC SpellLib line is 2.2.0, so the declared lower bound is satisfied. That range observation is not a current-host runtime PASS.

## Exact semantic spell inventory

The exact release artifact contains one provider spell registry class, `GGSpells`, with exactly **12** `Supplier<AbstractSpell>` fields. Its static initializer performs exactly **12** `registerSpell(...)` calls with **zero branch opcodes**. A focused clean-room reconciliation maps all twelve fields to twelve concrete classes and twelve root spell IDs.

| School/family | Registry ID | Exact concrete class |
|---|---|---|
| Geo | `chunker` | `ChunkerSpell` |
| Geo | `dripstone_bolt` | `DripstoneBoltSpell` |
| Geo | `eroding_boulder` | `ErodingBoulderSpell` |
| Geo | `fissure` | `FissureSpell` |
| Geo | `geo_conductor` | `GeoConductorSpell` |
| Geo | `petrivise` | `PetriviseSpell` |
| Geo | `pillar_of_the_resounding_earth` | `PillarOfTheResoundingEarthSpell` |
| Geo | `seismic_surf` | `SeismicSurfSpell` |
| Geo | `tremor_spike` | `TremorSpikeSpell` |
| Geo | `tremor_step` | `TremorStepSpell` |
| Holy | `solar_beam` | `SolarBeamSpell` |
| Holy | `solar_storm` | `SolarStormSpell` |

The exact localization root-key set independently contains the same twelve spell IDs and no additional root spell ID for the unregistered prototype described below.

Phase 2BR therefore closes a candidate semantic delta of **+12 provider-owned spell identities** under the current metric: ten Geo spells and two Holy spells.

## Explicit exclusions and deduplication

### `EarthshatterSpell`

`EarthshatterSpell` exists as a concrete `AbstractSpell` subclass in the exact JAR, but the exact `GGSpells` registry contains no supplier field for it, the static initializer does not register it, and the focused audit records `earthshatter_registered=false`. It contributes **+0** to the current semantic denominator.

### `EarthquakeMixin` and `StormSpellMixin`

Two abstract classes named `EarthquakeMixin` and `StormSpellMixin` extend Iron's `AbstractSpell`, but neither is a `GGSpells` field or a provider spell registration. They therefore contribute **+0 provider spell identities**. Phase 2BR does not infer their runtime transformation mechanism or claim they are player-acquirable spells.

Any provider-side school reassignment or behavior adaptation of an already Iron's-owned spell remains a modification of the existing Iron's identity rather than a new provider-owned spell identity unless a separate registration is proven.

### Generic project-page drift

The publisher's generic project page now describes additional spell names beyond the exact 1.1.0-1.21.1 registry, reflecting later/project-wide content. Those names are not backfilled into this current 1.21.1 inventory. The exact file `7041615` registry is authoritative for the twelve identities above.

## Catalog reachability evidence

The exact artifact packages the following focus path:

- `data/gtbcs_geomancy_plus/tags/item/geo_focus.json` -> `mowziesmobs:bluff_rod`;
- `data/irons_spellbooks/tags/item/school_focus.json` -> `#gtbcs_geomancy_plus:geo_focus`.

This establishes a provider-native Geo school-focus route into the Iron's host focus tag. Under the already-cataloged Iron's Scroll Forge/focus contract, this is sufficient to close catalog-level reachability for the registered Geo spell family. Exact assembled-pack acquisition behavior remains runtime QA.

For the two Holy spells, exact packaged Umvuthi loot identifiers reference:

- `gtbcs_geomancy_plus:solar_beam`;
- `gtbcs_geomancy_plus:solar_storm`;
- `irons_spellbooks:randomize_spell`;
- `irons_spellbooks:scroll`.

The exact publisher 1.1.0 file changelog independently states that Solar Beam and Solar Storm are obtained by defeating Umvuthi. Exact loot weights, randomization behavior and live assembled-pack drops remain runtime QA rather than catalog facts.

## Registry gates/config

Focused exact-artifact analysis finds:

- `12` provider spell supplier fields;
- `12` `registerSpell(...)` calls;
- `0` branch opcodes in the spell registry static initializer;
- `0` registry config references;
- `0` registry mod-gate references.

No deployed per-spell provider enable/disable gate is evidenced in the exact registry path. This is sufficient for semantic registry closure, not for a claim that every host-side runtime config or integration path has been exercised in the assembled modpack.

## Authority boundary

- Iron's Spells 'n Spellbooks remains authority for its casting pipeline, spell host contracts, mana/cooldown and scroll/focus infrastructure.
- GTBC's Geomancy Plus owns the twelve provider spell identities and its Geo school/content.
- Mowzie's Mobs remains authority for its base entities/items and related native gameplay state; GTBC integration with Bluff/Umvuthi surfaces does not transfer that authority to Black Arcana.
- GTBC SpellLib remains shared library infrastructure and is not counted again as a spell provider here.
- Black Arcana retains its own canonical casting, hazards, world safety, Corruption, Strain and Arcane Danger authority. No duplicate resource pool, spell registration or provider effect pipeline is introduced by this catalog closure.

## Runtime state — fail-closed

Phase 2BR does not promote current-host runtime PASS. Still requiring assembled-pack/runtime validation where integration is later consumed:

- exact Iron's 3.16.3 host compatibility for the twelve casts;
- Geo school registration/display/focus behavior in the full pack;
- Mowzie-linked projectile/entity/item behavior and ownership/friendly-fire boundaries;
- Umvuthi loot settlement and dedicated-server behavior;
- world mutation/protection behavior of terrain-oriented spells;
- multiplayer, reload/restart and exactly-once side-effect behavior;
- numerical balance and provider-specific config settlement.

## Component accounting

This durable provider record proposes GTBC's Geomancy Plus as **component #66** with semantic delta **+12**. It does not by itself alter the canonical shared ledgers.

Until a separate latest-main shared-ledger reconciliation is reviewed, passes exact-HEAD CI, merges, and passes exact merge-SHA post-merge CI:

- canonical semantic minimum remains **1332**;
- canonical technical component closure remains **65/100**;
- this provider remains `COMPONENT #66 CANDIDATE` / `+12 CANDIDATE`.

See [`EXACT-1.1.0-ARTIFACT-AUDIT.md`](./EXACT-1.1.0-ARTIFACT-AUDIT.md) and the Phase 2BR checkpoint for evidence details.