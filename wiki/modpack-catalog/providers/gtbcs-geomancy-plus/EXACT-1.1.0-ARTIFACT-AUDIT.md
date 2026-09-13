# GTBC's Geomancy Plus 1.1.0-1.21.1 — exact release artifact audit

## Scope

Phase 2BR inspected the exact published NeoForge 1.21.1 release artifact corresponding to the physical pack's installed GTBC's Geomancy Plus line. The work is clean-room, evidence-only and does not copy or retain upstream implementation, assets, recipe payloads or localization prose.

Publisher release identity:

- CurseForge project `1352485`;
- file `7041615`;
- filename `gtbcs_geomancy_plus-1.1.0-1.21.1.jar`;
- exact release SHA-1 `67e9652799f35f1fbd09968da6f400d0229f5599`;
- exact release SHA-256 `b645cf8852b3453f2d7ccc10cd4b4f897edcc6f857f912042dc9f4d96c8e8bf7`.

The repository does not currently preserve a separate cryptographic hash for the user's local physical GTBC Geomancy Plus JAR. Therefore this audit is an **exact publisher release artifact** audit aligned to the installed mod-id/version line, not a claim of independently proven local-JAR byte equivalence. Under the canonical semantic taxonomy, any later promotion is therefore `COUNTED_RELEASE_BOUNDED`, not `COUNTED_EXACT`.

## Evidence runs

### Structural exact-artifact run

Audit branch HEAD: `c9d9bfb86bb036427192c50139f1c9093f5d508e`

Workflow run: `34737230548` — GREEN.

Text-only artifact:

- artifact ID `10310854594`;
- name `gtbcs-geomancy-plus-1.1.0-exact-artifact-audit`;
- digest `sha256:69d0a4ba925405e6a6f07db79618adea081ca980b73d357c9797001e2f330998`.

Retained evidence is limited to cryptographic hashes, metadata/dependency declarations, class/type/signature identities, aggregate registry/branch/gate facts, localization keys and structured resource identifiers/paths.

### Focused registry reconciliation

Audit branch HEAD: `bf90b58d15a1c5f1379b562291e8a30b62fc2e92`

Workflow run: `34737352893` — GREEN.

Text-only artifact:

- artifact ID `10311950155`;
- name `gtbcs-geomancy-plus-1.1.0-registry-reconciliation`;
- digest `sha256:a948b8ce7d71b43538756cb9a3ef26dc8b3bf02d4e4c4ef04ee16fc00a391dab`.

The focused job hard-fails unless it can reconcile exactly twelve registry fields, twelve `registerSpell(...)` calls, zero registry initializer branch opcodes, twelve field-to-concrete-class mappings and twelve exact root spell IDs while proving `EarthshatterSpell` unregistered.

### Geo reachability gate reconciliation

Audit branch HEAD: `7596802cefa164f0cc61c391b1fae09d12115e7d`

Workflow run: `34738729721` — GREEN.

Text-only artifact:

- artifact ID `10312146416`;
- name `gtbcs-geomancy-plus-1.1.0-reachability-reconciliation`;
- digest `sha256:2056724a748d103a25fc4069fb0c186ce8bea92a82b78515b03b85959df1596c`.

This job hard-checks all ten registered Geo concrete classes. Each is a direct subclass of Iron's `AbstractSpell`, and none declares provider overrides of `allowCrafting`, `isEnabled` or `canBeCraftedBy`. The resulting provider override count for those host gates is zero.

This proves only inheritance of the Iron's host gate contract; it does not promote generic host config or assembled-pack runtime behavior to PASS.

## Artifact metadata

Exact `META-INF/neoforge.mods.toml` evidence records:

- mod id `gtbcs_geomancy_plus`;
- version `1.1.0-1.21.1`;
- display name `GTBC's Geomancy Plus`;
- license `All Rights Reserved`;
- NeoForge `[21.1.0,)`;
- Minecraft `[1.21.1,1.22)`;
- GTBC SpellLib `[1.3.1-1.21.1,)`.

Artifact structural size observed by the audit:

- 325 JAR entries;
- 99 parsed classes.

## Exact spell registry closure

`GGSpells` exposes exactly twelve `Supplier<AbstractSpell>` fields:

1. `FISSURE_SPELL`
2. `TREMOR_SPIKE_SPELL`
3. `TREMOR_STEP_SPELL`
4. `ERODING_BOULDER_SPELL`
5. `CHUNKER_SPELL`
6. `SEISMIC_SURF`
7. `DRIPSTONE_BOLT`
8. `PILLAR_OF_THE_RESOUNDING_EARTH`
9. `GEO_CONDUCTOR_SPELL`
10. `PETRIVISE_SPELL`
11. `SOLAR_STORM_SPELL`
12. `SOLAR_BEAM_SPELL`

The static initializer performs exactly twelve `registerSpell(...)` calls and contains zero branch opcodes. The focused reconciliation establishes the exact mapping:

| Registry field | Concrete class | Spell ID |
|---|---|---|
| `FISSURE_SPELL` | `FissureSpell` | `fissure` |
| `TREMOR_SPIKE_SPELL` | `TremorSpikeSpell` | `tremor_spike` |
| `TREMOR_STEP_SPELL` | `TremorStepSpell` | `tremor_step` |
| `ERODING_BOULDER_SPELL` | `ErodingBoulderSpell` | `eroding_boulder` |
| `CHUNKER_SPELL` | `ChunkerSpell` | `chunker` |
| `SEISMIC_SURF` | `SeismicSurfSpell` | `seismic_surf` |
| `DRIPSTONE_BOLT` | `DripstoneBoltSpell` | `dripstone_bolt` |
| `PILLAR_OF_THE_RESOUNDING_EARTH` | `PillarOfTheResoundingEarthSpell` | `pillar_of_the_resounding_earth` |
| `GEO_CONDUCTOR_SPELL` | `GeoConductorSpell` | `geo_conductor` |
| `PETRIVISE_SPELL` | `PetriviseSpell` | `petrivise` |
| `SOLAR_STORM_SPELL` | `SolarStormSpell` | `solar_storm` |
| `SOLAR_BEAM_SPELL` | `SolarBeamSpell` | `solar_beam` |

The exact localization root spell-key set contains the same twelve IDs:

`chunker`, `dripstone_bolt`, `eroding_boulder`, `fissure`, `geo_conductor`, `petrivise`, `pillar_of_the_resounding_earth`, `seismic_surf`, `solar_beam`, `solar_storm`, `tremor_spike`, `tremor_step`.

This independent key reconciliation is supporting evidence only; the authoritative semantic count comes from the exact registry mapping.

## Non-counted spell-like classes

### `EarthshatterSpell`

The exact JAR contains `EarthshatterSpell`, a concrete `AbstractSpell` subclass. It is **not** among the twelve `GGSpells` fields, is not reached by a thirteenth `registerSpell(...)` call and is explicitly reconciled as `earthshatter_registered=false`.

Disposition: `UNREGISTERED / +0`.

### `EarthquakeMixin` and `StormSpellMixin`

The structural audit observes abstract `AbstractSpell` subclasses named `EarthquakeMixin` and `StormSpellMixin`. They are not `GGSpells` fields and do not create provider registrations in the exact registry.

Disposition under the semantic metric: `NON-REGISTRY ADAPTATION CLASS / +0`.

Phase 2BR does not infer their runtime transformation mechanism or behavior from class names alone.

## Registry config and optional-gate closure

Focused registry analysis records:

- registry config references: `0`;
- registry mod-gate references: `0`;
- static initializer branch opcodes: `0`.

Therefore the twelve exact provider spell registrations are unconditional at the provider registry path inspected here. Generic host/runtime configuration remains a distinct assembled-pack QA surface.

## School/focus and Geo reachability evidence

The exact JAR contains one Geo `SchoolType` construction path with zero branch opcodes in the school static initializer.

Packaged focus identifiers:

- `data/gtbcs_geomancy_plus/tags/item/geo_focus.json` -> `mowziesmobs:bluff_rod`;
- `data/irons_spellbooks/tags/item/school_focus.json` -> `#gtbcs_geomancy_plus:geo_focus`.

The dedicated reachability audit separately proves that all ten exact registered Geo classes inherit, rather than override, Iron's `allowCrafting`, `isEnabled` and `canBeCraftedBy` host gates. Combined with the exact focus path and the already-canonical Iron's 3.16.3 Scroll Forge/focus contract used by this catalog, this closes catalog-level Geo reachability under the same evidence standard used for other Iron's addons.

This does not prove the deployed generic host config, UI or networking state; those remain assembled-pack/runtime QA.

## Holy-spell acquisition evidence

The exact release packages Umvuthi loot data whose retained identifiers include:

- `gtbcs_geomancy_plus:solar_beam`;
- `gtbcs_geomancy_plus:solar_storm`;
- `irons_spellbooks:randomize_spell`;
- `irons_spellbooks:scroll`.

The publisher's exact 1.1.0 file changelog also states that Solar Beam and Solar Storm are obtained by defeating Umvuthi.

This closes catalog-level player acquisition for those two spell identities without retaining loot weights or payload internals. Exact live drop rates and full-pack behavior remain fail-closed/runtime QA.

## Other structured surfaces observed

The exact artifact also contains:

- provider loot-modifier paths for Bluff and Umvuthi;
- four provider recipe resources for Codex of Shattered Horizons, Geo Rune, Geo Upgrade Orb and The Stonecaller;
- provider entities/projectiles and effects used by the spell implementation;
- Geo-specific attributes and school content.

These are not counted as additional spell identities under the current semantic metric.

## Publisher-page drift boundary

The current generic project page advertises additional spell names beyond the twelve identities present in the exact NeoForge 1.21.1 release artifact. The project also has a newer 1.20.1 2.0.0 release line. Phase 2BR does not project later/project-wide content backward into the installed 1.21.1 file.

For current-pack semantic inventory, exact file `7041615` registry evidence outranks generic project-page scale/content descriptions.

## Clean-room boundary

The audit did not retain or reproduce:

- method bodies;
- bytecode disassembly;
- recipe payloads/ingredients;
- localization prose;
- textures/models/animations/sounds;
- upstream source reconstruction;
- binary redistribution.

No upstream implementation is copied into Black Arcana. The audit exists only to identify factual current-release registry, dependency, reachability and authority boundaries.

## Result

Phase 2BR exact publisher-release evidence closes **12 provider-owned current spell registrations** at `COUNTED_RELEASE_BOUNDED` evidence strength:

- **10 Geo**;
- **2 Holy**;
- `EarthshatterSpell` excluded as unregistered;
- non-registry adaptation classes excluded;
- later/project-wide page content excluded;
- Geo host-gate inheritance verified across all ten registered Geo classes;
- Holy acquisition supported by exact Umvuthi loot identifiers and exact release changelog.

Candidate semantic delta: **+12 `COUNTED_RELEASE_BOUNDED`**.

Candidate technical component: **#66**.

Canonical shared values remain **1332 semantic minimum / 65 of 100 components** until a separate shared-ledger reconciliation merges and passes exact merge-SHA CI.