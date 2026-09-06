# Ars 'n' Spells

Status: `PHASE 2 — CURRENT 3.2.4 CROSS-ENGINE BRIDGE VERIFIED; DISCRETE BRIDGE RITUALS NORMALIZED`

## Runtime identity

- Mod id: `ars_n_spells`
- Current JAR: `ars_n_spells-3.2.4.jar`
- Runtime version: `3.2.4`
- Loader/game: NeoForge 1.21.1
- Correct Phase 2 class: `BRIDGE / COMPAT / PROGRESSION`
- Granular capability catalog: `YES` — because the bridge exposes discrete rituals and cross-engine casting/progression behavior.

The PR #62 baseline classified this component as `ARS GLYPH / SYSTEM PROVIDER`. Current public 3.2.4 evidence shows that its primary role is bridging Ars Nouveau and Iron's Spells 'n Spellbooks rather than acting as an independent glyph provider.

## Verified cross-engine capabilities

Current public documentation describes the bridge as supporting configurable combinations of:

- unification/sharing of mana behavior between Ars Nouveau and Iron's;
- equipment bonuses that can apply across the two magic systems;
- shared spell-school progression behavior;
- cross-boundary casting between the systems;
- binding custom Ars Nouveau spells into Iron's spellbooks;
- using Iron's native spell wheel for bound Ars spells.

These are authority-sensitive integration surfaces. Black Arcana must not create a second generic Ars↔Iron's mana/progression/casting bridge around them.

## Current 3.2.4 ritual set

The 3.2.4 changelog explicitly identifies and fixes four bridge rituals introduced by the 3.x line:

1. Spellbook Binding
2. Spell Transcription
3. Spell Uninscription
4. Mana Infusion

Current documentation also describes the Spell Loom as the survival path for the carrier-scroll workflow used by this bridge.

The binding command `/ans bind_scroll_to_irons_book` is documented as respecting the configuration that controls whether Ars spells may be placed in Iron's spellbooks.

## Deduplication / authority

### Mana/resource routing

Ars 'n' Spells already owns the installed generic Ars Nouveau ↔ Iron's mana-unification bridge. Black Arcana must not:

- create a parallel combined mana pool for those same engines;
- debit both host pools for one bridged cast unless the provider's canonical contract explicitly requires it;
- refund one side independently after the bridge has committed the action;
- infer free casting when one side is unavailable.

### Spellbook/casting routing

Bound Ars spells executed through an Iron's spellbook remain provider-routed cross-engine casts. Black Arcana observation/integration must preserve a single causal cast identity and avoid processing the same cast once as “Iron's” and again as “Ars”.

### Progression/equipment

Shared progression/equipment effects must remain provider-native. The existence of cross-system bonuses is not permission to mirror or recompute those bonuses in Black Arcana.

## Phase 2 impact

This bridge materially covers:

- cross-engine mana/resource unification;
- custom spell storage in another engine's spellbook;
- cross-engine spell-wheel execution;
- spell transcription/binding lifecycle;
- progression/equipment interoperability.

Any future Black Arcana “universal spellbook” or generic Ars/Iron's resource bridge must prove a distinct requirement that Ars 'n' Spells 3.2.4 cannot already satisfy.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Cross-engine feature set and 3.2.4 ritual/fix behavior: current public Ars 'n' Spells project/changelog — HIGH at feature level.
- Exact internal registry IDs and every configuration interaction: not fully normalized in this pass.
- No Java bytecode was decompiled.
