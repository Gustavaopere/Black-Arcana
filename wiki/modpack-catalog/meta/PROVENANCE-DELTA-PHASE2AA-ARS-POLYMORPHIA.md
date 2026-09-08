# Provenance Delta — Phase 2AA Ars Polymorphia 1.0.3

Status: `EXACT SOURCE-PINNED / CLEAN-ROOM`

## Installed identity

Physical modlist authority:

- mod id: `ars_polymorphia`;
- JAR: `ars_polymorphia-1.0.3.jar`;
- version: `1.0.3`;
- SHA-1: `8cce819e83f6360ab9aa8b44ac841511172a6a79`;
- CurseForge hash: `3576413974`.

Related physical hosts in the same snapshot:

- Ars Nouveau `5.13.1`;
- Polymorph+ `1.3.1+1.21.1`.

## Exact source checkpoint

Official repository:

`Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`

The commit message is `ver: 1.0.3`, matching the installed provider version.

Audited source surfaces include:

- `gradle.properties`;
- generated NeoForge mod metadata template;
- required mixin config;
- mod initializer;
- `CraftingLecternTileMixin`;
- terminal/menu accessors and client screen mixin;
- `CraftingTerminalWidget`;
- `APNetworking`;
- `PacketResetCraftingResult`.

## Build/runtime declaration

The exact source declares:

- Minecraft 1.21.1;
- NeoForge 21.1.115+;
- Java 21 mixin compatibility;
- Ars Nouveau build host 5.4.2.938, runtime range `[5.4.2,)`;
- required dependency mod id `polymorph`, runtime range `[1.0.7,)`;
- LGPL 3.0 license.

## Current-host drift

Physical Ars Nouveau 5.13.1 is newer than the source build host. Because Ars Polymorphia mixes directly into Ars storage/crafting internals, runtime compatibility must be validated rather than inferred from the permissive dependency range alone.

Physical top-level modlist exposes `polymorph_plus`, not `polymorph`. External project documentation describes Polymorph+ as an unofficial port/replacement of Polymorph, but this phase does not promote that into proof that the installed binary exposes the exact required dependency id/API contract. Direct JAR metadata/runtime validation remains open.

## Clean-room posture

Source was read only to establish factual provider behavior, authority boundaries, mixin/network footprint and compatibility risks. No upstream code, assets, GUI sprites or text are copied into Black Arcana.
