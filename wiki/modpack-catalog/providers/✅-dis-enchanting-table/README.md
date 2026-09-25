# Dis-Enchanting Table — 5.0.2

Status: `✅ CATALOGED / PHYSICAL SHA-PINNED / EXACT PUBLISHER RELEASE / ENCHANTMENT-ECONOMY UTILITY / ZERO SPELL-RITUAL-MAGIC-ACTION OWNERSHIP / +0 STRICT SEMANTIC MAGIC / RUNTIME ECONOMY QA FAIL-CLOSED`

## Current physical identity

Current sibling authority at audit start:

`neoforge-rpg-skilltree@5ad350730a16e786f91396336c16c7b193feb7ac`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Magic + Ores and Resources + Technology/✅-dis-enchanting-table v5.0.2.md`

Physical identity:

- order: **#221**;
- JAR: `disenchanting_table-merged-1.21.1-5.0.2.jar`;
- mod id: `disenchanting_table`;
- runtime: `5.0.2`;
- Minecraft 1.21.1;
- merged Fabric/NeoForge distribution;
- physical SHA-1: `c054a8bef63addff4d4a9520ec4c7a915c3fc1d1`.

## Exact publisher release

CurseForge project: `933354`.

Exact 1.21.1 file:

- file ID: `6581607`;
- filename: `disenchanting_table-merged-1.21.1-5.0.2.jar`;
- uploaded: 2025-05-26;
- Release;
- Fabric + NeoForge;
- supported game versions: 1.21 / 1.21.1;
- requires MonoLib.

Exact changelog:

- simplifies block inventory for hopper behavior;
- fixes menu shift-click errors;
- adds disenchanting sound;
- migrates config suffix from `-common` to `-server`;
- auto-outputs disenchanted items when `automatic_disenchanting` is enabled.

Publisher file:

`https://www.curseforge.com/minecraft/mc-mods/dis-enchanting-table/files/6581607`

Official source organization/repository:

`https://github.com/Mods-For-Lupin/Dis-Enchanting-Table-Mod`

The public repository has advanced beyond the exact 5.0.2 line, so it is used only as role/architecture context here and is not claimed as an immutable exact source pin.

## Provider role

Dis-Enchanting Table owns one transactional utility domain:

- accept an enchanted item;
- remove/extract enchantment data through the provider's table;
- produce the corresponding item/book outputs;
- charge configured XP/economy cost;
- optionally automate input/output through the block inventory.

This is enchantment economy / item transformation.

It is **not** a spell-casting provider.

## Enchantment identity boundary

The provider consumes existing enchantment identities from Minecraft or other mods.

It does not mint a new semantic spell/ritual identity merely because it extracts an enchantment into a book.

Authority remains:

- Minecraft/NeoForge and the original enchantment provider own enchantment identity/effects;
- Dis-Enchanting Table owns the extraction transaction;
- Apothic Enchanting/Create Enchantment Industry own their separate enchanting/economy systems.

Black Arcana must not double-process the same extraction or duplicate its XP/output settlement.

## Semantic accounting

Provider-owned spells: **0**.

Provider-owned glyph/spell-part identities: **0**.

Provider-owned rituals/rites: **0**.

Provider-owned equivalent discrete magical actions under the Black Arcana semantic metric: **0**.

The disenchant transaction is an item/block utility operation, not a provider-owned spell/rite identity.

Enchantments manipulated by the table remain owned by their original registry/provider and are not recounted here.

Strict semantic delta:

**+0**

## Authority boundary

Black Arcana must not:

- replay disenchant after provider settlement;
- charge XP a second time;
- duplicate enchanted-book output;
- treat a hopper transfer as a cast;
- reinterpret an enchantment as a new Black Arcana spell because the table extracted it.

## Runtime QA remains fail-closed

Catalog closure does not establish:

- deployed server config values;
- automatic-disenchanting behavior;
- hopper sided-I/O correctness;
- exactly-once XP settlement;
- duplicate-output resistance;
- player-proximity/resource selection;
- shift-click/menu behavior;
- chunk unload/restart lifecycle;
- modded enchantment data fidelity;
- interaction with Create Enchantment Industry or Apothic Enchanting.

These are runtime/economy compatibility gates, not semantic catalog blockers.

## Result

**✅ Cataloged.**

Dis-Enchanting Table 5.0.2 is an enchantment-economy utility provider with no provider-owned spell, glyph, ritual or equivalent semantic magic-action identity.

Strict semantic contribution: **+0**.
