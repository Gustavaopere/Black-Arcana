# Provider Audit Queue Delta — Dungeon's Delight 1.5.1

Date: `2026-09-24`

This overlay applies to `dungeonsdelight` until the current physical magic-provider queue is regenerated integrally.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `dungeonsdelight` | `neoforge-dungeonsdelight-1.21.1-1.5.1.jar` / distribution 1.5.1 / sibling-preserved internal metadata 1.5.0 / certified row #416 | ✅ `CATALOGED / EXACT SOURCE-PINNED 1.5.1 / 12 MOB EFFECTS / 2 ENCHANTMENTS / COOKING + ITEM + ENTITY SUPPORT / ZERO SPELL-RITUAL-ABILITY REGISTRY / +0 STRICT SEMANTIC MAGIC / RUNTIME QA FAIL-CLOSED` |

## Physical evidence

Sibling:

`neoforge-rpg-skilltree@49d9910ca0abfb9c0608c2730ab3ae8cefc59a9a`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Food + Magic/✅-dungeons-delight v1.5.1.md`

No independent installed-JAR digest is preserved in that dossier.

## Exact source evidence

`Yirmiri/Dungeons-Delight@0c2d621ebc7dcce3df5dad0ea485209ef2396f9c`

The exact pin declares `mod_version=1.5.1`, registers the current provider registry families and contains no spell/ritual/ability registry surface.

## Closed by current evidence

- distribution identity 1.5.1;
- exact source version 1.5.1;
- 12 provider mob-effect registrations;
- 2 provider enchantments;
- provider cooking/recipe registries;
- explicit absence of provider spell/ritual/ability registrar in exact source;
- semantic contribution fixed at +0.

## Runtime gates remain fail-closed

- physical binary ↔ source byte equality;
- installed metadata 1.5.0 divergence;
- config values;
- effect overlap;
- combat/enchantment scaling;
- XP-drain stacking;
- dispenser exactly-once behavior;
- item migration;
- reload/save/restart;
- full-pack Farmer's Delight + RunicLib compatibility.

## Semantic accounting

Dungeon's Delight contributes **+0** to the strict semantic magic numerator. Mob effects, enchantments, foods and equipment remain outside the action metric.

The strict minimum therefore remains unchanged and the technical provider denominator remains `PENDING REBASE`.
