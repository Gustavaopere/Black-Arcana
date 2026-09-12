# Provenance Delta — Phase 2BM Ars Polymorphia 1.0.3

Status: `EXACT SOURCE-PINNED / CLEAN-ROOM / PHYSICAL BINARY EQUIVALENCE NOT CLAIMED`

## Installed identity

Physical modlist authority:

- mod id: `ars_polymorphia`;
- JAR: `ars_polymorphia-1.0.3.jar`;
- version: `1.0.3`;
- SHA-1: `8cce819e83f6360ab9aa8b44ac841511172a6a79`;
- CurseForge hash: `3576413974`.

Related physical hosts:

- Ars Nouveau `5.13.1`, mod id `ars_nouveau`;
- Polymorph+ `1.3.1+1.21.1`, mod id `polymorph_plus`.

## Exact source checkpoint

Official repository/version checkpoint:

`Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`

The signed commit message is `ver: 1.0.3`. The same source checkpoint declares:

- mod version `1.0.3`;
- license `GNU LGPL 3.0`;
- Minecraft target property `1.21.1`;
- NeoForge baseline `21.1.115` with range `[21.1.115,)`;
- Ars Nouveau build host `5.4.2.938` with runtime range `[5.4.2,)`;
- required Polymorph range `[1.0.7,)`;
- generated dependency mod id `polymorph`;
- Java 21 mixin compatibility.

The source also declares `minecraft_version_range=[1.21,1.21.1)`, which is recorded as-is because it is inconsistent with the explicit `minecraft_version=1.21.1` property. No binary correction is inferred.

## Read-only factual surfaces inspected

- source tree shape and provider-owned classes/resources;
- `gradle.properties`;
- NeoForge metadata template;
- required mixin config;
- provider network registrar;
- serverbound reset/settlement payload;
- crafting lectern mixin flow.

These surfaces are used only to establish identity, registry absence, dependency declarations, authority boundaries and integration footprint.

## Current-host drift

Physical host identity is not silently substituted for source dependencies:

- `polymorph_plus` is not assumed to satisfy a required `polymorph` mod-id/API contract merely because it is thematically/replacement-compatible;
- Ars `5.13.1` is not assumed mixin-compatible with code built against `5.4.2.938`;
- the source Minecraft range inconsistency is not rewritten.

Direct current-host runtime validation remains fail-closed.

## Clean-room posture

No upstream implementation bodies, source snippets, assets, GUI sprites, localization text, models, sounds or other creative content are copied/adapted into Black Arcana. The catalog stores only original factual summaries and identifiers needed for interoperability/provenance. Any future code-level adapter would require a separate exact-version API/runtime review before implementation.
