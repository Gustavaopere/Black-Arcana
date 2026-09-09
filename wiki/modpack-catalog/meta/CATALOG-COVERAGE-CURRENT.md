# Current Magic Catalog Coverage

## Operational percentage

**Canonical coverage: 36/100 = 36%.**

Phase 2AG / PR #137 is merged to canonical `main@2de722272814d2d5664266f5fc8ad05ba25d2940` and closed `ars_n_spells` as component **36**.

Phase 2AH audits `monstersspellbooks` but does **not** increment the numerator: exact physical/release 0.0.16.3 is known, while the official public source head still declares mod 0.0.14 and older host versions. An unresolved current-version registry/internals delta receives zero closed-component points.

This metric is intentionally conservative. It measures **current magic/cross-domain provider components closed to the strongest evidence presently available**, not a guessed percentage of every individual spell object. A provider with a partial current inventory or unresolved current-version delta contributes zero closed component points.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: 21.1.248
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

The historical 2026-09-07 queue used **612 top-level entries / 103 candidate components**. It is preserved as history and is not the current denominator.

## Current working denominator

The current operational denominator remains **100 magic/cross-domain component units** from the physical reconciliation introduced in Phase 2AF:

- 98 entries from the former 103-unit candidate set still survive the current physical modlist;
- 5 former entries are no longer physically present: `ars_morph`, `backportedspellbooks`, `crystal_chronicles`, `gtbcs_geomancy_plus`, `woodwalkers_spellbooks`;
- 2 current magic/cross-domain candidates not represented by the old 103-unit baseline remain under classification: `soul_fire_d` and `reliquified_lenders_cataclysm_new_relics_fix`.

This denominator is operational, not immutable. Reconcile it whenever the physical provider set changes.

## Closed component count

- component **35**: `not_enough_glyphs`, canonical via PR #135;
- component **36**: `ars_n_spells`, canonical via PR #137.

Phase 2AG closed Ars 'n' Spells at its evidence ceiling while explicitly retaining unknown exact 3.3.2 internal signatures as fail-closed. That closure is now canonical.

## Phase 2AH partial checkpoint — Monsters & Spellbooks

Exact current artifact/release evidence:

- `monstersspellbooks-0.0.16.3.jar`;
- SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`;
- CurseForge project/file `1428928/8788560`;
- publisher scale `90+ spells / 2 new spell schools`.

Official public source baseline:

- `RedReaper28/Monsters-Spellbooks-1.21.1@1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`;
- 98 source-baseline spell registrations across 11 families;
- source-baseline `necro` and `aero` school registrations;
- build metadata still declares mod `0.0.14`, NeoForge `21.1.216`, Iron's `1.21.1-3.15.4`.

Because exact 0.0.16.3 registry/API parity is not proven and the exact release's Aero-removal note conflicts with residual Aero registration in the public source head, this provider remains **PARTIAL / ZERO NEW POINTS**.

## Partial providers still receive zero points

Examples include:

- `monstersspellbooks` — exact 0.0.16.3 artifact/release, but public source build metadata remains 0.0.14 and exact current registry parity is unresolved;
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