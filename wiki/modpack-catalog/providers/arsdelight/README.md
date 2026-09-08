# Ars Nouveau's Flavors & Delight 2.2.2

Status: `SOURCE CATALOG COMPLETE / INSTALLED CURRENT-HOST QA OPEN`

## Installed identity

- mod id: `arsdelight`;
- physical JAR: `arsdelight-2.2.2.jar`;
- physical version: `2.2.2`;
- SHA-1: `98e98fc1f03192bb7680ef9a3ba9a99c2df625bb`;
- source checkpoint: `Minecraft-LightLand/Ars-Nouveau-Flavors-Delight@1443c80842575f7d775c522d2b2cd32441592e26`;
- source license: LGPL-2.1.

## Provider role

Ars Delight is a **crossover content provider** between Ars Nouveau and Farmer's Delight. It is authoritative for the items, blocks, effects, recipes and crossover runtime it registers, but it is not the owner of:

- Ars mana;
- Ars spell identity/resolution;
- Farmer's Delight food/feast/cutting-board semantics;
- Black Arcana casting, hazards, Corruption, Strain, world safety or persistence;
- RPG Skill Tree progression/runtime.

Black Arcana therefore has no reason to adopt Ars Delight as a casting/progression authority. Any future integration is observer/content-aware only behind a real boundary and must preserve exactly-once settlement.

## Physical/current-host boundary

The physical pack currently contains:

- Ars Nouveau 5.13.1;
- Farmer's Delight 1.3.4;
- Ars Elemental 0.7.10.1;
- Cuisine Delight 1.2.10;
- `thirst` from Thirst Was Reclaimed 1.21.1-3.0.4.

Archwood Good and Diet were not found as top-level physical entries in this checkpoint.

The source metadata only proves Ars Nouveau `[5.8.1,)` and Farmer's Delight `[1.3,)` eligibility. Current-host runtime compatibility — especially mixins into Ars internals and the Thirst fork/API boundary — remains unvalidated.

## Base registry inventory

Verified source/Notion inventory:

- 42 base `ADFood` entries;
- 8 base non-food items;
- 8 base crate/cabinet/feast blocks;
- 5 base jelly blocks + 1 jelly BE type;
- 4 base pie blocks + 4 slice items;
- 5 base provider effects.

These categories overlap at the block-item/content-surface level and must not be added together as a fake unique-content count.

Optional source-conditioned content is cataloged separately: Ars Elemental and Archwood Good add their own entries only when their providers are loaded.

## High-value runtime seams

1. `LivingHealEvent` → Flourishing Ars-mana credit and Synchronized Shield absorption.
2. `SpellDamageEvent.Pre/Post` → Wilden damage amplification and Freezing Spell child effect.
3. `MaxManaCalcEvent` / `ManaRegenCalcEvent` → Wilden Ars-stat calculation.
4. `EffectResolveEvent.Pre` → spell-aware Farmer's Delight Cutting Board transaction/cancellation.
5. Enchanter's Knife → Ars `ICasterTool` melee-hit spell resolution.
6. `IPrismaticBlock` + spell-context attachment + `EffectInfuse` mixin → Jelly infusion.
7. Drygmy mixin → Ars fake-player tool lending/durability.
8. Global loot modifiers → Wilden/Chimera crossover drops.

## Black Arcana boundary

- no second mana pool/credit around Ars Delight;
- no second spell resolver or cooldown ledger;
- no duplicate food/heal/spell-damage proc;
- no replay after provider event cancellation;
- no copy of FD serving state;
- no coupling to provider mixin internals;
- no source/asset copying under clean-room policy.

## Runtime QA still open

Source catalog completion is not runtime PASS. The physical JAR/current-host matrix, event ordering, mixin application, optional providers, full-pack nutrition/loot/spell integrations and client/dedicated boot remain explicit validation work.
