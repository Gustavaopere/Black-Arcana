# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AG revision: 36/100 = 36%.**

Canonical `main` immediately before Phase 2AG is **35/100 = 35%** at `6ef2fb6fee567dc4fbe3d340166829d042132bfb`. The 36th point becomes canonical only when this revision is merged to `main`; while it exists only on the Phase 2AG branch/PR, the canonical value remains 35/100.

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

Phase 2AF / PR #135 is canonical and closed `not_enough_glyphs` as component **35**.

Phase 2AG closes `ars_n_spells` as component **36** at the available evidence ceiling:

- exact physical/release identity: Ars 'n' Spells `3.3.2`;
- official NeoForge 1.21.1 source baseline: `3.3.0` at `a9930223c96806e5d748ea69d02f9a32cab62de9`;
- 5 ritual identities under the physical pack condition where Iron's is present;
- 5 provider-owned mana-unification modes;
- Spell Loom/carrier lifecycle;
- cross-cast settlement and finite 8-slot native-wheel proxy pool;
- 8 `ars_cross_*` proxy registry objects explicitly excluded from standalone semantic-spell inflation;
- exact 3.3.1 receipt-HUD removal and exact 3.3.2 contextual mana-HUD fix;
- exact 3.3.2 internal signatures remain unverified/fail-closed rather than guessed.

The point is awarded for closing the **provider component at its evidence ceiling**, not for pretending the exact 3.3.2 JAR was decompiled.

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