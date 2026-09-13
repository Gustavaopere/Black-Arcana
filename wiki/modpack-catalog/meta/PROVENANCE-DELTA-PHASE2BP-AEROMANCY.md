# Provenance Delta — Phase 2BP SnackPirate's Aeromancy Additions 1.2.8

Status: `EXACT PUBLIC SOURCE PIN / PHYSICAL HASH AUTHORITY RETAINED / CLEAN-ROOM FACTUAL INSPECTION ONLY`

## Physical authority

- JAR: `aero_additions-1.2.8.jar`
- mod id/version: `aero_additions` / `1.2.8`
- SHA-1: `dee32c9fa84d6e39846608f8f77591ea56f`
- CurseForge hash: `3079423735`
- physical snapshot: current 595-entry modlist, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`

The physical artifact remains authority for what is installed. This tranche does not claim a reproducible source build or a source-produced JAR hash match.

## Exact public source checkpoint

- repository: `snackerpirater/aero-additions`
- commit: `ae282b32d25ad76ef8d01c637ec05566a767ae4c`
- tree: `fcee08e613fbfa030f034268a0240c8693ab7f45`
- recursive tree listing: complete (`truncated=false`)
- commit date: 2026-06-15
- `gradle.properties` identifies `mod_id=aero_additions`, `mod_version=1.2.8`, Minecraft 1.21.1 and NeoForge 21.1.228
- generated metadata requires Iron's `[1.21.1-3.15.0,1.21.1-4.0.0)` and ExpandAbility `[12.0.0,13.0.0)`

This is sufficient to source-pin the provider's public 1.2.8 registry/dependency contract. It is not elevated to binary identity.

## License surface

`gradle.properties` declares `mod_license=MIT`, and generated mod metadata projects that declaration into the mod descriptor. The complete source tree does not expose a root `LICENSE`; the only license file observed is `TEMPLATE_LICENSE.txt`, whose own text explicitly limits itself to NeoForged MDK template files.

Therefore this audit does not broaden reuse rights from the template license or rely on a source-code licensing interpretation. Black Arcana remains clean-room and uses the source only for factual interoperability/catalog evidence.

No implementation bodies, creative recipes, localization prose, textures, models, animations, sounds or other creative assets are copied or adapted.

## External host source used narrowly

The public Iron's Spells 'n Spellbooks 3.16.3 source line at `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` is used only to interpret:

- the seven-argument `SchoolType` defaults (`requiresLearning=false`, `allowLooting=true`);
- `DefaultConfig` defaults for enabled/crafting state;
- Scroll Forge school-focus enumeration and its enabled/crafting/player gates.

The physical pack also contains Iron's 3.16.3 by version label, but no cryptographic source/binary equivalence is claimed.

The Aeromancy source build compiles against Iron's 3.16.1 and NeoForge 21.1.228; the physical pack uses Iron's 3.16.3 and NeoForge 21.1.248. Generated provider metadata admits the physical Iron's version. These are compatibility facts, not runtime PASS evidence.

## Result

Phase 2BP supports a candidate semantic delta of **+10 `COUNTED_SOURCE_PINNED`** provider spell identities and candidate component promotion to **#64 / 64 of 100**, while preserving current assembled-pack runtime QA as a separate fail-closed gate. Shared ledgers are intentionally not changed by this evidence tranche.
