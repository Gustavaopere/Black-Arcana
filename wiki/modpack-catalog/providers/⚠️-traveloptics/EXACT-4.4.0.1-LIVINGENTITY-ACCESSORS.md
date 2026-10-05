# T.O Magic n' Extras 4.4.0.1 — LivingEntity accessor checkpoint

Status: `EXACT FILE 6342780 / 49 NUMERIC LIVINGENTITY ACCESSORS CLASSIFIED / 8 EXACT VALUES / 41 UNRESOLVED`

## Authority

This checkpoint derives from two temporary **NON-MERGE** clean-room audits against exact publisher File `6342780`:

- CurseForge project/file: `1046916 / 6342780`;
- exact SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- LivingEntity classification PR **#616**:
  - HEAD: `294e6441475bbc8e7a61ebf22423bd4638ebe177`;
  - workflow run: `37246922722` — **SUCCESS**;
  - artifact: `11319870514`;
  - digest: `sha256:9b6b47ae19b0d2288d13b6d1a124376e0fba9e460107ba93b1d7083e41b2d3ce`;
  - result: **49 targets / 15 ENTITY_UNUSED / 34 ENTITY_SLOT_READ**;
- entity-unused scalar PR **#617**:
  - authoritative HEAD: `54bbb4d91e336e8a8b865ed1855dd616dda954e8`;
  - workflow run: `37247139145` — **SUCCESS**;
  - artifact: `11319088574`;
  - digest: `sha256:2223139cf8d43acff7c3841d1de322e6e8c0b2064b2e461826ab5449a29eebef`;
  - result: **15 targets / 8 OK / 7 UNKNOWN**.

The candidate surface comes from method-signature audit **#608**. Only numeric accessors carrying exactly one `LivingEntity` parameter were considered.

## Classification semantics

`ENTITY_UNUSED` is emitted only when the JVM local slot assigned to the `LivingEntity` parameter is never loaded by the exact method.

`ENTITY_SLOT_READ` means the parameter local slot is loaded at least once. This is deliberately conservative:

- it proves the method is not eligible for entity-independent scalar evaluation;
- it does **not** claim which entity attribute/state is read;
- it does **not** reconstruct or retain a damage/range/duration formula.

Only `ENTITY_UNUSED` methods entered the follow-up straight-line evaluator.

## Exact classification — 49 methods

| Concrete class | Accessor | Entity loads | Classification |
| --- | --- | ---: | --- |
| `BloodHowlSpell` | `getRecastCount(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `BloodHowlSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `AbyssalBlastSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `AbyssalBlastSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `BlackoutSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `PsychicBoltSpell` | `getRecastCount(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `PsychicBoltSpell` | `getEffectDuration(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `ReversalSpell` | `calculateDamageMultiplier(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `SpectralBlinkSpell` | `getEffectLevel(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `EternalSentinelSpell` | `getGolemDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `OrbitalVoidSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `CursedMinefieldSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `VoidEruptionSpell` | `getRecastCount(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `VoidEruptionSpell` | `getRange(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `VoidEruptionSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `VortexPunchSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `VortexPunchSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `AstralSenseSpell` | `getDuration(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `AshenBreathSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `LingeringStrainSpell` | `getDuration(LivingEntity, int)` | 1 | `ENTITY_SLOT_READ` |
| `IgnitedOnslaughtSpell` | `getBerserkerDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `IgnitedOnslaughtSpell` | `getRevenantDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `BurningJudgmentSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `MeteorStormSpell` | `getDamage(LivingEntity, int)` | 1 | `ENTITY_SLOT_READ` |
| `LavaBombSpell` | `getProjectileCount(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `GyroSlashSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `GyroSlashSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `GyroSlashSpell` | `getFlameJetDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `NullflareSpell` | `getRecastCount(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `NullflareSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `SummonDesertDwellers` | `getKoboletonDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `SummonDesertDwellers` | `getWadjetDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `SwordOfTheAncientsSpell` | `getKobolediatorDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `AxeOfTheDoomedSpell` | `getAptrgangrDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `CursedRevenantsSpell` | `getDraugrDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `DespairSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `DespairSpell` | `getRecastCount(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `HalberdHorizonSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `MechanizedPredatorSpell` | `getWatcherDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `MechanizedPredatorSpell` | `getProwlerDamage(int, LivingEntity)` | 3 | `ENTITY_SLOT_READ` |
| `RapidLaserSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `DeathLaserSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `DeathLaserSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `EmPulse` | `getDuration(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `EmPulse` | `getRadius(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `AerialCollapseSpell` | `getEffectiveCastTime(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `AerialCollapseSpell` | `getRadius(int, LivingEntity)` | 0 | `ENTITY_UNUSED` |
| `AerialCollapseSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |
| `SteleCascadeSpell` | `getDamage(int, LivingEntity)` | 1 | `ENTITY_SLOT_READ` |

## Exact evaluated values — 8 methods

The strict evaluator accepts only straight-line numeric constants/arithmetic and known static numeric constants. Branches, invocation, object access, unresolved fields/locals or unsupported opcodes return `UNKNOWN`.

| Registry ID | Exact accessor | File-6342780 result |
| --- | --- | --- |
| `traveloptics:blood_howl` | `BloodHowlSpell.getRecastCount(int, LivingEntity)` | L1=2, L2=3, L3=4, L4=5, L5=6 |
| `traveloptics:psychic_bolt` | `PsychicBoltSpell.getRecastCount(int, LivingEntity)` | L1=5, L2=5, L3=5 |
| `traveloptics:void_eruption` | `VoidEruptionSpell.getRecastCount(int, LivingEntity)` | L1=1, L2=2, L3=3 |
| `traveloptics:void_eruption` | `VoidEruptionSpell.getRange(int, LivingEntity)` | L1=20.0, L2=20.0, L3=20.0 |
| `traveloptics:nullflare` | `NullflareSpell.getRecastCount(int, LivingEntity)` | L1=5, L2=5, L3=5, L4=5, L5=5 |
| `traveloptics:despair` | `DespairSpell.getRecastCount(int, LivingEntity)` | L1=2, L2=3, L3=3, L4=4, L5=4, L6=5, L7=5, L8=6, L9=6, L10=7 |
| `traveloptics:em_pulse` | `EmPulse.getRadius(int, LivingEntity)` | L1=4.0, L2=6.0, L3=8.0, L4=10.0, L5=12.0 |
| `traveloptics:aerial_collapse` | `AerialCollapseSpell.getRadius(int, LivingEntity)` | L1=4.0, L2=6.0, L3=8.0, L4=10.0, L5=12.0 |

## ENTITY_UNUSED but evaluator-UNKNOWN — 7 methods

These methods do not read the `LivingEntity` argument, but the strict evaluator encountered instance-object access (`aload_0`) and refused to infer the result:

- `AbyssalBlastSpell.getEffectiveCastTime(int, LivingEntity)`;
- `BlackoutSpell.getEffectiveCastTime(int, LivingEntity)`;
- `CursedMinefieldSpell.getEffectiveCastTime(int, LivingEntity)`;
- `VortexPunchSpell.getEffectiveCastTime(int, LivingEntity)`;
- `GyroSlashSpell.getEffectiveCastTime(int, LivingEntity)`;
- `DeathLaserSpell.getEffectiveCastTime(int, LivingEntity)`;
- `AerialCollapseSpell.getEffectiveCastTime(int, LivingEntity)`.

No effective-cast-time value is assigned from this audit.

## Evidence boundary

All facts here are exact for publisher File `6342780` only.

They are **not** projected to current physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

For the 34 `ENTITY_SLOT_READ` methods, no damage/range/duration/count/formula value is inferred. For the seven evaluator-UNKNOWN methods, no effective cast-time value is inferred.

This checkpoint does not close:

- current-physical stat equality;
- final damage formulas;
- effective host/config multipliers;
- PvP/boss rules;
- `traveloptics:blackout` acquisition;
- current physical loot-modifier provenance/wiring.

Traveloptics remains **⚠️ partial/conditioned** and strict current-physical contribution remains **+0**.
