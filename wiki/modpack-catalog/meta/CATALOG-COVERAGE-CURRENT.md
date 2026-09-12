# Current Magic Catalog Coverage

## User-facing semantic magic coverage

The principal percentage reported to the user is the coverage of **semantic magic objects**: spells, glyphs/spell-parts, rituals/rites and equivalent discrete magical actions. Provider count, JAR count, technical proxies, items, gear, familiars, affixes and machines do not substitute for that denominator.

The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BE canonically closes a **strict counted minimum of 874 semantic magic objects** from provider records that meet the ledger's inclusion rule. The global denominator is still incomplete and no semantic percentage is declared.

The latest semantic promotion is **Cataclysm: Spellbooks +59**. Exact hash-matched 1.1.13 artifact evidence closes 59 unconditional provider spell registrations; ten additional root localization identities are not registered in the installed artifact and remain excluded. The generic/current 65-spell publisher scale is not substituted for the physical 1.1.13 registry. See [`../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Alshanex's Familiars +18**. Exact hash-matched 4.0.3 artifact evidence closes seven provider-owned spell registrations and eleven packaged custom `alshanex_familiars:ritual_recipe` identities. Sound/Melodic content remains counted only under Tunes n' Tomes, while familiar AI/passives and external Iron's spell casts remain excluded. See [`../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md).

The preceding semantic correction is **Werewolves +1**. Exact source pin `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b` proves that `LEAP` is an `ActionSkill`, that `SURVIVAL31` grants it, that the node is connected into the generated normal `werewolf_level` tree, and that the provider has a dedicated server-handled Leap input path. Hidden-selector presentation therefore does not make Leap unreachable. Werewolves contributes **8** counted semantic actions rather than 7; `hide_name` remains excluded as presentation-only and the separate `no_leap_cooldown` refinement remains an open modifier-acquisition question rather than a separate semantic action. See [`SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md`](./SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md).

Phase 2AY itself has a semantic delta of **0**: GTBC's SpellLib 2.2.0 is publisher-defined shared spell/addon library/API infrastructure and does not establish an independent standalone spell catalog. Its reusable spell/helper, imbuement, Curio, trade, particle, summon and attribute surfaces do not mint semantic spell identities by themselves.

Therefore:

- semantic numerator delta from Cataclysm: Spellbooks 1.1.13 exact closure: **+59**;
- semantic numerator delta from Alshanex's Familiars 4.0.3 exact closure: **+18**;
- semantic numerator delta from the preceding Werewolves correction: **+1**;
- semantic numerator/denominator delta attributable to GTBC's SpellLib: **+0**;
- strict reconstructible semantic minimum: **874**;
- the global semantic denominator remains incomplete because other providers still have open granular inventories;
- **do not derive a spell/magic percentage from the provider-component metric below**.

The preceding semantic-only promotion was **Malum +26**: whole-interval path history across the observed `1.8.2` source window plus stable endpoint blobs close 26 base-Malum `SpiritRiteType` identities. Release-bounded Codex evidence separately proves that the two special identities, `undirected_rite` and `unchained_rite`, are player-facing rather than sentinel/proxy slots: `TotemMagicEntries.setupEntries(ArcanaProgressionScreen)` adds each as a distinct progression entry backed by its corresponding `RiteHolder`, `SpiritRiteTextPage`, and `SpiritRiteRecipePage`, while every observed `CodexLangDatagen.java` snapshot in the 1.8.2 interval preserves dedicated entries for both. The same release-bounded audit also records 37 active `GeasEffectType` identities and 9 `SpiritArcanaType` resource identities, but those are excluded from the current semantic-action metric by definition. Exact installed-JAR/source equivalence and runtime/API/recipe mechanics remain separate gates. The preceding semantic-only promotion was **Hexalia +25**: 19 player-facing Nature's Ritual identities plus 6 Celestial Infusion identities release-bounded across the observed 1.3.5 metadata / 1.3.6 filename-source boundary. Neither semantic promotion changes the internal provider-component closure metric below.

The current Goety reconciliation remains an **evidence-only +0 delta**: the installed `goety-3.1.4.jar` is physical authority, while public `Vivideru/Goety-3` checkpoints for 3.1.0 and 3.1.1 expose a stable `ModItems.java` blob containing 123 active Focus item registrations. The prior official-Wiki inventory of 110 named base Focuses is retained as a documentary subset rather than a complete current registry. Exact 3.1.4 JAR↔source equivalence, player-facing reachability, semantic deduplication and runtime/API seams remain open, so none of the additional registry identities enter the strict **874** minimum at this checkpoint. The authoritative Goety capability interpretation is recorded in [`CAPABILITY-MATRIX-DELTA-GOETY.md`](./CAPABILITY-MATRIX-DELTA-GOETY.md).

The previous chat-only working tally is not an authority and is not used as an input to the versioned ledger.

## Phase 2BG promotion candidate — Leyline Spellbooks 1.0.3

The canonical baseline entering Phase 2BG remains **874 semantic objects / 55/100 components**. Exact hash-matched Leylines 1.0.3 evidence closes 14 unconditional registered spells and their current host eligibility. The durable Phase 2BG branch therefore proposes **+14 semantic objects**, Iron subtotal **541**, strict minimum **888**, and Leylines as candidate component **#56 / 56/100**.

This is a promotion candidate only until exact clean-HEAD CI, latest-main reconciliation, merge and exact post-merge CI succeed. Numerical balance, complete-modpack runtime QA and any Black Arcana adapter/API seam remain separate fail-closed gates.

## Internal provider-component closure metric

**Canonical provider-component coverage after Phase 2BE: 55/100 = 55%.**

Phase 2BF exact-artifact reconciliation closes Somake 1.0.8-fix registry identity at 67 current registrations under the physical optional-provider set, but the provider remains `CONDITIONAL` because the deployed COMMON spell-lock config and complete survival acquisition/reachability are not authoritative. Phase 2BF therefore changes neither metric: **874** strict semantic objects and **55/100** closed provider components.

Phase 2BF / PR #192 was audited at exact clean HEAD `85b15aec9faf395cef5460d06a17be58ccd16af8`, which passed Black Arcana CI **#2490**. It was squash-merged as `cc4cfc1d740f7714188e25a3586d8b43bb5eb969`; that exact merge SHA passed post-merge Black Arcana CI **#2491**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest, dedicated-server smoke and canonical QA-JAR publication.

Phase 2BE / PR #189 was audited at exact HEAD `e787699d25b283b8040cd179f605143e8ee396de`, which passed Black Arcana CI **#2483**. It was squash-merged to `main` as `cce7f51794e4e65b0d97511eb55f710afc6e02f0`. Black Arcana CI **#2484 attempt 1** ended before compilation/tests on a transient external read timeout fetching Iron's API from `code.redspace.io`; rerunning the same job on the unchanged merge SHA produced **#2484 attempt 2 GREEN**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

Phase 2BD / PR #186 was audited at exact HEAD `acfcff0fca09b3c2f7b4fcf082618a970e1d19c0`, which passed Black Arcana CI **#2464**. It was squash-merged to `main` as `95ec538ff1c34766450393522ce3affe1039d0dd`; that exact merge SHA passed post-merge Black Arcana CI **#2465**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

Phase 2AY / PR #175 merged to `main` as `9a4e1cd6a462a278083ab946b5ed054864c3315e` after exact audited HEAD `2260c46261ac9ab99d839f307fd7b4519d38eef2` passed Black Arcana CI **#2420**. The exact merge SHA then passed post-merge Black Arcana CI **#2421**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

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

GTBC's SpellLib and FamiliarsLib were already members of those 100 component units, so their closure changes the numerator only. The denominator must be reconciled whenever the physical provider set changes.

## Canonical recent closure sequence

| Component | Phase / PR | Provider | Result |
|---:|---|---|---|
| 47 | Phase 2AS / PR #155 | `apothic_compats` | canonical |
| 48 | Phase 2AT / PR #156 | `apothic_spawners` | canonical |
| 49 | Phase 2AU / PR #158 | `apothic_enchanting` | canonical |
| 50 | Phase 2AV / PR #160 | `apotheosis` | canonical |
| 51 | Phase 2AW / PR #161 | `apotheoticcreation` | canonical; historical immediate post-merge GameTest failure superseded by later full current-main GREEN validation |
| 52 | Phase 2AX / PR #166 | `familiarslib` | canonical at `main@4238275d2086a00c6f31960114733d74b8cdb1d8`; post-merge CI #2337 GREEN |
| 53 | Phase 2AY / PR #175 | `gtbcs_spell_lib` | canonical at `main@9a4e1cd6a462a278083ab946b5ed054864c3315e`; post-merge CI #2421 GREEN |
| 55 | Phase 2BE / PR #189 | `cataclysm_spellbooks` | canonical at `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0`; audited HEAD `e787699d25b283b8040cd179f605143e8ee396de` CI #2483 GREEN; post-merge CI #2484 attempt 2 GREEN |
| 54 | Phase 2BD / PR #186 | `alshanex_familiars` | canonical at `main@95ec538ff1c34766450393522ce3affe1039d0dd`; audited HEAD `acfcff0fca09b3c2f7b4fcf082618a970e1d19c0` CI #2464 GREEN; post-merge CI #2465 GREEN |

Components #1–#46 remain part of the same canonical numerator and are preserved by prior cumulative snapshots/provider records.

## Phase 2BE — Cataclysm: Spellbooks 1.1.13 component #55, canonical

Phase 2BE closes the physically installed spell identity inventory to exact artifact evidence:

- exact JAR `cataclysm_spellbooks-1.1.13-1.21.jar` / SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`;
- isolated non-merge PR #188 materialized exact File ID `8792628` and hash-matched the physical artifact;
- 59 `Supplier<AbstractSpell>` fields, 59 `registerSpell(...)` calls, 59 spell-class instantiations and 0 conditional branches in the exact registry initializer;
- exact group distribution: 7 Abyssal + 4 Ender + 1 Evocation + 5 Holy + 11 Fire + 5 Ice + 4 Nature + 22 Technomancy = **59**;
- ten additional root localization keys have no current registered spell identity and remain excluded;
- semantic delta: **+59**, yielding strict counted minimum **874** and Iron ecosystem subtotal **527**;
- the generic/current publisher scale of 65 spells is not substituted for the installed 1.1.13 registry;
- numerical mechanics, acquisition, runtime QA and future integration seams remain separate/fail-closed;
- clean-room audit retained only factual identity/registry/resource evidence and copied no upstream implementation or assets.

See [`PHASE2BE-CATACLYSM-SPELLBOOKS-1.1.13-EXACT-CHECKPOINT.md`](./PHASE2BE-CATACLYSM-SPELLBOOKS-1.1.13-EXACT-CHECKPOINT.md).

## Phase 2BD — Alshanex's Familiars 4.0.3 component #54

Phase 2BD closes the current provider identity inventory against the exact physical artifact:

- exact JAR `alshanex_familiars-1.21.1_v4.0.3.jar` / SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`;
- isolated Curse Maven download of exact File ID `8675568` hash-matched the physical artifact;
- 7 provider-owned spell registrations closed from exact registry/member/literal evidence;
- 11 packaged custom `alshanex_familiars:ritual_recipe` identities closed from exact structured resources;
- semantic delta: **+18**, strict counted minimum **815**;
- Sound/Melodic content remains owned/counted under Tunes n' Tomes and is not duplicated;
- runtime QA, numerical mechanics and future familiar adapter seams remain separately pending/fail-closed;
- clean-room audit retained only factual identity/registry/resource evidence and copied no upstream implementation or assets.

See [`PHASE2BD-ALSHANEX-4.0.3-EXACT-CHECKPOINT.md`](./PHASE2BD-ALSHANEX-4.0.3-EXACT-CHECKPOINT.md).

## Phase 2AY — GTBC's SpellLib 2.2.0 component #53, canonical

Phase 2AY closes the physically installed shared spell/addon library to the strongest current publisher evidence:

- physical artifact `gtbcs_spell_lib-2.2.0-1.21.1.jar`, mod id `gtbcs_spell_lib`, version `2.2.0`, physical SHA-1 `36cce8ab3117e89ae992a84a566d596709db2ffe`;
- exact CurseForge project/file `1194714 / 8824651` for the installed 2.2.0 line;
- publisher documentation defines SpellLib as reusable library/API infrastructure rather than standalone gameplay content;
- exact 2.2.0 release notes add Healing Received, Damage Taken and Summon Health attributes;
- reusable `AdvancedSpell`, imbuement, Curio, trade, particle and summon facilities are infrastructure consumed by addons and do not prove independent spell identities;
- semantic magic delta: **0**;
- no JAR decompilation or source copying was used; unsupported internal/API signatures remain fail-closed.

Iron's and consuming addons retain authority for their concrete spell/casting identities. Black Arcana retains authority for its own canonical casting, costs, targeting/effects, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and WorldEffectPolicy.

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

FamiliarsLib's source commit is release-correlated, not cryptographically tied to the installed binary: no matching release tag or reproducible-build proof was established. Do not call it an exact source-to-JAR pin. Its observed license surfaces disagree, so no reuse conclusion is inferred. GTBC's SpellLib is treated conservatively as publisher/physical factual evidence only. Clean-room policy remains read-only factual inspection: no provider code/assets/text are copied or adapted.

## Black Arcana integration disposition

FamiliarsLib remains authority for its own familiar attachment/lifecycle/networking framework. Iron's remains authority for the external spells referenced by FamiliarsLib tags and casting interoperability. GTBC's SpellLib remains authority for its library facilities. Black Arcana remains authority for its own canonical magic runtime.

Stage 07.07 Borrowed Sight must not accept FamiliarsLib entities by thematic inference or generic tameable detection. A future bridge requires a verified provider-native ownership seam behind a dedicated adapter, with server-side revalidation and fail-closed behavior. Phase 2AX does **not** add that adapter, and Phase 2AY adds no runtime integration.

## Partial providers still receive zero component points

Examples remain:

- `leylines` — current total inventory not verified;
- `somakespells` — current granular spell inventory remains incomplete;
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