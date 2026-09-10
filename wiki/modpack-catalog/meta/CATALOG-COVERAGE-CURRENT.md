# Current Magic Catalog Coverage

## Operational percentage

**Canonical coverage at the reconciled Phase 2AV base: 49/100 = 49%.**

`main@f3a3f95a10cf830b6bf973612d519e53d9168adc` is the branch base. That commit merged Phase 2AU / PR #158 and makes `apothic_enchanting` 1.6.2 canonical component **#49**.

Phase 2AV represents candidate component **#50**, `apotheosis` 8.8.0. Therefore this revision describes **50/100 = 50% only as a candidate** until CI GREEN on the exact reconciled HEAD, a final latest-main gate, merge and post-merge `main` confirmation.

The complete pre-Phase-2AV current-coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AV.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AV.md). Provider-specific evidence lives under `wiki/modpack-catalog/providers/**` plus the corresponding phase checkpoint/capability files.

This metric counts current magic/cross-domain provider components closed to the strongest available evidence. It is not a percentage of spell/enchantment/registry objects, and partial provider inventories receive zero closed-component points.

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
| 49 | Phase 2AU / PR #158 | `apothic_enchanting` | canonical at `main@f3a3f95a10cf830b6bf973612d519e53d9168adc` |
| 50 | Phase 2AV | `apotheosis` | candidate in this revision |

Components #1–#41 remain part of the same canonical numerator and are preserved by the prior cumulative snapshots/provider records.

## Phase 2AV — Apotheosis 8.8.0 component #50, candidate

Phase 2AV closes the installed `apotheosis` Adventure/RPG provider at exact physical + publisher + exact official source evidence:

- physical artifact `Apotheosis-1.21.1-8.8.0.jar`, mod id `apotheosis`, SHA-1 `1e4837fcaf24fe73dba1082656736d872690b303`;
- CurseForge project/file `313970 / 8826922`, released 2026-09-07 for NeoForge / Minecraft 1.21.1;
- exact official source `Shadows-of-Fire/Apotheosis@e825cd9dcb9a6fff5e163659812ff32390e343a6`, root tree `98ffba7432210ac6b5d807a83fc8e49e74db31fd`;
- exact metadata: Minecraft 1.21.1, Java 21, NeoForge 21.1.235+, Placebo 9.9.2+, Apothic Attributes 2.10.0+, with separately ordered optional Apothic Enchanting 1.6.2+ and Apothic Spawners 1.4.0+;
- exact physical pack satisfies those declared minimums with NeoForge 21.1.248, Placebo 9.9.2, Apothic Attributes 2.10.1, Apothic Enchanting 1.6.2 and Apothic Spawners 1.4.0;
- exact bootstrap owns dynamic/data-backed registries for rarity, affix, gem, affix loot, invader, rogue spawner, elite, purity weights, augment, tiered augment and rarity override;
- provider attachments/components own player world-tier unlock/state, invader/spawn state, bonus loot/damage reduction metadata and affixed/gem/rarity/UI item state;
- provider owns reforging, salvaging, augmenting, gem cutting and related menu/recipe surfaces;
- seven registered payload providers: configuration and boss/reroll S2C state plus provider-gated item-link/radial/gem-case/world-tier C2S/bidirectional state;
- no standalone spell/mana/ritual/casting registration or payload surface was observed in the exact 8.8.0 source-tree/bootstrap/network audit.

`apotheosis` does not absorb the already-cataloged `apothic_attributes`, `apothic_enchanting` or `apothic_spawners` components. Their separate mod IDs, artifacts and authority records remain intact.

Black Arcana retains canonical server-authoritative casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety. Provider world-tier/UI C2S requests are not BA cast intents. Similar names or magical flavor do not create a bridge.

## Integration / clean-room boundary

Exact source internals are used as read-only factual evidence only. The audit does not promote implementation classes into supported APIs. Any runtime integration must prefer a proven provider-native public/data/event seam, remain behind a Black Arcana adapter/boundary, preserve reload lifecycle and fail closed if no exact safe seam exists.

Source code at the exact pin is MIT. Exact source assets are All Rights Reserved, and the current CurseForge project surface is labeled All Rights Reserved. No provider code/assets/text are copied or adapted.

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
5. merge only after latest-main reconciliation and CI GREEN on the reconciled HEAD;
6. increment the canonical numerator only after merge and post-merge main confirmation;
7. change the denominator whenever physical reconciliation changes the provider set.

Phase 3 remains blocked until provider catalog/deduplication establishes real Black Arcana gaps.
