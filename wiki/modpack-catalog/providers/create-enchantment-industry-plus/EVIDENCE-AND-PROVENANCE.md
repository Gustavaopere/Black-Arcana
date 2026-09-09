# Create Enchantment Industry Plus 1.1.1 — evidence and provenance

## Physical authority

Current physical pack evidence:

- JAR: `create_enchantment_industry_plus-1.1.1-1.21.1.jar`
- mod id: `create_enchantment_industry_plus`
- runtime version: `1.1.1`
- SHA-1: `c7e87eb00e10cb347f6372e17d38da51ce6f1975`
- Minecraft 1.21.1 / NeoForge 21.1.248

Relevant physical providers in the same modlist:

- Create `6.0.10`;
- Create: Enchantment Industry `2.5.3b`;
- Create: Dragons Plus `1.11.8b`.

The physical modlist remains authority for presence and runtime identity.

## Publisher release evidence

CurseForge project/file:

- project `776497`;
- file `6452325`;
- filename `create_enchantment_industry_plus-1.1.1-1.21.1.jar`;
- NeoForge / Minecraft 1.21.1;
- release date 2025-04-22.

The 1.1.1 public changelog identifies three release deltas:

- recipes changed from ink to black dye;
- Ink Sac → Glow Ink Sac conversion added;
- grinding recipe added.

Publisher descriptions also mention an Ink Sac drain/recovery flow. That description is retained as public evidence but is not silently substituted for the exact source tree when the exact source does not contain a drain/emptying recipe.

## Exact official source pin

Official repository:

- `TiesToetToet/create_enchantment_industry_plus`
- exact revision `fb97ed35288f7ff2c80d43ef33f051db93d281d5`
- commit date 2025-04-22
- source `mod_version=1.1.1`
- Minecraft `1.21.1`
- Java 21 toolchain context
- NeoForge source baseline `21.1.159`

Exact source tree results:

- 2 addon Java files;
- 1 registered item (`create_enchantment_industry_plus:sac`);
- 6 addon recipe definitions;
- 1 `neoforge:never` host-recipe disable overlay;
- 0 mixin configs;
- 0 standalone spells;
- 0 glyphs;
- 0 rituals;
- 0 provider mana/cast runtime;
- no provider packet or persistence surface observed.

## Declared dependency evidence

Exact `neoforge.mods.toml` declares:

- NeoForge `[21.1.0,)`;
- Minecraft `[1.21.1,1.22)`;
- Create `[6.0.4,6.1.0)`;
- Create: Enchantment Industry `[2.0.0,)`.

The exact recipes additionally reference `create_dragons_plus:black_dye` and `create_dragons_plus:grinding`, but Create: Dragons Plus is not declared as a metadata dependency. The current pack contains it, so this is recorded as an undeclared data-level dependency rather than converted into a fabricated formal dependency.

## Exact-source discrepancy ledger

### Public drain flow

- publisher-facing description: drain Ink Sac to recover Empty Ink Sac + ink;
- exact 1.1.1 source tree: no `emptying`/drain recipe path found;
- disposition: **REVIEW_REQUIRED / fail-closed** until the physical recipe owner/ID is demonstrated.

### License metadata

- exact `gradle.properties`: `MIT License`;
- Modrinth: MIT;
- CurseForge: LGPLv3;
- repository `LICENSE.txt`: Forge-origin LGPL 2.1 boilerplate text.

Disposition: factual inspection is allowed for cataloging, but no source/assets are copied and no derivation/reuse grant is inferred from conflicting metadata.

## Clean-room result

This phase performs read-only source/data inspection for factual inventory, authority mapping and deduplication only. Black Arcana does not import provider code, recipes, assets or implementation patterns. Provider execution authority stays with Create / Create: Enchantment Industry / Create: Dragons Plus as applicable.