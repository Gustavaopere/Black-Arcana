# T.O Magic n' Extras 4.4.0.1 — all entity-reading accessor dependency map

Status: `EXACT FILE 6342780 / 34 OF 34 ENTITY_SLOT_READ ACCESSORS DEPENDENCY-CLASSIFIED / 24 HOST-SPELL-POWER ONLY / 9 SUMMON-DAMAGE AUGMENTED / 1 HOST-SPELL-POWER + MATH.MIN / NUMERIC OUTPUTS STILL ENTITY+CONFIG CONDITIONAL / CURRENT PHYSICAL NOT PROJECTED`

## Purpose

The canonical LivingEntity checkpoint classifies 49 numeric accessors from exact publisher File `6342780` as:

- **15** `ENTITY_UNUSED`;
- **34** `ENTITY_SLOT_READ`.

A previous focused audit classified one selected entity-reading accessor for each of the five spell identities that still lacked numeric accessor/host-bridge coverage. This checkpoint extends the dependency classification to **all 34/34 entity-reading numeric accessors**.

It deliberately does **not** reconstruct formulas or assign entity-independent numeric values.

## Exact clean-room audit

Temporary NON-MERGE PR **#658**:

- exact artifact: CurseForge project/file `1046916 / 6342780`;
- exact SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- audit HEAD: `01f3ea2c87f1f69abca87aae678220017f0c6d1d`;
- dedicated workflow: `Traveloptics All Entity Accessor Dependency Audit`;
- workflow run: `37455559549`;
- job: `112242173861`;
- extraction step: **SUCCESS**;
- text-only artifact: `11409587136`;
- artifact digest: `sha256:eb4511931f7ea27c2b1b434f459be2d5a40d89b996f555c3efcfb1987bb48d3c`.

Retention was limited to:

- exact class/method identity and JVM descriptor;
- entity local-slot load count;
- branch count;
- unordered field/member invocation identities;
- arithmetic opcode counts.

Not retained:

- numeric constants;
- instruction order;
- reconstructed formulas;
- method bodies;
- assets/localization;
- binary bytes.

## Aggregate result

Across all **34** canonical `ENTITY_SLOT_READ` accessors:

- **34/34** invoke host `getSpellPower(int, Entity)`;
- **24/34** have no provider/host field reference and no branch; their entity dependency is only through host `getSpellPower`;
- **9/34** additionally reference Iron's `AttributeRegistry.SUMMON_DAMAGE`, query the LivingEntity attribute map/value, and contain one branch;
- **1/34**, `AerialCollapseSpell.getDamage`, adds `Math.min(float,float)` while retaining no field reference and no branch;
- **32/34** contain retained arithmetic opcodes;
- **2/34** expose no additional arithmetic in this bounded classification: `AshenBreathSpell.getDamage` and `LavaBombSpell.getProjectileCount`;
- total entity local-slot loads: **52**.

The dependency surface therefore collapses to three canonical families.

## Family A — host spell-power only

These **24** methods read their LivingEntity only by passing it into host `getSpellPower(int, Entity)`. The bounded audit found:

- no field refs;
- no branches;
- no additional entity member calls.

| Registry ID | Exact accessor | Entity loads | Arithmetic classification |
| --- | --- | ---: | --- |
| `traveloptics:blood_howl` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:abyssal_blast` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:psychic_bolt` | `getEffectDuration(int, LivingEntity)` | 1 | `f2i ×1; fadd ×1; fmul ×1` |
| `traveloptics:reversal` | `calculateDamageMultiplier(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:spectral_blink` | `getEffectLevel(int, LivingEntity)` | 1 | `f2i ×1; fmul ×1; iadd ×1` |
| `traveloptics:orbital_void` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:void_eruption` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:vortex_punch` | `getDamage(int, LivingEntity)` | 1 | `f2i ×1; fadd ×1; fmul ×1` |
| `traveloptics:astral_sense` | `getDuration(int, LivingEntity)` | 1 | `f2i ×1; fadd ×1; fmul ×1` |
| `traveloptics:ashen_breath` | `getDamage(int, LivingEntity)` | 1 | none |
| `traveloptics:lingering_strain` | `getDuration(LivingEntity, int)` | 1 | `f2i ×1; iadd ×1; imul ×1` |
| `traveloptics:burning_judgment` | `getDamage(int, LivingEntity)` | 1 | `fmul ×1` |
| `traveloptics:meteor_storm` | `getDamage(LivingEntity, int)` | 1 | `d2i ×1; dadd ×1; f2d ×1; fmul ×1` |
| `traveloptics:lava_bomb` | `getProjectileCount(int, LivingEntity)` | 1 | none |
| `traveloptics:gyro_slash` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:gyro_slash` | `getFlameJetDamage(int, LivingEntity)` | 1 | `f2i ×1; fadd ×1; fmul ×1` |
| `traveloptics:nullflare` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:cursed_revenants` | `getDraugrDamage(int, LivingEntity)` | 1 | `fmul ×1` |
| `traveloptics:despair` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:halberd_horizon` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |
| `traveloptics:rapid_laser` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1` |
| `traveloptics:death_laser` | `getDamage(int, LivingEntity)` | 1 | `fmul ×1` |
| `traveloptics:em_pulse` | `getDuration(int, LivingEntity)` | 1 | `f2i ×1; fmul ×1` |
| `traveloptics:stele_cascade` | `getDamage(int, LivingEntity)` | 1 | `fadd ×1; fmul ×1` |

For these methods, the exact provider-side entity dependency is bounded to the host spell-power result. The arithmetic op counts do not define a formula and no constants are retained.

## Family B — host spell power + SUMMON_DAMAGE

These **9** summon-damage methods additionally query Iron's `AttributeRegistry.SUMMON_DAMAGE`.

The retained dependency pattern is:

- host `getSpellPower(int, Entity)`;
- `LivingEntity.getAttributes()`;
- `AttributeMap.hasAttribute(...)`;
- `LivingEntity.getAttributeValue(...)`;
- Iron's `AttributeRegistry.SUMMON_DAMAGE`;
- exactly one branch.

| Registry ID | Exact accessor | Entity loads |
| --- | --- | ---: |
| `traveloptics:eternal_sentinel` | `getGolemDamage(int, LivingEntity)` | 3 |
| `traveloptics:ignited_onslaught` | `getBerserkerDamage(int, LivingEntity)` | 3 |
| `traveloptics:ignited_onslaught` | `getRevenantDamage(int, LivingEntity)` | 3 |
| `traveloptics:summon_desert_dwellers` | `getKoboletonDamage(int, LivingEntity)` | 3 |
| `traveloptics:summon_desert_dwellers` | `getWadjetDamage(int, LivingEntity)` | 3 |
| `traveloptics:sword_of_the_ancients` | `getKobolediatorDamage(int, LivingEntity)` | 3 |
| `traveloptics:axe_of_the_doomed` | `getAptrgangrDamage(int, LivingEntity)` | 3 |
| `traveloptics:mechanized_predator` | `getWatcherDamage(int, LivingEntity)` | 3 |
| `traveloptics:mechanized_predator` | `getProwlerDamage(int, LivingEntity)` | 3 |

This proves that summon-damage output is not governed only by ordinary spell power. It also depends on the host summon-damage attribute surface when available. No numeric coefficient or branch semantics are inferred.

## Family C — host spell power + bounded Math.min

One method is structurally distinct:

| Registry ID | Exact accessor | Entity loads | Additional member | Arithmetic |
| --- | --- | ---: | --- | --- |
| `traveloptics:aerial_collapse` | `getDamage(int, LivingEntity)` | 1 | `java.lang.Math.min(float,float)` | `fadd ×1; fmul ×1` |

It has:

- no field refs;
- no branch;
- entity dependency through host `getSpellPower(int, Entity)`;
- one additional `Math.min(float,float)` call.

This establishes the presence of a bounded minimum/clamp-like operation but does **not** establish its operands, threshold or damage formula.

## Current Iron's host dependency layer

Current host authority remains Iron's Spellbooks `1.21.1-3.16.3`, physical SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`, with public source pin `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`.

At that pin, `AbstractSpell.getSpellPower(int, Entity)` depends on:

1. spell base/per-level power;
2. LivingEntity global `SPELL_POWER`;
3. current school power;
4. effective `POWER_MULTIPLIER`.

The exact File-`6342780` mechanics baseline supplies the provider base/per-level power inputs. Final entity-dependent outputs still require live entity attributes/config and, for Family B, summon-damage attribute state.

## Catalog consequence

After this checkpoint:

- **34/34** entity-reading numeric accessors have a bounded dependency map;
- **30/33** exact spell identities own at least one entity-reading accessor and are now dependency-classified at that surface;
- the three exact spell identities without an `ENTITY_SLOT_READ` accessor remain `blackout`, `cursed_minefield` and `cursed_blast`;
- File-only numeric scalar closure remains **37 outputs across 24/33** identities;
- current-host effective-cast bridge remains **7 results**;
- numeric accessor/bridge identity coverage remains **28/33**;
- the remaining entity-dependent methods still have no entity-independent numeric return assigned;
- no final damage, duration, count, range, PvP/boss rule or current-physical stat is inferred.

The previous five-identity dependency checkpoint remains valid as a historical subset, but this file supersedes it for the complete `ENTITY_SLOT_READ` dependency surface.

No result is projected to current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

Traveloptics remains **⚠️ partial/conditioned** and strict current-physical contribution remains **+0**.
