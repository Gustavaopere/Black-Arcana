# Ars Controle — Ars Nouveau control/automation provider

Status: `PHASE 2R / SOURCE-PINNED 1.6.16 REVALIDATED / 9 SEMANTIC SPELL PARTS / CATALOG COMPLETE / RUNTIME+CONFIG+CLIENT+PACK QA PENDING`

## Exact installed identity

- JAR: `ars_controle-1.21.1-1.6.16.jar`
- Mod id: `ars_controle`
- Runtime version: `1.21.1-1.6.16`
- Physical SHA-1: `795567371450debec83fe634fd0114c295f7da5a`
- Loader/game: NeoForge 1.21.1

## Exact source checkpoint

Read-only factual cataloging is revalidated against release commit `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0` (`ver: 1.6.16`).

At that revision `gradle.properties` declares:

- `mc_version=1.21.1`;
- `neo_version=21.1.217`;
- `mod_id=ars_controle`;
- `mod_version=1.6.16`;
- `mod_license=LGPLv3`;
- Ars Nouveau build baseline `5.13.1.1403`;
- Curios baseline `9.0.12`;
- CC:Tweaked baseline `1.112.0`.

The root upstream `LICENSE` is GNU Lesser General Public License v3. Source is inspected read-only for factual cataloging; Black Arcana copies/adapts no upstream code or assets.

The physical pack remains newer than the source build in NeoForge (`21.1.248` vs `21.1.217`) and Curios (`9.5.1+1.21.1` vs `9.0.12`). The source build now targets Ars Nouveau `5.13.1.1403`, matching the installed Ars Nouveau `5.13.1` line. Effective assembled-pack runtime compatibility remains a separate QA gate.

## Provider authority

Ars Nouveau remains authority for mana, Source, spell grammar, resolver/cast lifecycle and the base Ars ritual/warp infrastructure. Ars Controle owns only its added filters/effect, control blocks/items, persisted endpoint/reference state and provider-specific routing behavior.

Black Arcana must not turn a routed/delayed provider spell into a second cast, charge mana/cooldown/Mastery/Arcane Danger twice, infer valid remote endpoints from stale state, or treat Ars Controle infrastructure as permission to weaken Black Arcana targeting/world-safety rules.

## Exact registry correction

The 1.6.16 source-pinned release registers:

- 4 blocks;
- 6 items: 4 block items + Remote + Portable Brazier Relay;
- 3 BlockEntityTypes;
- 2 persistent/network-synchronized data components;
- 4 attachment types;
- 1 creative tab;
- 9 Ars spell parts: 1 effect + 8 filters.

The Temporal Stability Sensor is a registered block but has no BlockEntityType in `ACRegistry.Tiles`.

A prior Notion dossier described "4 block entities" and "31 Ars/logic components". Those values are retained as historical/editorial context only. They do not match the exact registry: the 1.6.16 release source registers 3 block-entity types and 9 glyph/spell parts. Internal concepts/classes must not be promoted to player glyphs without registry evidence.

## 1.6.16 revalidation boundary

The exact upstream compare from `ecbb83ba512bc9ca7a025556fb9c62dbd32b6430` (`ver: 1.6.15`) to `14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0` (`ver: 1.6.16`) contains six commits. The only gameplay Java file changed is `WarpingSpellPrismBlock.java`; the remaining changes are dependency/version metadata, translations and optimized assets.

Most importantly, `src/main/java/dev/qther/ars_controle/registry/ACRegistry.java` is blob-identical across both release checkpoints: Git blob `b38959053740605768a8945ed40c012c6bef5953`. Therefore the exact registered content surface is unchanged at 1.6.16: 4 blocks, 6 items, 3 block entities, 2 data components, 4 attachments, 1 creative tab and the same 9 Ars spell parts.

This closes the version drift at catalog level without adding or removing semantic magic identities. Runtime behavior of the Warping Spell Prism remains a separate fail-closed QA concern.

## Closed Phase 2R source catalog

- exact registries: closed;
- glyphs/spell parts: 9/9 individually cataloged;
- default glyph acquisition: 9/9 resolved;
- player-facing systems: 6/6 individually cataloged;
- default system acquisition: 6/6 resolved;
- persistence: 2 data components + 4 attachments classified;
- networking: 5 payloads classified;
- configs/defaults: classified;
- capability delegation: classified;
- mixin/validator/ritual relay behavior: classified;
- optional ComputerCraft surface: classified and currently absent from physical pack;
- provider authority/deduplication rules: closed;
- narrow provider queue/capability/provenance deltas: written.

## Important source findings

- Warping Spell Prism can add a 600-tick provider region ticket by default; Black Arcana does not inherit that permission.
- The 1.6.16 Warping Spell Prism path was updated for Ars Nouveau 5.13.1 compatibility and direct-hit direction handling. Provider Source settlement, cross-dimension recreation and assembled-pack exactly-once behavior remain runtime QA concerns; this revalidation does not infer a PASS.
- Scryer's Linkage declares `load_time=600`, but its audited 1.6.15 block/tile/capability paths do not demonstrate the matching region-ticket operation.
- Remote multiple selection iterates a closed block box without an explicit source-visible volume/range cap in the audited path.
- Portable Brazier Relay suppresses normal brazier ticking and reuses/recontextualizes the original Ars ritual object rather than cloning it.

## Delivery and later validation

The source catalog is complete. PR delivery is tracked through the Phase 2R checkpoint and GitHub history; installed-JAR runtime/config/client/full-modpack QA remains a later explicit validation layer and is not inferred from source inspection.

Shared provenance tables remain high-churn; `PROVENANCE-DELTA-PHASE2R-ARS-CONTROLE.md` is the authoritative narrow provenance overlay until those indexes are safely regenerated.
