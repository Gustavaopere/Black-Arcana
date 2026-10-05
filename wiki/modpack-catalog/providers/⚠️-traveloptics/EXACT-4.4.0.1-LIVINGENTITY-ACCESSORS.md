# T.O Magic n' Extras 4.4.0.1 — LivingEntity accessor checkpoint

Status: `EXACT FILE 6342780 / 49 NUMERIC LIVINGENTITY ACCESSORS CLASSIFIED / 8 FILE-LOCAL EXACT VALUES / 7 DIRECT-DELEGATE HOST BRIDGES / 34 ENTITY-SLOT-READ NUMERICALLY UNRESOLVED / 5 IDENTITY-GAP METHODS DEPENDENCY-CLASSIFIED`

## Authority

This checkpoint derives from three temporary **NON-MERGE** clean-room audits against exact publisher File `6342780`:

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
- effective-cast direct-delegate PR **#619**:
  - authoritative HEAD: `4ae4daea3dd3cf2e7b9e3d1b76cddaceb0ae5683`;
  - workflow run: `37249217412` — **SUCCESS**;
  - artifact: `11320511282`;
  - digest: `sha256:f1f35c1bee04ee3df73550d4609d95653551150af520d77b2ab6cc1a16123d48`;
  - result: **7 targets / 7 DIRECT_DELEGATE YES / 0 NO**.


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

## ENTITY_UNUSED direct-delegate bridge — 7 methods

Audit #619 proves that all seven previously evaluator-UNKNOWN methods are exact direct delegates to `getCastTime(level)`: one `this` load, zero provider field refs, zero branches, and `DIRECT_DELEGATE=YES` for every target.

The current Iron's Spellbooks 1.21.1-3.16.3 source pin `e4056af90302d37eb1739f5ff05020b020e6e252` establishes that `AbstractSpell.getCastTime(level)` returns `0` only for `INSTANT`, otherwise the spell's raw `castTime` field. All seven exact Traveloptics targets are `LONG`.

| Registry ID | Exact provider accessor relation | Current-host-resolved result |
| --- | --- | ---: |
| `traveloptics:abyssal_blast` | direct `getCastTime(level)` delegate | **50 ticks** |
| `traveloptics:blackout` | direct `getCastTime(level)` delegate | **39 ticks** |
| `traveloptics:cursed_minefield` | direct `getCastTime(level)` delegate | **45 ticks** |
| `traveloptics:vortex_punch` | direct `getCastTime(level)` delegate | **15 ticks** |
| `traveloptics:gyro_slash` | direct `getCastTime(level)` delegate | **25 ticks** |
| `traveloptics:death_laser` | direct `getCastTime(level)` delegate | **20 ticks** |
| `traveloptics:aerial_collapse` | direct `getCastTime(level)` delegate | **10 ticks** |

These seven values are **not counted as File-6342780-alone scalar outputs**. They require the current Iron's 3.16.3 host contract. Canonical boundary: `EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md`.

## Five identity-gap ENTITY_SLOT_READ methods — dependency-classified

Audit #623 selects one numeric `ENTITY_SLOT_READ` accessor from each spell identity still outside the File-only scalar/current-host numeric bridge coverage. All five read their LivingEntity exactly once, reference no provider field, contain no branch and invoke only host `getSpellPower(int, Entity)`.

| Registry ID | Exact accessor | Retained dependency | Arithmetic classification | Numeric disposition |
| --- | --- | --- | --- | --- |
| `traveloptics:reversal` | `calculateDamageMultiplier(int, LivingEntity)` | host `getSpellPower(int, Entity)` only | `fadd ×1; fmul ×1` | entity/config dependent — no value assigned |
| `traveloptics:spectral_blink` | `getEffectLevel(int, LivingEntity)` | host `getSpellPower(int, Entity)` only | `fmul ×1; f2i ×1; iadd ×1` | entity/config dependent — no value assigned |
| `traveloptics:ashen_breath` | `getDamage(int, LivingEntity)` | host `getSpellPower(int, Entity)` only | none | entity/config dependent — no value assigned |
| `traveloptics:lingering_strain` | `getDuration(LivingEntity, int)` | host `getSpellPower(int, Entity)` only | `imul ×1; f2i ×1; iadd ×1` | entity/config dependent — no value assigned |
| `traveloptics:rapid_laser` | `getDamage(int, LivingEntity)` | host `getSpellPower(int, Entity)` only | `fadd ×1` | entity/config dependent — no value assigned |

Current Iron's 3.16.3 source pins `getSpellPower` to spell base/per-level power × entity SPELL_POWER × school power × effective POWER_MULTIPLIER. All five File-6342780 baseline rows use spell-power inputs 1/1. The provider-side arithmetic is deliberately not reconstructed. See `EXACT-4.4.0.1-ENTITY-POWER-DEPENDENCY-CHECKPOINT.md`.

## Evidence boundary

All facts here are exact for publisher File `6342780` only.

They are **not** projected to current physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

For all 34 `ENTITY_SLOT_READ` methods, no damage/range/duration/count/formula value is inferred. Five selected identity-gap methods now have their host dependency bounded to `getSpellPower(int, Entity)`; the other entity-reading methods remain dependency-unclassified beyond their slot-read status. The seven entity-unused effective-cast methods are structurally closed as direct delegates and numerically resolved only through the separately pinned current-host bridge; they are not File-only scalar results.

This checkpoint does not close:

- current-physical stat equality;
- final damage formulas;
- effective host/config multipliers;
- PvP/boss rules;
- `traveloptics:blackout` acquisition;
- current physical loot-modifier provenance/wiring.

Traveloptics remains **⚠️ partial/conditioned** and strict current-physical contribution remains **+0**.
