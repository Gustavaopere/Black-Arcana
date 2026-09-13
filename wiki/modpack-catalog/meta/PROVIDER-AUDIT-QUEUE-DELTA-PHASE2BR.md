# Provider audit queue delta — Phase 2BR

This file records the exact queue/coverage delta proposed by the GTBC's Geomancy Plus 1.1.0-1.21.1 durable evidence tranche. It intentionally does **not** rewrite the shared ledgers in this PR.

## Provider

`gtbcs_geomancy_plus` — GTBC's Geomancy Plus `1.1.0-1.21.1`.

## Evidence state

- physically present on the current 1.21.1 modlist line;
- exact matching publisher release file `1352485 / 7041615` inspected clean-room;
- exact release SHA-1 `67e9652799f35f1fbd09968da6f400d0229f5599`;
- exact release SHA-256 `b645cf8852b3453f2d7ccc10cd4b4f897edcc6f857f912042dc9f4d96c8e8bf7`;
- physical local-JAR byte hash is not preserved in the current repository, so no `hash-matched physical` claim is made;
- structural audit run `34737230548` GREEN;
- focused registry reconciliation run `34737352893` GREEN;
- Geo reachability-gate reconciliation run `34738729721` GREEN, artifact `10312146416`, digest `sha256:2056724a748d103a25fc4069fb0c186ce8bea92a82b78515b03b85959df1596c`.

Because exact publisher-release bytes are inspected but independently matching local physical-JAR bytes are unavailable, the existing canonical semantic evidence state is **`COUNTED_RELEASE_BOUNDED`**.

## Semantic delta candidate

Exact provider registry closes twelve unconditional registrations:

- Geo: 10;
- Holy: 2;
- total: **+12**.

Exact IDs:

`chunker`, `dripstone_bolt`, `eroding_boulder`, `fissure`, `geo_conductor`, `petrivise`, `pillar_of_the_resounding_earth`, `seismic_surf`, `tremor_spike`, `tremor_step`, `solar_beam`, `solar_storm`.

Explicit +0 exclusions:

- `EarthshatterSpell` — concrete class present but not registered;
- `EarthquakeMixin` — non-registry adaptation class;
- `StormSpellMixin` — non-registry adaptation class;
- Geo school type — taxonomy/support;
- generic/later project-page spells not present in exact file `7041615`;
- GTBC SpellLib infrastructure already counted separately as +0.

Proposed semantic state after future shared reconciliation:

`COUNTED_RELEASE_BOUNDED / +12`

Proposed strict minimum:

`1332 -> 1344`.

## Technical component candidate

GTBC's Geomancy Plus has not previously been promoted as a closed technical component. Earlier canonical work left its exact-JAR extraction pending.

Proposed component:

`#66`.

Proposed component closure after future shared reconciliation:

`65/100 -> 66/100`.

This percentage is component coverage only and must never be presented as spell/magic coverage.

## Catalog reachability evidence

Geo:

`mowziesmobs:bluff_rod -> #gtbcs_geomancy_plus:geo_focus -> irons_spellbooks:school_focus`.

The dedicated exact-release reachability audit verifies all ten registered Geo concrete classes are direct Iron's `AbstractSpell` subclasses and that none overrides `allowCrafting`, `isEnabled` or `canBeCraftedBy`. Therefore they inherit the host gates used by the already-canonical Iron's Scroll Forge/focus contract rather than substituting provider-local reachability rules.

Holy:

exact Umvuthi loot identifiers reference both provider Holy spell IDs plus Iron's scroll/randomization identifiers; exact publisher file notes both are obtained by defeating Umvuthi.

This closes catalog-level acquisition/reachability without claiming deployed generic host config or assembled-pack runtime PASS.

## Runtime state

Remain fail-closed:

- full-pack Iron's compatibility;
- deployed generic host configuration;
- Geo school/focus runtime UI;
- Mowzie entity/projectile integration;
- Umvuthi live loot rates/settlement;
- world mutation/protection behavior;
- multiplayer and restart/reload behavior;
- numerical balance/config settlement.

No Black Arcana runtime adapter is promoted by this documentation phase.

## Shared-ledger reconciliation required after durable merge

After this durable provider-evidence PR merges and its exact merge SHA passes canonical post-merge CI, a separate latest-main reconciliation should update only the relevant shared records, including:

- `CATALOG-COVERAGE-CURRENT.md`;
- `CURRENT-MAGIC-PROVIDERS.md`;
- `PROVIDER-AUDIT-QUEUE.md`;
- `SEMANTIC-MAGIC-COVERAGE.md`;
- provider README status from candidate to canonical component accounting.

That reconciliation should promote **1344 semantic minimum / 66 of 100 components** only after its own exact-HEAD and exact merge-SHA gates pass.

Existing conditional/blocking rows remain unchanged:

- Not Enough Glyphs 4.6.1 — 39 config-conditioned candidates;
- Somake Spells 1.0.8-fix — 67 exact registry identities, deployed config/reachability unresolved;
- Gaze 1.1.7.1 — Soulward Shield counted, 26 rites remain config-conditioned;
- Phase 3 remains blocked until the semantic denominator is reconstructible.