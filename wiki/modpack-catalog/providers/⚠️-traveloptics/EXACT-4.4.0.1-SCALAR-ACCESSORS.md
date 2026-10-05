# T.O Magic n' Extras 4.4.0.1 — exact publisher scalar-accessor checkpoint

Status: `EXACT FILE 6342780 / 29 BOUNDED ACCESSORS / 29 OK / CURRENT PHYSICAL NOT PROJECTED`

## Authority

This checkpoint derives from two temporary NON-MERGE clean-room audits against the exact publisher artifact:

- CurseForge project/file: `1046916 / 6342780`;
- exact SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- method-surface audit PR **#608**:
  - authoritative HEAD: `9ac1ed6adafa3012bd2fb0c12580996458b1a660`;
  - workflow run: `37239537679` — **SUCCESS**;
  - artifact: `11317320326`;
  - digest: `sha256:090d8fb6b055253e41ca7ca2739d739be9b57669c09236d05485c8cee5c4fee8`;
- bounded scalar audit PR **#609**:
  - authoritative HEAD: `ce1121071381900178202454687a329349da9605`;
  - workflow run: `37239919430` — **SUCCESS**;
  - artifact: `11317076423`;
  - digest: `sha256:c5936eae280589d07d2ba3c684422ec7bd92b088f9f193236242b71b33b46e56`.
- remaining simple-accessor audit PR **#613**:
  - authoritative HEAD: `f4f31b3a0e88a4c8a7c608db3dc42a0c79d09463`;
  - workflow run: `37243561977` — **SUCCESS**;
  - artifact: `11317109960`;
  - digest: `sha256:ac3b0b8a7e6ac8137094defe89d21d73263e50cf5cd4a4c8d07a599eebb64726`;
  - 15 targets / 15 OK / 0 UNKNOWN.

The method-surface audit established the declared accessors. Audits #609 and #613 then evaluated the full selected set of 29 numeric `()` / `(int)` no-`LivingEntity` accessors through the same strict straight-line JVM subset. Unsupported control flow, invocation, unresolved fields/locals or unsupported opcodes would have returned `UNKNOWN`.

Combined result: **29 targets / 29 OK / 0 UNKNOWN**.

## Retention boundary

Only the following are retained:

- exact class identity;
- exact method identity/descriptor;
- evaluated numeric return values for valid spell levels, or the single constant value where the accessor has no level parameter.

No bytecode instructions, method bodies, source reconstruction, assets, localization prose or binary content are retained.

## Interpretation boundary

These are **exact raw accessor outputs for publisher File `6342780` only**.

They are not automatically:

- blocks;
- ticks;
- seconds;
- hearts;
- final damage;
- final entity health after modifiers;
- deployed-config values;
- current-physical values.

A semantic unit is not assigned merely from a method name. Counts are retained as counts; all other values remain raw accessor outputs unless another exact contract independently establishes their unit/meaning.

Nothing here is projected to current physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

## Exact scalar accessors

| Registry ID | Exact accessor | Raw exact File-6342780 result |
| --- | --- | --- |
| `traveloptics:blackout` | `BlackoutSpell.getRadius(int)` | L1=8.0, L2=10.0, L3=12.0 |
| `traveloptics:blackout` | `BlackoutSpell.getEffectDuration(int)` | L1=30.0, L2=30.0, L3=30.0 |
| `traveloptics:blackout` | `BlackoutSpell.getAntiMagicZoneDuration(int)` | L1=160.0, L2=200.0, L3=240.0 |
| `traveloptics:orbital_void` | `OrbitalVoidSpell.getOrbCount(int)` | L1=3, L2=6, L3=9, L4=12, L5=15 |
| `traveloptics:vortex_punch` | `VortexPunchSpell.getDuration()` | 25 |
| `traveloptics:astral_sense` | `AstralSenseSpell.getRadius(int)` | L1=25.0, L2=30.0, L3=35.0 |
| `traveloptics:burning_judgment` | `BurningJudgmentSpell.getDuration(int)` | L1=40.0, L2=80.0, L3=120.0, L4=160.0, L5=200.0, L6=240.0 |
| `traveloptics:meteor_storm` | `MeteorStormSpell.getDuration(int)` | L1=220, L2=280, L3=340, L4=400, L5=460, L6=520 |
| `traveloptics:nullflare` | `NullflareSpell.getRange(int)` | L1=4.0, L2=6.0, L3=8.0, L4=10.0, L5=12.0 |
| `traveloptics:nullflare` | `NullflareSpell.getEffectDuration()` | 200.0 |
| `traveloptics:cursed_blast` | `CursedBlastSpell.getRange()` | 30.0 |
| `traveloptics:cursed_blast` | `CursedBlastSpell.getDamage()` | 2.0 |
| `traveloptics:mechanized_predator` | `MechanizedPredatorSpell.getWatcherCount(int)` | L1=1.0, L2=2.0, L3=3.0, L4=4.0, L5=5.0 |
| `traveloptics:eternal_sentinel` | `EternalSentinelSpell.getGolemHealth(int)` | L1=90.0, L2=135.0, L3=180.0 |
| `traveloptics:ignited_onslaught` | `IgnitedOnslaughtSpell.getBerserkerHealth(int)` | L1=33.0, L2=41.0, L3=49.0, L4=57.0, L5=65.0 |
| `traveloptics:ignited_onslaught` | `IgnitedOnslaughtSpell.getRevenantHealth(int)` | L1=40.0, L2=50.0, L3=60.0, L4=70.0, L5=80.0 |
| `traveloptics:burning_judgment` | `BurningJudgmentSpell.getFlameStrikeCount(int)` | L1=2.0, L2=3.0, L3=4.0, L4=5.0, L5=6.0, L6=7.0 |
| `traveloptics:lava_bomb` | `LavaBombSpell.getMotionScale()` | 1.0 |
| `traveloptics:summon_desert_dwellers` | `SummonDesertDwellers.getKoboletonCount(int)` | L1=1.0, L2=2.0, L3=3.0, L4=4.0, L5=5.0 |
| `traveloptics:summon_desert_dwellers` | `SummonDesertDwellers.getKoboletonHealth(int)` | L1=5.0, L2=10.0, L3=15.0, L4=20.0, L5=25.0 |
| `traveloptics:summon_desert_dwellers` | `SummonDesertDwellers.getWadjetHealth(int)` | L1=70.0, L2=90.0, L3=110.0, L4=130.0, L5=150.0 |
| `traveloptics:sword_of_the_ancients` | `SwordOfTheAncientsSpell.getKobolediatorHealth(int)` | L1=90.0, L2=125.0, L3=160.0 |
| `traveloptics:axe_of_the_doomed` | `AxeOfTheDoomedSpell.getAptrgangrHealth(int)` | L1=70.0, L2=115.0, L3=160.0 |
| `traveloptics:cursed_revenants` | `CursedRevenantsSpell.getDraugrCount(int)` | L1=1.0, L2=2.0, L3=3.0, L4=4.0, L5=5.0 |
| `traveloptics:cursed_revenants` | `CursedRevenantsSpell.getDraugrHealth(int)` | L1=8.0, L2=13.0, L3=18.0, L4=23.0, L5=28.0 |
| `traveloptics:halberd_horizon` | `HalberdHorizonSpell.getRingCount(int)` | L1=2, L2=3, L3=4, L4=5, L5=6, L6=7 |
| `traveloptics:mechanized_predator` | `MechanizedPredatorSpell.getWatcherHealth(int)` | L1=5.0, L2=10.0, L3=15.0, L4=20.0, L5=25.0 |
| `traveloptics:mechanized_predator` | `MechanizedPredatorSpell.getProwlerHealth(int)` | L1=80.0, L2=100.0, L3=120.0, L4=140.0, L5=160.0 |
| `traveloptics:stele_cascade` | `SteleCascadeSpell.getRingsAndRows(int)` | L1=1, L2=2, L3=3, L4=4, L5=5, L6=6 |

## Catalog consequence

This checkpoint deepens **18/33** spell cards and closes all **29** selected numeric `()` / `(int)` no-`LivingEntity` accessors from the #608 method surface.

It does not:

- close final damage formulas;
- assign units to raw duration/range/radius values;
- close PvP/boss rules;
- close effective config/multiplier behavior;
- close current-physical stat equality;
- close `traveloptics:blackout` survival acquisition;
- close current physical loot-modifier wiring/provenance.

Traveloptics therefore remains **⚠️ partial/conditioned** and contributes **+0 strict** for the current physical artifact.
