# Phase 2AQ — Apothic Compat 2.0.2 checkpoint

## State

`AUDIT PREPARED / COVERAGE ORDINAL BLOCKED ON CONCURRENT PHASE 2AP`

This branch was created from canonical:

`main@068ca67e786d95255ccecb70433dd66d26a4b3e4`

At branch creation, that main already contained merged Phase 2AO / PR #150 and represented 43/100 coverage.

A concurrently created branch already reserves Phase 2AP for `create_enchantment_industry_plus` 1.1.1:

`docs/magic-catalog-phase2ap-create-enchantment-industry-plus-1.1.1`

At the last check it pointed exactly to the same main and contained no divergent commit yet. Because its eventual coverage result is unknown, Phase 2AQ must **not** pre-allocate component #44/#45 or a final numerator by assumption.

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
- MIT

Official source:

- repository `Nightwielder23/apothic-category-compat`
- branch line `1.21.1`
- exact source revision `cebf69a37f8c6573fc0c0295e627f4636e7bd026`
- commit message `ported to neoforge 1.21.1 with apotheosis 8.x data map architecture`
- exact metadata `mod_version=2.0.2`
- Minecraft 1.21.1
- NeoForge baseline 21.1.230
- Apotheosis baseline 8.5.4
- runtime dependency range Apotheosis `[8.5,9)`
- root source license MIT

## Exact inventory closed

- standalone spells: 0
- glyphs: 0
- rituals: 0
- provider mana/casting resource: 0
- mixins: 0
- Java classes: 4
- item loot-category overrides: 13
- target category IDs: 1 (`apotheosis:bow`)
- config keys: 1 (`affix_blacklist`)
- reload command roots/aliases: 2
- NeoForge runtime event hooks: 3

## Architecture conclusion

Apotheosis remains authority over loot-category and affix systems. Apothic Compat contributes data and a bounded blacklist/reload compatibility policy. None of this becomes a second Black Arcana spell/cast/proc runtime.

Black Arcana retains all canonical magic authority and must not reuse the provider's private reflection into `AffixRegistry.byType` as a generic integration seam.

## Static QA discrepancy

The exact provider reload path has an observable static edge case:

- after a non-empty blacklist has filtered the host `byType` pool,
- changing config to an empty blacklist and running only `/ac reload`
- calls `AffixBlacklist.apply()` with an empty set;
- the method returns before reconstructing the already-filtered pool.

A normal Apotheosis pool rebuild lifecycle restores the host map before the empty provider policy is reapplied. Runtime test on the physical stack remains required before claiming live unblacklist semantics.

## Remaining gates before PR/merge

1. re-fetch latest `main`;
2. reconcile the concurrent Phase 2AP outcome;
3. determine the correct component ordinal and canonical numerator from evidence, not reservation order;
4. update global coverage/queue/provenance only after that reconciliation;
5. compare branch against the reconciled latest main;
6. run Black Arcana CI on the exact reconciled HEAD;
7. repeat latest-main gate immediately before merge;
8. merge only if CI is GREEN and no authority/design conflict appeared;
9. confirm final `main` SHA and post-merge CI.

Until gate 2 resolves, this branch is useful audited preparation but is not a canonical component closure.
