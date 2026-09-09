# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AT revision: 48/100 = 48%.**

The latest canonical base for this branch is `main@063135e690b4c066db582be1be6dd1e1387f1758`, where canonical coverage is **47/100 = 47%** after Phase 2AS / PR #155 merged `apothic_compats` as component #47. Exact-SHA post-merge workflow #2239 is GREEN on that canonical merge SHA.

Phase 2AT represents candidate component **#48**, `apothic_spawners` 1.4.0. The numerator becomes canonical only after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge, and post-merge `main` confirmation.

The detailed pre-Phase-2AT cumulative coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AT.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AT.md). Provider-specific evidence remains in `wiki/modpack-catalog/providers/**` and the corresponding phase checkpoint/capability files.

This metric is intentionally conservative. It measures **current magic/cross-domain provider components closed to the strongest evidence presently available**, not a guessed percentage of every individual spell object. A provider with a partial current inventory or unresolved current-version delta contributes zero closed component points.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: 21.1.248
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

The historical 2026-09-07 queue used **612 top-level entries / 103 candidate components**. It is preserved as history and is not the current denominator.

## Current working denominator

The current operational denominator remains **100 magic/cross-domain component units** after direct ID reconciliation of the historical 103-candidate set against the physical modlist:

- **98** of the former 103 candidate mod IDs still survive the current physical modlist;
- the **5 actually absent** former candidates are `ars_morph`, `morerelics`, `reliquary`, `vestis` and `woodwalkers_spellbooks`;
- **2** current magic/cross-domain candidates not represented by the old 103-unit baseline are `soul_fire_d` and `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100` current operational units.

Correction retained from Phase 2AF: `backportedspellbooks`, `crystal_chronicles` and `gtbcs_geomancy_plus` are physically present in the same 595-entry / SHA-1 `7aaece...` modlist and are not removed components.

This denominator is operational, not immutable. Reconcile it whenever the physical provider set changes.

## Canonical recent closure sequence

The cumulative numerator through component #47 is canonical on `main@063135e690b4c066db582be1be6dd1e1387f1758`.

| Component | Phase / PR | Provider | Canonical result |
|---:|---|---|---|
| 35 | Phase 2AF / PR #135 | `not_enough_glyphs` | canonical |
| 36 | Phase 2AG / PR #137 | `ars_n_spells` | canonical |
| 37 | Phase 2AH / PR #140 | `monstersspellbooks` | canonical |
| — | Phase 2AI / PR #141 | `somakespells` | canonical re-audit, **zero coverage delta** because current granular inventory remains partial |
| 38 | Phase 2AJ / PR #143 | `aces_spell_utils` | canonical |
| 39 | Phase 2AK / PR #144 | `emf_compat_iron_spells` | canonical |
| 40 | Phase 2AL / PR #145 | `efiscompat` | canonical |
| 41 | Phase 2AM / PR #147 | `reliquified_lenders_cataclysm_new_relics_fix` | canonical |
| 42 | Phase 2AN / PR #149 | `apothic_attributes` | canonical |
| 43 | Phase 2AO / PR #150 | `soul_fire_d` | canonical |
| 44 | Phase 2AP / PR #151 | `create_enchantment_industry_plus` | canonical; PR #153 later corrected metadata with zero coverage delta |
| 45 | Phase 2AQ / PR #152 | `apothic_compat` | canonical at merge SHA `bdf5271c265b5f40ee5a9e7695c7d71374a4c31c` |
| 46 | Phase 2AR / PR #154 | `backportedspellbooks` | canonical at merge SHA `ac4df420158616d2fb993fb5fbf6b8325c207c27` |
| 47 | Phase 2AS / PR #155 | `apothic_compats` | canonical at merge SHA `063135e690b4c066db582be1be6dd1e1387f1758`; post-merge workflow #2239 GREEN |

Earlier components #1–#34 remain part of the same canonical numerator and are not renumbered by this normalization. Their detailed history remains in preserved catalog snapshots and provider/phase documents.

## Phase 2AS — Apothic Compats component #47, canonical

Phase 2AS / PR #155 closed `apothic_compats` 0.2.4.2 at exact physical + exact official source evidence and is canonical at merge SHA `063135e690b4c066db582be1be6dd1e1387f1758`.

Key closure facts remain preserved in the pre-2AT snapshot and provider-specific files. The semantic result remains 0 standalone spells/glyphs/rituals/cast resource, with provider-owned compatibility datapacks/runtime glue only. Black Arcana does not duplicate Ars/Malum resource settlement, Apothic affix/gem semantics, projectile velocity processing, or provider offensive proc chains.

## Phase 2AT — Apothic Spawners component #48, candidate

Phase 2AT closes `apothic_spawners` 1.4.0 at exact physical + exact official release-source evidence:

- physical artifact `ApothicSpawners-1.21.1-1.4.0.jar`, mod id `apothic_spawners`, SHA-1 `b3be29751daea738e691db8949cce079e5aae3be`;
- exact official release source `Shadows-of-Fire/Apothic-Spawners@d3bc0b40d46bee476fc770f8e4e44a1c35ecddd3`, tree `7cd127fe22a9810b22bd8203cb2286d53b840e25`;
- exact source metadata closes Minecraft 1.21.1 / Java 21 / NeoForge 21.1.187+ / Placebo 9.9.0+;
- **0 standalone spells, 0 glyphs, 0 rituals, 0 provider mana/cast resource and no C2S cast-intent path**;
- exactly 16 `spawner_stat` identities and 32 stock modifier recipes, 16 direct + 16 inverse;
- exactly 2 common mixins and 0 client mixins;
- one clientbound PLAY config payload, protocol/version `2`;
- explicit tile NBT persistence for stats, modified state, instability countdown and captured spawn data;
- bounded Nuclear Spawner behavior: 60 ticks, explosion radius 8, 12 spawn attempts and provider unstable-spawner loot.

Apothic Spawners owns spawner lifecycle, persistence, modifiers, Capturing/Echoing and its Nuclear Spawner reaction. Black Arcana retains casting, costs, targeting, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`. BA-caused world mutation must pass `WorldEffectPolicy` first; any subsequent provider-owned instability transition is not processed a second time by BA.

Component #48 becomes canonical only after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge and post-merge `main` confirmation.

## Partial providers still receive zero points

Examples remain:

- `leylines` — public signature names known, total current inventory not verified;
- `somakespells` — exact physical/release surface is audited, but current granular spell inventory is not closed;
- `cataclysm_spellbooks` — installed 1.1.13 remains ahead of the exact public source inventory already audited;
- `gaze` — public surface audited, exact current registry/source-JAR closure still pending.

## Update rule

After each provider closure:

1. re-read the physical modlist and current `main`;
2. reconcile concurrent PR ownership;
3. close the provider to the strongest exact evidence available;
4. preserve explicit evidence layers when release/source/JAR versions differ;
5. merge only after latest-main reconciliation and CI GREEN on the reconciled HEAD;
6. increment the numerator only once the closure revision is canonical on `main`;
7. change the denominator whenever physical reconciliation changes the provider set.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.
