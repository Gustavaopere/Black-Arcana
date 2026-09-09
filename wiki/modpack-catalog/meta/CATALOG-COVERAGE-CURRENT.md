# Current Magic Catalog Coverage

## Operational percentage

**Phase 2AF candidate coverage: 35/100 = 35%.**

Before PR #135 is merged, canonical `main` remains **34/100 = 34%**. Once this checkpoint is merged to `main`, the canonical value becomes **35/100 = 35%**.

This percentage is intentionally conservative. It measures **current magic/cross-domain provider components closed to the strongest evidence presently available**, not a guessed percentage of every individual spell object. A provider with a partial inventory or an unverified current-version delta contributes zero closed component points until its current surface is closed.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: 21.1.248
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

The previous `PROVIDER-AUDIT-QUEUE.md` baseline used **612 top-level entries / 103 candidate components** from 2026-09-07. It is historical and must not be used as the current denominator without reconciliation.

## Current working denominator

Immediate physical reconciliation yields a **working denominator of 100 current magic/cross-domain component units**:

- 98 entries from the former 103-unit candidate set still survive the current physical modlist;
- 5 former entries are no longer physically present: `ars_morph`, `backportedspellbooks`, `crystal_chronicles`, `gtbcs_geomancy_plus`, `woodwalkers_spellbooks`;
- 2 current magic/cross-domain candidates not represented by the old 103-unit baseline are under classification: `soul_fire_d` and `reliquified_lenders_cataclysm_new_relics_fix`.

This denominator is an operational checkpoint, not a claim that all 595 modlist rows have already been semantically reclassified. It must be revised if physical reconciliation changes the provider set.

## Closed component count

Canonical `main` immediately before Phase 2AF contains **34 closed current components** at the evidence ceiling used by the catalog. Phase 2AF closes `not_enough_glyphs` as component 35.

Partial providers do **not** receive a closed point. Known examples include:

- `leylines` — public signature names known, total current inventory not verified;
- `somakespells` — current granular inventory not yet closed;
- `cataclysm_spellbooks` — installed 1.1.13 while exact public source inventory remains behind the installed artifact;
- `gaze` — public surface audited, exact current registry/source-JAR closure still pending.

## Phase 2AF contribution

Not Enough Glyphs 4.6.1 contributes one closed component after merge because its current-pack conditional registration surface has been source-audited:

- 40 `APIRegistry.registerSpell` registrations under the physical pack conditions;
- 39 source-enabled by default because Momentum is source-disabled;
- 4 forms + 36 effects in canonical functional taxonomy;
- 13 current Binder perks/threads;
- 25 storage / 10 caster Spell Binder contract recorded with runtime QA caveat;
- fallback ownership preserved for Too Many Glyphs, Ars Omega, Ars Trinkets and Ars Scalaes namespaces;
- Ars Elemental and Ars Controle delegation behavior reconciled against their actual presence.

## Update rule

After each provider closure:

1. re-read the physical modlist and current `main`;
2. reconcile concurrent PR ownership;
3. close the provider to the strongest exact evidence available;
4. merge only after latest-main reconciliation and CI GREEN on the reconciled HEAD;
5. increment the numerator only after the closure is canonical on `main`;
6. change the denominator whenever the physical provider set changes.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.