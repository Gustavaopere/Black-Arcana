# Create Enchantment Industry Plus 1.1.1

Status: `EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION / CREATE+CEI RECIPE EXTENSION / 0 SPELLS+GLYPHS+RITUALS / 1 ITEM / 6 ADDON RECIPES + 1 HOST-RECIPE DISABLE / CREATE METADATA TABLE MIS-KEYED + CREATE DRAGONS PLUS DATA DEPENDENCY UNDECLARED / LICENSE-METADATA + FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `create_enchantment_industry_plus-1.1.1-1.21.1.jar`
- mod id: `create_enchantment_industry_plus`
- runtime version: `1.1.1`
- Minecraft: `1.21.1`
- loader: NeoForge
- physical SHA-1: `c7e87eb00e10cb347f6372e17d38da51ce6f1975`
- CurseForge project/file: `776497 / 6452325`
- exact official source: `TiesToetToet/create_enchantment_industry_plus@fb97ed35288f7ff2c80d43ef33f051db93d281d5`

The current physical modlist/JAR metadata is authority for installed identity. The official source commit is the repository's 2025-04-22 release-line commit and its `gradle.properties` declares `mod_version=1.1.1` for Minecraft 1.21.1.

## Provider role

Create Enchantment Industry Plus is not a spell system. It is a small Create / Create: Enchantment Industry data-and-item extension around ink processing.

Authority is split as follows:

- **Create 6.0.10** owns the Create processing machinery and recipe execution types such as pressing, filling and mixing;
- **Create: Enchantment Industry 2.5.3b** owns its enchantment/experience processing domain and the `create_enchantment_industry:experience` fluid consumed by one addon recipe;
- **Create: Dragons Plus 1.11.8b** owns `create_dragons_plus:black_dye` and the `create_dragons_plus:grinding` recipe type referenced directly by this addon's data;
- **Create Enchantment Industry Plus 1.1.1** owns its `sac` item and its six recipe definitions plus one explicit host-recipe disable overlay;
- **Black Arcana** retains casting, spell-domain, cost, cooldown/charge, targeting/effect, hazard, Corruption, Strain, Arcane Danger, Backlash and `WorldEffectPolicy` authority.

RPG Skill Tree receives no magic or processing runtime authority from this addon.

## Exact source surface

The exact 1.1.1 source tree contains only two Java files in the addon package:

1. the mod bootstrap, which initializes Create Registrate, lifecycle listeners and item registration;
2. `ModItems`, which registers exactly one plain item: `create_enchantment_industry_plus:sac`.

No standalone spell registry, glyph registry, ritual registry, cast resource, player magic state, network payload, attachment/persistence system or mixin configuration is present in the exact source tree.

### Exact semantic inventory

- standalone spells: **0**
- glyphs: **0**
- rituals: **0**
- provider mana/cast resource: **0**
- provider items: **1** (`create_enchantment_industry_plus:sac`)
- addon-owned recipe JSONs: **6**
- explicit host-recipe disable overlays: **1**
- Java source files: **2**
- mixins: **0**
- provider network payloads observed: **0**
- provider persistent player/world state observed: **0**

This component therefore closes as a recipe/content compatibility provider with zero spell identities. Its presence must not inflate the Black Arcana spell catalog.

## Exact data inventory

The source contains the following six addon recipe definitions:

1. `filling/ink_sac_glow_ink_sac.json`
   - `minecraft:ink_sac` + 250 `create_enchantment_industry:experience`
   - result: `minecraft:glow_ink_sac`
2. `filling/sac_inksac.json`
   - `create_enchantment_industry_plus:sac` + 250 `create_dragons_plus:black_dye`
   - result: `minecraft:ink_sac`
3. `grinding/inksac_dye.json`
   - recipe type: `create_dragons_plus:grinding`
   - `minecraft:ink_sac`
   - result: 250 `create_dragons_plus:black_dye`
4. `mixing/ink_ink_sac.json`
   - `minecraft:ink_sac` + 250 water
   - results: 250 `create_dragons_plus:black_dye` + one `create_enchantment_industry_plus:sac`
5. `mixing/ink_wither_rose.json`
   - `minecraft:wither_rose` + 250 water
   - result: 250 `create_dragons_plus:black_dye`
6. `pressing/leather_sac.json`
   - `minecraft:leather`
   - result: `create_enchantment_industry_plus:sac`

The source also supplies `data/create_enchantment_industry/recipes/mixing/ink.json` containing only a `neoforge:never` condition. This is an explicit **disable overlay for a host recipe**, not a seventh addon processing route.

## Metadata dependency boundary

The exact NeoForge source metadata has addon-keyed required dependency tables for:

- NeoForge `[21.1.0,)`;
- Minecraft `[1.21.1,1.22)`;
- Create: Enchantment Industry `[2.0.0,)`.

The source file also contains a Create range `[6.0.4,6.1.0)`, but that block is written under `[[dependencies.create_enchantment_industry]]`, **not** under `[[dependencies.create_enchantment_industry_plus]]`. The physical pack contains Create `6.0.10`, which satisfies the numeric range, but the loader treatment and physical-JAR parity of this mis-keyed source table are not asserted without direct artifact evidence.

Create: Dragons Plus is not declared in any metadata dependency table, yet four of the six addon recipes reference `create_dragons_plus` content or a `create_dragons_plus` recipe type.

The current physical pack contains Create: Dragons Plus `1.11.8b`, so the referenced namespace is physically present in this pack. That does not convert the missing metadata dependency into a general compatibility guarantee. If Create: Dragons Plus is absent or changes those identifiers, the affected recipe subset must fail closed rather than being replaced with an invented Black Arcana fallback.

## Publisher-description vs exact-source discrepancy

Public/project documentation describes an Ink Sac drain/recovery flow. The exact official 1.1.1 source tree inspected here contains **no `emptying`/drain recipe path** and no additional Java logic implementing such a route.

Therefore:

- the public drain description is retained as publisher-facing behavior/history;
- it is **not promoted as an exact addon-owned 1.1.1 recipe** from this source pin;
- if the physical pack exposes a drain route, its actual owner/recipe ID must be identified at runtime or from the responsible provider before Black Arcana records it as current authority.

This resolves the earlier descriptive ambiguity without inventing a recipe.

## Black Arcana disposition

Black Arcana must not:

- treat any of these recipes as spells, rituals or casts;
- duplicate Create machine settlement or Create: Enchantment Industry experience-fluid accounting;
- register a second `sac` item or duplicate the provider recipe IDs;
- synthesize a fallback `black_dye` fluid or grinding recipe type when Create: Dragons Plus is unavailable;
- infer a drain recipe that is not present in the exact source inventory;
- use recipe processing as evidence of Arcane Danger, Corruption, Strain or Backlash causality;
- transfer recipe or magic runtime authority to RPG Skill Tree.

A future BA integration may reference provider items/recipes only through verified identifiers and must preserve the real provider's execution and resource-settlement authority.

## Evidence ceiling / QA

Closed semantically from exact evidence:

- physical 1.1.1 identity and hash;
- exact public source-version pin;
- exact Java registration surface;
- exact item count and identity;
- exact six addon recipes;
- exact host-recipe disable overlay;
- exact source metadata dependency tables/ranges, including the mis-keyed Create block;
- exact data-level reliance on Create: Dragons Plus identifiers;
- exact zero-spell/glyph/ritual/mixin/network/persistence result for the inspected source tree.

Still fail-closed:

- byte-for-byte source/JAR reproducibility;
- physical-JAR metadata parity and NeoForge loader interpretation of the mis-keyed Create dependency table;
- full-modpack recipe reload/JEI/runtime behavior;
- whether any provider outside this addon supplies the publicly described drain route;
- behavior if Create: Dragons Plus identifiers change or the undeclared dependency is removed;
- multiplayer/resource-conservation QA across repeated recipe cycles;
- source/publisher license metadata reconciliation for any reuse beyond factual interoperability analysis.

## License / clean-room note

The exact source metadata declares `MIT License`, and Modrinth labels the project MIT. CurseForge currently labels the project LGPLv3, while the repository's `LICENSE.txt` is Forge-origin LGPL boilerplate rather than a clean project-level MIT text. This mismatch is preserved as a reuse-review boundary.

Black Arcana uses the inspected source/data only for factual cataloging and interoperability analysis. No code, assets, models or textures are copied or adapted.