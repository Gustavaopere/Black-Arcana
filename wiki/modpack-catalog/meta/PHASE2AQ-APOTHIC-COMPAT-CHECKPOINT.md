# Phase 2AQ — Apothic Compat 2.0.2 checkpoint

## State

`CATALOG CLOSURE CANDIDATE / EXACT PHYSICAL+PUBLISHER+OFFICIAL SOURCE VERSION / APOTHEOSIS DATA-MAP+AFFIX-BLACKLIST COMPAT / COMPONENT #45 CANDIDATE / NOT CANONICAL UNTIL EXACT-HEAD CI GREEN + LATEST-MAIN GATE + MERGE`

## Reconciled base

Initial preparation began from:

`main@068ca67e786d95255ccecb70433dd66d26a4b3e4`

Phase 2AP subsequently closed `create_enchantment_industry_plus` as component #44 and merged through PR #151. The canonical base is now:

`main@70a97ec0cf58cecebe4054f43ea5b212e757e365`

The pre-existing Phase 2AQ work was reconciled with that main by a true two-parent merge commit:

`404d6b2646da578de30e9e288e6e493ac4bb8c03`

After reconciliation the branch is 0 commits behind canonical main. Canonical coverage is **44/100 = 44%**; this component proposes **45/100 = 45%** only after final validation and merge.

Branch:

`docs/magic-catalog-phase2aq-apothic-compat-2.0.2`

## Physical anchor

- Minecraft 1.21.1
- NeoForge 21.1.248
- 595 top-level entries
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- `apothic_compat-2.0.2.jar`
- mod id `apothic_compat`
- physical SHA-1 `868506b8367be2c155acde0ef186b5a3e6ba8db9`

Physical host stack:

- Apotheosis 8.8.0
- Placebo 9.9.2
- Apothic Attributes 2.10.1

## Exact provider evidence

Publisher:

- CurseForge project/file `1516278 / 8219980`
- exact NeoForge 1.21.1 release 2.0.2
- release date 2026-06-09
- MIT

Official source:

- repository `Nightwielder23/apothic-category-compat`
- exact release tag `v2.0.2-neoforge-1.21.1`
- exact source revision `cebf69a37f8c6573fc0c0295e627f4636e7bd026`
- commit message `ported to neoforge 1.21.1 with apotheosis 8.x data map architecture`
- exact metadata `mod_version=2.0.2`
- Minecraft 1.21.1
- NeoForge baseline 21.1.230
- Apotheosis baseline 8.5.4
- runtime dependency range Apotheosis `[8.5,9)`
- root source license MIT

The exact GitHub release asset is `apothic_compat-2.0.2.jar` with published SHA-256 `eaee4ee2be65b95fe10ee749dc2d023b90fb63338825f5ba0b697124f42295de`. This independently supports release identity but is not used to claim byte-for-byte equivalence with the physical pack artifact without comparing the physical bytes.

## Exact inventory closed

- standalone spells: **0**
- glyphs: **0**
- rituals: **0**
- provider mana/casting resource: **0**
- mixins: **0**
- Java classes: **4**
- item loot-category overrides: **13**
- target category IDs: **1** (`apotheosis:bow`)
- config keys: **1** (`affix_blacklist`)
- reload command roots/aliases: **2** (`/apothiccompat`, `/ac`)
- NeoForge runtime event hooks: **3**
- provider packet/persistence surface observed: **0**

The 13 data-map entries are compatibility data, not spells. All exact entries target `apotheosis:bow`.

## Architecture conclusion

Apotheosis remains authority over loot-category semantics, affix identities/registry/pools, affix rolling and synchronization. Apothic Compat contributes exactly its data-map values plus a bounded blacklist/reload compatibility policy. None of this becomes a second Black Arcana spell/cast/proc runtime.

Black Arcana retains casting, transactional costs, targeting, BA cooldowns/charges, spell/hazard effects, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`. RPG Skill Tree remains progression/Mastery/perk authority only through real contracts.

Black Arcana must not reuse the provider's private reflection into `AffixRegistry.byType` as a generic integration seam.

## Exact command correction against editorial docs

The exact installed-version source is authoritative for command identities:

- `/apothiccompat reload`
- `/ac reload`

Both require permission level 2. Later/editorial references to `/apothiccategorycompat` or `/acc` belong to renamed/newer lines and must not be projected onto physical 2.0.2.

## Static QA discrepancy

The exact provider reload path has an observable static edge case:

- after a non-empty blacklist has filtered the host `byType` pool,
- changing config to an empty blacklist and running only `/ac reload`
- calls `AffixBlacklist.apply()` with an empty set;
- the method returns before reconstructing the already-filtered pool.

A normal Apotheosis pool rebuild lifecycle restores the host map before the empty provider policy is reapplied. Runtime test on the physical stack remains required before claiming live unblacklist semantics.

## Remaining fail-closed boundaries

- byte-for-byte exact source/release asset ↔ physical JAR reproducibility;
- private reflection parity against physical Apotheosis 8.8.0;
- runtime presence/registry-ID parity for every one of the 13 target items, especially Continued ports;
- full-modpack data-map priority and affix behavior;
- live non-empty→empty blacklist reload regression;
- any future 2.1.0 behavior, renamed command or extra category route not present in exact 2.0.2 evidence.

## Merge gate

Before component #45 becomes canonical:

1. update global coverage/queue/provenance from the reconciled base;
2. review the complete branch diff against latest main;
3. run Black Arcana CI on the exact branch/PR HEAD;
4. re-fetch latest `main` immediately before merge;
5. if `main` advanced, reconcile semantically and rerun CI on the new exact HEAD;
6. merge only with expected exact HEAD;
7. confirm PR merged state and final `main` SHA;
8. verify final main represents **45/100 = 45%**.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.
