# Provider Audit Queue Delta — Phase 2AC

Provider: `arssophisticatedcompat` / Ars Sophisticated Compatibility 0.3.0

## Closed in catalog

- physical filename/mod id/runtime version/SHA-1;
- current physical Ars Nouveau, Sophisticated Core and Sophisticated Storage host versions;
- distinction between installed `arssophisticatedcompat-0.3.0.jar` and accessible official `arssophisticatedstoragecompat-0.3.0.jar`;
- official 0.3.0 functional-family surface: Source Storage, Storage Source Link, Potion Jar, Enchanter's Upgrade;
- provider authority split and deduplication constraints;
- clean-room provenance boundary;
- Notion dependency drift: Sophisticated Core 1.5.0 -> physical 1.5.1.

## Remains open / fail-closed

- exact public source or exact binary inspection for installed SHA-1 `7cc6c1e1d92d109230f68b6a63dc4bfb13c245a6`;
- exact registry IDs/recipes;
- dependency version ranges;
- config schema/defaults;
- capacity/conversion/repair formulas;
- potion representation and cadence;
- networking/mixins/event hooks;
- physical-artifact license;
- real-modpack runtime validation on Ars Nouveau 5.13.1 + Sophisticated Core 1.5.1 + Sophisticated Storage 1.5.91.

## Queue disposition

Phase 2 catalog may advance after this documentation lands because all unobserved implementation-specific claims are explicitly fail-closed. No Black Arcana adapter should be implemented from this entry until the exact physical binary/API gate is closed.

The next provider must be selected from the latest 2026-09-08 physical modlist rather than the older 612-entry guide snapshot.