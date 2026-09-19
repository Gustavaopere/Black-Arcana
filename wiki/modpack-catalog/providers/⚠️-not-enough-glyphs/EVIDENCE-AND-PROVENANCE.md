# Not Enough Glyphs 4.6.2 — Evidence and Provenance Ledger

## Physical installed artifact

Current sibling modlist checkpoint `8211ce36e899cc8f55d24f937b0c7200fb0b3ae1` records:

- filename: `not_enough_glyphs-1.21.1-4.6.2.jar`;
- mod id: `not_enough_glyphs`;
- name: `Not Enough Glyphs`;
- runtime version: `4.6.2`;
- official CurseForge project/file: `1023517 / 8880291`;
- current physical pack SHA-1: **not yet captured in Black Arcana authority material**;
- previous 4.6.1 SHA-1 `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4`: historical only;
- current source dependency on Sauce: `0.0.50.97`;
- current pack NeoForge remains determined by the sibling physical modlist, not by this provider source.

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
- audited commit: `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`;
- `gradle.properties` at that commit declares `mod_version=4.6.2`;
- source target Minecraft: `1.21.1`;
- source target NeoForge: `21.1.220`;
- source Ars Nouveau dependency: `5.12.0.1368`;
- source Sauce dependency: `0.0.50.97`;
- source Ars Elemental dependency: `0.7.9.4.170`;
- source metadata license string: `LGPL`.

Exact compare from 4.6.1 source pin `2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b` to 4.6.2 touches only build/changelog/version metadata, generated language/cache, `AbstractEffectFilter.java` and `PropagateUnderfoot.java`. `ArsNouveauRegistry.java` remains Git blob `28c2007999ec6e534b8c5cd2c90b012c81072cff`, and `EffectMomentum.java` remains blob `7dd4f7ebe06cbadd282fddb1a6ca603013d2af2a` with its explicit disabled override.

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
| installed filename/version | HIGH — current sibling physical modlist |
| source 4.6.2 registration matrix | HIGH — exact source-semver commit plus byte-identical registry blob across 4.6.1→4.6.2 |
| current-pack conditional registration matrix | HIGH — physical mod presence crossed with exact registration code |
| exact source tree equals installed binary byte-for-byte | **NOT PROVEN** |
| current host-stack runtime interoperability | **NOT VERIFIED** |
| Binder slots 10–24 cast behavior | **NOT VERIFIED** |
| downstream claim behavior of every provider effect | **NOT VERIFIED** |

## Clean-room

Source was inspected for interoperability, behavior and deduplication. No provider implementation, asset, model, sound or text is incorporated into Black Arcana runtime by this documentation phase. Any future reuse beyond interface/interoperability analysis requires an explicit compatible-license/provenance decision.
