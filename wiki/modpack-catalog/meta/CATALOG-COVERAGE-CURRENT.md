# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AH revision: 37/100 = 37%.**

Canonical `main` immediately before Phase 2AH is **36/100 = 36%** at `2de722272814d2d5664266f5fc8ad05ba25d2940`. The 37th point becomes canonical only when this revision is merged to `main`; while it exists only on the Phase 2AH branch/PR, the canonical value remains 36/100.

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
- **2** current magic/cross-domain candidates not represented by the old 103-unit baseline remain under classification: `soul_fire_d` and `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100` current operational units.

Correction from the earlier Phase 2AF reconciliation text: `backportedspellbooks`, `crystal_chronicles` and `gtbcs_geomancy_plus` are physically present in the same 595-entry / SHA-1 `7aaece...` modlist and must not be listed as removed.

This denominator is operational, not immutable. Reconcile it whenever the physical provider set changes.

## Closed component count

Phase 2AF / PR #135 is canonical and closed `not_enough_glyphs` as component **35**.

Phase 2AG / PR #137 is canonical and closed `ars_n_spells` as component **36** at the available evidence ceiling:

- exact physical/release identity: Ars 'n' Spells `3.3.2`;
- official NeoForge 1.21.1 source baseline: `3.3.0` at `a9930223c96806e5d748ea69d02f9a32cab62de9`;
- 5 ritual identities under the physical pack condition where Iron's is present;
- 5 provider-owned mana-unification modes;
- Spell Loom/carrier lifecycle;
- cross-cast settlement and finite 8-slot native-wheel proxy pool;
- 8 `ars_cross_*` proxy registry objects explicitly excluded from standalone semantic-spell inflation;
- exact 3.3.2 internal signatures remain unverified/fail-closed rather than guessed.

Phase 2AH closes `monstersspellbooks` as component **37** when this revision becomes canonical:

- exact physical identity: `monstersspellbooks-0.0.16.3.jar`, SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`;
- exact CurseForge release: project/file `1428928 / 8788560`, 2026-09-01;
- complete current public-source inventory: **98 explicit `registerSpell(...)` registrations**;
- source-family distribution: blood 5, ender 12, evocation 3, fire 10, holy 4, hydro 8, ice 8, lightning 14, nature 7, necro 25, technomancy 2;
- two source SchoolTypes observed: Necro plus retained Aero; Aero contributes zero current spell registrations and exact 0.0.16.2 release marks it soft-deleted;
- public source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2` is contemporaneous with the release but still carries stale `mod_version=0.0.14` metadata;
- `ModSpellRegistry` is unchanged across the public source interval containing the 0.0.16.2/0.0.16.3 work;
- exact 0.0.16.3 binary numerical/API/config/network/save internals remain unverified/fail-closed.

The point is awarded for closing the **provider component at its evidence ceiling**, not for pretending the installed JAR was decompiled or that stale source metadata is an exact binary pin.

## Partial providers still receive zero points

Examples include:

- `leylines` — public signature names known, total current inventory not verified;
- `somakespells` — current granular inventory not closed;
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