# Not Enough Glyphs 4.6.1 — Evidence and Provenance Ledger

## Physical installed artifact

Current physical modlist supplied 2026-09-08:

- filename: `not_enough_glyphs-1.21.1-4.6.1.jar`;
- mod id: `not_enough_glyphs`;
- name: `Not Enough Glyphs`;
- runtime version: `4.6.1`;
- SHA-1: `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4`;
- modlist hash field: `2985019018`;
- embedded Sauce JAR: `sauce-1.21.1-0.0.42.89.jar`;
- current pack NeoForge: `21.1.248`.

Installed optional-provider facts used for conditional registration:

- Ars Elemental `0.7.10.1`: present;
- Ars Controle `1.6.15`: present;
- Too Many Glyphs: absent;
- Ars Omega: absent;
- Ars Trinkets: absent;
- Ars Scalaes: absent.

## Exact public source-semver pin

Repository: `Alexthw46/NotEnoughGlyphs`

- branch: `1.21`;
- audited commit: `2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b`;
- `gradle.properties` at that commit declares `mod_version=4.6.1`;
- source target Minecraft: `1.21.1`;
- source target NeoForge: `21.1.220`;
- source Ars Nouveau dependency: `5.12.0.1368`;
- source Sauce dependency: `0.0.42.89`;
- source Ars Elemental dependency: `0.7.9.4.170`;
- source metadata license string: `LGPL`.

The installed pack is newer than some source build-time hosts (NeoForge 21.1.248, Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1). This does not prove incompatibility, but full runtime host acceptance must remain QA rather than inferred PASS.

## Source surfaces audited

Phase 2AF inspected, at the exact source pin:

- conditional glyph/perk registration;
- registry objects;
- glyph recipe generation;
- Spell Binder item/caster/container;
- Binder C2S networking;
- Binder resolver/perks;
- NEG event handlers;
- Trail/Missile projectile behavior;
- Scribe's Table and Summoning Focus mixins;
- representative/current primitives across NEG, Too Many Glyphs fallback, Ars Omega fallback, Ars Trinkets fallback and Ars Scalaes fallback;
- generated language/recipe surfaces where needed.

## Confidence split

| Claim | Confidence |
|---|---|
| installed filename/version/SHA-1 | HIGH — physical modlist |
| source 4.6.1 registration and formulas | HIGH — exact source-semver commit |
| current-pack conditional registration matrix | HIGH — physical mod presence crossed with exact registration code |
| exact source tree equals installed binary byte-for-byte | **NOT PROVEN** |
| current host-stack runtime interoperability | **NOT VERIFIED** |
| Binder slots 10–24 cast behavior | **NOT VERIFIED** |
| downstream claim behavior of every provider effect | **NOT VERIFIED** |

## Clean-room

Source was inspected for interoperability, behavior and deduplication. No provider implementation, asset, model, sound or text is incorporated into Black Arcana runtime by this documentation phase. Any future reuse beyond interface/interoperability analysis requires an explicit compatible-license/provenance decision.
