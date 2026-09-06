# Ars Additions

Status: `PHASE 2 — CURRENT 21.3.0 PUBLIC CAPABILITIES NORMALIZED; NUMERIC/REGISTRY DETAIL PARTIAL`

## Runtime identity

- Mod id: `ars_additions`
- Current JAR: `ars_additions-1.21.1-21.3.0.jar`
- Runtime/version: `1.21.1-21.3.0`
- Loader/game: NeoForge 1.21.1
- Phase 2 class: `ARS GLYPH / SYSTEM PROVIDER`

## Verified player-facing capabilities

### Retaliate

Form glyph. The current public 1.21.1 documentation describes it as targeting the entity that most recently hit the caster, provided that hit occurred within the previous five seconds.

Phase 2 semantic family: `conditional / event-context targeting`.

### Mark

Effect glyph. Stores a reference to the targeted block or entity inside a Reliquary.

Phase 2 semantic family: `stored target reference`.

### Recall

Form glyph. Uses a target reference stored in a Reliquary and applies the following spell context to that referenced block/entity.

Phase 2 semantic family: `remote / stored-reference targeting`.

Mark + Recall therefore cover a meaningful portion of remote target persistence. A Black Arcana mechanic that merely “marks something and later casts at it” is not automatically a gap.

## Verified infrastructure/content

- Warp Index: remote access to Ars Nouveau Storage Lecterns.
- Stabilized Warp Index: cross-dimensional form of that remote access.
- Ender Source Jar: remote Source access.
- Codex Entry variants: teach a random glyph for the corresponding tier.
- Ritual of Arcane Permanent: chunk-loading ritual; the public documentation states that it is configurable and disabled by default.
- Unstable Reliquary: stores references used by Mark/Recall.
- Wixie Enchanting Apparatus: automates Enchanting Apparatus recipes/enchanting through the Ars ecosystem.
- Ruined Warp Portals and Nexus Tower are documented world structures associated with exploration/teleportation content.

## Authority / deduplication

- Ars Nouveau remains authority for Source, glyph execution, spell context and Storage Lecterns.
- Ars Additions owns the additional reference/remote-access capabilities above; Black Arcana must not create a parallel reference store merely to duplicate Mark + Recall.
- Chunk loading is not a generic Black Arcana world-effect entitlement. If a future bridge needs chunk-loading behavior, it must respect the provider/configuration and Black Arcana no-force-load/world-safety policies rather than infer permission from this ritual.
- Remote Source access must not become a second Source economy or free resource generator.

## Data still unverified

The current public project documentation used for this pass does not normalize all of the following for 21.3.0:

- registry IDs for every capability;
- exact glyph tiers;
- exact mana costs;
- exact cooldowns/timing where applicable;
- exact structure loot tables and acquisition rates.

Those fields remain `UNVERIFIED`, not inferred.

## Provenance / confidence

- Presence/JAR/runtime identity: current 2026-09-06 modlist — HIGH.
- Capability semantics above: current public Ars Additions 1.21.1 documentation — HIGH at feature level.
- Exact numeric/registry fields not listed above — `UNVERIFIED / PENDING`.
- No Java bytecode was decompiled for this catalog pass.
