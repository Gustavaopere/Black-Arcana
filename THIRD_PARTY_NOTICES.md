# Third-Party Notices and Provenance

Black Arcana is a clean-room forbidden-magic project. It interoperates with external Minecraft mods and uses public/observable behavior as design input, but external source code and assets do not enter this repository merely because a mechanic is referenced or a dependency is compiled against.

## Status vocabulary

- `REFERENCE_ONLY` — behavior/architecture may be studied; no source/assets are intended to be copied.
- `DEPENDENCY_API` — Black Arcana writes its own integration against an allowed external API/dependency.
- `COMPATIBILITY_TARGET` — external mod is supported/tested without source ownership.
- `PLATFORM_DEPENDENCY` / `PLATFORM_API_RUNTIME` — target platform/runtime relationship, not a source-reuse grant.
- `BUILD_TOOL` / `TEST_TOOL` — development infrastructure, not runtime/content source material.
- `DERIVED_CODE` — copied/adapted source; exact revision/file/license obligations required.
- `DERIVED_ASSET` — copied/adapted asset; separate asset rights required.
- `REVIEW_REQUIRED` — available evidence is insufficient to authorize derivation or a final redistribution claim.
- `PERMISSION_REQUIRED` — explicit additional permission is required before public copying/adaptation.

## Clean-room boundary: Mahou Tsukai

Mahou Tsukai is a behavioral/design reference only. Black Arcana's Stage 01 catalog translates observable concepts into original names, rules, costs, safety contracts and integration choices before implementation.

Project policy forbids using Mahou Tsukai code, decompiled implementation, assets, models, sounds, copied text or implementation details as source material. No reuse license is relied upon by Black Arcana for those materials. If direct reuse were ever proposed, it would remain `PERMISSION_REQUIRED`/`REVIEW_REQUIRED` until explicit applicable rights were recorded.

The clean-room audit must also check terminology and audiovisual assets so that independent implementation does not accidentally import protected expression from the reference or unrelated third-party fiction.

## Platform and development infrastructure

The following relationships are required to build/test/run the project but do not authorize Black Arcana to copy platform or tool source/assets:

| Relationship | Pinned project evidence | Classification | Release/provenance posture |
| --- | --- | --- | --- |
| Minecraft / Mojang | Minecraft `1.21.1` | `PLATFORM_DEPENDENCY` | proprietary target platform; no Minecraft source/assets are treated as Black Arcana source material |
| NeoForge | `21.1.248` | `PLATFORM_API_RUNTIME` | final Stage 09 audit must record the exact release/license/notices that apply to the release relationship |
| ModDevGradle | `2.0.144` | `BUILD_TOOL` | final Stage 09 audit must record exact release/license provenance; build use is not source derivation |
| Gradle | `9.2.1` bootstrap | `BUILD_TOOL` | final Stage 09 audit must record exact distribution/license provenance where relevant |
| JUnit | `5.11.4` | `TEST_TOOL` | test-only relationship; final audit records exact license provenance where relevant |

Until that final reconciliation is recorded, these entries may support normal platform/build/test use but are `REVIEW_REQUIRED` for any stronger redistribution or source-derivation claim.

## Dependency / compatibility evidence — through 2026-09-11

| Upstream | Exact build/pack evidence | Intended use | Source/asset derivation status |
| --- | --- | --- | --- |
| Iron's Spells 'n Spellbooks | build version `1.21.1-3.16.3`, stable `:api` classifier | `DEPENDENCY_API` for active-spell/mana/provider integration | upstream custom/All-Rights-Reserved terms have been observed for the current project line; own addon/API integration only. Source/assets are `REVIEW_REQUIRED`/`PERMISSION_REQUIRED` unless exact terms/source revision explicitly permit reuse |
| Apprentice's Codex | installed `0.9.7.1`; JAR `apprentice_codex-0.9.7.1+mc1.21.1.jar`; exact source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-source factual audit for the 83-spell Iron's-native provider, School Affinity, provider registries, equipment/acquisition and optional compatibility boundaries | exact `gradle.properties` and root license declare MIT; upstream `ASSETS_LICENSE.md` declares original project assets CC0-1.0 unless otherwise noted and upstream third-party notices preserve separate terms. Source was inspected read-only for factual cataloging; no upstream code/assets are copied/adapted into Black Arcana. Any future `DERIVED_CODE` or `DERIVED_ASSET` proposal requires a separate derivation record and exact notice/license review |
| Cataclysm: Spellbooks | installed `1.1.13-1.21`; JAR `cataclysm_spellbooks-1.1.13-1.21.jar`; CurseForge File ID `8792628`; physical/audit SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`; separate public source baseline still declares `1.1.11-1.21` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 59 current registered spell identities for catalog/deduplication while preserving the stale public source only as historical evidence | current CurseForge and source `TEMPLATE_LICENSE.txt` identify PolyForm Shield 1.0.0, while public-source `gradle.properties` declares `All Rights Reserved`; neither surface is treated as a derivation grant. Exact binary inspection was restricted to hash/metadata, archive/resource/localization IDs, class/member signatures, filtered root-ID literals and narrow registry/constructor facts. No implementation body/source reconstruction/assets/models/sounds/upstream prose are copied/adapted; exact numerical mechanics, acquisition and runtime/API integration remain `REVIEW_REQUIRED`/fail-closed |
| Leyline Spellbooks | installed `1.0.3`; JAR `leylines-1.0.3.jar`; CurseForge File ID `8565076`; physical/audit SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 14 current spell identities plus bounded progression/resource and Iron's-host eligibility evidence | project is **All Rights Reserved**. Binary inspection is restricted to hash/metadata/resource/registry IDs, class/member signatures, narrow registry/default-control facts and structured acquisition/progression references; no implementation body/source reconstruction/assets/models/sounds/upstream prose are copied/adapted. Exact numerical runtime behavior, persistence/network internals and provider-specific adapter/API contracts remain `REVIEW_REQUIRED`/fail-closed |
| Somake Spells | installed `1.0.8`; JAR `somakespells-1.0.8-1.21.1-fix.jar`; CurseForge File ID `8417850`; physical/audit SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 67 current spell registrations under the current optional-provider set, plus publisher release-line evidence for Elemental Charges, Aqua/Symmetry, progression, rituals and equipment | project is **All Rights Reserved**. No matching publisher source revision was located. Binary inspection was restricted to cryptographic identity, factual archive/resource/registry IDs, class/member signatures and narrow gate/config control-flow facts; no implementation body/source reconstruction/assets/models/sounds/upstream prose are copied/adapted. Effective COMMON config, survival acquisition/reachability, stable API seams and Somake↔deprecated-T.O Aqua runtime ownership remain `REVIEW_REQUIRED`/fail-closed |
| Alshanex's Familiars | installed `4.0.3`; JAR `alshanex_familiars-1.21.1_v4.0.3.jar`; CurseForge File ID `8675568`; physical/audit SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 7 current provider spells and 11 custom ritual identities for catalog/deduplication | project is **All Rights Reserved**. Binary inspection was restricted to hash identity, factual archive/resource identifiers, structured ritual type/result IDs, class/member signatures, filtered spell-ID literals and a narrow registry static-initializer count/branch check. No implementation body/source reconstruction, assets, models, sounds or upstream prose are copied/adapted; any stronger derivation remains `PERMISSION_REQUIRED`/`REVIEW_REQUIRED`, and runtime/API integration remains fail-closed |
| Ars Nouveau | CurseForge file `8517890`, pack/build baseline `5.13.0` | `DEPENDENCY_API`, `COMPATIBILITY_TARGET` | code license has been observed as LGPLv3 with separately restricted assets; exact source revision for this binary is not pinned here, so `DERIVED_CODE`/assets remain `REVIEW_REQUIRED` |
| Eidolon: Repraised | CurseForge file `8064602`, version `1.21.1-0.5.0.2` | `DEPENDENCY_API`, `COMPATIBILITY_TARGET` for occult/ritual integration | LGPLv3 observed for the project line; exact source revision not pinned here, so derivation remains `REVIEW_REQUIRED` |
| Goety | installed `3.1.4`; JAR `goety-3.1.4.jar`; CurseForge File ID `8689429`; physical/audit SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`; exact artifact evidence closes 123 Focus + 238 non-Focus ritual actions | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit for Phase 2BH; no runtime/API authority transfer | exact artifact metadata reports `MIT License`; public source remains mixed MIT/ARR. Apply stricter clean-room posture: no implementation bodies, recipe ingredient lists, assets/models/sounds/localization prose copied/adapted; runtime/API integration remains `REVIEW_REQUIRED`/fail-closed |
| Malum | installed `1.8.2`; bounded source line from `SammySemicolon/Malum-Mod@f56691e56e591a6d8d1859ff119e749375e14d61` through `03b743a37f3eeb0cc7f4364f0730e1f135f78408`; read-only inspection of `MalumSpiritRiteTypes.java`, supporting `MalumSpiritRiteEffectTypes.java`, `MalumGeasEffectTypes.java`, `MalumSpiritTypes.java`, `TotemMagicEntries.java`, `CodexLangDatagen.java` and their relevant path histories | optional spirit/soul `DEPENDENCY_API / COMPATIBILITY_TARGET`; factual catalog/deduplication uses whole-interval registry evidence for 26 base rites, 37 active Geas effect types and 9 Spirit types, plus release-bounded player-facing progression/recipe-page evidence proving `undirected_rite` and `unchained_rite` are real rite entries rather than proxy registry slots | **license conflict remains unresolved:** CurseForge declares GNU LGPLv3, while exact `gradle.properties` on the audited line declares `All Rights Reserved` and no root LICENSE resolves the discrepancy. Source was consulted read-only for factual names/counts/path history/blob identity, progression-entry/recipe-page presence and semantic reachability only. No upstream code/assets/text are copied/adapted. Source-derived implementation/API specification and provider-resource mutation remain `REVIEW_REQUIRED`/blocked and fail-closed |
| Gaze | installed `1.1.7.1`; JAR `gaze-1.1.7.1.jar`; CurseForge File ID `7261638`; Modrinth project/version `NlvaJ5WE / od4ltbRo`; physical/audit SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`; exact evidence PR #201/run `34676660467` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 26 Gaze Spirit Rite identities, two Geas effect types, eight rune items and one Gaze-owned Iron's spell for catalog/deduplication; only Soulward Shield is currently promoted semantically because the Rite registry remains config-conditional | project is **All Rights Reserved**. Exact binary inspection is restricted to cryptographic identity, factual metadata/registry/type/member/resource-path evidence and narrow config/provider-gate control facts. No implementation bodies/source reconstruction, recipe ingredient lists, numerical balance values, localization prose, assets, models or sounds are copied/adapted. `disableGazeRites`, runtime/API/resource-settlement seams and any stronger derivation remain `REVIEW_REQUIRED`/fail-closed |
| Goety Cataclysm | installed `1.21.1-1.8.2`; CurseForge File ID `8518940` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` for Goety↔Cataclysm authority/dedup mapping | project is All Rights Reserved and the public repository located does not expose the matching 1.21.1 source revision. No decompilation/source-derived internals; provider-specific implementation remains fail-closed |
| Goety Iron | installed `3.1`; JAR `GoetyIron-1.21.1-NeoForge-3.1.jar`; CurseForge File ID `8662179`; Modrinth project/version `tZpynDu5 / YZXNIxvk`; physical and Modrinth SHA-1 `c8529867e798661ed01fb2948abda23735888fc6` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact/public-release audit for the Goety↔Iron's servant bridge, including cross-loader release synchronization and public servant/behavior provenance | **license conflict unresolved:** CurseForge declares MIT while exact Modrinth project metadata declares All Rights Reserved and `source_url=null`. Publisher changelogs establish content equivalence for NeoForge `3.0.0` ↔ Forge `2.1.0` and an identical synchronized delta for NeoForge `3.1` ↔ Forge `2.2`, but do not prove structural/binary registry equivalence. Apply the stricter clean-room posture: public metadata/behavior may be cataloged, but no upstream code/assets/text are copied or adapted; internal registry/API claims remain `REVIEW_REQUIRED`/fail-closed |
| Hexalia | installed filename `hexalia-neoforge-1.3.6.jar`, runtime metadata `1.3.5`; publisher release File ID `8658488`; source release commit `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` source audit for witchcraft/brews/rituals/data + future API verification | publisher CurseForge project and exact NeoForge metadata declare MIT. Source may be inspected read-only for factual cataloging, with no upstream code/assets copied/adapted. Because installed runtime metadata reports `1.3.5` while the physical/release line is `1.3.6`, exact installed-JAR equivalence remains `REVIEW_REQUIRED` pending runtime/artifact QA |
| Toxony | installed `0.10.7`; JAR `toxony-0.10.7.jar`; exact public version commit `MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` factual source audit for Toxicity, Oils, Mutagens, Affinities and external-compat boundaries | **license conflict unresolved:** exact `gradle.properties` and public release metadata declare GNU LGPL 3.0/LGPLv3 while the root `LICENSE` at the same commit contains GNU GPL v3 text. Read-only factual cataloging only; no upstream code/assets copied/adapted; source-derived implementation/API coupling remains `REVIEW_REQUIRED` and fail-closed until reconciled |
| Mobstein | installed `5.4.4`; JAR `mobstein-5.4.4-neoforge-1.21.1.jar`; CurseForge File ID `8040734` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-release/public-guide audit for corporeal resurrection, anatomy, surgery, reconstructed creatures, experiments, structures and boss progression | project is **All Rights Reserved**. Only exact release metadata plus publisher-authored public guide/changelogs are used. No source/JAR bytecode is decompiled, copied or adapted; internal registries/API remain unverified and provider-specific integration stays fail-closed. Exact 5.4.4 changelog declares Sable compatibility but does not document the seam |
| Vampirism Integrations | installed `1.10.2`; exact source `TeamLapen/VampirismIntegrations@bff02b9686408691aea2c0c910ccb712edb18bd5` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` source audit for loader eligibility, Cold Sweat/Jade behavior and conditional data maps | exact pinned `LICENCE` is GNU LGPL v3. Source was inspected read-only to derive factual catalog constraints; no source code/assets are copied or adapted. Any future `DERIVED_CODE` proposal still requires a separate derivation-register entry and LGPL compliance review |
| Werewolves | installed `2.0.3.3`; exact source `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` source audit for faction/forms/actions/skills/effects/leveling/Lord/minion/refinement semantics | exact pinned `LICENSE` is GNU LGPL v3. Source was inspected read-only to derive factual catalog constraints; no source code/assets are copied or adapted. Any future `DERIVED_CODE` proposal still requires a separate derivation-register entry and LGPL compliance review |
| RPG Skill Tree | sibling repository `Gustavaopere/neoforge-rpg-skilltree` | progression/mastery/attribute provider | API/compatibility integration only. Black Arcana must not copy implementation across repositories without separately resolving that repository's exact license/provenance obligations |
| Curios | Stage 05A baseline `9.5.1+1.21.1` | optional equipment snapshot `DEPENDENCY_API` | LGPLv3-or-later observed historically; exact source revision not pinned here, so source derivation remains `REVIEW_REQUIRED` |

Artifact IDs/versions establish what was compiled/tested. They are not source-reuse licenses.

## Black Arcana-owned license

Black Arcana-owned source/assets are currently **All Rights Reserved**, as declared by project metadata and the root `LICENSE`. That project-level copyright posture does not override or absorb third-party obligations.

## Derivation register

No third-party `DERIVED_CODE` or `DERIVED_ASSET` record is authorized merely by the tables above. Before substantial source or assets are copied/adapted, record:

```text
Local file(s):
Upstream project/URL:
Upstream commit/tag:
Upstream file(s)/resource(s):
Use type: DERIVED_CODE | DERIVED_ASSET
License/permission:
Required copyright/notice/source obligations:
Modification note/date:
Permission evidence (if required):
```

## Retroactive release audit

Before a public release, scan source and binary resources to confirm:

- no Mahou Tsukai or other unlicensed implementation entered the repository;
- external API/provider code is isolated to the intended adapter boundaries;
- no copied translations, textures, models, sounds or other assets lack provenance;
- source files with unusually close third-party structure/naming are reviewed;
- platform/runtime/build/test dependencies are reconciled against exact versions and applicable notice/redistribution obligations;
- bundled libraries/binaries are represented by the release provenance records;
- player-facing terminology remains within the original Black Arcana identity vocabulary or otherwise has documented rights.

## Release policy

A release must fail closed when actual copied/adapted material has `REVIEW_REQUIRED`, `PERMISSION_REQUIRED` or unknown rights. Normal platform, build, test, dependency/API and compatibility support may continue without granting Black Arcana any rights to external source/assets.

The built JAR must carry the root `LICENSE` and this `THIRD_PARTY_NOTICES.md` file.
