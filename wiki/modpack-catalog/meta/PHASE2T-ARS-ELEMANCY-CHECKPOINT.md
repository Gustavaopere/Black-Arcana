# Phase 2T — Ars Elemancy 1.18.3 checkpoint

Status: `SOURCE CATALOG COMPLETE / RUNTIME+CONFIG+CLIENT+FULL-PACK QA PENDING`

Execution branch: `docs/magic-catalog-phase2t-ars-elemancy`
Base main at phase start: `8af81c925a6d6d725e1663de516fc20b393ec207`
Provider source pin: `Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`
Physical JAR: `ars_elemancy-1.21.1-1.18.3.jar`
Physical SHA-1: `f7e01437c86fc74e2abb2ad93554dc20c30b214b`

## Closed source surface

- 105 item registrations;
- 84/84 armor IDs across 21 sets;
- 7/7 foci;
- 7/7 essences;
- 7/7 bangles;
- 6 dual composite schools + Elemancer host-elemental identity;
- 33 ArmorMaterials;
- 3 Ars PerkSlots;
- 0 local glyphs;
- 0 local perks;
- 0 local network payloads;
- recipe/acquisition families classified;
- Curios tags classified;
- focus/armor/bangle behaviors classified;
- config/defaults classified;
- presentation/Starbuncle mapping classified;
- authority/deduplication rules written.

## Corrections to older Phase 2 summary

The provider is still correctly classified as gear/support rather than a glyph provider, but its owned equipment surface is substantially larger than the old high-level README: 105 items and 21 armor sets. The six named dual schools are equipment/compat SpellSchool objects, not evidence of local glyph registries.

Runtime/config/client/full-pack QA remains pending. No Black Arcana runtime Stage is promoted.