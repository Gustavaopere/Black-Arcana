# Apprentice's Codex

Status: `CURRENT 0.9.7.1 IDENTITY VERIFIED; PUBLIC FULL SPELL TABLE NOT YET COMPLETE`

- Current JAR: `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- Mod id: `apprenticecodex`
- Runtime version: `0.9.7.1`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary casting authority: Iron's Spells 'n Spellbooks.
- Public repository license: MIT.

## Current provider scope

Current public descriptions characterize Apprentice's Codex as a broad Iron's side-grade expansion with **around 60 spells** plus spellcasting weapons, curios, spellbooks and utility blocks.

The publicly described spell families include:

- summoned weapon and magical firearm combat;
- barriers, guard stances and traps;
- healing and mana recovery;
- light and remote-vision utility;
- personal/storage and pet-storage utility;
- structure/treasure location;
- forestry, terrain shaping and crop harvesting;
- smelting/processing and item collection.

The content layer also includes spellcasting weapon families and support infrastructure such as the Spellcaster Workbench, Atelier Station and Spell Dispenser. Public documentation notes datapack configurability for several behaviors.

## Current 0.9.7.1 additions publicly verified

The current 0.9.7.1 release material publicly identifies these new spells/capabilities:

| Spell | Publicly established role |
|---|---|
| `Combustion Jet` | Heat-wave / force effect that knocks enemies away |
| `Blood Brand` | Blood-themed spell; exact current mechanics pending granular verification |
| `Shiden` | Current spell addition; exact mechanics pending granular verification |
| `Catch Flame` | Spell with interaction against loaded Essence Smokers in range |

The names above are current-release evidence. Phase 2 will not infer missing numbers or internal mechanics from the names alone.

## Full spell catalog status

The public project page confirms the provider's approximate size and categories, but the material collected in this pass does not yet provide a single complete 0.9.7.1 table containing every current spell name, registry ID and quantitative field.

Therefore:

- current presence/version — VERIFIED;
- approximate `~60` spell scale — VERIFIED PUBLIC CLAIM;
- broad semantic categories — VERIFIED;
- four 0.9.7.1 additions above — VERIFIED;
- exact complete 0.9.7.1 spell list — `PENDING`;
- exact mana/cooldown/cast time/damage/range/acquisition — `PENDING` unless individually evidenced later.

A future Phase 2 pass may inspect non-code resources from the officially distributed current JAR or official Wiki/documentation to resolve IDs/names. Java bytecode will not be decompiled merely to fill catalog gaps.

## Deduplication impact

Apprentice's Codex is one of the largest threats to accidental duplicate Black Arcana spells because its public scope already spans:

- magical firearms and summoned weapons;
- barriers/guards;
- traps;
- healing/mana restoration;
- movement/utility;
- remote vision;
- storage;
- structure/treasure detection;
- forestry/harvesting;
- terrain/crafting/processing automation.

### Chaos

Generic force blasts, summoned weapons, magical guns or explosive attacks cannot be accepted as Chaos merely because their VFX are red/magenta. Apprentice's Codex already covers a large combat/utility breadth.

### Order

Barriers, defensive stances, utility and detection overlap parts of an Order fantasy. Order still needs imposed-law/seal/constraint semantics with a measurable gameplay difference.

### Binding

Pet-storage/summon-adjacent utilities do not equal the planned typed persistent binding contract, but they must be considered before adding convenience spells around linked entities.

### Divination

Remote vision and structure/treasure location directly overlap divination. This is especially relevant to Black Arcana's pending 07.07 Familiars & Divination: the later domain must integrate/deduplicate rather than blindly duplicate these utilities.

## Provenance / confidence

- Presence/version: current modlist — HIGH.
- Around-60 scope and broad feature categories: current public project material — HIGH at feature level.
- 0.9.7.1 added spell names above: current release material — HIGH.
- Full spell list and numbers: `UNVERIFIED / PENDING`.
- Repository license metadata: MIT — VERIFIED publicly; this does not remove the Black Arcana provenance-ledger requirement before source-derived implementation work.
