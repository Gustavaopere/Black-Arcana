# Provenance Delta — Phase 2AB Ars Sable 1.1.2

Status: `EXACT SOURCE-PINNED / CLEAN-ROOM`

## Physical identity

Current physical modlist:

- `ars_sable-1.21.1-1.1.2.jar`;
- mod id `ars_sable`;
- version `1.1.2`;
- SHA-1 `df43ad58fb9ca3b7acf7f62dc97ed75fd6da3da8`;
- CurseForge hash `2760241931`.

Current physical Sable host:

- `sable-neoforge-1.21.1-2.0.5.jar`;
- mod id `sable`;
- version `2.0.5`;
- SHA-1 `05f666e973d32baaaf405acb9bbed6615b909971`;
- CurseForge hash `2399697702`.

## Exact source

Official repository: `baileyholl/ars-sable`.

Exact installed-version checkpoint:

`1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` — commit message `1.1.2`.

Tree: `18e56f1b49fea455ccdbd910b4f066b3232aaf88`.

Audited source surfaces include:

- `gradle.properties`;
- `META-INF/neoforge.mods.toml`;
- `ars_sable.mixins.json`;
- mod initializer/registries;
- Source Jar and `SableSourceProvider`;
- Storage Lectern tracking;
- Warp Portal/scroll adapters;
- persistent tracked-position structures;
- Sable sublevel observer;
- entity/pathfinding/Planarium/Mob Jar/camera/render mixins;
- networking registrar;
- four upstream GameTest classes;
- release changelog.

## Dependency contract

Exact source metadata requires:

- NeoForge `[21,)`;
- Minecraft `[1.20.6,1.21.2)`;
- Ars Nouveau `[5.11.7,)`;
- Sable `[1.0,)`.

Build pins were Ars Nouveau `5.11.7.1354` and Sable `1.2.2`. Physical pack uses Ars Nouveau 5.13.1 and Sable 2.0.5.

The declared ranges permit loader resolution but do not guarantee the 29 direct mixin/API hooks against Sable 2.x. Current-host runtime QA therefore remains explicit.

## License / clean-room

Source metadata and NeoForge metadata declare LGPLv3. Black Arcana nevertheless uses this repository read-only for factual interoperability/catalog evidence. No provider code, assets, text, models or sounds are copied or adapted into Black Arcana.

## Evidence hierarchy

- physical modlist establishes installed identities/versions/hashes;
- exact source commit establishes provider implementation at 1.1.2;
- Notion contributes operational context/QA framing but does not override source/runtime evidence;
- no current-pack behavior is marked PASS without execution against the physical host versions.
