# T.O Magic n' Extras — current Iron's 3.16.3 SUMMON_DAMAGE host contract

Status: `EXACT FILE 6342780 DEPENDENCY + CURRENT IRON'S 1.21.1-3.16.3 SOURCE PIN / 9 ACCESSORS ACROSS 6 SPELLS / HOST ATTRIBUTE SEMANTICS CLOSED / PROVIDER FORMULAS NOT RECONSTRUCTED / CURRENT PHYSICAL TRAVELOPTICS NOT PROJECTED`

## Purpose

Exact Traveloptics File `6342780` audit #658 proves that nine entity-reading summon-damage accessors do more than ordinary host spell-power lookup: they additionally reference Iron's `AttributeRegistry.SUMMON_DAMAGE`, query the caster/entity attribute surface and contain one branch.

This checkpoint binds that exact provider dependency to the **current installed Iron's Spellbooks 1.21.1-3.16.3 host contract**.

It does not reconstruct Traveloptics formulas or branch semantics.

## Traveloptics exact dependency evidence

Canonical exact-alpha dependency map:

- [`EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`](EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md);
- exact publisher artifact: CurseForge `1046916 / 6342780`;
- SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- audit PR **#658** — NON-MERGE;
- audit HEAD: `01f3ea2c87f1f69abca87aae678220017f0c6d1d`;
- run: `37455559549` — **SUCCESS**;
- artifact: `11409587136`;
- artifact digest: `sha256:eb4511931f7ea27c2b1b434f459be2d5a40d89b996f555c3efcfb1987bb48d3c`.

The nine exact methods reference:

- host `getSpellPower(int, Entity)`;
- Iron's `AttributeRegistry.SUMMON_DAMAGE`;
- `LivingEntity.getAttributes()`;
- `AttributeMap.hasAttribute(...)`;
- `LivingEntity.getAttributeValue(...)`;
- one branch.

No provider formula, numeric coefficient, branch outcome or instruction sequence is retained.

## Current Iron's host authority

Current physical host:

- Iron's Spellbooks `1.21.1-3.16.3`;
- physical SHA-1: `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

Matching public source pin:

- repository: `iron431/irons-spells-n-spellbooks`;
- commit: `e4056af90302d37eb1739f5ff05020b020e6e252`;
- `gradle.properties`: Minecraft `1.21.1`, `mod_version=1.21.1-3.16.3`.

At that exact source pin:

1. `AttributeRegistry.SUMMON_DAMAGE` is registered as Iron's `summon_damage`;
2. it is a `MagicPercentAttribute`, which directly extends NeoForge `PercentageAttribute`;
3. its registered default/base value is **1.0**;
4. its configured bounds are `-100 .. 100`;
5. it is syncable;
6. `AttributeRegistry.modifyEntityAttributes(EntityAttributeModificationEvent)` iterates every entity type supplied by the event and adds every registered Iron's attribute entry to that type.

Therefore `SUMMON_DAMAGE` is a first-class current-host attribute surface, not a Traveloptics-local field.

The value returned by `LivingEntity.getAttributeValue(SUMMON_DAMAGE)` remains entity-state dependent because attribute modifiers can change it from the registered base value.

## Nine accessors / six spells

| Registry ID | Exact File-6342780 accessor | Current host dependency |
| --- | --- | --- |
| `traveloptics:eternal_sentinel` | `getGolemDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:ignited_onslaught` | `getBerserkerDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:ignited_onslaught` | `getRevenantDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:summon_desert_dwellers` | `getKoboletonDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:summon_desert_dwellers` | `getWadjetDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:sword_of_the_ancients` | `getKobolediatorDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:axe_of_the_doomed` | `getAptrgangrDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:mechanized_predator` | `getWatcherDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |
| `traveloptics:mechanized_predator` | `getProwlerDamage(int, LivingEntity)` | `getSpellPower` + `SUMMON_DAMAGE` attribute surface |

## What is closed

For these nine accessors, the catalog may now state with exact provider + pinned current-host evidence:

- their entity dependency is not ordinary spell power alone;
- they additionally inspect the current Iron's `SUMMON_DAMAGE` attribute;
- that host attribute has a registered base/default of **1.0** before entity-specific modifiers;
- the attribute is percentage-style and syncable;
- final accessor output remains dependent on live entity attributes plus ordinary spell-power/config state.

## What is not closed

This checkpoint does **not** establish:

- whether the provider branch applies a fallback, multiplier, additive term or other operation in each exact method;
- a final summon damage number;
- the value of `SUMMON_DAMAGE` on a particular player/entity after equipment, effects, perks or other modifiers;
- current-physical Traveloptics equality;
- current-world runtime behavior;
- PvP/boss interactions.

No numeric Traveloptics damage formula is reconstructed.

## Catalog consequence

The six affected spell cards gain a host-dependency note. Numeric closure does not change:

- File-only scalar closure remains **37 outputs across 24/33** identities;
- provider/current-host numeric accessor/bridge coverage remains **28/33** identities;
- all 34 entity-reading accessors remain numerically entity/config conditional.

No result is projected to current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

Traveloptics remains **⚠️ partial/conditioned** and strict current-physical contribution remains **+0**.
