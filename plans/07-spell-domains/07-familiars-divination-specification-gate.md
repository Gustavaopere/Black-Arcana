# 07.07 — Familiars & Divination Specification Gate

## State

`IN PROGRESS / RUNTIME PARTIALLY IMPLEMENTED / REQUIRED BEFORE 07.07 CANONICAL COMPLETION`

Canonical runtime evidence exists for the merged Noetic substrate, Borrowed Sight camera flow, Astral Severance lifecycle, bounded Astral representation/control transport, server-authored Astral camera presentation and the strict server-owned Astral control-config authority merged by PR #242 at `e2ff0421d78f3e29f210403eeb824957b7adb2be`. This document remains the canonical completeness gate for the seven-spell family.

This document closes an ambiguity in Stage 07.07: an approved fantasy, preparatory candidate entry or partial runtime is not automatically a complete spell specification.

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

The canonical clean-room per-spell traceability map is [`docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md). It links each of the seven candidates to the existing external-reference ledger, observable-only catalog, Stage 01 disposition, Black Arcana-owned candidate specification and host-authority boundary without promoting provider theme or reference implementation details into runtime authority.

The canonical Stage 01 [`classification-matrix.md`](../../docs/reference/classification-matrix.md) freezes `World = OFF` for all seven Stage 07.07 targets: Astral Severance, Namescry, Gaze of Stillness, Nullifying Gaze, Occult Appraisal, Borrowed Sight and Pact Sanctuary. For this family, `OFF` means the spell owns no terrain/block mutation mode and gains no implicit force-load or remote world-interaction authority. Read-only perception, camera presentation and bounded temporary entity-state/AI effects do not convert that classification into a terrain-mutation mode. Any future world mutation or projection interaction requires a separate reviewed contract through the canonical Stage 04 world-safety authority.

No value may be promoted from a safety ceiling, descriptive candidate phrase, test fixture or provider theme into a final balance contract without an explicit reviewed decision.

## Classification

- `FROZEN / CURRENT` — production/runtime code already supplies the relevant authority or behavioral boundary.
- `FROZEN / CURRENT + PREPARATORY` — a meaningful runtime boundary exists, but remaining final policy/tuning is still preparatory.
- `PREPARATORY` — intended behavior/class is stated, but the final Stage 07/08 contract is not frozen.
- `MISSING / BLOCKER` — the required field is not sufficiently specified to serve as canonical Stage 08 input.
- `N/A BY DESIGN` — the mechanic deliberately has no such behavior, and that absence itself must be preserved.

A spell is not specification-complete while any required field remains `MISSING / BLOCKER` or while a `PREPARATORY` field still controls gameplay balance/authority that Stage 08 needs.

## Current runtime baseline

The Noetic substrate recognizes four observation kinds:

- `ASTRAL_SEVERANCE`;
- `NAMESCRY`;
- `BORROWED_SIGHT`;
- `OCCULT_APPRAISAL`.

The runtime also contains Gaze of Stillness / Nullifying Gaze and Pact Sanctuary contracts. Borrowed Sight has a server-authored client camera path. Astral Severance has a dedicated server-owned projection/session lifecycle, a dedicated projection entity, server-owned logical pose/movement substrate, bounded C2S MOVE/RETURN transport, server-authored S2C camera presentation, and a strict optional server-owned `ControlLimits` config authority. No production Astral control profile/default is bundled, so MOVE gameplay remains fail-closed.

`NoeticSafetyCeilings` provides absolute implementation ceilings, including a generic observation maximum range of 128 blocks and maximum duration of 600 ticks. These are safety caps, not final spell range/duration or movement values.

## Gate matrix

### Astral Severance

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | FROZEN / CURRENT + PREPARATORY | Dedicated non-owning astral representation/viewpoint is tied to the physical caster while the physical body remains authoritative and vulnerable; server-authored camera presentation is canonical while movement/look input redirection remains pending. |
| Host integration | FROZEN / CURRENT + PREPARATORY | Black Arcana owns projection/session/control authority. Eidolon flavor/integration remains optional intent, not a verified required authority bridge. |
| Invocation | PREPARATORY | Activation seam exists only downstream of an already-authorized canonical cast transaction. Exact player-facing channel activation/release and upkeep transaction are not yet wired/frozen. |
| Target rules | FROZEN / CURRENT | Projection identity is server-generated and bound to one physical caster; generic observed-entity Astral admission is rejected; server movement is same-session, range-bounded and loaded-only. |
| Resource cost | MISSING / BLOCKER | Only the class `channel/resource drain` is stated. Resource authority and amount are not frozen. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown contract/value/group is frozen. |
| Scaling equation | MISSING / BLOCKER | No final range/duration/movement/resource scaling equation is frozen. Safety ceilings and test fixture values must not substitute for it. |
| Progression gate | PREPARATORY | Candidate tier is T3; final progression/mastery gate remains Stage 08 input through the RPG Skill Tree boundary only. |
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Current runtime authorizes no terrain/block mutation or remote interaction, projection movement is loaded-only and no chunk is force-loaded. Any future interaction or mutation requires a separate reviewed Stage 04-backed contract. |
| Boss/PvP behavior | FROZEN / CURRENT + PREPARATORY | Projection is non-combat/non-owning; physical body remains vulnerable; no offensive attribution or PvP bypass is authorized. Final server/PvP tuning remains open. |
| Config surface | FROZEN / CURRENT + PREPARATORY | PR #242 freezes the strict server-owned schema/reload authority for `black_arcana:astral_severance` `ControlLimits`, with absent config explicitly fail-closed and hard Noetic ceilings used only as upper validation bounds. No production `maxStepBlocks` / `maxLookDeltaDegrees` profile or default is bundled or frozen; final tuning remains Stage 08 input. |
| Tests | FROZEN / CURRENT + PREPARATORY | Automated lifecycle, identity, movement, loaded-only, entity wiring, payload validation/round-trip, camera presentation/restoration, strict config-authority parsing/reload and dedicated-server coverage exist. Canonical cast/channel wiring, movement/look input redirect and real-client coexistence acceptance remain required. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Astral Severance to the observable `Mental Displacement` fantasy, the `REIMAGINE` decision, the Black Arcana-owned candidate spec and the `CORE + PROBE` host boundary; Mahou code/assets are explicitly excluded. |

**Current Astral boundary:** PR #138 canonically merged the dedicated lifecycle; PR #235 merged the dedicated projection representation, server movement substrate and C2S MOVE/RETURN transport at `29454a7dd604ba0ea0200724d53bd9526b09cb10`; PR #240 merged the server-authored S2C camera presentation at `834c3f7e2c236161e04e21c1e690ca9e0503a39b`; and PR #242 merged the strict fail-closed server-owned control-config authority at `e2ff0421d78f3e29f210403eeb824957b7adb2be`. RETURN is wired to production runtime. The camera path is canonical. MOVE is registered/validated/rate-limited but its production gameplay handler remains fail-closed because PR #242 intentionally bundles no production control profile/default; an explicit reviewed production value contract must exist before MOVE wiring. Final PR #242 head `599e6ba3f3bb679abf2fb982601a8d91b709c885` passed push workflow `34798093347` and PR workflow `34798096283`; exact-SHA post-merge workflow `34798341265` passed the complete pipeline and published canonical QA artifact `black-arcana-e2ff0421d78f3e29f210403eeb824957b7adb2be` (artifact `10330163687`, SHA-256 `a9d5b656b98f945677596dfbfdcbc570f9153a1dd3c37f226c16498a727e80b3`). Movement/look input redirection and canonical cast/channel transaction wiring are still missing.

### Namescry

| Required field | Status | Current supported statement |
|---|---|---|
| Fantasy | PREPARATORY | Limited remote perception of an explicitly resolved loaded target under server policy. |
| Host integration | PREPARATORY | Eidolon ritual or Black Arcana core are candidate hosts; no mandatory provider bridge is frozen. |
| Invocation | PREPARATORY | Candidate design is a channel using a focus item plus resource; exact invocation surface is not frozen. |
| Target rules | FROZEN / CURRENT + PREPARATORY | Current policy is loaded-only, same-dimension, in-range, live target and explicit player consent; the candidate additionally requires limited remote data. |
| Resource cost | MISSING / BLOCKER | `focus item + mana/channel` is only a cost class; provider/resource authority and amount are not frozen. |
| Cooldown | MISSING / BLOCKER | No canonical cooldown value/group is frozen. |
| Scaling equation | MISSING / BLOCKER | No scaling equation is frozen. |
| Progression gate | PREPARATORY | Candidate tier is T3; final gate remains Stage 08 input. |
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Namescry is read-only perception of an already-loaded authorized target; it owns no terrain/block mutation, force-loading or remote action authority. |
| Boss/PvP behavior | PREPARATORY | Player observation requires explicit server-authorized consent/privacy policy; additional PvP/server-policy details remain to freeze. |
| Config surface | MISSING / BLOCKER | No canonical config surface is frozen. |
| Tests | PREPARATORY | Unloaded/cross-dimension denial, privacy, interruption and bounded data/range tests are required. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Namescry to observable `Scrying`, the `REIMAGINE` decision, the Black Arcana-owned candidate spec and the Black Arcana-owned privacy/target authority; no Mahou implementation details are required. |

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
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Gaze of Stillness is a bounded entity-control effect only; it owns no terrain/block mutation or world-state mutation path. |
| Boss/PvP behavior | PREPARATORY | Diminishing returns and boss/player duration multipliers are required; exact multipliers remain Stage 08 work. |
| Config surface | MISSING / BLOCKER | Safety ceilings exist, but final tunable config surface is not frozen. |
| Tests | PREPARATORY | Facing/LOS, escape, reapplication immunity and boss/PvP policy tests are required. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Gaze of Stillness to observable `Binding gaze`, the `REIMAGINE` decision and the Black Arcana-owned reciprocal LOS/facing/CC contract. Iron's remains only a supported invocation surface where separately evidenced. |

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
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Nullifying Gaze is restricted to explicitly registered effect/state adapters; it owns no terrain/block mutation path and cannot use this classification to bypass protected provider/world invariants. |
| Boss/PvP behavior | PREPARATORY | Protected effects and boss resistance are required; exact policy remains to freeze. |
| Config surface | MISSING / BLOCKER | Safety ceilings/allowlist bounds are not themselves a complete balance config surface. |
| Tests | PREPARATORY | Approved effect removed, protected/unknown effect untouched and boss-policy tests are required. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Nullifying Gaze to observable `Reversion`, the `REIMAGINE` decision and the original allowlist/tag/adapter nullification policy; reference-specific invariant bypasses are explicitly rejected. |

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
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Occult Appraisal is read-only whitelisted presentation and owns no terrain/block mutation, arbitrary capability mutation or hidden-state write path. |
| Boss/PvP behavior | PREPARATORY | Privacy restrictions apply; player/container exposure must remain explicitly authorized. Exact PvP surface remains to freeze. |
| Config surface | MISSING / BLOCKER | No canonical metadata/config surface is frozen beyond current hard safety bounds/whitelist behavior. |
| Tests | PREPARATORY | Metadata whitelist, player/container restrictions and no-hidden-NBT-leak tests are required. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Occult Appraisal to observable `Insight`, the `REIMAGINE` decision and the Black Arcana-owned metadata whitelist/privacy contract; arbitrary capability/NBT exposure is explicitly excluded. |

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
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Current production path changes camera presentation only and does not authorize terrain/block mutation, force-loading or remote world interaction. |
| Boss/PvP behavior | FROZEN / CURRENT + PREPARATORY | Arbitrary hostile-player observation is denied; player observation requires explicit server-authorized consent. Additional balance policy remains to freeze. |
| Config surface | MISSING / BLOCKER | Current safety ceilings are not the final spell config surface. |
| Tests | FROZEN / CURRENT + PREPARATORY | Automated server/client transport contracts exist; real-client camera feel/restoration is still deferred, and candidate ownership/unload/logout cases remain acceptance requirements. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Borrowed Sight to observable `Shared Vision`, the `REIMAGINE` decision and the Black Arcana-owned consent/camera/session contract. Ars familiar identity remains a provider boundary, not borrowed spell logic. |

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
| World-effect mode | FROZEN / CURRENT | Stage 01 freezes `World = OFF`. Pact Sanctuary is a bounded temporary entity-AI/targeting influence only; it owns no terrain/block mutation or permanent faction mutation path. |
| Boss/PvP behavior | PREPARATORY | Boss/event exclusions are required; players are not generic hostile mobs and no PvP sanctuary bypass is implied. |
| Config surface | MISSING / BLOCKER | Hard safety bounds exist, but canonical gameplay config/tuning is not frozen. |
| Tests | FROZEN / CURRENT + PREPARATORY | Runtime has bounded sanctuary contracts; candidate acceptance requires ordinary-mob suppression, boss exclusion, familiar-unload cleanup and tick-budget instrumentation. |
| Provenance link | FROZEN / CURRENT | [`STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md) links Pact Sanctuary to observable `Familiar's Garden`, the `REIMAGINE` decision and the Black Arcana-owned bounded aura/hostility policy. Ars familiar lifecycle is consumed only through supported provider seams. |

## Cross-spell blockers before Stage 08

07.07 cannot become canonical Stage 08 balance input until all seven candidates have, at minimum:

- one canonical invocation route that terminates in the existing Black Arcana cast/channel pipeline where applicable;
- explicit resource authority and cost model without creating a second mana/resource;
- cooldown identity/group semantics where a cooldown exists;
- a defined scaling equation or explicit `NO SCALING` decision;
- final progression gate contract with RPG Skill Tree only through a real boundary;
- explicit boss/PvP policy;
- bounded config surface and validation ranges;
- exact tests for the final contract.

The clean-room per-spell provenance linkage is now frozen by [`docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md`](../../docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md). This closes traceability only and does not promote any remaining balance/runtime field.

The seven-spell world-effect classification is now frozen to `OFF` by [`docs/reference/classification-matrix.md`](../../docs/reference/classification-matrix.md). This closes only the required world-effect-mode field: it does not authorize projection interaction, force-loading, terrain/block mutation or any provider/world mutation outside a separately reviewed Stage 04-backed contract.

Astral Severance additionally still requires:

- canonical client movement/look input redirection for its dedicated projection identity; the camera presentation/restoration path itself is already canonical;
- canonical player-facing cast/channel/upkeep transaction wiring;
- an explicit reviewed production `ControlLimits` profile/value contract before the MOVE gameplay handler is installed; the server-owned config schema/authority itself is already canonical;
- completion of remaining real-client/coexistence acceptance under D031.

## Stage 08 handoff rule

Stage 08 may tune below existing safety ceilings. It must not:

- raise a value above Stage 07 hard safety ceilings without an explicit reviewed architecture/safety change;
- treat a safety ceiling or test fixture as the default balance value;
- select a provider resource without verifying provider authority and transaction support;
- invent a cooldown group from a spell id;
- transfer casting, targeting, channel, privacy or projection authority to the client;
- use provider theme/similarity as evidence of an integration contract;
- reinterpret `World = OFF` as permission for terrain mutation, force-loading or remote world interaction.

Until this gate is closed, Stage 07.07 remains `IN PROGRESS`, and Stage 08 remains blocked from using the Noetic family as canonical balance input yet.