# 05A.06 — Equipment & Containment Items

## Objective
Make forbidden-magic preparation visible in character build/equipment instead of reducing the system to perks or a single resistance number.

## Scope
Black Arcana may add specialized containment equipment such as robes/armor, masks/helms, gloves, mantles and containment artifacts. Final names/models/recipes are content decisions; this task freezes the mechanical infrastructure first.

## Equipment provider
Implement a server-side Black Arcana equipment resistance provider that snapshots equipped armor/items at hazard-session activation. Contributions may include Arcane Resistance, Corruption Resistance, strain capacity/recovery, profile-specific containment, emergency backlash absorption and explicit set effects. Vanilla armor/toughness are not automatically converted into Arcane Resistance.

## Item data
Prefer explicit Black Arcana data components/tags/registries for containment properties rather than slot-name conditionals scattered through cast code. Set bonuses resolve through stable set identity/tags and produce diagnostic contribution breakdowns.

## Emergency protection
Rare equipment may prevent/reduce lethal backlash only through a transactional protection contract: evaluate predicted lethal backlash, reserve one eligible resource/charge/durability use, consume exactly once, apply bounded absorption and commit/compensate atomically. Root-cast/damage identity prevents duplicate consumption. Profiles may disallow emergency protection or retain unavoidable floors.

## Design constraints
Do not create a generic ladder of interchangeable `+10%` items. Important items should have distinct containment, corruption, strain, emergency or affinity-specific roles.

Numeric tuning belongs to Stage 08 Progression & Balance; Stage 05A establishes behavior contracts and hard ceilings.

## RED
Tests cover snapshot inclusion, post-cast gear swaps, set composition, zero contribution from ordinary armor, exactly-once emergency consumption, duplicate/failure idempotency, unavoidable floors and depleted/broken items.

## GREEN
Implement equipment provider, containment data contracts, set resolver and transactional emergency-protection interface. A minimal test item/set may be introduced only to prove infrastructure.

## REFACTOR
Keep item-specific behavior behind registered containment definitions/providers. Hazard core must not know concrete item classes.

## Acceptance
A player can build meaningful Arcane/Corruption resistance from Black Arcana equipment with snapshot-safe behavior and no generic vanilla armor shortcut.
