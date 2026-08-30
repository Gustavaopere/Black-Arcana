# Source provenance

This file indexes third-party projects used by Black Arcana as clean-room behavioral references, optional dependencies, compatibility targets or sibling-system integrations.

**A public repository, documentation page, installed JAR or observable gameplay mechanic is not permission to copy implementation or assets.** Before source/asset derivation, consult [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`plans/09-hardening-release/06-provenance-license.md`](plans/09-hardening-release/06-provenance-license.md).

| Source | Black Arcana use | Compliance posture |
| --- | --- | --- |
| [Mahou Tsukai](https://www.curseforge.com/minecraft/mc-mods/mahou-tsukai) | clean-room behavioral/design reference only | `REFERENCE_ONLY`; do not copy/decompile/reuse code, assets, text, models, sounds or implementation details on the basis of this project |
| [Iron's Spells 'n Spellbooks](https://github.com/iron431/irons-spells-n-spellbooks) | optional active-spell/mana integration through the published addon-facing API; build baseline `1.21.1-3.16.3` | `DEPENDENCY_API`; source/assets are not imported by implication |
| [Ars Nouveau](https://github.com/baileyholl/Ars-Nouveau) | optional mana/resource/glyph-compatible utility integration; pack baseline `5.13.0` | `DEPENDENCY_API / COMPATIBILITY_TARGET`; avoid duplicating generic Ars-owned mechanics |
| [Eidolon: Repraised](https://www.curseforge.com/minecraft/mc-mods/eidolon-repraised) | optional occult/ritual integration; pack baseline `0.5.0.2` | `DEPENDENCY_API / COMPATIBILITY_TARGET`; extension capability must be proven against exact version |
| [Malum](https://www.curseforge.com/minecraft/mc-mods/malum) | optional spirit/soul integration; pack baseline `1.8.2` | `DEPENDENCY_API / COMPATIBILITY_TARGET`; target current Spirit Rite model, not removed legacy assumptions |
| [RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree) | sibling progression/mastery/attribute provider | `DEPENDENCY_API / COMPATIBILITY_TARGET`; Black Arcana consumes a provider boundary rather than copying RPG implementation |
| [Curios](https://github.com/TheIllusiveC4/Curios) | optional Stage 05A equipment/resistance snapshot provider, baseline `9.5.1+1.21.1` | `DEPENDENCY_API`; no global/per-tick registry/inventory scan |

## Canonical reference evidence

Black Arcana's clean-room catalog and host analysis live under [`docs/reference/`](docs/reference/README.md), including:

- `mahou-observable-catalog.md` — observable/public behavior inventory;
- `classification-matrix.md` — `KEEP/REIMAGINE/MERGE/DROP/DEFER` disposition;
- `candidate-specifications.md` and design documents — original implementation-facing contracts;
- `host-capability-map.md` — authority split across external magic mods;
- `runtime-host-baseline.md` — exact installed-pack versions used by Stage 03.

Those documents specify what Black Arcana may independently implement. They are not source-code derivation records.
