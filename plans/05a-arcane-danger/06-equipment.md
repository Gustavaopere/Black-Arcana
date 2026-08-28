# 06.06 — Equipment & Containment Items

## Objective
Make forbidden-magic preparation visible in character build/equipment instead of reducing the system to perks or a single resistance number.

## Scope
Black Arcana may add specialized containment equipment such as robes/armor, masks/helms, gloves, mantles and containment artifacts. Final names/models/recipes are content decisions; this task freezes the mechanical infrastructure first.

## Equipment provider
Implement a server-side Black Arcana equipment resistance provider that snapshots equipped armor/items at hazard-session activation.

Equipment contributions may include:
- Arcane Resistance;
- Corruption Resistance;
- strain-capacity/recovery modifiers;
- profile-specific containment bonuses;
- emergency backlash absorption;
- explicit set effects.

Vanilla armor value/toughness are not automatically converted into Arcane Resistance.

## Item data
Prefer explicit Black Arcana data components/tags/registries for containment properties rather than slot-name conditionals scattered through cast code.

Set bonuses are resolved as a provider over stable set identity/tags. The provider produces a diagnostic contribution list so preflight/debug can explain where resistance came from.

## Emergency protection
Rare equipment may prevent/reduce a lethal backlash event only through a transactional protection contract:
- evaluate predicted lethal backlash after resistance;
- reserve a single eligible item/charge/durability resource;
- consume/break/start cooldown exactly once per qualifying backlash settlement;
- apply bounded reduction/absorption;
- commit or compensate atomically;
- use root-cast/damage identity to prevent double consumption.

Emergency protection is not permanent immortality. Profiles may disallow it or enforce unavoidable damage/corruption/strain.

## Set design constraints
Do not create a generic ladder of interchangeable `+10%` items. Important items should have distinct roles, for example:
- stable always-on containment;
- better corruption protection but weaker immediate backlash protection;
- strain recovery/capacity specialization;
- one-time emergency ward;
- affinity-specific containment for a spell family.

Numeric tuning belongs to Stage 09 Progression & Balance; Stage 06 establishes ceilings and behavior contracts.

## RED
Tests:
- armor contribution is included in snapshot;
- removing armor after cast does not change that root cast's backlash;
- equipping armor after cast does not retroactively reduce it;
- set bonus activates only for valid composition;
- normal armor with no BA containment data contributes zero;
- emergency item consumes exactly once;
- failed/duplicate backlash cannot duplicate durability/charge consumption;
- emergency protection cannot reduce below profile unavoidable floor;
- broken/depleted item no longer contributes.

## GREEN
Implement equipment provider, containment data contracts, set resolver and transactional emergency-protection interface. A minimal test item/set may be introduced only to prove the infrastructure.

## REFACTOR
Keep item-specific behavior behind registered containment definitions/providers. Hazard core must not know concrete item classes.

## Acceptance
A player can build meaningful Arcane/Corruption resistance from Black Arcana equipment, with snapshot-safe behavior and no generic vanilla armor shortcut.
