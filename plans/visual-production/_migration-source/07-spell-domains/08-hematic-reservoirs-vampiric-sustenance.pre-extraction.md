# 07.08 — Hematic Reservoirs & Vampiric Sustenance

## State

`PLANNED / NOT IMPLEMENTED / SEQUENCED AFTER 07.07`

This document is an implementation plan only. It does not make any reservoir, Vampirism feeding bridge, Create integration, persistence format, packet, block, multiblock or Hematic Reserve runtime canonical by itself.

Stage 07.07 remains the active incomplete Stage 07 domain. 07.08 must not be promoted into implementation ahead of 07.07 merely because this design is documented. When implementation starts, it must branch from the then-latest `main`, not from this planning branch or from the historical 07.01 implementation base.

Planning baseline used here: `main@a3b01c124ec0e9cc852e9945121795a1bfb19273`.

## Goal

Extend the canonical Blood & Curses runtime with bounded blood storage and vampire-aware blood consumption while preserving all existing Black Arcana authority and provider boundaries.

The intended player-facing behavior is:

1. blood can live in ordinary provider-owned fluid storage, including Create tanks when the exact installed API permits safe interoperability;
2. Black Arcana can additionally provide a large open-basin/multiblock Hematic Reservoir for deep pools, cisterns and lake-like constructions without requiring a wall of individual tanks;
3. a blood-magic user may bind to one eligible source through a server-owned link;
4. when the user is a Vampirism vampire and a refill is requested, blood pays Vampirism thirst first;
5. only causally proven surplus after thirst acceptance may enter the Black Arcana Hematic Reserve;
6. provider-native feeding/bites remain Vampirism-owned; Black Arcana may receive only proven surplus from a sufficiently expressive exact-version hook and must otherwise fail closed.

Canonical priority invariant:

`blood source -> Vampirism thirst acceptance -> exact surplus -> Hematic Reserve acceptance`

No path may debit blood twice, credit thirst twice, infer surplus from animation/damage, or create blood through unit rounding.

## Current canonical context

Stage 07.01 already implements Blood & Curses runtime under `src/main/java/dev/gustavopere/blackarcana/content/blood/`, including `BloodPriceCostProvider`, `BloodSafetyCeilings`, `SanguineHarvestPlanner`, `EquilibriumTransferPlanner`, `LawOfRecurrenceTracker` and the frozen `BloodDomainSpecifications`.

`BloodPriceCostProvider` is already a transactional decorator around an authoritative ordinary resource provider: it rewrites only the bounded resource portion, reserves real health separately and participates in the canonical cast transaction. 07.08 must extend this architecture rather than replacing the delegate, adding a second cast engine, or silently changing Blood Price semantics.

Relevant frozen decisions include D004 (no mandatory second mana pool), D006 (server authority), D008 (bounded power), D009 (integration boundaries), D017 (composite resource transactions), D019/D026 (bounded targeting/work), D023 (event-driven synchronization), D029/D030 (Arcane Danger authority) and D031 (deferred real-modpack acceptance does not become synthetic PASS evidence).

## Provider evidence and authority matrix

The latest physical modlist supplied to the project is authoritative for presence/version at planning time:

| Provider | Physical version / identity | Authority in 07.08 | Planning evidence status |
|---|---|---|---|
| NeoForge | `21.1.248`, mod id `neoforge` | platform capability and fluid contracts | present in physical modlist |
| Create | `6.0.10`, mod id `create`, physical SHA-1 `0e97e49837bed766e6f28a4c95b04885d6acc353` | Create machines/tanks and their native behavior | present in physical modlist |
| Create: Fluid | `2.1.5`, mod id `fluid`, physical SHA-1 `ad3e3fccf953f5b96784aefde2b6d61612e87f86` | extension-specific fluid behavior only where its exact contract is needed | present in physical modlist |
| Vampirism | `1.10.13`, mod id `vampirism`, physical SHA-1 `349b6e4ea893c98a580775b1725399903e222228` | vampire identity, player thirst/blood state and native feeding | present in physical modlist |
| Bloodlines | `1.21-3.0.9`, mod id `bloodlines`, physical SHA-1 `b14ff359c7530c0e40ca289cc023bd1c19a070af` | only Bloodlines-owned features if a future explicit bridge needs them | present in physical modlist; no 07.08 hook assumed |
| Black Arcana | current `main` | Hematic Reserve, binding identity, custom reservoir semantics, cast/resource composition and safety | canonical runtime authority |

The pertinent Notion provider audit states that Vampirism fluid blood and Vampirism player blood/thirst are separate provider surfaces and records `1 player blood unit = 100 mB` for `vampirism:blood`. The current public 1.21 `latest` API also exposes `VReference.FOOD_TO_FLUID_BLOOD = 100`, but that branch is already on Vampirism 1.10.14 and is therefore not authority for the physically installed 1.10.13.

The Notion source pin previously recorded for the Vampirism 1.21 audit does not resolve as a current GitHub commit. Therefore **the exact 1.10.13 JAR/API must be inspected before implementation**. The 100 mB conversion is a strong provider-native design lead, not permission to invent exact-version player-state or feeding hooks.

## Architectural authority

### Black Arcana owns

- the semantic concept and cap of a personal **Hematic Reserve** used only by Blood & Curses costs;
- reservoir multiblock formation, controller identity, stored amount/capacity and structural lifecycle for the custom Black Arcana reservoir;
- source binding records and link validation;
- the transaction planner that orders sinks as thirst first, reserve second;
- replay/deduplication, server-side admission, persistence, networking and diagnostics for Black Arcana-owned state;
- integration boundaries/adapters around optional providers.

### Vampirism owns

- whether a player is a vampire;
- current/max thirst or equivalent player blood state;
- the semantics of drinking/feeding/bite success;
- any provider-native feeding cooldown, target eligibility, permissions, advancement or side effect;
- any native container/feeding-adapter behavior.

Black Arcana must not mutate a guessed capability field, poll a HUD value as authority, recreate feeding eligibility, or synthesize a second bite event.

### Create / NeoForge fluid providers own

- fluid storage contents exposed through their supported transfer surface;
- native tank validity, connectivity and machine behavior;
- simulate/execute semantics of the exact available fluid handler.

A Create tank is a possible **blood source endpoint**, not the semantic owner of vampire thirst or Hematic Reserve.

## Hematic Reserve is not a second global mana pool

D004 remains intact. The Hematic Reserve is a Blood & Curses domain-specific consumable buffer, not a permanent Black Arcana-wide mana bar and not the default cost authority for unrelated spells.

Implementation must expose it behind the existing cost-provider architecture so an eligible Blood & Curses spell may compose a reserve-backed cost where its spell contract explicitly says so. The ordinary provider remains authoritative everywhere the spell definition still requires it.

Do not silently retrofit all Stage 07.01 spells to consume the reserve. Any spell that gains reserve support requires an explicit specification/balance amendment and tests showing how the reserve composes with its existing cost.

The reserve must have a hard capacity. Capacity progression, if any, belongs to Stage 08 balance/progression contracts and cannot be made unbounded by repeatedly building larger reservoirs.

## Blood source abstraction

Implementation should introduce a Black Arcana-owned boundary conceptually equivalent to a `HematicSource` without requiring core code to know Create classes.

Required source operations:

- stable source identity suitable for a persisted link;
- side-effect-free availability quote/simulation;
- exact bounded extraction request;
- execute extraction exactly once after all sink capacity is known;
- explicit failure when the source is unloaded, stale, structurally invalid, not blood, inaccessible or provider-incompatible;
- no automatic chunk loading.

Planned source families:

1. `BlackArcanaReservoirSource` — backed by the custom controller and Black Arcana-owned storage state;
2. `FluidHandlerHematicSource` — adapter over an exact-version supported NeoForge/provider fluid handler, accepting only the provider-native blood fluid/tag identity verified during implementation;
3. Create compatibility should reuse the fluid-handler boundary when the exact Create 6.0.10 surface permits that safely. A Create-specific adapter is added only if provider behavior actually requires one.

No source may be discovered by global or periodic world scans. Binding is explicit and stores a stable server-authored reference.

## Custom Hematic Reservoir multiblock

### Player-facing form

The custom reservoir is an open-basin/cistern multiblock intended to support visually deep pools, reservoirs and lake-like constructions at scales that would otherwise require many Create tanks.

Tinkers-style smeltery/furnace construction is **conceptual inspiration only**. Black Arcana must not copy Tinkers code, assets, block models, text, sounds, recipes or multiblock implementation.

### Controller authority

One controller is the sole authoritative owner of:

- structure identity/revision;
- validated interior bounds;
- capacity;
- stored blood amount;
- formation/invalid state;
- persistence dirtying and external transfer boundary.

The visible blood surface is presentation derived from controller state. It must not also be a freely drainable independent set of world `FluidState`s that duplicates the controller inventory.

### Structure model

Prefer a small number of original Black Arcana components:

- one custom Hematic Reservoir Controller;
- optionally one original casing/glass family if required for readability;
- a data/tag-driven allowlist for compatible wall/floor blocks where this preserves deterministic validation and avoids unnecessary bespoke models.

Do not make arbitrary tagged blocks valid until their geometry/occlusion behavior has been validated. Tags are a configuration surface, not a reason to accept structurally unsafe blocks.

### Bounded validation

The first release must use a bounded rectangular/orthogonal basin model with hard dimensions/volume ceilings. Exact numeric limits are implementation/balance values and must be selected with tests/performance evidence; this plan intentionally does not invent provider-derived limits.

Formation/revalidation rules:

- validation is triggered by explicit formation attempt and relevant structural changes, not every server tick;
- never scan unloaded chunks and never force-load a chunk to validate a reservoir;
- reject structures exceeding hard search/dimension/cell budgets before traversing the full candidate volume;
- one connected formed structure has one authoritative controller;
- breaking/invalidation revokes extraction until a bounded revalidation succeeds;
- controller removal must invalidate links safely and preserve/drop stored contents only according to an explicit, tested policy;
- no arbitrary natural-lake flood fill in v1.

For v1, “blood lake” means a deliberately formed, bounded Black Arcana reservoir whose interior can visually resemble a lake. Natural terrain-wide lakes and unbounded flood-fill ownership are explicitly out of scope.

## Binding contract

Binding is a server-authoritative action. The client may request a bind against a target hint; the server resolves the controller/fluid endpoint, validates range/permissions/source identity and writes the link.

A persisted link must contain only stable bounded identity, for example the logical source kind plus dimension and controller/endpoint identity/revision required to reject stale replacements. Exact serialized fields are implementation detail and must follow existing persistence conventions.

A link must never mean “search the surrounding area for blood.”

Link lifecycle:

- bind succeeds only against a loaded, valid, supported source;
- rebinding replaces the previous link intentionally;
- unlink is explicit and idempotent;
- stale/broken/unloaded/foreign-dimension links fail closed without chunk loading;
- source replacement at the same coordinates must not be accepted if its stable identity/revision proves it is a different reservoir;
- creating a successful link immediately performs at most one bounded refill attempt using the same transaction path as later manual/cast-triggered refill;
- no continuous per-tick siphon.

## Canonical refill transaction

The transaction planner must operate on server-owned state and preserve exact accounting across providers. Cross-mod state cannot be treated as magically ACID; D017 still applies.

### Preflight

1. validate player identity, link identity, source load/state, request/replay context and hard per-operation limits;
2. simulate source availability without mutation;
3. if Vampirism is installed and the exact adapter identifies the player as a vampire, query the exact current thirst deficit/acceptance through the verified provider surface;
4. query local Hematic Reserve remaining capacity;
5. convert the two sink capacities into source units with deterministic integer/fixed-point arithmetic and retained remainder state where required;
6. compute the exact source amount needed, capped by source availability and operation budget;
7. simulate exact extraction for that amount again immediately before commit.

### Commit

On the server thread and after the final recheck:

1. execute source extraction **once** for the exact planned amount;
2. apply the provider-native thirst credit up to its exact planned/accepted amount;
3. credit only the mathematically remaining exact surplus to Hematic Reserve;
4. persist/dirty Black Arcana-owned state;
5. emit event-driven presentation sync/feedback.

If the exact Vampirism API requires a different safe ordering, implementation must adapt to its real transaction semantics rather than forcing this abstract order. In particular, an adapter that cannot make its terminal mutation sufficiently reliable requires explicit escrow/compensation design before it can participate in a composite transaction.

There must be no retry path that can repeat an already executed source debit or thirst credit under the same operation identity.

### Required invariants

Let `S` be exact source units actually extracted, `T` the source-equivalent amount actually accepted by Vampirism thirst, `R` the source-equivalent amount actually credited to Hematic Reserve, and `D` explicitly retained conversion remainder.

For every successful operation:

- `0 <= T <= thirstDeficitEquivalent`;
- `0 <= R <= reserveMissingEquivalent`;
- thirst is always filled before reserve receives any amount;
- `S = T + R + delta(D)` under the chosen exact conversion representation;
- full thirst + full reserve implies `S = 0`;
- no failure path may result in `T + R > S`;
- no rounding direction may mint blood over repeated conversions.

Floating-point arithmetic is not acceptable for provider-unit conservation.

## Vampirism thirst adapter gate

Before production code is written, inspect the **exact physically installed Vampirism 1.10.13 API/JAR** and record in provenance/plan notes:

- exact public/supported method(s) for vampire identity;
- exact current/max player blood/thirst read surface;
- exact supported mutation/feeding surface for adding blood, including clamping/side effects;
- thread/server requirements;
- whether simulation/acceptance can be determined without mutating;
- whether the fluid/player conversion constant in this release is exactly the expected provider-native value;
- whether the API contract makes a reserve-first rollback impossible, requiring a different safe transactional composition.

Until those points are verified, the Vampirism sink adapter is `FAIL-CLOSED / NOT IMPLEMENTABLE FROM ASSUMPTION`.

Reflection into private implementation, mixin injection into provider internals or direct mutation of undocumented fields is not an acceptable default bridge. Such approaches require a separate reviewed compatibility decision and exact-version maintenance rationale.

## Provider-native bite/feeding surplus

The desired behavior is that biting/feeding can restore both Vampirism thirst and Hematic Reserve, with thirst priority.

This feature is **strictly conditional on a causal exact-version hook**.

An acceptable 1.10.13 hook must expose enough information to prove, for one feeding action:

- the feeding player/caster;
- successful provider-native feeding identity;
- the amount of blood/intake available to that action or another exact quantity from which surplus can be computed;
- how much of that action was accepted by the Vampirism thirst state, or sufficient before/after data delivered within the same causal event to derive it safely once;
- cancellation/failure semantics sufficient to avoid crediting on a denied/failed feed.

If the provider exposes only a generic attack, damage event, animation, target blood change, or an unrelated eventual player-thirst delta, **do not infer bite surplus**. Polling player thirst before/after ticks is not causal enough. In that case reservoir/link refill may ship without bite-to-reserve conversion and the bite feature remains explicitly fail closed.

Black Arcana must never refill Vampirism thirst a second time after Vampirism has already completed a native bite. For native feeding, Black Arcana is at most a surplus observer/consumer.

## Create / fluid integration

The Create path is deliberately simple unless exact 6.0.10 behavior proves otherwise:

- a supported tank exposing the standard exact-version fluid capability can be bound as a `FluidHandlerHematicSource`;
- only verified blood fluid identity is eligible;
- use side-effect-free simulation followed by one exact execute extraction;
- do not cache provider handler instances across lifecycle invalidation unless the exact capability contract permits it;
- do not bypass Create's own connectivity/tank invariants;
- do not treat Create tank capacity as Black Arcana reservoir capacity;
- if Create/Create: Fluid add non-standard semantics that cannot satisfy the source boundary, fail closed or introduce a narrow adapter behind D009.

Multiple Create tanks are intentionally a valid but space-limited player strategy. Black Arcana's custom multiblock exists to provide a different large-reservoir building fantasy, not to replace or rewrite Create tanks.

## Cost integration with Blood & Curses

The Hematic Reserve must enter casting only through the existing canonical `CostProvider`/reservation pipeline.

Planned sequence for any future reserve-enabled Blood & Curses spell:

1. spell specification explicitly declares Hematic Reserve as a cost component or allowed substitution;
2. preflight quotes reserve cost without mutation;
3. reservation participates in the canonical composite transaction under D017;
4. effect failure before commit refunds the reserve reservation;
5. successful effect commits exactly once;
6. Arcane Danger remains a separate canonical hazard transaction under D029 and does not become “paid” with blood unless a later explicit design says so.

Do not make the binding/refill system itself a second cast pipeline.

## Persistence

Black Arcana-owned persistence must cover at minimum:

- per-player Hematic Reserve amount and exact conversion remainder if needed;
- per-player optional bound source reference;
- custom reservoir controller identity/revision, validated bounds, capacity and stored amount;
- schema/version marker sufficient for bounded migration.

Persistence requirements:

- absent new data in an old save defaults safely to empty reserve/no link;
- malformed entries are rejected/pruned individually without discarding unrelated valid state;
- loaded amount is clamped to current hard capacity with an explicit conservative migration policy;
- stale links remain stale rather than silently rebinding by proximity;
- source/controller identity collisions are rejected;
- no persistence restore may trigger chunk loading or automatic siphoning.

Whether player reserve/link state belongs in existing global Overworld SavedData or another already-canonical Black Arcana store must be decided from current persistence architecture during implementation; this plan does not invent a duplicate store.

## Networking and UX

Client packets carry intention only. Candidate actions are bind, unlink and explicit refill; exact packet classes/names are implementation details.

Server responses/presentation should expose bounded read-only information needed by the UX:

- linked/unlinked/stale source status;
- source display kind, not provider-internal mutable objects;
- Hematic Reserve current/capacity;
- refill result split into thirst contribution and reserve contribution when permitted;
- clear failure reason for unloaded/stale/unsupported/provider-unavailable sources.

Do not sync full reservoir state every tick. Reuse D023 event-driven synchronization: login/relevant persistence restore, bind/unlink, successful transfer, structural state change and explicit bounded inspection are appropriate triggers.

## Performance and world-safety requirements

- no global reservoir registry scan each tick;
- no nearest-blood search loop;
- no arbitrary flood fill across natural terrain;
- no automatic chunk loading/force-loading;
- no O(volume) structure validation per tick;
- transfer work is bounded per operation;
- presentation surfaces cannot become authoritative fluid inventories;
- any placement/removal of blocks/fluids performed by the system must route through `WorldEffectPolicy` when it constitutes a Black Arcana world mutation;
- external provider tanks remain provider-owned and are not rewritten by Black Arcana world effects.

## Proposed implementation phases

All Java paths below are **planned**, not claims that those classes already exist. Exact names may change during implementation if the existing package architecture dictates a better fit.

### Phase A — exact provider contract audit

No production bridge code before this closes.

1. inspect the exact physical `Vampirism-1.21-1.10.13.jar`/API and record supported identity, thirst and feeding surfaces;
2. reconcile the stale Notion source pin with the exact release evidence;
3. inspect NeoForge 21.1.248 fluid transfer contract used by the project;
4. verify Create 6.0.10/Create: Fluid 2.1.5 exposure of tank blood through that contract;
5. verify exact blood fluid identity/conversion and Bloodlines non-involvement unless a real hook is needed;
6. update `SOURCES.md`/`THIRD_PARTY_NOTICES.md` or the project's current provenance surface only with facts actually used.

Exit gate: provider matrix records exact symbols/signatures or explicitly marks a feature unsupported/fail-closed. No guessed hook survives the phase.

### Phase B — pure state and transaction planner (TDD)

Start RED with pure tests for:

- reserve cap and reservation lifecycle;
- thirst-first allocation;
- exact unit conversion/remainder;
- zero debit when both sinks are full;
- partial source availability;
- partial reserve capacity;
- replay/duplicate operation rejection;
- arithmetic overflow and malformed values.

Then add the minimum pure Black Arcana contracts under the Blood domain. Candidate concepts: `HematicReserve`, `HematicTransferPlan`, `HematicSource`, `BoundHematicSourceRef` and an operation/replay identity. Names are provisional.

### Phase C — Black Arcana custom reservoir

TDD structure validation before renderer polish:

- smallest valid structure;
- missing floor/wall/controller;
- second controller rejection;
- hard dimension/volume ceiling rejection;
- boundary across unloaded chunk rejection without loading it;
- structure mutation invalidation;
- save/reload preserves exact amount/capacity/identity;
- stale link after controller replacement;
- concurrent extraction serialized without negative storage.

Only after server state is green add blocks/block entity/menus/rendering necessary for the approved visual design.

### Phase D — generic fluid and Create source adapter

Using only exact verified APIs:

- detect supported blood fluid;
- quote/simulate extraction;
- execute exact extraction once;
- reject non-blood fluids/mixed unsupported endpoints;
- invalidate stale capability references safely;
- prove one transfer cannot double-debit a Create tank;
- test optional-provider absence.

If standard fluid capability is sufficient, do not create a parallel Create-only transaction system.

### Phase E — binding and manual refill

Implement server-owned bind/unlink/refill against the common source boundary.

Tests must cover:

- client target hint cannot author the final source;
- range/permission/dimension/source revision revalidation;
- immediate one-shot refill on successful bind;
- stale/unloaded source denial;
- rebind semantics;
- no background/per-tick drain;
- source debit equals committed sink credit under conversion accounting.

### Phase F — Vampirism thirst sink

Only after Phase A confirms exact 1.10.13 symbols.

Tests/adaptor fixtures must prove:

- non-vampire path does not mutate thirst;
- vampire with thirst deficit consumes source into thirst before reserve;
- exact provider clamp/acceptance is respected;
- full thirst routes eligible amount only to reserve;
- full thirst + full reserve debits nothing;
- adapter/provider failure cannot mint reserve blood;
- optional Vampirism absence fails safely.

Run real-modpack acceptance later under D031; mocks/fixtures do not prove host behavior.

### Phase G — provider-native bite surplus

Proceed only if Phase A identifies a causal feed hook meeting the requirements above.

RED tests first for successful feed, cancelled/failed feed, full/partial thirst, exact surplus, duplicate event/replay and no second thirst credit.

If no safe hook exists in 1.10.13, close this phase as `FAIL-CLOSED — PROVIDER CONTRACT INSUFFICIENT` and ship no heuristic replacement.

### Phase H — cost-provider composition

Add reserve-backed cost only to spells explicitly amended to use it. Tests must cover D017 reserve/refund/commit semantics and coexistence with current Blood Price/delegate authority.

No Stage 07.01 spell changes merely because the reserve runtime now exists.

### Phase I — client presentation, QA and hardening

- event-driven reserve/link sync;
- reservoir visual surface derived from server state;
- low/high fill states;
- stale/unloaded source presentation;
- dedicated-server classloading safety;
- malformed packet/rate-limit tests;
- performance tests for maximum allowed structure and repeated bounded transfers;
- assembled-modpack Create/Vampirism interactions recorded as manual evidence rather than inferred from unit/GameTests.

## Test matrix / minimum acceptance

Before any 07.08 implementation can be called canonical, evidence must include at least:

- pure JUnit RED->GREEN for allocation, conversion, reserve and replay invariants;
- NeoForge GameTests for multiblock formation/invalidation/persistence and server-side binding;
- integration tests/fixtures for source simulation/execute and transactional failure paths;
- exact-provider adapter tests compiled against the version actually used by the project;
- optional-mod absence/classloading tests;
- dedicated-server smoke;
- full NeoForge build and built-JAR inspection;
- proof that no global/per-tick reservoir scan or chunk force-load was introduced;
- assembled-modpack/manual Create tank test;
- assembled-modpack/manual Vampirism thirst test;
- bite-surplus manual test only if a verified provider hook exists;
- save/reload and controller break/rebuild scenarios;
- concurrency/replay regression coverage.

Automated mocks cannot upgrade real-provider/manual rows to PASS.

## Explicit non-goals for v1

- arbitrary natural blood lakes discovered by flood fill;
- chunk-force-loaded remote blood networks;
- continuous passive siphoning every tick;
- global Black Arcana mana replacement;
- changing Vampirism feeding rules;
- copying Tinkers multiblock implementation or assets;
- making Bloodlines a dependency without a verified requirement;
- direct private-field/mixin coupling to Vampirism as a convenience shortcut;
- unbounded reservoir dimensions or reserve capacity;
- retrofitting every Blood & Curses spell to reserve costs automatically.

## Open gates and risks

1. **Vampirism 1.10.13 exact API/JAR inspection is mandatory.** Current public `latest` source is 1.10.14 and cannot substitute for the installed release.
2. **The Notion Vampirism source pin is stale/non-resolving.** Repair provenance when the exact release source/JAR is pinned.
3. **Bite surplus may be impossible safely.** Lack of a sufficiently causal hook means fail closed, not polling or damage inference.
4. **Cross-provider transaction rollback is not assumed.** If the exact thirst mutation can fail after source debit, design explicit compensation/escrow or revise ordering before implementation.
5. **Large multiblocks create performance and chunk-boundary risk.** Hard structure/search budgets are required before implementation values are accepted.
6. **Visual fluid duplication is a dupe risk.** Controller storage must remain the sole source of truth.
7. **Stage sequencing still matters.** 07.08 is planned now but implementation waits until the currently active 07.07 gate is closed/reconciled with latest `main`.

## Definition of done

07.08 is complete only when all implemented portions satisfy the following simultaneously:

- Black Arcana remains authoritative for its reserve, reservoir, binding and transaction planner;
- Vampirism remains authoritative for vampire identity/thirst/feeding;
- Create/NeoForge remain authoritative for external fluid storage transactions;
- thirst-first/exact-surplus accounting is proven with no duplication or rounding creation;
- custom reservoir is bounded, persistent, chunk-safe and server-authoritative;
- linking is explicit and causes at most one immediate bounded refill, never a hidden per-tick siphon;
- reserve costs, where enabled, use the existing canonical cost transaction instead of a parallel cast pipeline;
- bite surplus exists only if the exact 1.10.13 hook proves causality; otherwise it is documented fail-closed;
- optional integrations fail safely;
- CI/build/GameTests/dedicated-server checks are green on a branch reconciled with the then-latest `main`;
- required real-modpack rows remain explicitly PASS/PENDING/FAIL according to observed evidence, never inferred;
- final merge is performed only after the mandatory latest-`main` resynchronization and revalidation protocol.
