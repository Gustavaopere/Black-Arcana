# Current Magic Catalog Coverage

## User-facing semantic magic coverage

The principal percentage reported to the user is the coverage of **semantic magic objects**: spells, glyphs/spell-parts, rituals/rites and equivalent discrete magical actions. Provider count, JAR count, technical proxies, items, gear, familiars, affixes and machines do not substitute for that denominator.

Phase 2AX has a semantic delta of **0**: FamiliarsLib 1.7.x provides familiar lifecycle/data/networking and spellcasting interoperability, but the audited release-correlated source tree does not register an independent spell catalog. Its Iron's spell files are classification tags over external spells, and the 1.7 publisher changelog explicitly moves historical Sound-school content to Tunes 'n Tomes.

Therefore:

- semantic numerator delta from Phase 2AX: **+0**;
- semantic denominator delta attributable to FamiliarsLib: **+0**;
- the global semantic denominator remains incomplete because other providers still have open granular inventories;
- **do not derive a spell/magic percentage from the provider-component metric below**.

The reconstructible semantic ledger now lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Against the physical 595-entry snapshot and reconstruction base `main@4f3dab1a4801393873f9d4b7857782fcf6298e56`, it currently closes a **strict counted minimum of 770 semantic magic objects** from provider records that meet the ledger's inclusion rule. The base passed Black Arcana CI **#2349**, attempt 2, on the exact SHA. This is not a final denominator and no percentage is declared: conditional registrations, current publisher lower bounds and providers with open exact inventories remain outside the strict sum.

The latest semantic-only delta is **Hexalia +25**: 19 player-facing Nature's Ritual identities plus 6 Celestial Infusion identities are release-bounded across the observed 1.3.5 metadata / 1.3.6 filename-source boundary. Hexalia mutations, Mortar & Pestle recipes, Small Cauldron/brews, Censer combinations, idols and equipment remain outside this semantic-object metric. This semantic promotion does **not** change the internal provider-component closure metric below.

The previous chat-only working tally is not an authority and is not used as an input to the versioned ledger.

## Internal provider-component closure metric

**Canonical provider-component coverage after Phase 2AX: 52/100 = 52%.**

Phase 2AX / PR #166 merged to `main` as `4238275d2086a00c6f31960114733d74b8cdb1d8` after final pre-merge HEAD `b5b36a6fa3b1a5bf3b2add56ec3c604592f5ca71` passed Black Arcana CI #2336. The exact merge SHA then passed post-merge Black Arcana CI #2337 / workflow run `34430446827`, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

The historical Phase 2AW nuance remains recorded: its immediate post-merge workflow #2308 failed at Foundation GameTest after unit tests, diff sanity, NeoForge build and JAR verification had passed, while later current-main validation #2334 completed the full gate successfully. This does not change the canonical #51 status of Apotheotic Creation.

The complete pre-Phase-2AX coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AX.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AX.md). Provider-specific evidence lives under `wiki/modpack-catalog/providers/**` plus the corresponding phase checkpoint/capability files.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: `21.1.248`
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

## Current working component denominator

The internal operational denominator remains **100 magic/cross-domain component units** under the established physical reconciliation:

- 103 historical candidate IDs;
- 5 historically listed candidates now absent: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 current candidates added beyond the historical baseline: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100`.

FamiliarsLib was already one of those 100 component units, so Phase 2AX changed the component numerator only. The denominator must be reconciled whenever the physical provider set changes.

## Canonical recent closure sequence

| Component | Phase / PR | Provider | Result |
|---:|---|---|---|
| 47 | Phase 2AS / PR #155 | `apothic_compats` | canonical |
| 48 | Phase 2AT / PR #156 | `apothic_spawners` | canonical |
| 49 | Phase 2AU / PR #158 | `apothic_enchanting` | canonical |
| 50 | Phase 2AV / PR #160 | `apotheosis` | canonical |
| 51 | Phase 2AW / PR #161 | `apotheoticcreation` | canonical; historical immediate post-merge GameTest failure superseded by later full current-main GREEN validation |
| 52 | Phase 2AX / PR #166 | `familiarslib` | canonical at `main@4238275d2086a00c6f31960114733d74b8cdb1d8`; post-merge CI #2337 GREEN |

Components #1–#46 remain part of the same canonical numerator and are preserved by prior cumulative snapshots/provider records.

## Phase 2AX — FamiliarsLib 1.7.1 component #52, canonical

Phase 2AX closes the installed familiar-framework library to the strongest currently available evidence:

- physical artifact `familiarslib-1.21.1-1.7.1.jar`, mod id `familiarslib`, runtime `1.21.1-1.7`, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`;
- CurseForge project/file `1316458 / 8059464`, release 2026-05-08 for NeoForge / Minecraft 1.21.1;
- official source repository `Alshanex/FamiliarsLib`;
- strongest release-correlated source commit `56561e7fd474fbd5c5166c1ac96f235faae156ab`, same date and same familiar-bed bug-fix intent as the 1.7.1 publisher changelog;
- correlated source tree `9d39b4751b9e52874f66cf2187afab239d00b251`, recursive `truncated=false`;
- source metadata declares Minecraft 1.21.1, NeoForge development baseline 21.1.90, Iron's `1.21.1-3.15.5`, Curios 9.2.2, mod version `1.21.1-1.7`;
- source owns serializable player-familiar attachment state and familiar lifecycle/storage/summon transport;
- `PayloadHandler` registers 17 optional payload handlers, split 9 play-to-server and 8 play-to-client;
- the tree contains spellcasting-familiar abstractions and Iron's spell classification tags, but no provider-owned spell registry or `data/familiarslib/spells/**` content;
- the 1.7 publisher changelog states that Sound-school content was removed and moved to Tunes 'n Tomes;
- consequently FamiliarsLib contributes **0 independent semantic spell/magic objects** to the user-facing metric.

## Exactness and license boundary

The source commit is release-correlated, not cryptographically tied to the installed binary: no matching release tag or reproducible-build proof was established. Do not call it an exact source-to-JAR pin.

License surfaces also disagree: the release-correlated source property says `All Rights Reserved`, the current CurseForge project/file surface reports GPLv3, and the current Modrinth project surface reports MIT. This audit does not resolve that conflict into a reuse permission. Clean-room policy remains conservative: factual read-only inspection only; no provider code/assets/text are copied or adapted.

## Black Arcana integration disposition

FamiliarsLib remains authority for its own familiar attachment/lifecycle/networking framework. Iron's remains authority for the external spells referenced by FamiliarsLib tags and casting interoperability. Black Arcana remains authority for its own canonical magic runtime.

Stage 07.07 Borrowed Sight must not accept FamiliarsLib entities by thematic inference or generic tameable detection. A future bridge requires a verified provider-native ownership seam behind a dedicated adapter, with server-side revalidation and fail-closed behavior. Phase 2AX does **not** add that adapter.

## Partial providers still receive zero component points

Examples remain:

- `leylines` — current total inventory not verified;
- `somakespells` — current granular spell inventory remains incomplete;
- `cataclysm_spellbooks` — installed 1.1.13 remains ahead of the exact public source baseline already audited;
- `gaze` — exact current registry/source-JAR closure remains pending.

These partials are also reasons the global semantic spell/magic denominator remains open. Their current lower-bound/open evidence is tracked explicitly in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md) rather than being silently added to the strict semantic count.

## Update rule

After each provider closure:

1. re-read physical modlist and current `main`;
2. reconcile concurrent PR/branch ownership;
3. close the provider to the strongest exact evidence available;
4. preserve physical/publisher/source/license evidence layers when they differ;
5. keep semantic magic-object coverage separate from provider-component closure;
6. merge only after latest-main reconciliation and CI GREEN on the exact reconciled HEAD;
7. increment the canonical component numerator only after merge and post-merge main confirmation;
8. change either denominator only when evidence for that metric changes.

Phase 3 remains blocked until provider catalog/deduplication establishes real Black Arcana gaps and the semantic magic denominator is reconstructible.