# Current Magic Catalog Coverage

## Operational percentage

**Canonical coverage at the reconciled Phase 2AW base: 50/100 = 50%.**

`main@517b3e9c6da648c1470c227a11f571d951fbee47` merged Phase 2AV / PR #160 and makes `apotheosis` 8.8.0 canonical component **#50**. Exact-SHA post-merge workflow #2295 / run `34417733744` completed successfully on that main commit.

Phase 2AW represents candidate component **#51**, `apotheoticcreation` 2.0.0. Therefore this revision describes **51/100 = 51% only as a candidate** until CI GREEN on the exact reconciled HEAD, a final latest-main gate, merge and post-merge `main` confirmation.

The complete pre-Phase-2AW current-coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AW.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AW.md). Provider-specific evidence lives under `wiki/modpack-catalog/providers/**` plus the corresponding phase checkpoint/capability files.

This metric counts current magic/cross-domain provider components closed to the strongest available evidence. It is not a percentage of spells, affixes, filters or registry objects, and partial provider inventories receive zero closed-component points.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: 21.1.248
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

## Current working denominator

The operational denominator remains **100 magic/cross-domain component units** under the established physical reconciliation:

- 103 historical candidate IDs;
- 5 historically listed candidates now absent: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 current candidates added beyond the historical baseline: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100`.

The denominator must be reconciled whenever the physical provider set changes.

## Canonical recent closure sequence

| Component | Phase / PR | Provider | Result |
|---:|---|---|---|
| 42 | Phase 2AN / PR #149 | `apothic_attributes` | canonical |
| 43 | Phase 2AO / PR #150 | `soul_fire_d` | canonical |
| 44 | Phase 2AP / PR #151 | `create_enchantment_industry_plus` | canonical; later metadata correction had zero coverage delta |
| 45 | Phase 2AQ / PR #152 | `apothic_compat` | canonical |
| 46 | Phase 2AR / PR #154 | `backportedspellbooks` | canonical |
| 47 | Phase 2AS / PR #155 | `apothic_compats` | canonical |
| 48 | Phase 2AT / PR #156 | `apothic_spawners` | canonical |
| 49 | Phase 2AU / PR #158 | `apothic_enchanting` | canonical |
| 50 | Phase 2AV / PR #160 | `apotheosis` | canonical at `main@517b3e9c6da648c1470c227a11f571d951fbee47` |
| 51 | Phase 2AW | `apotheoticcreation` | candidate in this revision |

Components #1–#41 remain part of the same canonical numerator and are preserved by the prior cumulative snapshots/provider records.

## Phase 2AW — Apotheotic Creation 2.0.0 component #51, candidate

Phase 2AW closes the installed narrow Create ↔ Apotheosis filter bridge at exact physical + publisher + exact official source evidence:

- physical artifact `apotheoticcreation-2.0.0.jar`, mod id `apotheoticcreation`, SHA-1 `6bbb91aea834941b47a6af3318b091f64e4375ab`;
- physical Create 6.0.10 and Apotheosis 8.8.0;
- CurseForge project/file `956637 / 8391265`, release 2026-07-08 for NeoForge / Minecraft 1.21.1;
- publisher Source link resolves to `maxpowa/ApotheoticCreation`;
- exact official source `maxpowa/ApotheoticCreation@ed56ccf54e1be132c983c524597300e852098840`, source tree `5c5d51ef69b5f0f50d398d7f0479b8ca83894f7d`;
- exact metadata: Minecraft 1.21.1, NeoForge development baseline 21.1.235, mod version 2.0.0, Create range `[6,)`, Apotheosis range `[8,)`, MIT;
- recursive exact tree is complete (`truncated=false`) and contains one Java source file;
- that class registers exactly two Create `ITEM_ATTRIBUTE_TYPE` entries: `apotheoticcreation:rarity` and `apotheoticcreation:affix`;
- rarity matching reads Apotheosis `LootRarity` / `RarityRegistry` state through provider helpers/codecs;
- affix matching reads Apotheosis `AffixRegistry` / item-affix state through provider helpers/codecs;
- visible affix enumeration intentionally excludes affix paths `socket` and `durable`;
- addon-defined `MapCodec`/`StreamCodec` pairs serialize the two attribute values inside Create-owned filter storage/transport;
- no addon-owned spell/mana/ritual/casting surface, standalone payload registration, SavedData or attachment container was observed in the complete exact source tree.

The addon is not authority for the data it translates. Apotheosis retains rarity/affix authority; Create retains Attribute Filter semantics, enclosing storage/transport and logistics authority. Apotheotic Creation owns the registration/translation bridge plus serialization of its two attribute values. Black Arcana must not mirror either registry or reinterpret Create downstream routing as its own cast/hazard runtime.

Smart Observers, Brass Tunnels and other Create consumers are downstream consumers of normal Create filtering behavior, not separate hooks established by this addon. No special Black Arcana integration is justified merely by their thematic usefulness.

## Integration / clean-room boundary

Exact source internals are used read-only as factual evidence. The bridge already provides the provider-native interoperability seam; Black Arcana has no reason to duplicate its rarity/affix classification. Any future coupling must remain behind a specific boundary and fail closed if the exact provider contract is unavailable.

The exact source metadata and root license are MIT, and the current CurseForge project surface also labels the project MIT. No code/assets/text are copied or adapted.

## Partial providers still receive zero points

Examples remain:

- `leylines` — current total inventory not verified;
- `somakespells` — current granular spell inventory remains incomplete;
- `cataclysm_spellbooks` — installed 1.1.13 remains ahead of the exact public source baseline already audited;
- `gaze` — exact current registry/source-JAR closure remains pending.

## Update rule

After each provider closure:

1. re-read physical modlist and current `main`;
2. reconcile concurrent PR/branch ownership;
3. close the provider to the strongest exact evidence available;
4. preserve physical/publisher/source/license evidence layers when they differ;
5. merge only after latest-main reconciliation and CI GREEN on the exact reconciled HEAD;
6. increment the canonical numerator only after merge and post-merge main confirmation;
7. change the denominator whenever physical reconciliation changes the provider set.

Phase 3 remains blocked until provider catalog/deduplication establishes real Black Arcana gaps.