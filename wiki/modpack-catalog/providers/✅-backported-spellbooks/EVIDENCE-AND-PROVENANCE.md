# Backported Spellbooks — evidence and provenance

## Physical authority

Current physical inventory is the authority for installed identity:

- JAR: `backportedspellbooks-0.1.2.jar`;
- mod id: `backportedspellbooks`;
- display name: `Backported Spellbooks`;
- embedded/runtime metadata version: `0.1.0`;
- SHA-1: `747847c1f38c73250ebac05ea06b41a381187850`;
- Minecraft 1.21.1 / NeoForge 21.1.248.

The filename and embedded version are intentionally preserved as different facts.

## Exact publisher release

CurseForge:

- project `1543731`;
- file `8158731`;
- filename `backportedspellbooks-0.1.2.jar`;
- NeoForge / Minecraft 1.21.1;
- beta file;
- release date 2026-05-28;
- project environment: Server;
- project license label: MIT.

Exact file changelog adds Miasmic Staff, Quicksilver Spellbook, Slime Boots, four spells (`Slime Aspect`, `Sulfur Clouds`, `Sulfur Bomb`, `Sulfur Release`) and two Sulfur Caves ore families (`Corroded Fossils`, `Quicksilver`).

The project description still advertises a much smaller early feature set, so it is treated as stale editorial text rather than the complete 0.1.2 inventory.

## Official source timeline

Official repository: `RedReaper28/BackportedSpellbooks-1.21.1`.

Relevant revisions:

- `4149c37c77dda46ab0a8697c438101e07ff14d19` — 2026-05-18 source point, aligned by date with publisher file 0.1.1;
- `07cb65efca0c264762a21c2d6bce0f83e3947226` — terminal 2026-05-28 source point, aligned by date with publisher file 0.1.2.

The repository has no exact `0.1.2` tag/release pin. The terminal source still declares `mod_version=0.1.0` in `gradle.properties`. That agrees with the physical embedded metadata and disagrees with the release filename. The catalog does not rewrite this mismatch.

## Spell-delta alignment

At the May 18 source point, the provider spell registry contains two registrations: Pale Thorn and Resin Spray.

At the May 28 source head it contains six registrations. The additional four are:

- Slime Aspect;
- Sulfur Bomb;
- Sulfur Clouds;
- Sulfur Release.

Those four names are the exact spell delta named by the 0.1.2 publisher changelog. This supports semantic use of the May 28 source as the strongest current source-line evidence while still keeping source↔physical-JAR equivalence unproven.

## Source metadata

Release-day source `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `neo_version=21.1.216`;
- `mod_id=backportedspellbooks`;
- `mod_name=Backported Spellbooks`;
- `mod_version=0.1.0`;
- `mod_license=All Rights Reserved`;
- Iron's development baseline `1.21.1-3.15.4`.

Exact `neoforge.mods.toml` formally requires only:

- NeoForge `[21.1.216,)`;
- Minecraft `[1.21.1]`.

It does not formally declare Iron's Spells, Vanilla Backport or Ace's Spell Utils despite direct source imports/build dependencies. Those relationships are recorded as undeclared source-level expectations, not fabricated metadata declarations.

## Physical host stack relevant to the source

The current modlist physically contains:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Vanilla Backport `1.1.7.10`;
- Ace's Spell Utils `1.2.7.2-1.21.1`;
- Curios `9.5.1+1.21.1`;
- NeoForge `21.1.248`.

Presence is not the same as proven API compatibility. Source baseline drift remains runtime QA.

## Registry/source inventory method

The audit uses explicit provider registration code and data/resource paths. It does not infer registry identities from filenames alone.

Closed at the release-day source ceiling:

- 6 Iron's spell registrations;
- 1 SchoolType;
- 19 item registry objects including 4 block items;
- 4 blocks;
- 5 entity types;
- 4 mob effects;
- 2 particles;
- 1 fluid + 1 fluid type;
- 19 recipe JSONs;
- 2 configured ore features + 2 placed features + 2 NeoForge biome modifiers;
- no mixin config;
- no provider custom payload registration observed;
- no provider-owned SavedData/attachment/data-component player/world persistence subsystem observed.

Normal per-entity serialization inherited or implemented by entity classes is not reclassified as a provider-owned player/world persistence authority.

## Worldgen evidence

Both exact source biome modifiers use `neoforge:add_features`, target `minecraft:sulfur_caves`, and add their placed feature at `underground_ores`:

- `backportedspellbooks:corroded_fossil_ore_placed`;
- `backportedspellbooks:quicksilver_ore_placed`.

This independently matches the publisher's 0.1.2 Sulfur Caves statement.

## Binary evidence boundary

The exact public CurseForge file could not be directly obtained through the available read path for byte/hash comparison during this audit. Therefore:

- physical SHA-1 is retained as physical-inventory evidence;
- publisher file ID/name/date is retained as publisher evidence;
- release-day source head is retained as source-line evidence;
- no byte-for-byte source/JAR identity is asserted.

## License discrepancy / clean-room

Evidence conflicts:

- CurseForge project label: MIT;
- release-day source `gradle.properties`: `All Rights Reserved`.

No license grant is inferred from the more permissive surface. Read-only source/data inspection is used only for factual cataloging, interoperability boundaries and deduplication. Black Arcana does not copy provider code, assets, text, models, textures, sounds or implementation patterns.

Any future derivation/reuse remains `REVIEW_REQUIRED` until licensing is independently reconciled.