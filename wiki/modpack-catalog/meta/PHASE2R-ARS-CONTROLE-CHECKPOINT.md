# Phase 2R — Ars Controle 1.6.15 checkpoint

State: `INITIAL EXACT-REGISTRY + 9/9 GLYPH SURFACE SOURCE-PINNED / SYSTEMS AUDIT IN PROGRESS`

## Baseline

- Black Arcana base inherited through the planning branch: `main@29c239adf21f523ae5688e7a7baba29f956bebf4`.
- Execution branch: `docs/magic-catalog-phase2r-ars-controle`.
- Provider JAR: `ars_controle-1.21.1-1.6.15.jar`.
- Mod id: `ars_controle`.
- Physical SHA-1: `fdf381d5733698abe336354c7541299ab495ecae`.
- Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.
- Source license declaration: LGPLv3.

## Exact registry result

`ACRegistry` registers 4 blocks, 6 items, 3 BlockEntityTypes, 2 persistent/network-synchronized data components, 4 attachments, 1 creative tab and exactly 9 Ars spell parts.

This resolves two prior editorial discrepancies:

- four blocks do not imply four BlockEntityTypes; Temporal Stability Sensor has no registered tile type;
- the Notion dossier's 31 logic/component concepts are not 31 registered glyphs in exact 1.6.15. The current spell registry contains 9 parts.

## Glyph closure for this checkpoint

9/9 identities, recipes and core executable semantics are source-pinned:

- Precise Delay;
- Above;
- Below;
- Level;
- OR;
- XOR;
- XNOR;
- NOT;
- Random.

Precise Delay is Tier II / 0 base mana / 55 Scribe XP. Filters are Tier I / 0 base mana / 27 Scribe XP under the provider/base Ars contracts checked for the installed release line.

## Remaining Phase 2R work

- Warping Spell Prism;
- Scryer's Linkage;
- Scroll Holder;
- Temporal Stability Sensor;
- Remote;
- Portable Brazier Relay;
- config and networking authority;
- Ars ritual mixins / lifecycle hooks;
- optional CC:Tweaked and other compatibility gates;
- acquisition/recipes for provider blocks/items;
- capability matrix, audit queue and provenance closure;
- final main reconciliation, CI and merge gate.

No Black Arcana runtime Stage is promoted by this catalog checkpoint.
