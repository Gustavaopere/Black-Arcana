# Ars Controle — Ars Nouveau control/automation provider

Status: `PHASE 2R / SOURCE-PINNED 1.6.15 CATALOG MATERIAL SURFACE CLOSED / GLOBAL DELTAS+FINAL QA PENDING`

## Exact installed identity

- JAR: `ars_controle-1.21.1-1.6.15.jar`
- Mod id: `ars_controle`
- Runtime version: `1.21.1-1.6.15`
- Physical SHA-1: `fdf381d5733698abe336354c7541299ab495ecae`
- Loader/game: NeoForge 1.21.1

## Exact source checkpoint

Read-only factual cataloging is pinned to `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.

At that revision `gradle.properties` declares:

- `mc_version=1.21.1`;
- `neo_version=21.1.217`;
- `mod_id=ars_controle`;
- `mod_version=1.6.15`;
- `mod_license=LGPLv3`;
- Ars Nouveau build baseline `5.10.6.1245`;
- Curios baseline `9.0.12`;
- CC:Tweaked baseline `1.112.0`.

The root upstream `LICENSE` is GNU Lesser General Public License v3. Source is inspected read-only for factual cataloging; Black Arcana copies/adapts no upstream code or assets.

The physical pack is newer in important providers, including NeoForge `21.1.248`, Ars Nouveau `5.13.1` and Curios `9.5.1+1.21.1`; effective runtime compatibility is therefore a separate QA gate.

## Provider authority

Ars Nouveau remains authority for mana, Source, spell grammar, resolver/cast lifecycle and the base Ars ritual/warp infrastructure. Ars Controle owns only its added filters/effect, control blocks/items, persisted endpoint/reference state and provider-specific routing behavior.

Black Arcana must not turn a routed/delayed provider spell into a second cast, charge mana/cooldown/Mastery/Arcane Danger twice, infer valid remote endpoints from stale state, or treat Ars Controle infrastructure as permission to weaken Black Arcana targeting/world-safety rules.

## Exact registry correction

The source-pinned release registers:

- 4 blocks;
- 6 items: 4 block items + Remote + Portable Brazier Relay;
- 3 BlockEntityTypes;
- 2 persistent/network-synchronized data components;
- 4 attachment types;
- 1 creative tab;
- 9 Ars spell parts: 1 effect + 8 filters.

The Temporal Stability Sensor is a registered block but has no BlockEntityType in `ACRegistry.Tiles`.

A prior Notion dossier described "4 block entities" and "31 Ars/logic components". Those values are retained as historical/editorial context only. They do not match the exact 1.6.15 registry: the current release source registers 3 block-entity types and 9 glyph/spell parts. Internal concepts/classes must not be promoted to player glyphs without registry evidence.

## Closed Phase 2R material surface

- exact registries: source-pinned;
- glyphs/spell parts: 9/9 individually cataloged;
- default glyph acquisition: 9/9 source-pinned;
- player-facing systems: 6/6 individually cataloged;
- default system acquisition: 6/6 resolved;
- persistence: 2 data components + 4 attachments classified;
- networking: 5 payloads classified;
- configs/defaults: source-pinned;
- capability delegation: source-pinned;
- mixin/ritual relay behavior: source-pinned;
- optional ComputerCraft surface: source-pinned and currently absent from physical pack;
- provider authority/deduplication rules: source-pinned.

## Important source findings

- Warping Spell Prism can add a 600-tick provider region ticket by default; Black Arcana does not inherit that permission.
- Prism helper calculates Source for entity targets, but the audited entity-hit execution returns before the block-target Source deduction path; runtime settlement is unresolved.
- Scryer's Linkage declares `load_time=600`, but its audited 1.6.15 block/tile/capability paths do not demonstrate the matching region-ticket operation.
- Remote multiple selection iterates a closed block box without an explicit source-visible volume/range cap in the audited path.
- Portable Brazier Relay suppresses normal brazier ticking and reuses/recontextualizes the original Ars ritual object rather than cloning it.

## Remaining Phase 2R closure

- write narrow global provider/capability/provenance deltas;
- reconcile shared provenance indexes without destroying concurrent work;
- review PR diff for scope/whitespace;
- refetch and merge latest `main` if it advances;
- execute full repository CI on the exact reconciled HEAD;
- only then mark PR ready/merge;
- installed-JAR runtime/config/client/full-modpack QA remains a later explicit validation layer and is not inferred from source inspection.
