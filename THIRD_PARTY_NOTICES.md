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

## Dependency / compatibility evidence — 2026-08-30

| Upstream | Exact build/pack evidence | Intended use | Source/asset derivation status |
| --- | --- | --- | --- |
| Iron's Spells 'n Spellbooks | build version `1.21.1-3.16.3`, stable `:api` classifier | `DEPENDENCY_API` for active-spell/mana/provider integration | upstream custom/All-Rights-Reserved terms have been observed for the current project line; own addon/API integration only. Source/assets are `REVIEW_REQUIRED`/`PERMISSION_REQUIRED` unless exact terms/source revision explicitly permit reuse |
| Ars Nouveau | CurseForge file `8517890`, pack/build baseline `5.13.0` | `DEPENDENCY_API`, `COMPATIBILITY_TARGET` | code license has been observed as LGPLv3 with separately restricted assets; exact source revision for this binary is not pinned here, so `DERIVED_CODE`/assets remain `REVIEW_REQUIRED` |
| Eidolon: Repraised | CurseForge file `8064602`, version `1.21.1-0.5.0.2` | `DEPENDENCY_API`, `COMPATIBILITY_TARGET` for occult/ritual integration | LGPLv3 observed for the project line; exact source revision not pinned here, so derivation remains `REVIEW_REQUIRED` |
| Malum | pack baseline `1.8.2` | optional spirit/soul `DEPENDENCY_API / COMPATIBILITY_TARGET` | LGPLv3 observed for the project line; exact source revision and obligations not pinned here, so derivation remains `REVIEW_REQUIRED` |
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