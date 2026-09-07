# Ars 'n' Spells

Status: `PHASE 2 — CURRENT 3.3.0 INSTALLED; CROSS-ENGINE BRIDGE VERIFIED; 3.3.0 DELTA PARTIALLY NORMALIZED`

## Runtime identity

- Mod id: `ars_n_spells`
- Current JAR: `ars_n_spells-3.3.0.jar`
- Runtime version: `3.3.0`
- Loader/game: NeoForge 1.21.1
- Correct Phase 2 class: `BRIDGE / COMPAT / PROGRESSION`
- Granular capability catalog: `YES` — because the bridge exposes discrete rituals and cross-engine casting/progression behavior.
- Previous catalog baseline: `3.2.4`.

The PR #62 baseline classified this component as `ARS GLYPH / SYSTEM PROVIDER`. Current public 3.3.0 evidence still identifies its primary role as bridging Ars Nouveau and Iron's Spells 'n Spellbooks rather than acting as an independent glyph provider.

## Verified cross-engine capabilities

Current public 3.3.0 project/release documentation describes the bridge as supporting configurable combinations of:

- unification/sharing of mana behavior between Ars Nouveau and Iron's;
- equipment bonuses that can apply across the two magic systems;
- shared spell-school progression behavior;
- cross-boundary casting between the systems;
- binding custom Ars Nouveau spells into Iron's spellbooks;
- using Iron's native spell wheel for bound Ars spells.

These are authority-sensitive integration surfaces. Black Arcana must not create a second generic Ars↔Iron's mana/progression/casting bridge around them.

## Bridge ritual baseline retained from 3.2.4

The 3.2.4 audit established four bridge rituals in the 3.x line:

1. Spellbook Binding
2. Spell Transcription
3. Spell Uninscription
4. Mana Infusion

The same provider line also documents the Spell Loom as the survival path for carrier-scroll/spellbook workflows. The binding command `/ans bind_scroll_to_irons_book` was documented as respecting the configuration that controls whether Ars spells may be placed in Iron's spellbooks.

No ritual is treated as removed in 3.3.0 because the current 3.3.0 public material continues to describe the Spell Loom, Iron's scroll/spellbook carriers, inscription/transcription and cross-casting. Exact registry-by-registry parity with the 3.2.4 audit remains a runtime/source normalization task rather than an assumption.

## Verified 3.3.0 delta

The installed NeoForge 1.21.1 file is the 3.3.0 release. Public 3.3.0 release notes report a substantial bridge/casting refresh, including:

- reworked cross-mod spell casting and resource payment;
- stronger handling of mana and other supported shared-resource paths;
- improved Iron's scroll/spellbook carrier behavior and long-cast settlement;
- improved school detection, custom-school support, progression tracking, equipment bonuses, mana limits, Resonance and Source Jar behavior;
- improved inscription/transcription preservation of inventory contents and native spell data;
- packet validation hardened against stale or repeated cross-cast requests;
- a redesigned Spell Loom/interface and a much larger icon/background authoring surface.

The public source `CHANGELOG.md` for 3.3.0 additionally verifies optional addon-aware school resolution for Ars Elemental and Ars Zero using declared Ars metadata, with augments/cast methods/filters remaining generic rather than deciding the payload school. It also documents Covenant compatibility changes.

### Evidence boundary

The public release page and the public source changelog expose overlapping but not identical 3.3.0 summaries. Therefore:

- features directly stated by either current official surface are accepted at feature level;
- exact internal registry IDs, packet layouts, settlement ordering and every compatibility branch are **NOT inferred** from the older 3.2.4 implementation;
- any integration that depends on an internal 3.3.0 signature remains fail-closed until source/JAR-level confirmation for that signature.

## Deduplication / authority

### Mana/resource routing

Ars 'n' Spells already owns the installed generic Ars Nouveau ↔ Iron's mana-unification bridge. Black Arcana must not:

- create a parallel combined mana pool for those same engines;
- debit both host pools for one bridged cast unless the provider's canonical contract explicitly requires it;
- refund one side independently after the bridge has committed the action;
- infer free casting when one side is unavailable.

The 3.3.0 release explicitly reports reworked resource payment. That increases, rather than weakens, the requirement that Black Arcana observe the provider's settled result instead of reproducing the cost algorithm.

### Spellbook/casting routing

Bound Ars spells executed through an Iron's spellbook remain provider-routed cross-engine casts. Black Arcana observation/integration must preserve a single causal cast identity and avoid processing the same cast once as “Iron's” and again as “Ars”.

The 3.3.0 release also reports protection against stale/repeated cross-cast requests. Black Arcana must not bypass that provider-native anti-replay boundary with an independent packet/cast path.

### Progression/equipment

Shared progression/equipment effects must remain provider-native. The existence of cross-system bonuses is not permission to mirror or recompute those bonuses in Black Arcana.

### School resolution

For addon glyphs supported by Ars 'n' Spells, school ownership/resolution remains provider-native. Black Arcana must not infer a school from a registry-name heuristic when the bridge resolves it from Ars metadata or an explicit provider mapping.

## Phase 2 impact

This bridge materially covers:

- cross-engine mana/resource unification;
- custom spell storage in another engine's spellbook;
- cross-engine spell-wheel execution;
- spell transcription/binding lifecycle;
- progression/equipment interoperability;
- provider-native cross-engine school resolution, including current addon-aware paths documented for Ars Elemental and Ars Zero.

Any future Black Arcana “universal spellbook” or generic Ars/Iron's resource bridge must prove a distinct requirement that Ars 'n' Spells 3.3.0 cannot already satisfy.

## Provenance / confidence

- Presence/JAR/runtime: uploaded 612-entry modlist + Notion audit, reconciled 2026-09-07 — HIGH.
- Exact current release: Ars 'n' Spells 3.3.0, NeoForge 1.21.1 — HIGH from the current official release page.
- Cross-engine feature set: current official project/release documentation — HIGH at feature level.
- Ars Elemental/Ars Zero school-resolution delta: public 3.3.0 source changelog — HIGH at documented behavior level.
- Four-ritual details and command behavior: retained from the previously audited 3.2.4 baseline where current 3.3.0 evidence does not state a removal — MEDIUM/HIGH; exact 3.3.0 internals still require normalization.
- Exact internal registry IDs, packet layouts and every configuration interaction in 3.3.0: not fully normalized in this pass.
- No installed 3.3.0 Java bytecode was decompiled in this pass.