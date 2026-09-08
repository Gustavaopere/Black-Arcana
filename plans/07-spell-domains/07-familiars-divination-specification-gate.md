# 07.07 — Familiars & Divination Specification Gate

## State

`PLANNING / REQUIRED BEFORE 07.07 CANONICAL COMPLETION / NO RUNTIME IMPLEMENTATION`

Planning baseline: `main@8af81c925a6d6d725e1663de516fc20b393ec207`.

This document closes an ambiguity in Stage 07.07: an approved fantasy or a preparatory candidate entry is not automatically a complete spell specification.

`plans/07-spell-domains/README.md` requires every Stage 07 spell specification to state:

1. fantasy;
2. host integration;
3. invocation;
4. target rules;
5. resource cost;
6. cooldown;
7. scaling equation;
8. progression gate;
9. world-effect mode;
10. boss/PvP behavior;
11. config surface;
12. tests;
13. provenance link.

The current source of Noetic candidate intent is `docs/design/candidate-specifications.md`. That file explicitly marks exact numeric balance as Stage 08 work. Current production code/tests prevail for what is already implemented.

No value may be promoted from a safety ceiling, descriptive candidate phrase or provider theme into a final balance contract without an explicit Stage 08 decision.

## Classification

- `FROZEN / CURRENT` — production `main` already supplies the relevant authority/behavioral boundary.
- `PREPARATORY` — the candidate specification states the intended behavior/class, but the final Stage 07/08 contract is not frozen.
- `MISSING / BLOCKER` — the required field is not sufficiently specified to serve as canonical Stage 08 input.
- `N/A BY DESIGN` — the mechanic deliberately has no such behavior, and that absence itself must be preserved.

A spell is not specification-complete while any required field remains `MISSING / BLOCKER` or while a `PREPARATORY` field still controls gameplay balance/authority that Stage 08 needs.

## Current runtime baseline

The merged Noetic substrate currently recognizes four observation kinds:

- `ASTRAL_SEVERANCE`;
- `NAMESCRY`;
- `BORROWED_SIGHT`;
- `OCCULT_APPRAISAL`.

The merged substrate also contains Gaze of Stillness / Nullifying Gaze runtime and Pact Sanctuary runtime contracts.

`NoeticSafetyCeilings` provides absolute implementation safety ceilings, including a generic observation maximum range of 128 blocks and maximum duration of 600 ticks. The class explicitly states Stage 08 may tune below those ceilings. They are **not** the spells' final range/duration values.

## Gate matrix

### Astral Severance

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | PREPARATORY | Controllable non-combat astral viewpoint/avatar while the physical body remains server-side and vulnerable. |
| Host integration | PREPARATORY | Black Arcana core owns the mechanic; Eidolon flavor/integration is only optional intent, not a verified required bridge. |
| Invocation | PREPARATORY | Candidate design requires a channeled projection. Exact activation/release interaction is not frozen. |
| Target rules | PREPARATORY | Projection is centered on the caster/body relationship, bounded by loaded-only same-dimension/range authority; canonical avatar identity is still missing. |
| Resource cost | MISSING / BLOCKER | Only the class `channel/resource drain` is stated. Resource authority and amount are not frozen. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown contract/value is frozen. |
| Scaling equation | MISSING / BLOCKER | No scaling equation is frozen. Safety ceilings must not be used as a substitute. |
| Progression gate | PREPARATORY | Candidate tier is T3; final progression/mastery gate remains Stage 08 input. |
| World-effect mode | PREPARATORY | Default plan is no terrain mutation and no remote world interaction. Exact canonical mode must be frozen before implementation. |
| Boss/PvP behavior | PREPARATORY | Projection is non-combat by default; body remains vulnerable. No offensive PvP bypass is authorized. |
| Config surface | MISSING / BLOCKER | No canonical config keys/ranges are frozen. |
| Tests | PREPARATORY | Range return, body-damage interruption, logout restoration and dimension-change denial are required candidate tests; expanded lifecycle tests are defined in `07-familiars-divination.md`. |
| Provenance link | MISSING / BLOCKER | Candidate specification exists, but the final per-spell provenance link/ledger entry required for canonical completion is not frozen here. |

**Completion blocker:** canonical bounded astral avatar/viewpoint lifecycle plus the missing balance/config/provenance fields.

### Namescry

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | PREPARATORY | Limited remote perception of an explicitly resolved loaded target under server policy. |
| Host integration | PREPARATORY | Eidolon ritual or Black Arcana core are candidate hosts; no mandatory provider bridge is frozen. |
| Invocation | PREPARATORY | Candidate design is a channel using a focus item plus resource; exact invocation surface is not frozen. |
| Target rules | FROZEN / CURRENT + PREPARATORY | Current policy is loaded-only, same-dimension, in-range, live target and explicit player consent; the candidate additionally requires limited remote data. |
| Resource cost | MISSING / BLOCKER | `focus item + mana/channel` is only a cost class; provider/resource authority and amount are not frozen. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown contract/value is frozen. |
| Scaling equation | MISSING / BLOCKER | No scaling equation is frozen. |
| Progression gate | PREPARATORY | Candidate tier is T3; final gate remains Stage 08 input. |
| World-effect mode | PREPARATORY | Read-only perception/no force-load is the intended boundary; no terrain mutation is justified. |
| Boss/PvP behavior | PREPARATORY | Player observation requires explicit server-authorized consent/privacy policy; additional PvP/server-policy details remain to freeze. |
| Config surface | MISSING / BLOCKER | No canonical config surface is frozen. |
| Tests | PREPARATORY | Unloaded/cross-dimension denial, privacy, interruption and bounded data/range tests are required. |
| Provenance link | MISSING / BLOCKER | Final per-spell provenance link is not frozen. |

### Gaze of Stillness

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | PREPARATORY | Reciprocal facing/LOS maintains bounded movement suppression. |
| Host integration | PREPARATORY | Iron's active-spell presentation plus Black Arcana CC policy is candidate intent; provider bridge details must remain evidence-based. |
| Invocation | PREPARATORY | Maintained gaze/channel semantics are intended; exact cast/channel contract is not frozen by the candidate document. |
| Target rules | FROZEN / CURRENT + PREPARATORY | Current Noetic gaze runtime/policy supplies bounded gaze safety; candidate requires facing/LOS and escape by breaking them. |
| Resource cost | MISSING / BLOCKER | `mana per tick` is only a class; amount and provider transaction contract are not frozen. |
| Cooldown | MISSING / BLOCKER | Post-channel cooldown is intended, but no canonical value/group is frozen. |
| Scaling equation | MISSING / BLOCKER | No final CC/scaling curve is frozen. |
| Progression gate | PREPARATORY | Candidate tier is T2; final gate remains Stage 08 input. |
| World-effect mode | N/A BY DESIGN / PREPARATORY | Entity-control effect only; no terrain mutation is authorized by the candidate. |
| Boss/PvP behavior | PREPARATORY | Diminishing returns and boss/player duration multipliers are required; exact multipliers remain Stage 08 work. |
| Config surface | MISSING / BLOCKER | Safety ceilings exist, but final tunable config surface is not frozen. |
| Tests | PREPARATORY | Facing/LOS, escape, reapplication immunity and boss/PvP policy tests are required. |
| Provenance link | MISSING / BLOCKER | Final per-spell provenance link is not frozen. |

### Nullifying Gaze

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | PREPARATORY | Remove/suppress only explicitly registered nullifiable effects/mechanics. |
| Host integration | PREPARATORY | Iron's presentation plus explicit Black Arcana/provider adapters is candidate intent. |
| Invocation | PREPARATORY | Gaze/channel is intended; exact invocation contract remains to freeze. |
| Target rules | FROZEN / CURRENT + PREPARATORY | Current nullification registry is allowlist-oriented; unknown/protected effects must remain untouched. |
| Resource cost | MISSING / BLOCKER | `mana/channel` is only a class; amount/authority are not frozen. |
| Cooldown | MISSING / BLOCKER | Cooldown is intended but no canonical value/group is frozen. |
| Scaling equation | MISSING / BLOCKER | No final nullification count/duration/scaling equation is frozen. |
| Progression gate | PREPARATORY | Candidate tier is T3; final gate remains Stage 08 input. |
| World-effect mode | N/A BY DESIGN / PREPARATORY | Effect/state interaction only; no terrain mutation is authorized. |
| Boss/PvP behavior | PREPARATORY | Protected effects and boss resistance are required; exact policy remains to freeze. |
| Config surface | MISSING / BLOCKER | Safety ceilings/allowlist bounds are not themselves a complete balance config surface. |
| Tests | PREPARATORY | Approved effect removed, protected/unknown effect untouched and boss-policy tests are required. |
| Provenance link | MISSING / BLOCKER | Final per-spell provenance link is not frozen. |

### Occult Appraisal

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | PREPARATORY | Reveal a bounded whitelist of approved target metadata rather than arbitrary state. |
| Host integration | PREPARATORY | Core/Iron's presentation is candidate intent; no mandatory provider bridge is frozen. |
| Invocation | PREPARATORY | Small channel/mana is intended; exact input/cast contract remains to freeze. |
| Target rules | FROZEN / CURRENT + PREPARATORY | Current observation policy requires loaded, same-dimension, live, in-range target and LOS for appraisal; snapshot output is whitelisted. |
| Resource cost | MISSING / BLOCKER | `small channel/mana` is qualitative only. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown contract/value is frozen. |
| Scaling equation | MISSING / BLOCKER | No scaling equation or metadata-unlock curve is frozen. |
| Progression gate | PREPARATORY | Candidate tier is T2; final gate remains Stage 08 input. |
| World-effect mode | N/A BY DESIGN | Read-only presentation; no terrain mutation or arbitrary capability mutation is authorized. |
| Boss/PvP behavior | PREPARATORY | Privacy restrictions apply; player/container exposure must remain explicitly authorized. Exact PvP surface remains to freeze. |
| Config surface | MISSING / BLOCKER | No canonical metadata/config surface is frozen beyond current hard safety bounds/whitelist behavior. |
| Tests | PREPARATORY | Metadata whitelist, player/container restrictions and no-hidden-NBT-leak tests are required. |
| Provenance link | MISSING / BLOCKER | Final per-spell provenance link is not frozen. |

### Borrowed Sight

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | FROZEN / CURRENT | Viewpoint of an owned familiar or explicitly consenting bonded target while server session remains authoritative. |
| Host integration | FROZEN / CURRENT + PREPARATORY | Black Arcana owns session/camera authority; verified Ars familiar ownership adapter exists. Other familiar providers require their own verified ownership adapters. |
| Invocation | PREPARATORY | Channeled viewing is the intended spell interaction, but the current production camera path does not by itself freeze Stage 08 resource/channel values. |
| Target rules | FROZEN / CURRENT | Loaded-only, same dimension, hard range, live target; owned familiar or explicit consent; active sessions are continuously revalidated. |
| Resource cost | MISSING / BLOCKER | `mana/channel + range` is qualitative candidate intent; exact resource authority/amount remains unfrozen. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown value/group is frozen for Stage 08. |
| Scaling equation | MISSING / BLOCKER | No final range/duration/resource scaling equation is frozen. |
| Progression gate | PREPARATORY | Candidate tier is T2; final gate remains Stage 08 input. |
| World-effect mode | N/A BY DESIGN / FROZEN | Current production path changes camera presentation only and does not authorize terrain/world interaction. |
| Boss/PvP behavior | FROZEN / CURRENT + PREPARATORY | Arbitrary hostile-player observation is denied; player observation requires explicit server-authorized consent. Additional balance policy remains to freeze. |
| Config surface | MISSING / BLOCKER | Current safety ceilings are not the final spell config surface. |
| Tests | FROZEN / CURRENT + PREPARATORY | Automated server/client transport contracts exist; real-client camera feel/restoration is still deferred, and candidate ownership/unload/logout cases remain acceptance requirements. |
| Provenance link | MISSING / BLOCKER | Final per-spell provenance linkage required by Stage 07 is not frozen. |

**Important:** implemented camera transport does not make Borrowed Sight specification-complete for Stage 08.

### Pact Sanctuary

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | FROZEN / CURRENT + PREPARATORY | Familiar-centered bounded sanctuary/aura suppresses hostility from eligible ordinary mobs toward eligible members without permanent faction mutation. |
| Host integration | FROZEN / CURRENT + PREPARATORY | Black Arcana owns aura/runtime authority; familiar ownership is provider-bound through explicit adapters. Candidate intent mentions Ars familiar integration where supported. |
| Invocation | PREPARATORY | Aura activation/upkeep is intended; exact cast/ritual invocation is not frozen here. |
| Target rules | FROZEN / CURRENT + PREPARATORY | Runtime has bounded radius/member/entity processing and eligibility rules; provider ownership/target policy remains fail-closed where unsupported. |
| Resource cost | MISSING / BLOCKER | `upkeep + radius budget` is qualitative only. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown contract/value is frozen. |
| Scaling equation | MISSING / BLOCKER | No final radius/upkeep/member scaling equation is frozen. Existing safety ceilings are not balance values. |
| Progression gate | PREPARATORY | Candidate tier is T3; final gate remains Stage 08 input. |
| World-effect mode | N/A BY DESIGN / PREPARATORY | Temporary entity-AI/targeting influence only; no permanent faction or terrain mutation is authorized. |
| Boss/PvP behavior | PREPARATORY | Boss/event exclusions are required; players are not generic hostile mobs and no PvP sanctuary bypass is implied. |
| Config surface | MISSING / BLOCKER | Hard safety bounds exist, but canonical gameplay config/tuning is not frozen. |
| Tests | FROZEN / CURRENT + PREPARATORY | Runtime has bounded sanctuary contracts; candidate acceptance requires ordinary-mob suppression, boss exclusion, familiar-unload cleanup and tick-budget instrumentation. |
| Provenance link | MISSING / BLOCKER | Final per-spell provenance link is not frozen. |

## Cross-spell blockers before Stage 08

07.07 cannot become canonical Stage 08 balance input until all seven candidates have, at minimum:

- one canonical invocation route that terminates in the existing Black Arcana cast/channel pipeline where applicable;
- explicit resource authority and cost model without creating a second mana/resource;
- cooldown identity/group semantics where a cooldown exists;
- a defined scaling equation or explicit `NO SCALING` decision;
- final progression gate contract with RPG Skill Tree only through a real boundary;
- explicit world-effect classification, including `NONE/READ_ONLY` where appropriate;
- explicit boss/PvP policy;
- bounded config surface and validation ranges;
- exact tests for the final contract;
- clean-room per-spell provenance linkage.

Astral Severance additionally requires its canonical projection lifecycle to be designed and reviewed before implementation.

## Stage 08 handoff rule

Stage 08 may tune below existing safety ceilings. It must not:

- raise a value above Stage 07 hard safety ceilings without an explicit reviewed architecture/safety change;
- treat a safety ceiling as the default balance value;
- select a provider resource without verifying provider authority and transaction support;
- invent a cooldown group from a spell id;
- transfer casting, targeting, channel, privacy or projection authority to the client;
- use provider theme/similarity as evidence of an integration contract.

Until this gate is closed, Stage 07.07 remains `IN PROGRESS`, and Stage 08 remains blocked from using the Noetic family as canonical balance input.
