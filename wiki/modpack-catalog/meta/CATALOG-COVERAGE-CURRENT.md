# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AU revision: 49/100 = 49%.**

The latest reconciled repository base for this branch is `main@29a0099e899e03d80bf904c2d5ead72f40421fe8`, where canonical catalog coverage remains **48/100 = 48%** after Phase 2AT / PR #156 merged `apothic_spawners` 1.4.0 as component #48. The intervening PR #157 is Stage 05 keyboard-focus work and has zero catalog coverage delta; none of its changed files overlaps this Phase 2AU tranche.

Phase 2AU represents candidate component **#49**, `apothic_enchanting` 1.6.2. The numerator becomes canonical only after CI GREEN on the exact reconciled HEAD, a final latest-main gate, merge and post-merge `main` confirmation.

The detailed pre-Phase-2AU cumulative coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AU.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AU.md). Provider-specific evidence remains in `wiki/modpack-catalog/providers/**` and the corresponding phase checkpoint/capability files.

This metric measures current magic/cross-domain provider components closed to the strongest available evidence, not a guessed percentage of every spell/enchantment object. Partial current inventories receive zero closed-component points.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: 21.1.248
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

## Current working denominator

The operational denominator remains **100 magic/cross-domain component units** under the physical reconciliation already established by the catalog:

- 103 historical candidate IDs;
- 5 historically listed candidates now absent: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 current candidates added beyond the historical baseline: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100`.

The denominator must be reconciled again whenever the physical provider set changes.

## Canonical recent closure sequence

| Component | Phase / PR | Provider | Result |
|---:|---|---|---|
| 42 | Phase 2AN / PR #149 | `apothic_attributes` | canonical |
| 43 | Phase 2AO / PR #150 | `soul_fire_d` | canonical |
| 44 | Phase 2AP / PR #151 | `create_enchantment_industry_plus` | canonical; PR #153 later corrected metadata with zero coverage delta |
| 45 | Phase 2AQ / PR #152 | `apothic_compat` | canonical |
| 46 | Phase 2AR / PR #154 | `backportedspellbooks` | canonical |
| 47 | Phase 2AS / PR #155 | `apothic_compats` | canonical |
| 48 | Phase 2AT / PR #156 | `apothic_spawners` | canonical at merge SHA `3c9795820f48cbe01a28ed1d4c3f1238cce816a0` |
| 49 | Phase 2AU | `apothic_enchanting` | candidate in this revision |

Components #1–#41 remain part of the same canonical numerator and are preserved in the pre-2AU snapshot and provider/phase records.

## Phase 2AU — Apothic Enchanting component #49, candidate

Phase 2AU closes `apothic_enchanting` 1.6.2 at exact physical + exact publisher + exact official source evidence:

- physical artifact `ApothicEnchanting-1.21.1-1.6.2.jar`, SHA-1 `2623af251d3ddeae1d8e710afa76afe753834bab`;
- CurseForge project/file `1063926 / 8797650`, uploaded 2026-09-03;
- exact official source `Shadows-of-Fire/Apothic-Enchanting@00fbcf00a2f42701645daf8906e54f67ec65a5dc`, root tree `cad9b01b8d366e770cb811552884848afb320b30`;
- source metadata requires Minecraft 1.21.1+, NeoForge 21.1.187+, Placebo 9.9.0+ and Apothic Attributes 2.4.0+;
- no standalone spell/glyph/ritual registration surface and no provider mana/cast resource observed;
- Eterna/Quanta/Arcana table-stat authority plus synced `max_eterna`;
- exactly 20 provider enchantment keys;
- provider-native `EnchantableItem` / `EnchantmentStatBlock` extension surfaces and data-backed enchanting-stat registry;
- infusion recipe authority and `set_ench_hard_cap` IMC seam;
- persistent Raven-table stats;
- four PLAY payloads: three clientbound + one serverbound server-validated Raven-table control;
- exactly 17 common + 3 client mixins.

The Enchantability redesign is sourced to 1.6.1 by the exact changelog. Exact 1.6.2 source contains a comparison whose observed implementation is not silently reconciled with the changelog wording; physical runtime interpretation remains QA/fail-closed.

Apothic Enchanting owns enchanting semantics. Black Arcana retains canonical server-authoritative casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety. Provider `Arcana` is an enchanting statistic and must not be conflated with Black Arcana.

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
4. preserve source/publisher/JAR evidence layers when they differ;
5. merge only after latest-main reconciliation and CI GREEN on the reconciled HEAD;
6. increment the canonical numerator only after merge and post-merge main confirmation;
7. change the denominator whenever physical reconciliation changes the provider set.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.
