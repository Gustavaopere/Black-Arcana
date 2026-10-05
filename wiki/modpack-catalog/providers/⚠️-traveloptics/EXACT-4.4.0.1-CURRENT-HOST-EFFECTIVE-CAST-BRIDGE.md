# T.O Magic n' Extras 4.4.0.1 — current-host effective-cast bridge

Status: `EXACT FILE 6342780 PROVIDER RELATION + CURRENT IRON'S 3.16.3 HOST CONTRACT / 7 EFFECTIVE CAST TIMES RESOLVED / CURRENT PHYSICAL TRAVELOPTICS NOT PROJECTED`

## Purpose

Seven exact Traveloptics `getEffectiveCastTime(int, LivingEntity)` methods were previously bounded as:

- `ENTITY_UNUSED` — the LivingEntity parameter is not read;
- evaluator-UNKNOWN — the strict File-only scalar evaluator stopped at instance-object access.

The remaining question was whether those methods merely delegate to a host accessor or perform additional provider-side arithmetic/control flow.

This checkpoint closes that question and then combines it with the **current installed Iron's Spellbooks 1.21.1-3.16.3 host contract**.

It deliberately keeps two evidence layers distinct:

1. exact publisher Traveloptics File `6342780`;
2. current Iron's host `1.21.1-3.16.3`.

It does **not** project the result onto the modified current Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

## Exact Traveloptics direct-delegate evidence

Temporary NON-MERGE audit PR **#619**, authoritative v2:

- exact artifact: CurseForge `1046916 / 6342780`;
- exact SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- HEAD: `4ae4daea3dd3cf2e7b9e3d1b76cddaceb0ae5683`;
- workflow run: `37249217412` — **SUCCESS**;
- artifact: `11320511282`;
- digest: `sha256:f1f35c1bee04ee3df73550d4609d95653551150af520d77b2ab6cc1a16123d48`;
- targets: **7**;
- `DIRECT_DELEGATE=YES`: **7**;
- `DIRECT_DELEGATE=NO`: **0**;
- provider field refs: **0**;
- branches: **0**.

The retained relation for every target is:

`getEffectiveCastTime(int, LivingEntity)` → direct delegate to `getCastTime(int)`.

No bytecode instruction sequence or method body is retained.

## Current Iron's host contract

Current physical host authority:

- JAR: `irons_spellbooks-1.21.1-3.16.3.jar`;
- runtime: `1.21.1-3.16.3`;
- physical SHA-1: `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

Matching public source pin:

- repository: `iron431/irons-spells-n-spellbooks`;
- commit: `e4056af90302d37eb1739f5ff05020b020e6e252`;
- `gradle.properties`: `mod_version=1.21.1-3.16.3`.

At that exact source pin, `AbstractSpell.getCastTime(int spellLevel)`:

- returns `0` for `CastType.INSTANT`;
- otherwise returns the spell's `castTime` field directly.

The seven target spells are all exact-alpha `CastType.LONG`, so the non-INSTANT branch applies.

## Bridged results

The exact File-`6342780` mechanics baseline already closes each target's raw/default `castTime` field.

Combining the exact provider direct-delegate relation with the current host contract yields:

| Registry ID | Exact alpha cast type | Exact alpha raw `castTime` | Exact File-6342780 method relation | Result under current Iron's 3.16.3 host |
| --- | --- | ---: | --- | ---: |
| `traveloptics:abyssal_blast` | `LONG` | 50 ticks | direct `getCastTime(level)` delegate | **50 ticks** |
| `traveloptics:blackout` | `LONG` | 39 ticks | direct `getCastTime(level)` delegate | **39 ticks** |
| `traveloptics:cursed_minefield` | `LONG` | 45 ticks | direct `getCastTime(level)` delegate | **45 ticks** |
| `traveloptics:vortex_punch` | `LONG` | 15 ticks | direct `getCastTime(level)` delegate | **15 ticks** |
| `traveloptics:gyro_slash` | `LONG` | 25 ticks | direct `getCastTime(level)` delegate | **25 ticks** |
| `traveloptics:death_laser` | `LONG` | 20 ticks | direct `getCastTime(level)` delegate | **20 ticks** |
| `traveloptics:aerial_collapse` | `LONG` | 10 ticks | direct `getCastTime(level)` delegate | **10 ticks** |

The `LivingEntity` argument is not read by these exact provider methods, so these seven provider overrides bypass the ordinary entity-dependent `AbstractSpell.getEffectiveCastTime(...)` reduction path and instead return the host `getCastTime(level)` result directly.

## Evidence boundary

These seven values are **not File-6342780-alone scalar outputs**. They are a cross-authority bridge:

- exact File-`6342780` provider method relation;
- current physical Iron's 3.16.3 host contract;
- exact File-`6342780` raw/default cast-time field.

Therefore:

- the existing File-only scalar count remains **37 resolved bounded outputs across 24/33 spell cards**;
- this checkpoint adds **7 host-resolved effective-cast-time results across 7 spell identities**;
- four of those seven spell identities were not previously present in the 37-row File-only scalar table, so combined documented accessor/bridge coverage touches **28/33** spell identities;
- no current physical Traveloptics equality is claimed;
- no value is projected onto SHA-1 `7b74816e...`;
- no player/entity cast-time-reduction modifier is inferred or applied;
- no final damage, range unit, PvP/boss rule or acquisition route is inferred.

Traveloptics remains **⚠️ partial/conditioned** and strict current-physical contribution remains **+0**.
