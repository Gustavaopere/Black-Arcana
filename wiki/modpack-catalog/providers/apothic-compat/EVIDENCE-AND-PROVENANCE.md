# Apothic Compat 2.0.2 — evidence and provenance

## Physical evidence

Current physical modlist anchor:

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Installed provider row:

- `apothic_compat-2.0.2.jar`;
- mod id `apothic_compat`;
- display `Apothic Compat`;
- version `2.0.2`;
- SHA-1 `868506b8367be2c155acde0ef186b5a3e6ba8db9`.

Relevant physical host stack:

- Apotheosis `8.8.0`;
- Placebo `9.9.2`;
- Apothic Attributes `2.10.1`.

## Publisher evidence

Exact CurseForge file:

- project `1516278`;
- file `8219980`;
- filename `apothic_compat-2.0.2.jar`;
- release `2.0.2`;
- NeoForge 1.21.1;
- uploaded 2026-06-09;
- Client & Server publisher environment;
- MIT publisher license.

The publisher release describes the first NeoForge 1.21.1/Apotheosis 8.x build, identifies the data-map model and enumerates the item overrides that the exact source confirms.

## Exact official source evidence

Repository:

`Nightwielder23/apothic-category-compat`

Exact source pin:

`cebf69a37f8c6573fc0c0295e627f4636e7bd026`

Commit message:

`ported to neoforge 1.21.1 with apotheosis 8.x data map architecture`

The exact pin's `gradle.properties` declares `mod_version=2.0.2`, so this is an exact source-version pin rather than a different-version baseline.

Exact tree facts:

- 4 Java classes;
- 0 mixin manifests/classes;
- one `loot_category_overrides.json` data map;
- exactly 13 item mappings, all to `apotheosis:bow`;
- one semantic config key, `affix_blacklist`;
- one NeoForge mod metadata file;
- root `LICENSE` is MIT.

## License / clean-room

The exact root `LICENSE` and exact NeoForge metadata both declare MIT. The publisher surfaces also label MIT.

This audit used source/data read-only for factual cataloging, authority classification and interoperability risk analysis. No provider code or assets were copied or adapted into Black Arcana.

Even with compatible licensing, source similarity is not needed for Black Arcana: BA-specific integration must use independently designed boundaries and provider-native APIs/data surfaces where available.

## Evidence ceiling

Closed from exact evidence:

- physical identity/version/hash;
- exact publisher release;
- exact source version/revision;
- declared dependencies;
- 4-class source surface;
- 0-mixin result;
- exact 13-value data map;
- command/event/config lifecycle;
- private-reflection blacklist implementation and its caught failure behavior;
- static empty-blacklist reload asymmetry.

Still fail-closed:

- byte-for-byte source/JAR reproducibility;
- exact runtime behavior against physical Apotheosis 8.8.0's private `AffixRegistry.byType` field;
- full-modpack interaction with all 13 target item providers;
- whether every target item is present/unchanged in the current pack at runtime unless separately verified;
- live `/ac reload` empty-blacklist regression behavior until executed on the physical stack.

## Component-order note

This audit is being prepared on Phase 2AQ because a concurrently created Phase 2AP branch already reserves `create_enchantment_industry_plus` 1.1.1. Phase 2AP's coverage result is not yet canonical, so this branch must not pre-allocate a final component ordinal or canonical numerator before reconciling that concurrent work.
