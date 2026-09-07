# Source provenance

This file indexes third-party projects and platform/build relationships used by Black Arcana as clean-room behavioral references, optional dependencies, compatibility targets, sibling-system integrations or development infrastructure.

**A public repository, documentation page, installed JAR, observable gameplay mechanic or build dependency is not permission to copy implementation or assets.** Before source/asset derivation, consult [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`plans/09-hardening-release/06-provenance-license.md`](plans/09-hardening-release/06-provenance-license.md).

| Source | Black Arcana use | Compliance posture |
| --- | --- | --- |
| Minecraft 1.21.1 / Mojang | target game/platform | `PLATFORM_DEPENDENCY`; proprietary platform relationship only; no Minecraft code/assets are treated as reusable Black Arcana source material |
| NeoForge `21.1.248` | mod-loader/runtime/API platform | `PLATFORM_API_RUNTIME`; exact release/license/notice obligations are part of the final provenance audit and must be reviewed before distribution claims |
| ModDevGradle `2.0.144` | Gradle plugin/build tooling | `BUILD_TOOL`; exact release/license provenance remains a final hardening audit item |
| Gradle `9.2.1` bootstrap | build execution tooling | `BUILD_TOOL`; exact distribution/license provenance remains a final hardening audit item |
| JUnit `5.11.4` | test framework | `TEST_TOOL`; exact release/license provenance remains a final hardening audit item |
| [Mahou Tsukai](https://www.curseforge.com/minecraft/mc-mods/mahou-tsukai) | clean-room behavioral/design reference only | `REFERENCE_ONLY`; do not copy/decompile/reuse code, assets, text, models, sounds or implementation details on the basis of this project |
| [Iron's Spells 'n Spellbooks](https://github.com/iron431/irons-spells-n-spellbooks) | optional active-spell/mana integration through the published addon-facing API; build baseline `1.21.1-3.16.3` | `DEPENDENCY_API`; source/assets are not imported by implication |
| [Ars Nouveau](https://github.com/baileyholl/Ars-Nouveau) | optional mana/resource/glyph-compatible utility integration; pack baseline `5.13.0` | `DEPENDENCY_API / COMPATIBILITY_TARGET`; avoid duplicating generic Ars-owned mechanics |
| [Eidolon: Repraised](https://www.curseforge.com/minecraft/mc-mods/eidolon-repraised) | optional occult/ritual integration; pack baseline `0.5.0.2` | `DEPENDENCY_API / COMPATIBILITY_TARGET`; extension capability must be proven against exact version |
| [Goety Cataclysm `1.21.1-1.8.2`](https://www.curseforge.com/minecraft/mc-mods/goety-cataclysm/files/8518940) | exact-artifact/public-surface audit for installed Goety↔Cataclysm addon; authority/deduplication mapping only | `REFERENCE_ONLY / COMPATIBILITY_TARGET / ARR`; exact installed artifact is pinned, but the public source repository located during audit does not expose a matching 1.21.1 revision; do not decompile/copy code or infer internals from the non-matching 1.20.1 branch |
| [Goety Iron `3.1`](https://www.curseforge.com/minecraft/mc-mods/goety-iron/files/8662179) | exact-artifact/public-description/changelog audit for installed Goety↔Iron's servant bridge | `REFERENCE_ONLY / COMPATIBILITY_TARGET`; project page declares MIT, but no exact public source revision was located during audit, so registry/API internals remain fail-closed and no source-derivation claim is made |
| [Malum `1.8.2`](https://github.com/SammySemicolon/Malum-Mod/tree/03b743a37f3eeb0cc7f4364f0730e1f135f78408) | exact version-line metadata + publisher changelog audit for installed spirit/rite/Geas provider | `REFERENCE_ONLY / COMPATIBILITY_TARGET`; source-internal specification is blocked by unresolved licensing conflict: CurseForge declares LGPLv3 while exact `gradle.properties` declares All Rights Reserved and no root LICENSE resolves it; only metadata/changelog-visible behavior is promoted |
| [Hexalia release `1.3.6`](https://github.com/AstralyaStudios/Hexalia/tree/4952c65233bf31e9f0d3e55ff76be7fa1007ee3d) | source-pinned release-line audit for witchcraft/brews/rituals/data; installed filename `1.3.6`, runtime metadata `1.3.5` | `REFERENCE_ONLY / COMPATIBILITY_TARGET`; publisher CurseForge project and exact NeoForge metadata declare MIT, so read-only factual source cataloging is allowed. No source/assets are copied/adapted. Exact installed-JAR equivalence remains unverified because of the filename/runtime-version mismatch |
| [Toxony `0.10.7`](https://github.com/MrFrostyDev/Toxony_Mod/tree/881bf7fe632659e748c279966a2bf49b99f7503f) | exact-version read-only factual catalog for installed Toxicity/Oil/Mutagen provider; authority/deduplication and future boundary analysis | `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE CONFLICT`; exact `gradle.properties` and public release metadata declare LGPLv3 while the root `LICENSE` contains GPLv3 text. No code/assets are copied/adapted; source internals are not implementation authority and provider-specific adapters remain fail-closed until license/API/runtime reconciliation |
| [Mobstein `5.4.4`](https://www.curseforge.com/minecraft/mc-mods/mobstein-upgrade-useless-animals/files/8040734) | exact-artifact + publisher-public-guide audit for installed corporeal resurrection/anatomy/experiment provider; authority and semantic deduplication only | `REFERENCE_ONLY / COMPATIBILITY_TARGET / ARR`; exact release is pinned and publisher gameplay documentation/changelogs are cataloged, but no source or bytecode is decompiled/copied and no registry/API internals are inferred. Mobstein-specific runtime integration remains fail-closed; 5.4.4 declares Sable compatibility without documenting the seam |
| [Vampirism Integrations](https://github.com/TeamLapen/VampirismIntegrations/tree/bff02b9686408691aea2c0c910ccb712edb18bd5) | exact-source compatibility audit for installed `1.10.2`; cataloging loader eligibility, Cold Sweat/Jade boundaries and conditional data maps | `REFERENCE_ONLY / COMPATIBILITY_TARGET`; exact pin licensed GNU LGPL v3 was inspected read-only; no upstream code/assets are copied or adapted into Black Arcana |
| [Werewolves](https://github.com/TeamLapen/Werewolves/tree/b72635b3e014e406b25bb79adb9d340f7443660b) | exact-source provider audit for installed `2.0.3.3`; cataloging faction/forms/actions/skills/effects/leveling/Lord/minion/refinement contracts | `REFERENCE_ONLY / COMPATIBILITY_TARGET`; exact pin licensed GNU LGPL v3 was inspected read-only; no upstream code/assets are copied or adapted into Black Arcana |
| [RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree) | sibling progression/mastery/attribute provider | `DEPENDENCY_API / COMPATIBILITY_TARGET`; Black Arcana consumes a provider boundary rather than copying RPG implementation |
| [Curios](https://github.com/TheIllusiveC4/Curios) | optional Stage 05A equipment/resistance snapshot provider, baseline `9.5.1+1.21.1` | `DEPENDENCY_API`; no global/per-tick Curios scan |

## Canonical reference evidence

Black Arcana's clean-room catalog and host analysis live under [`docs/reference/`](docs/reference/README.md), including:

- `mahou-observable-catalog.md` — observable/public behavior inventory;
- `classification-matrix.md` — `KEEP/REIMAGINE/MERGE/DROP/DEFER` disposition;
- `candidate-specifications.md` and design documents — original implementation-facing contracts;
- `host-capability-map.md` — authority split across external magic mods;
- `runtime-host-baseline.md` — exact installed-pack versions used by Stage 03.

Those documents specify what Black Arcana may independently implement. They are not source-code derivation records.

## Final audit rule

Entries marked as a platform/build/test relationship are intentionally not treated as source-derivation grants. Stage 09 must reconcile the exact distributed/runtime/build artifacts with their applicable licenses/notices and record any redistribution obligation that actually applies to the Black Arcana release artifact.