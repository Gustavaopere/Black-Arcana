# Current Magic Catalog Coverage

## User-facing semantic magic coverage

The principal percentage reported to the user is the coverage of **semantic magic objects**: spells, glyphs/spell-parts, rituals/rites and equivalent discrete magical actions. Provider count, JAR count, technical proxies, items, gear, familiars, affixes and machines do not substitute for that denominator.

The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BL raises the strict counted minimum to **1316 semantic magic objects** by closing exact Goety Iron 3.1 (+14) and Goety Cataclysm 1.21.1-1.8.2 (+52). Phase 2BM and Phase 2BN add +0 through Ars Polymorphia and Ars Sable. Phase 2BO then closes Farmer's Spell 'n Spellbooks 1.0.5.1 at **+6 `COUNTED_SOURCE_PINNED`**, so the current strict minimum becomes **1322**. The global denominator remains incomplete and no semantic percentage is declared.

Phase 2BO closes exactly six unconditional provider-owned Gluttony spell registrations from exact public source pin `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`, reconciled to physical `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` / SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff`. Host-native Scroll Forge reachability is catalog-closed through the provider Gluttony focus path; generic random scroll loot is not claimed because `allowLooting=false`. This raises the Iron's ecosystem subtotal from **542 to 548** and closes provider component **#63** while keeping current-host runtime compatibility fail-closed. See [`../providers/farmers-spell/README.md`](../providers/farmers-spell/README.md) and [`PHASE2BO-FARMERS-SPELL-CHECKPOINT.md`](./PHASE2BO-FARMERS-SPELL-CHECKPOINT.md).

Phase 2BN has a semantic delta of **0**: exact official source pin `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` closes the provider's role as a narrow Ars Nouveau ↔ Sable spatial/sublevel compatibility layer. The exact source has 24 common + 5 client required mixins, protocol registrar version `2`, zero provider-owned payload registrations, and no provider-owned spell/glyph/ritual/school/resource/action registry. This closes provider component **#62** while keeping current-host runtime compatibility fail-closed.

Phase 2BM has a semantic delta of **0**: exact official source pin `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` closes the provider's role as an Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict bridge, without a provider-owned spell, glyph, ritual, school, mana/resource or equivalent magical-action registry. This closes provider component **#61** while keeping current-host runtime compatibility fail-closed.

Phase 2BK has a semantic delta of **0**: exact hash-matched Ignis Soulfires: Spellbooks 1.1.0 contains only its armor-material/item bridge surfaces and no provider-owned spell, ritual, rite or equivalent action registry. This closes provider component **#58** without changing the semantic numerator.

The latest semantic promotion before the Goety addon tranche was **Gaze +1**. Exact hash-matched 1.1.7.1 artifact evidence closes one Gaze-owned Iron's standalone spell, Soulward Shield. Its 26 Spirit Rites remain config-conditional because deployed `disableGazeRites` is unavailable.

Other preceding promotions remain canonical and historical at their recorded checkpoints: Goety +361, Leyline Spellbooks +14, Cataclysm: Spellbooks +59, Alshanex's Familiars +18, Werewolves Leap +1, Hexalia +25 and Malum +26.

Therefore:

- semantic numerator delta from Farmer's Spell 'n Spellbooks 1.0.5.1: **+6 `COUNTED_SOURCE_PINNED`**;
- semantic numerator/denominator delta attributable to Ars Sable 1.1.2: **+0**;
- semantic numerator/denominator delta attributable to Ars Polymorphia 1.0.3: **+0**;
- semantic numerator/denominator delta attributable to Ignis Soulfires: Spellbooks 1.1.0: **+0**;
- semantic numerator delta from Gaze 1.1.7.1 exact closure: **+1**;
- semantic numerator delta from Goety 3.1.4 exact closure: **+361**;
- semantic numerator delta from Leyline Spellbooks 1.0.3 exact closure: **+14**;
- semantic numerator delta from Cataclysm: Spellbooks 1.1.13 exact closure: **+59**;
- semantic numerator delta from Alshanex's Familiars 4.0.3 exact closure: **+18**;
- semantic numerator delta from the Werewolves correction: **+1**;
- semantic numerator/denominator delta attributable to GTBC's SpellLib: **+0**;
- semantic numerator delta from Goety Iron 3.1 exact closure: **+14**;
- semantic numerator delta from Goety Cataclysm 1.21.1-1.8.2 exact closure: **+52**;
- strict reconstructible semantic minimum: **1322**;
- the global semantic denominator remains incomplete because other providers still have open granular inventories;
- **do not derive a spell/magic percentage from the provider-component metric below**.

The previous chat-only working tally is not an authority and is not used as an input to the versioned ledger.

## Phase 2BO — Farmer's Spell 'n Spellbooks 1.0.5.1 component #63, source-pinned +6 closure

Physical identity is `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar`, mod id/version `farmers_spell / 1.0.5.1-1.21.1`, SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff`, CurseForge hash `810347191`. Exact public source is `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`.

The source-pinned registry closes exactly six unconditional Gluttony spells: `goodberry`, `phantom_loot`, `seal_coat`, `bad_apple`, `chaos_slash`, `preserve_circle`. The school is support taxonomy rather than a seventh semantic object. Provider data supplies the Gluttony focus route and Iron's 3.16.3 source-line Scroll Forge contract corroborates host-native catalog reachability; generic random scroll loot is deliberately excluded because the school sets `allowLooting=false`.

PR #214 corrected HEAD `d3a92c31d7ac5b38183224ef28c6737e721fc758` passed Black Arcana CI #2564 / run `34723967662`. Squash merge `34a5fd495da744800b32b051e38c6473c6f5ea15` passed exact-SHA post-merge CI #2565 / run `34724351805` and published artifact `10307207453` with digest `sha256:50b94c3efc207dfd143a10367cf234473ede7dbbc1f36b9acdd3d3ca1ccc67fa`.

This promotion yields **1322 semantic objects / 63 of 100 components**. Current-host runtime remains fail-closed: source targets NeoForge 21.1.238 and Farmer's Delight 1.3.2 while the physical pack uses NeoForge 21.1.248 and Farmer's Delight 1.3.4; seven direct mixins are required. GeckoLib is 4.9.2 on both sides by version label, which is not a runtime PASS. No provider-owned payload registrations are observed at the exact source pin.

## Phase 2BN — Ars Sable 1.1.2 component #62, source-pinned zero closure

Exact official source `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` matches the installed provider version 1.1.2 and closes its technical role as a compatibility/spatial layer between Ars Nouveau and Sable. The exact source exposes 24 common + 5 client required mixins, protocol registrar version `2`, zero provider-owned payload registrations, and no provider-owned spell/glyph/ritual/school/resource/action registry. The semantic delta is therefore **+0** and the strict minimum remains **1316** at that historical checkpoint.

PR #212 exact HEAD `c4facc0286da...` passed Black Arcana CI #2553 / run `34720437808`; squash merge `c1c422b5ec72fe4308104f04282732d6c2f2bbc1` passed exact-SHA post-merge CI #2554 / run `34720646567` and published canonical QA artifact `10306246238` (`sha256:a63f42f6746cc62e435e6a1c541daaed973b0b56d3dcc566cbc7cf4e9fa57e96`). Provider component **#62** is closed. Runtime compatibility remains fail-closed.

## Phase 2BM — Ars Polymorphia 1.0.3 component #61, source-pinned zero closure

Exact official source `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` matches the installed provider version 1.0.3 and closes its technical role as a recipe-conflict bridge for Ars Storage/Crafting Lecterns. The exact source exposes five required mixin/accessor bindings, protocol version `1`, and one provider-owned play-to-server unit payload, while establishing no provider-owned spell/glyph/ritual/school/resource/action registry. The semantic delta is therefore **+0**.

PR #210 exact HEAD `1b8d5d5761569f8ef1f3a32b7ece84cfb6ce6df6` passed Black Arcana CI #2543; squash merge `f2cdfe7b79d500540c281d70a76e8b6e3a77d311` passed exact-SHA post-merge CI #2544 / run `34713268914` and published canonical QA artifact `10303624842` (`sha256:f4ff7ce2fac582f435f037f3a8dd29469df25d8889b895b0c168c2b0d6da0719`). Runtime compatibility remains fail-closed.

## Phase 2BL — Goety addon exact closures, components #59 and #60

Exact hash-matched evidence closes **Goety Iron +14** (2 Focus + 12 non-Focus rituals) and **Goety Cataclysm +52** (28 Focus + 24 non-Focus rituals). Acquisition recipes are deduplicated against Focus identities; counted non-Focus rituals have distinct outcomes and no mod-loaded conditions. Phase 2BL moves the strict semantic minimum to **1316** and the separate provider-component metric to **60/100** at that checkpoint.

## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 component #58, exact zero closure

Exact hash-matched artifact evidence closes the provider as `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`: 11 provider classes, one armor-material registry, one five-item equipment registry, and no provider-owned spell/ritual/action registry. Semantic disposition is `ZERO_BRIDGE_INFRA` with **+0**. Evidence: NON-MERGE PR #203 run `34688273425`, artifact `10296406134`.

## Phase 2BJ — Gaze 1.1.7.1 semantic-only exact promotion

Exact hash-matched artifact evidence closes **+1** current semantic object: Gaze-owned Iron's spell Soulward Shield. Gaze's 26 exact player-facing Spirit Rites remain configuration-conditional because deployed COMMON `disableGazeRites` is unavailable. Gaze remains an open provider component.

## Phase 2BH — Goety 3.1.4 component #57, canonical

Exact 3.1.4 artifact identity closes **+361** and component #57. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524.

## Phase 2BG — Leyline Spellbooks 1.0.3 component #56, canonical

Exact hash-matched Leylines 1.0.3 evidence closes 14 unconditional registered spells and provider component #56. Durable PR #195 clean HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed CI #2503; squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI #2504.

## Internal provider-component closure metric

**Canonical provider-component coverage after Phase 2BO: 63/100 = 63%.**

The internal operational denominator remains **100 magic/cross-domain component units** under the established physical reconciliation. The denominator must be reconciled whenever the physical provider set changes.

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
| 54 | Phase 2BD / PR #186 | `alshanex_familiars` | canonical at `main@95ec538ff1c34766450393522ce3affe1039d0dd`; post-merge CI #2465 GREEN |
| 55 | Phase 2BE / PR #189 | `cataclysm_spellbooks` | canonical at `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0`; post-merge CI #2484 attempt 2 GREEN |
| 56 | Phase 2BG / PR #195 | `leylines` | canonical at `main@88f042f68429ff920314a7ec3a6923369edc93fd`; post-merge CI #2504 GREEN |
| 57 | Phase 2BH / PR #198 | `goety` | canonical at `main@4fcc40aaf8149b5511dbd882a5616ee5240cd640`; post-merge CI #2524 GREEN |
| 58 | Phase 2BK / PR #204 | `ignissoulfires_spellbooks` | exact hash-matched zero-semantic gear/bridge closure |
| 59 | Phase 2BL / PR #207 | `goetyiron` | canonical; exact-artifact semantic +14 closure |
| 60 | Phase 2BL / PR #207 | `goety_cataclysm` | canonical; exact-artifact semantic +52 closure |
| 61 | Phase 2BM / PR #210 | `ars_polymorphia` | canonical at `main@f2cdfe7b79d500540c281d70a76e8b6e3a77d311`; source-pinned zero-semantic bridge; post-merge CI #2544 GREEN |
| 62 | Phase 2BN / PR #212 | `ars_sable` | canonical at `main@c1c422b5ec72fe4308104f04282732d6c2f2bbc1`; source-pinned zero-semantic spatial bridge; post-merge CI #2554 GREEN |
| 63 | Phase 2BO / PR #214 | `farmers_spell` | source-pinned +6 semantic closure at evidence merge `main@34a5fd495da744800b32b051e38c6473c6f5ea15`; post-merge CI #2565 GREEN; runtime host QA fail-closed |

Components #1–#46 remain part of the same canonical numerator and are preserved by prior cumulative snapshots/provider records.

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

GTBC's SpellLib and FamiliarsLib were already members of those 100 component units, so their closure changes the numerator only. Farmer's Spell was likewise already an open unit in the denominator, so Phase 2BO changes only the numerator. The denominator must be reconciled whenever the physical provider set changes.

## Partial providers still receive zero component points

Examples remain:

- `not_enough_glyphs` — 39 source-enabled glyph registrations remain config-conditional because deployed SERVER overrides are unavailable;
- `somakespells` — exact registry identity is closed, but deployed spell-lock config and complete survival reachability remain conditional;
- `gaze` — exact registry identity is closed, but 26 Spirit Rites remain conditional on the unavailable deployed COMMON `disableGazeRites` value.

These partials are also reasons the global semantic spell/magic denominator remains open. Their current conditional/open evidence is tracked explicitly in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md) rather than being silently added to the strict semantic count.

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
