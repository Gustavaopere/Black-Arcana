# Phase 2AF Checkpoint — Not Enough Glyphs 4.6.1

## Scope

Close the installed Not Enough Glyphs 4.6.1 source-level current-pack primitive/system inventory, including conditional fallback ownership, Binder/perks, runtime boundaries and deduplication impact. Documentation only; no Black Arcana runtime Stage is promoted.

## Git synchronization

- repository: `Gustavaopere/Black-Arcana`;
- branch: `docs/magic-catalog-phase2af-not-enough-glyphs`;
- initial fresh base: `main@d103b259eed27705b2d4e44cbec60d78d4228054`;
- no open Not Enough Glyphs-equivalent PR existed when the branch was created;
- concurrent magic-provider PRs for Ars Two-Way Portals, Ars Polymorphia and Ars Sable were intentionally avoided;
- high-contention global provider queue/index files are not rewritten by this phase before final reconciliation.

## Physical identity

- `not_enough_glyphs-1.21.1-4.6.1.jar`;
- SHA-1 `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4`;
- embedded Sauce `0.0.42.89`;
- pack NeoForge `21.1.248`.

## Exact source-semver pin

`Alexthw46/NotEnoughGlyphs@2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b` declares `mod_version=4.6.1` and Minecraft 1.21.1.

Binary/source reproducibility is not independently proven; source authority is therefore used for source-level contracts while the physical modlist remains artifact identity authority.

## Current-pack inventory result

- 40 NEG calls to `APIRegistry.registerSpell` under installed-mod conditions;
- 39 source-enabled before external/user config;
- Momentum registered but explicitly disabled;
- 15 NEG-native registrations;
- 14 Too Many Glyphs fallbacks because TMG is absent;
- 8 Ars Omega fallbacks because Omega is absent;
- 2 Ars Trinkets fallbacks because Ars Trinkets is absent;
- 1 Ars Scalaes Resize fallback registered unconditionally;
- 4 real Ars Elemental primitives referenced/listed but not re-registered because Ars Elemental is present;
- Ars Controle Random fallback suppressed because Ars Controle is present.

## Binder correction

Current source is not accurately described by a single “25 spells” number:

- ItemHandler/container storage = 25;
- BinderCasterData/radial caster maxSlots = 10;
- first 10 storage slots are explicitly synchronized into caster state;
- storage slots 10–24 against the 10-slot caster remain runtime-QA territory.

## Other audited surfaces

- 13 current Binder perks/threads;
- exact thread formulas where implemented in NEG;
- two C2S Binder payloads;
- provider registry objects: Binder item/menu/data component, two projectile entities, three effects;
- Sauce-backed contingency events;
- Trail/Missile/Plane boundedness observations;
- Plow explicit claim check vs Flatten no equivalent local check observed;
- Scribe's Table/Summoning Focus mixins;
- exact generated glyph/Binder/perk acquisition recipes.

## Architecture result

- Ars/NEG/Sauce remain provider authority.
- No second mana, contingency engine, spell-container engine, projectile scheduler or target-filter pipeline is introduced.
- Historical namespaces remain provenance identities, not duplicate capabilities.
- Phase 3 remains blocked; this pass only removes uncertainty from the capability matrix.

## Remaining validation

- full physical-JAR/source equivalence: not proven;
- real-client/full-modpack host compatibility: pending;
- Binder storage 10–24 behavior: pending runtime test;
- complete protection-stack behavior for provider world mutations: pending;
- final branch must still reconcile with latest `origin/main`, rerun exact-head CI, clear review findings, and only then merge.
