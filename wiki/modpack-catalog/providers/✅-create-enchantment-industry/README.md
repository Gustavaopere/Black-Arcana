# Create: Enchantment Industry — 2.5.3b

Status: `✅ CATALOGED / CURRENT PHYSICAL 2.5.3b / EXACT OFFICIAL SOURCE VERSION PIN / XP+ENCHANTMENT INDUSTRIALIZATION SYSTEM / 0 PROVIDER-OWNED ENCHANTMENT IDENTITIES / 0 SPELLS+GLYPHS+RITUALS / +0 STRICT / RUNTIME ECONOMY QA SEPARATE`

## Current physical identity

Current sibling authority rechecked at `neoforge-rpg-skilltree@b9edb403c06567423d6c101d136b73a1065f2ad4`.

Canonical sibling dossier:

`PROJECT-INSTRUCTIONS/modlist/Addons + Create + Storage + Technology/✅-create-enchantment-industry v2.5.3b.md`

- JAR: `create-enchantment-industry-2.5.3b.jar`;
- mod id: `create_enchantment_industry`;
- runtime: `2.5.3b`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `f39af237b8bff853a89e8784518bdc36ba54a32e`;
- physical Create line: `6.0.10`;
- physical Apothic Enchanting: `1.6.2` according to the sibling dossier.

CurseForge project/file `688768 / 8762719` publishes the same `create-enchantment-industry-2.5.3b.jar` for NeoForge 1.21.1. The 2.5.3b changelog requires Apothic Enchanting 1.6.1+ for that integration and fixes the Infuser crash on that line.

## Exact official source pin

Official repository:

`DragonsPlusMinecraft/CreateEnchantmentIndustry`

Exact 2.5.3b source checkpoint:

`9a523a3a0fb967f28658eb289534e692f6c03a9b`

At that commit, `gradle.properties` declares:

- `minecraft_version = 1.21.1`;
- `neo_version = 21.1.248`, range `[21.1.228,)`;
- `mod_id = create_enchantment_industry`;
- `mod_version = 2.5.3b`;
- Create production baseline `6.0.10`;
- Create: Dragons Plus baseline `1.11.3`;
- Apothic Enchanting baseline/range `1.6.1` / `[1.6.1,)`;
- Apotheosis baseline/range `8.7.0` / `[8.7.0,)`.

This is an exact **source-version pin**, not a byte-for-byte source-build↔physical-JAR equivalence claim.

## Provider role

Create: Enchantment Industry industrializes Minecraft experience and enchantment processing through Create-style machines and data-driven rules.

Important authority split:

- CEI owns its Liquid Experience representation, machines, recipe/process rules and CEI data maps;
- Minecraft/provider enchantment registries own the enchantments being processed;
- Apothic Enchanting/Apotheosis own their enchantment/affix semantics when their integrations are present;
- Create owns its kinetic/processing execution framework;
- Black Arcana retains its own casting, costs, cooldowns, hazards, rituals, Corruption, Strain, Arcane Danger and world-safety runtime;
- RPG Skill Tree receives no enchantment/casting authority from CEI.

## Exact magic-relevant surface

### Enchantment registry boundary

The exact `CEIEnchantments` class registers **enchantment tags only**. It defines seven tag surfaces used by the Blaze Enchanter/Printer:

1. normal enchanting;
2. normal-enchanting exclusive;
3. super enchanting;
4. super-enchanting exclusive;
5. penalty curses;
6. denied penalty curses;
7. printer deny.

The exact source tree contains **no provider data definitions under `data/create_enchantment_industry/enchantment/**`**. Enchantment-related packaged data are limited to tags and data maps.

Therefore provider-owned enchantment identities established by CEI 2.5.3b: **0**.

### Enchantment data maps

`CEIDataMaps` registers five data maps keyed by the vanilla enchantment registry:

- enchanted-book printing custom cost;
- forging cost multiplier;
- split-enchantment forging cost multiplier;
- super-enchanting custom level extension;
- enchantment-processing rules.

These maps parameterize processing of existing enchantments. They do not register new enchantments. The packaged `super_enchanting/custom_level_extension.json` is empty at this exact checkpoint.

The generated processing rules explicitly reference existing vanilla `minecraft:mending` and `minecraft:infinity`; those remain Minecraft-owned enchantments.

### Experience / machine domain

Exact source establishes CEI-owned processing infrastructure including:

- `create_enchantment_industry:experience` / Liquid Experience;
- Experience Hatch conversion between player XP and supported experience fluid;
- Mechanical Grindstone / Grindstone Drain;
- Blaze Enchanter;
- Blaze Forger;
- Classic Blaze Enchanter;
- Printer and printing-behaviour registry;
- Experience Lantern;
- enchanting/super-enchanting templates and Super Experience items/blocks;
- one provider damage type, `create_enchantment_industry:grind`, used by the machinery domain.

These are processing/system/content surfaces, not standalone spells, glyphs or rituals.

### Cross-mod data integration

The exact data maps recognize compatible experience resources, including Ars Nouveau experience gems when Ars is loaded. That is an XP-conversion compatibility route; it does not transfer Ars spell/glyph ownership to CEI.

## Semantic disposition

Under the Black Arcana semantic-magic ledger:

- provider-owned standalone spells: **0**;
- provider-owned glyphs: **0**;
- provider-owned rituals: **0**;
- provider-owned enchantment identities: **0**;
- provider-owned magic semantic identities added to the strict spell/glyph/ritual denominator: **+0**.

CEI remains magic-relevant because it changes enchantment acquisition, levels, processing cost, XP economy and automation. Those are system/economy effects rather than new atomic magic identities.

## Runtime / economy QA remains separate

Catalog closure does not assert that every physical-pack processing path has been runtime-tested.

Important fail-closed QA includes:

- XP ↔ Liquid Experience conservation;
- repeated Experience Hatch transactions;
- Mechanical Grindstone disenchant output/XP exactly once;
- Blaze Enchanter and Blaze Forger level/cost settlement;
- super-enchanting caps and per-enchantment data-map overrides;
- Mending interaction;
- Apothic Enchanting Infuser compatibility;
- Printer copying/cost semantics;
- recipe/datapack reload idempotence;
- multiplayer/dedicated-server behavior.

No Black Arcana fallback should duplicate those provider-owned settlements.

## Current result

**✅ Cataloged.**

Create: Enchantment Industry 2.5.3b is cataloged as an enchantment/experience industrialization provider with **zero provider-owned spell, glyph, ritual or enchantment identities**. It contributes `+0` to the strict magic-identity denominator while remaining relevant to acquisition/economy/runtime QA.
