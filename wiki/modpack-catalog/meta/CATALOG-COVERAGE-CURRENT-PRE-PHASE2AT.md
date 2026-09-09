# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AS revision: 47/100 = 47%.**

The latest canonical base for this branch is `main@ac4df420158616d2fb993fb5fbf6b8325c207c27`, where canonical coverage is **46/100 = 46%** after Phase 2AR / PR #154 merged Backported Spellbooks as component #46.

Phase 2AS represents candidate component **#47**, `apothic_compats` 0.2.4.2. The numerator becomes canonical only after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge, and post-merge `main` confirmation.

The detailed pre-Phase-2AS cumulative coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AS.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AS.md). Provider-specific evidence remains in `wiki/modpack-catalog/providers/**` and the corresponding phase checkpoint/capability files.

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

The cumulative numerator through component #46 is canonical on `main@ac4df420158616d2fb993fb5fbf6b8325c207c27`.

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

Earlier components #1–#34 remain part of the same canonical numerator and are not renumbered by this normalization. Their detailed history remains in the preserved catalog snapshots and provider/phase documents.

## Phase 2AR — Backported Spellbooks component #46, canonical

Phase 2AR / PR #154 closed `backportedspellbooks` at the layered physical/publisher/release-day-source evidence ceiling and is canonical at merge SHA `ac4df420158616d2fb993fb5fbf6b8325c207c27`.

Key closed facts retained:

- physical artifact `backportedspellbooks-0.1.2.jar`, SHA-1 `747847c1f38c73250ebac05ea06b41a381187850`;
- physical/runtime metadata version `0.1.0`, intentionally preserved separately from publisher filename/release label `0.1.2`;
- exact publisher file `1543731 / 8158731`, released 2026-05-28 for NeoForge 1.21.1;
- release-day source `RedReaper28/BackportedSpellbooks-1.21.1@07cb65efca0c264762a21c2d6bce0f83e3947226`;
- exactly 6 provider spells: `slime_aspect`, `sulfur_bomb`, `sulfur_clouds`, `sulfur_release`, `pale_thorn`, `resin_spray`;
- one Pale Flora school/sub-school surface;
- provider content/worldgen/equipment proc boundaries closed at the source ceiling;
- no provider custom payload, SavedData/attachment/data-component persistence subsystem or mixin config observed in that release-day source tree;
- source/JAR byte equivalence and full-pack runtime QA remain fail-closed.

Iron's remains host casting/mana/cooldown authority. Backported Spellbooks owns its six addon spell identities and supporting content/procs. Black Arcana does not clone them or duplicate their provider settlement/proc/worldgen paths.

## Phase 2AS — Apothic Compats component #47, candidate

Phase 2AS closes `apothic_compats` 0.2.4.2 at an exact physical + exact official source evidence ceiling:

- physical artifact `apothic_compats-0.2.4.2.jar`, SHA-1 `46d3699a4af63531fe84c69fdd2623fbe71fbc75`;
- exact official source `ianm1647/apothic-compats@0b9c900344dc536e4748e3ad0f3f18e03f2c3ba4`, root tree `76e2e650732584a315b3faa3ab94ff8953e6caad`;
- exact source metadata declares version 0.2.4.2, Minecraft 1.21.1, NeoForge development baseline 21.1.242 and MIT metadata;
- source development Apotheosis baseline is 8.6.0 while the physical pack uses Apotheosis 8.8.0; live compatibility remains QA/fail-closed;
- **0 standalone spells, 0 glyphs, 0 rituals, 0 provider-owned mana/cast resource, 0 provider cast controller and 0 provider packet/payload surface observed** in the complete exact Java/resource source tree;
- exactly 3 required mixins, all adapting Amendments/Supplementaries blocks to Apothic Enchanting Arcana/Quanta statistics;
- one Ars Nouveau Apotheosis gem `apothic_compats:ars_nouveau/mana`, Ars-targeted affixes, 14 Ars affix-loot entries, 3 Ars gear sets and 3 regular Wilden invaders;
- 3 Malum-targeted provider gems and Malum/Lodestone/Apothic affix/gem-bonus integration;
- exactly 4 conditional custom Malum affix codecs: scythe/staff Cleaving and Thunderstruck;
- Cleaving can issue additional normal attacks; Thunderstruck can apply nearby lightning-tagged bypass-armor damage;
- server-side projectile join hook scales projectile velocity by Apothic `ARROW_VELOCITY`, guarded by persistent-data marker `apothic_compats.proj.done`;
- source-defined AE2/Ancient Reforging paths are not promoted to active-pack behavior because those exact mod IDs are absent from the current physical inventory.

Apotheosis/Apothic owns affix/gem/loot/category/invader semantics; Ars Nouveau and Malum/Lodestone retain their native magic/resource/effect authority; Apothic Enchanting owns its Arcana/Quanta stats. Apothic Compats owns only its compatibility definitions and exact observed glue. Black Arcana retains canonical casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.

In particular, BA must not reinterpret the Ars gem as a second mana system, duplicate the projectile velocity pass, map Apothic Enchanting `Arcana` to BA `Arcane Danger`, or turn provider Cleaving/Thunderstruck effects into a second BA offensive proc chain.

Component #47 becomes canonical only after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge and post-merge `main` confirmation.

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
