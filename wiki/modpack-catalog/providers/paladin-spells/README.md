# Paladin Spells — Iron's Spells Addon

Status: `PUBLIC SPELL LIST COMPLETE FOR CURRENT 1.1.1; FORMULAS PARTIAL`

- Current JAR: `paladin_spells-1.21.1-1.1.1.jar`
- Mod id: `paladin_spells`
- Runtime version: `1.21.1-1.1.1`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary casting authority: Iron's Spells 'n Spellbooks.
- Scaling authority: public project documentation states all five spells scale with **Holy spell power**.

Public sources used: current CurseForge project page and current 1.1.1 changelog. The project is distributed under CC BY-NC-SA 4.0.

## Current public spell catalog — 5 entries

| Spell | Semantic role | Public behavior established for Phase 2 |
|---|---|---|
| `Bulwark` | Defensive armor amplification | Increases armor based on the caster's current armor and Holy spell scaling |
| `Taunt` | Aggro control | Forces enemies in an area around the caster to target the caster |
| `Sworn Protector` | Ally damage interception | Redirects a percentage of damage from nearby players to the caster |
| `Bedrock Skin` | Defensive stance / immobilization | Immobilizes the caster while granting percentage damage mitigation |
| `Ram` | Armor-scaling mobility offense | Short dash through enemies; damage scales with caster armor |

## Current-version corrections

The public **1.1.1** changelog specifically records:

- `Sworn Protector`: duration behavior fixed for the 1.21 line;
- `Bulwark`: cooldown corrected to **45 seconds** on 1.21;
- `Bulwark`: duration was nerfed.

An older public changelog also records a historical `Bulwark` mana-cost-per-level reduction from 15 to 10. That historical change is useful context, but Phase 2 does not promote it to a final current formula until the current 1.1.1 data/config surface is confirmed.

## Authority observations

`Sworn Protector` is particularly important to Black Arcana deduplication because it is not merely a defense buff: it changes **who settles damage**. Any Black Arcana Order/Divine/Binding mechanic that intercepts ally damage must preserve:

- original damage provenance;
- exactly-once settlement;
- recursion prevention;
- death/invalid-target handling;
- PvP/protection rules;
- provider-native behavior when Paladin Spells is the active mechanic.

This catalog does not assert an implementation bug in 1.1.1. It only records the semantic authority risk that any bridge or duplicate mechanic would need to respect.

## Deduplication impact

### Divine / Celestial

Paladin Spells already provides a compact Holy defensive kit covering:

- armor amplification;
- aggro/tanking control;
- ally damage interception;
- high-mitigation rooted stance;
- armor-scaling charge offense.

Therefore a new Divine/Celestial school must not recreate these as differently named golden barriers, holy taunts or protector links.

### Order

`Bedrock Skin`, `Taunt` and `Sworn Protector` cover parts of imposed stance, target control and protection contracts. Order needs a stronger semantic delta in seals, local laws, geometric constraints, casting restrictions, stable boundaries or rule enforcement.

### Binding

`Sworn Protector` is a short-range protection relationship, but it is not the persistent typed external-resource link planned for Arcana Vincular. Still, any damage-sharing binding must deduplicate against and coexist safely with it.

## Quantitative fields still pending

The following remain `UNVERIFIED` for current 1.1.1 until confirmed from an appropriate current public/config/runtime surface:

- complete mana formulas;
- exact level ranges;
- exact duration/radius per level;
- exact mitigation/redirect percentages and scaling formulas;
- acquisition/loot/crafting details for each spell.

## Provenance / confidence

- Presence/version: current modlist — HIGH.
- Five spell names and semantic behavior: current public project page — HIGH.
- Bulwark 45 s cooldown and 1.1.1 fixes: current changelog — HIGH.
- Detailed numeric formulas not listed above: `UNVERIFIED`.
- No source-code behavior was used for this catalog.
