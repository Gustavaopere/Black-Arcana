# Provider Audit Queue — Phase 2J delta

Data: `2026-09-07`; Malum and base-Goety effective rows reconciled `2026-09-10`.

This file is a narrow status overlay over `PROVIDER-AUDIT-QUEUE.md`. It prevails only for the rows named below until the next integral regeneration of the 103-provider queue. It does not supersede `PROVIDER-AUDIT-QUEUE-DELTA-GOETY-ADDONS.md` for Goety Cataclysm/Goety Iron.

## Current rows

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `malum` | `malum-1.21.1-1.8.2.jar` / `1.8.2` | `RELEASE-BOUNDED CORE REGISTRY INVENTORIES CLOSED / SPIRIT RITES 26/26 PLAYER-FACING SEMANTIC IDENTITIES / GEAS EFFECT TYPES 37/37 NON-ADDITIVE / SPIRIT TYPES 9/9 NON-ADDITIVE / WHOLE-INTERVAL PATH HISTORY + SPECIAL-RITE CODEX REACHABILITY VERIFIED / SOURCE↔JAR EQUIVALENCE + RECIPES + RUNTIME/API/RESOURCE QA PENDING / LGPLv3↔ARR PROVENANCE CONFLICT BLOCKS SOURCE-DERIVED IMPLEMENTATION / FAIL-CLOSED` |
| `goety` | `goety-3.1.4.jar` / runtime `3.1.4` / SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7` | `OPEN CURRENT REGISTRY / PUBLIC 1.21.1 SOURCE LINE VERIFIED THROUGH 3.1.1 / MODITEMS BLOB db3c63b3 STABLE ACROSS AUDITED 3.1.0→3.1.1 CHECKPOINTS / 123 ACTIVE FOCUS ITEM REGISTRATIONS FACTUALLY CLOSED FOR THAT PUBLIC SOURCE INTERVAL / LEGACY WIKI 110 IS INCOMPLETE / EXACT 3.1.4 JAR-SOURCE + SEMANTIC REACHABILITY/DEDUP + RITUAL IDENTITIES + RUNTIME/API QA PENDING / FAIL-CLOSED` |
| `hexalia` | `hexalia-neoforge-1.3.6.jar` / runtime metadata `1.3.5` | `PUBLIC RELEASE+SOURCE PIN 1.3.6 / MIT / BREWS 8/8 / NATURE'S RITUAL 19/19 PLAYER-FACING / CELESTIAL INFUSION 6/6 / MUTATION 21/21 / MORTAR 12/12 / CENSER 10/10 / IDOLS+MAJOR CAPABILITY OUTPUTS AUDITED / INSTALLED FILENAME↔RUNTIME VERSION MISMATCH + API/RUNTIME QA PENDING` |
| `toxony` | `toxony-0.10.7.jar` / runtime `0.10.7` | `EXACT INSTALLED ARTIFACT + EXACT PUBLIC 0.10.7 SOURCE VERSION PIN 881bf7fe / EFFECTS 5/5 / OILS 9/9 / MUTAGEN EFFECTS 7/7 / AFFINITIES 11/11 / THRESHOLD MODEL + IRON'S/VAMPIRISM/WEREWOLVES COMPAT FACTUALLY AUDITED / GPLv3↔LGPLv3 LICENSE CONFLICT / RUNTIME+SUPPORTED-API QA PENDING / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED` |

## Goety interpretation — reconciled 2026-09-10

The old base-Goety catalog state treated the official Wiki list of 110 Focuses as the strongest current inventory and stated that no official/public 1.21.1 source line was available. That is stale.

The strongest safe current claims are:

- physical authority remains `goety-3.1.4.jar` / runtime `3.1.4`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`;
- public `Vivideru/Goety-3` is the 1.21.1+ source line;
- audited checkpoint `4230e3bce2842779a6667ae6e5bfef8f53a27541` declares Goety `3.1.0` and checkpoint `6c41a04f2d712097c4461f969a6bb8ee277149ef` declares `3.1.1`;
- no public source/tag matching distributed `3.1.2` or installed `3.1.4` has been established;
- `src/main/java/com/Polarice3/Goety/common/items/ModItems.java` has blob `db3c63b366803e2d46aa4a996b5bb0f358437a7f` at both audited endpoints;
- that registry contains **123 active Focus item registrations**: 26 Magic + 11 Necromancy + 11 Geomancy + 9 Frost + 12 Wild + 9 Wind + 11 Storm + 9 Abyss + 11 Nether + 14 Void;
- the legacy 110-name Wiki list omits 13 source-registered Focus IDs and is therefore a documentary subset, not a complete current-source registry;
- item registry membership is not automatically equivalent to a player-facing semantic action count;
- exact 3.1.4 JAR/source equivalence, reachability, object-level deduplication and discrete ritual identities remain unresolved;
- Goety contributes **+0** at this reconciliation checkpoint and the strict semantic minimum remains **796**;
- Goety remains authority for Soul Energy, Focus casting, rituals, servants and its own lifecycle/settlement semantics.

### Provenance boundary

`Vivideru/Goety-3/LICENSE.txt` is mixed-license: original `src/main/java/com/Polarice3/` code is stated as MIT, while `src/main/java/com/Vivideru/` additions are All Rights Reserved unless specifically stated otherwise. The audited `ModItems.java` is in the `com/Polarice3` scope.

The source is consulted read-only for factual identifiers/counts/blob/version provenance. No upstream implementation/assets/text are copied or adapted, the whole tree is not represented as MIT, and no source-derived 3.1.4 runtime/API contract is promoted.

Goety is therefore **open with a current public registry baseline**, not `LOWER_BOUND` based on the legacy Wiki and not `SOURCE-PINNED 3.1.4`.

## Malum interpretation — reconciled 2026-09-10

The full queue still describes Malum as a generic base provider with catalog pending. This overlay is authoritative for the Malum row until integral queue regeneration, and the old Phase 2I/2J interpretation is superseded by the release-bounded semantic audit.

The strongest safe current claims are:

- installed physical identity remains `malum-1.21.1-1.8.2.jar` / runtime `1.8.2`;
- the official `1.21.1` source history bounds the observed `1.8.2` interval from `f56691e56e591a6d8d1859ff119e749375e14d61` through `03b743a37f3eeb0cc7f4364f0730e1f135f78408`;
- whole-interval path history plus stable endpoint blobs closes **26 active base `SpiritRiteType` registrations**, **37 active `GeasEffectType` registrations**, and **9 `SpiritArcanaType` registrations** for factual release-bounded accounting;
- `TotemMagicEntries.java` plus all observed `CodexLangDatagen.java` snapshots in that interval independently establish that `undirected_rite` and `unchained_rite` are player-facing rite entries rather than sentinel/proxy slots;
- only the **26 Spirit Rites** are additive under the current semantic-magic metric; Geas effect types and Spirit resource/type identities remain non-additive by definition;
- the strict reconstructible semantic minimum therefore includes Malum **+26**, producing the current **796** total recorded in `SEMANTIC-MAGIC-COVERAGE.md`;
- exact installed-JAR/source byte equivalence remains unproven;
- exact recipes/inputs, numerical requirements, Rite Locus runtime lifecycle/budgets, resource query/consume/refund seams, reaping causality and safe public API/event hooks remain separate QA/integration gates;
- the LGPLv3↔`All Rights Reserved` source-license conflict remains unresolved, so source-derived implementation/API specification and provider-resource mutation contracts remain blocked/fail-closed.

Malum is therefore **closed for the narrow release-bounded semantic Rite inventory**, but it is **not provider-wide runtime/API/resource granular-complete** and receives no new implementation authority from this catalog result.

## Hexalia interpretation

The full queue row `GUIA+WEB LIDOS / RITUAIS-BREWS CATÁLOGO PENDENTE` is stale.

Merged Phase 2I work source-pinned the public 1.3.6 release and closed the major finite semantic inventories listed above. The remaining blocker is not “catalog absent”; it is exact installed-runtime/API validation because the physical filename says 1.3.6 while installed runtime metadata reports 1.3.5, plus the provider-specific behavior QA already recorded in the Hexalia catalog.

## Toxony interpretation

Phase 2J pins the exact public source version checkpoint:

`MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f`

Factual source coverage now proves:

- 5 harmful effects;
- 9 Oils;
- 7 Mutagen effect IDs;
- 11 Affinities;
- player Tolerance `10..999`, default `30`;
- practical threshold crossings `tox > 100`, `>300`, `>600`;
- max three stored Mutagen entries with duplicate stacking behavior;
- six player Affinity-selected Mutagen candidates plus separate `mob_mutagen` transformation;
- five Iron's School Spell Power mappings at stage 1+;
- source-observed silver compatibility against Vampirism/Werewolves tags;
- source-visible ChangeTox/ChangeTolerance/ChangeThreshold events as candidate, not approved, adapter seams.

A material catalog correction is recorded: exact 0.10.7 executable source uses a **200-tick (10-second)** Necrotic resurrection cooldown; `48000` is commented and must not be presented as active runtime behavior.

### Provenance blocker

At the same exact Toxony commit:

- `gradle.properties` and public distribution metadata declare LGPLv3;
- root `LICENSE` contains GPLv3 text.

Therefore source observations are factual catalog evidence only. Black Arcana does not derive implementation from those internals while the conflict remains unresolved.

## Phase 3 consequence

None of these rows becomes an automatic Phase 3 implementation approval.

- Goety: public current-line registry evidence is stronger than the stale Wiki inventory, but exact 3.1.4 source/JAR, semantic reachability/deduplication, ritual identities and supported runtime/API seams remain fail-closed;
- Malum: narrow semantic Rite inventory is closed, but source↔JAR equivalence, recipes, supported API/resource seams and runtime QA remain separate fail-closed gates;
- Hexalia: installed-runtime/API gates remain;
- Toxony: license/API/runtime gates remain.

Provider-native authority and fail-closed integration remain mandatory.

## Historical next-provider note

At the original Phase 2J checkpoint, the next grouped provider was Mobstein `5.4.4`; that historical pointer has since been completed and is not the current operational next-work queue. Current semantic-denominator closure order is maintained in `SEMANTIC-MAGIC-COVERAGE.md` and current operational project state in `plans/STATUS.md`.
