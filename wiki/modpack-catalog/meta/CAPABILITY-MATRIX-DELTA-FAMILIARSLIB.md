# Capability Matrix Delta — FamiliarsLib 1.7.1

Phase: **2AX**  
Physical provider: `familiarslib-1.21.1-1.7.1.jar`  
Mod id: `familiarslib`  
Runtime version: `1.21.1-1.7`  
Physical SHA-1: `7fa3f3116e35c12456425ae195924ced33fcc2eb`

## Closure disposition

FamiliarsLib is a real familiar-framework provider, but it is **not an independent semantic spell provider** at the audited 1.7.x source surface.

| Surface | Evidence | Authority / disposition | Semantic magic count delta |
|---|---|---|---:|
| Familiar lifecycle and base spellcasting-pet abstractions | complete release-correlated official source tree contains `AbstractSpellCastingPet` and specialized familiar bases | FamiliarsLib owns its familiar framework; this does not transfer Iron's casting/spell ownership to FamiliarsLib or Black Arcana | 0 |
| Player familiar persistence | `AttachmentRegistry` registers serializable `player_familiar_data` backed by `PlayerFamiliarData` | FamiliarsLib-owned familiar state; Black Arcana must not mirror or mutate it as a second authority | 0 |
| Familiar networking | `PayloadHandler` registers 17 optional protocol payload handlers: 9 play-to-server and 8 play-to-client | FamiliarsLib owns summon/selection/release/move/storage/sync transport; client requests do not become Black Arcana authority | 0 |
| Familiar spellbook / magic-school interoperability | source contains `AbstractFamiliarSpellbookItem`, `SchoolTypeAccessor`, familiar spellcasting behavior and registry-based school interoperability | consumes/coordinates external magic-school and spell state; no second spell registry inferred | 0 |
| Iron's spell classification tags | `data/familiarslib/tags/irons_spellbooks/spells/**` classifies external Iron's spells by attack/range/buff/defense/movement roles | tags are classification inputs, not provider-owned spell registrations | 0 |
| Sound school content | publisher changelog for `1.21.1-1.7` says all Sound-school content was removed and moved to Tunes 'n Tomes | do not count historical Sound content under FamiliarsLib 1.7.x | 0 |
| Provider-owned spells / rituals / glyphs | complete recursive source tree is `truncated=false`; no provider spell registry or `data/familiarslib/spells/**` content is present | **0 independent semantic magics** for the Phase 2 spell/magic-object metric | **0** |
| Black Arcana familiar-ownership adapter | Stage 07.07 requires verified ownership evidence; current BA runtime owns `FamiliarOwnershipRegistry` and does not contain a FamiliarsLib adapter | **FAIL-CLOSED** until an exact-version, provider-native ownership seam is proven and explicitly adapted | 0 |

## Provider-component coverage

FamiliarsLib already belongs to the reconciled 100-component magic/cross-domain denominator. Closing it therefore changes only the internal provider-component numerator:

- canonical base on `main@9cc91f1bf9b7f41708ea70635d5b36b282947866`: **51/100**;
- Phase 2AX candidate after this audit: **52/100**;
- denominator delta: **0**.

This internal component metric is not the user-facing percentage of spells/magics.

## Semantic spell/magic metric

Phase 2AX changes neither side of the semantic magic-object ratio:

- semantic numerator delta: **+0**;
- semantic denominator delta attributable to FamiliarsLib: **+0**.

The global semantic denominator is still incomplete because other providers remain partially inventoried. Do not derive a spell/magic percentage from `52/100`.

## Exactness boundary

The physical artifact is exact from the current modlist. Publisher evidence identifies CurseForge project/file `1316458 / 8059464`, uploaded 2026-05-08. The strongest official source correlation found is `Alshanex/FamiliarsLib@56561e7fd474fbd5c5166c1ac96f235faae156ab` from the same date with the matching familiar-bed bug-fix intent and tree `9d39b4751b9e52874f66cf2187afab239d00b251`.

There is no release tag or reproducibility proof tying that commit cryptographically to the installed JAR. Source-to-binary identity therefore remains **correlated, not proven exact**.

## Black Arcana boundary

No new Black Arcana runtime integration is authorized by this catalog closure. Black Arcana retains canonical casting, targeting, costs, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world-effect safety. Any future FamiliarsLib bridge must be a narrow provider-native adapter and fail closed when ownership cannot be proven.
