# 07.08 — Hematic Reservoirs & Vampiric Sustenance — Runtime Plan

## State

`PLANNED / NOT IMPLEMENTED / SEQUENCED AFTER 07.07`

This is the authoritative engineering plan for reservoir structure/state, source binding, provider transactions, persistence, networking data and world/performance safety. Concrete reservoir appearance, models/textures, blood-surface rendering, UI treatment and presentation QA live at:

`plans/visual-production/07-spell-domains/08-hematic-reservoir-presentation.md`

The exact pre-extraction mixed plan is retained for audit under `plans/visual-production/_migration-source/07-spell-domains/`.

Stage 07.07 remains the active incomplete Stage 07 domain. 07.08 must not enter implementation ahead of it merely because this plan exists. Implementation starts from the then-latest `main`.

## Goal and invariant

Extend canonical Blood & Curses with bounded blood storage and vampire-aware blood consumption without creating another casting engine or global mana pool.

Canonical accounting order:

`blood source -> Vampirism thirst acceptance -> exact surplus -> Hematic Reserve acceptance`

No path may debit blood twice, credit thirst twice, infer surplus from animation/damage, or mint blood through rounding.

## Canonical context

07.01 already owns Blood & Curses runtime and its transactional `BloodPriceCostProvider`. 07.08 extends that architecture; it does not replace the delegate or silently retrofit every Blood spell.

Relevant frozen decisions include D004, D006, D008, D009, D017, D019, D023, D026, D029, D030 and D031.

## Provider evidence gate

Planning-time physical pins:

- NeoForge `21.1.248`;
- Create `6.0.10`, SHA-1 `0e97e49837bed766e6f28a4c95b04885d6acc353`;
- Create: Fluid `2.1.5`, SHA-1 `ad3e3fccf953f5b96784aefde2b6d61612e87f86`;
- Vampirism `1.10.13`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`;
- Bloodlines `1.21-3.0.9`, SHA-1 `b14ff359c7530c0e40ca289cc023bd1c19a070af`.

These pins must be revalidated against the physical modlist when implementation starts.

Existing audit evidence records the design lead `1 player blood unit = 100 mB` for `vampirism:blood`, and public 1.21 latest source exposes `FOOD_TO_FLUID_BLOOD = 100`, but that source is 1.10.14. The exact installed Vampirism `1.10.13` JAR/API is mandatory evidence before production thirst/feeding code. The stale/non-resolving prior source pin must not be treated as authority.

## Authority

Black Arcana owns:

- personal Hematic Reserve semantics/cap for explicitly eligible Blood & Curses costs;
- custom reservoir formation, controller identity/revision, validated bounds, capacity, stored amount and lifecycle;
- explicit bound-source records and validation;
- thirst-first transfer planning, replay/deduplication and exact accounting;
- Black Arcana persistence, networking and diagnostics;
- optional-provider adapters at the Black Arcana boundary.

Vampirism owns vampire identity, thirst/player-blood state, native feeding/bite eligibility, cooldowns, provider side effects and native feeding/container behavior. Black Arcana must not mutate guessed private state or infer a feed from generic damage/animation.

Create/NeoForge fluid providers own their external storage contents, connectivity and exact simulate/execute behavior. A Create tank is a source endpoint, never Hematic Reserve authority.

## Hematic Reserve boundary

The reserve is a Blood-domain consumable buffer, not a second global mana bar. A spell may use it only when its explicit specification adds a reserve cost/substitution through the existing canonical `CostProvider`/D017 transaction path. Capacity is hard-bounded; progression/tuning belongs to Stage 08 below the structural ceiling.

## Hematic source abstraction

Core code must depend on a bounded Black Arcana source contract rather than Create implementation classes. A source must provide:

- stable persisted identity;
- side-effect-free availability quote/simulation;
- exact bounded extraction;
- one execute extraction after sink capacity is known;
- explicit stale/unloaded/invalid/not-blood/incompatible failure;
- no automatic chunk loading.

Planned families are a Black Arcana controller-backed source and an exact-version fluid-handler source. Reuse standard fluid capability for Create when sufficient; add a narrow Create adapter only if provider semantics actually require one. Source binding is explicit; never discover sources through global or periodic scans.

## Custom reservoir runtime

One controller is the sole source of truth for structure identity/revision, validated interior bounds, capacity, stored amount, formed/invalid state, persistence dirtying and external transfers.

A client-visible blood surface, if rendered, is derived presentation only and must never become an independently drainable set of `FluidState`s or a second inventory. The concrete presentation contract is in visual-production.

Runtime structure rules:

- v1 uses a bounded rectangular/orthogonal basin with hard dimension/volume/search ceilings selected from tests/performance evidence;
- formation/revalidation runs on explicit formation and relevant structural changes, never as an O(volume) per-tick scan;
- reject oversized candidates before full traversal;
- never inspect by force-loading an unloaded chunk;
- one connected formed structure has one authoritative controller;
- a second controller or broken boundary invalidates formation;
- controller removal/replacement invalidates stale links using stable identity/revision;
- stored-content preservation/drop policy must be explicit and tested;
- wall/floor compatibility may be data/tag-driven only after deterministic structural/geometry validation;
- no arbitrary natural-terrain lake flood fill in v1.

“Tinkers-style” remains conceptual multiblock inspiration only. Do not copy provider implementation. Asset/model/sound provenance constraints are owned by the visual-production spec.

## Binding contract

Binding is server-authoritative. A client may submit a target hint; the server resolves and validates the final endpoint, range, permission, dimension, source kind and stable identity/revision.

Lifecycle:

- bind only loaded valid supported sources;
- intentional rebind replaces the previous link;
- unlink is explicit/idempotent;
- stale, broken, unloaded and foreign-dimension links fail closed without chunk loading;
- replacement at the same position is rejected when identity/revision differs;
- successful bind performs at most one bounded refill attempt through the canonical transfer path;
- no hidden continuous/per-tick siphon.

## Canonical refill transaction

Preflight:

1. validate player/link/source/replay identity and operation ceilings;
2. simulate source availability;
3. when an exact supported Vampirism adapter identifies a vampire, query exact thirst deficit/acceptance;
4. query Hematic Reserve remaining capacity;
5. convert sink capacities to source units with deterministic integer/fixed-point arithmetic and retained remainder when required;
6. compute exact required source amount, capped by availability and operation budget;
7. simulate that exact extraction again immediately before commit.

Commit on the server thread:

1. execute source extraction once for the planned amount;
2. apply provider-native thirst credit up to its exact accepted amount;
3. credit only mathematically proven surplus to Hematic Reserve;
4. dirty/persist Black Arcana state;
5. emit event-driven read-only synchronization/feedback.

If the real provider mutation contract makes this ordering unsafe, design explicit compensation/escrow or revise the transaction before enabling the adapter. Never retry an operation in a way that can repeat an already executed debit or thirst credit.

For actual source amount `S`, thirst-equivalent acceptance `T`, reserve-equivalent credit `R` and retained conversion delta `D`, successful accounting must satisfy `S = T + R + delta(D)` with no direction of rounding capable of minting blood over repeated conversions. Full thirst + full reserve implies zero source debit.

Floating-point accounting is not acceptable for unit conservation.

## Vampirism exact-version gate

Before production code, prove from the physically installed 1.10.13 release:

- supported vampire identity API;
- exact current/max thirst read surface;
- supported mutation/feeding surface and clamp/side effects;
- server/thread requirements;
- whether acceptance can be simulated/read without mutation;
- exact fluid/player conversion constant;
- rollback/compensation implications for D017.

Until then the Vampirism sink is `FAIL-CLOSED / NOT IMPLEMENTABLE FROM ASSUMPTION`. Reflection/private-field mutation/mixin coupling is not an acceptable default bridge.

## Provider-native feeding surplus

Bite/feed -> reserve surplus is enabled only if one exact-version causal hook proves player identity, successful feed identity, exact intake, actual thirst acceptance (or causally equivalent before/after facts) and failure/cancellation semantics.

Generic damage, animation, target change or later thirst polling is insufficient. If the hook does not exist, this feature ships fail-closed. Black Arcana must never credit Vampirism thirst a second time after native feeding already did so.

## Create/fluid integration

When the exact standard fluid capability is sufficient:

- accept only verified blood fluid identity;
- simulate, then execute one exact extraction;
- do not cache invalid provider handler instances across lifecycle invalidation;
- preserve Create connectivity/tank invariants;
- never reinterpret Create capacity as Black Arcana reserve capacity;
- optional incompatibility fails closed behind the provider boundary.

## Cost integration

Any reserve-enabled Blood spell must explicitly amend its spell specification. Reserve quote/reservation/refund/commit participates in the existing canonical composite transaction. Arcane Danger remains separately authoritative; creating the reservoir does not automatically change any 07.01 spell.

## Persistence

Persist at minimum:

- per-player reserve amount and exact conversion remainder where needed;
- optional bound source reference;
- custom controller identity/revision, validated bounds, capacity and stored amount;
- schema/version information for bounded migration.

Old saves default to empty reserve/no link. Malformed entries are rejected individually. Loaded amounts are conservatively clamped to current hard capacity. Stale links never rebind by proximity. Restore may not trigger chunk loading or automatic siphoning. Reuse canonical persistence architecture rather than creating a duplicate global store.

## Networking and presentation-data contract

Client actions are bounded intent only: bind, unlink, explicit refill and bounded inspection as eventually approved. Server-authored read-only sync may expose:

- linked/unlinked/stale status;
- safe source display kind;
- reserve current/capacity;
- refill result split into thirst vs reserve contribution when permitted;
- bounded failure reason.

Do not sync full reservoir state each tick. Follow D023 event-driven triggers such as login/restore, bind/unlink, successful transfer, structural state change and explicit inspection.

How those fields are drawn, animated or sounded belongs exclusively to visual-production.

## Performance and world safety

- no global reservoir/source scan each tick;
- no nearest-blood search loop;
- no arbitrary natural flood fill;
- no chunk tickets/force loading;
- no O(volume) validation per tick;
- bounded transfer work per operation;
- presentation surfaces cannot become authoritative fluid inventories;
- Black Arcana block/fluid mutations use `WorldEffectPolicy` when applicable;
- external provider tanks remain provider-owned.

## Implementation sequence

A. Exact provider/JAR/API audit, including provenance repair and fluid identity/conversion.

B. Pure TDD for reserve cap/reservation, thirst-first allocation, exact conversion/remainder, zero-debit-full-sinks, partial availability/capacity, replay rejection, overflow/malformed values.

C. Custom reservoir server state first: valid/invalid structure, second-controller denial, hard bounds, unloaded-chunk denial, mutation invalidation, save/reload identity/amount, stale replacement, concurrent extraction. Blocks/block entity/menu/rendering are not acceptance for this server phase; presentation follows the visual-production plan after server state is green.

D. Generic fluid/Create source adapter from exact verified APIs; prove simulate/execute, non-blood rejection, stale capability invalidation, no double debit and provider absence.

E. Server-owned bind/unlink/manual refill; prove client hint cannot author final source, final revalidation, one-shot bind refill, stale/unloaded denial, no background drain and exact accounting.

F. Vampirism thirst sink only after exact-version gate; prove non-vampire path, thirst-first behavior, provider clamp, full-sink zero debit and provider failure safety.

G. Provider-native bite surplus only if a causal feed hook passes the gate; otherwise close as `FAIL-CLOSED — PROVIDER CONTRACT INSUFFICIENT`.

H. Reserve-backed cost composition only for explicitly amended spells under D017.

I. Runtime hardening: dedicated-server classloading, malformed/rate-limited intent, max-structure performance, repeated bounded transfers and real-provider/manual evidence. Client visual state/readability acceptance is tracked separately in visual-production.

## Minimum runtime acceptance

Canonical implementation requires JUnit RED->GREEN for allocation/conversion/replay, NeoForge GameTests for multiblock/binding/persistence, provider adapter tests against exact supported versions, optional-mod absence tests, dedicated-server smoke, full build/JAR inspection, proof of no global scans/force-loading, save/reload/controller-replacement cases and concurrency/replay coverage. Real Create/Vampirism rows remain explicit manual evidence under D031.

## Explicit non-goals

- natural blood lakes discovered by flood fill;
- force-loaded remote blood networks;
- continuous passive siphoning;
- global Black Arcana mana replacement;
- changing Vampirism feeding rules;
- copying Tinkers multiblock implementation;
- making Bloodlines a dependency without a verified requirement;
- private-field/mixin coupling to Vampirism as a convenience shortcut;
- unbounded structure dimensions/reserve capacity;
- automatically converting every Blood spell to reserve costs.

## Open gates and risks

1. Exact Vampirism 1.10.13 API/JAR inspection is mandatory.
2. The stale provider source pin must be repaired with exact-release evidence.
3. Bite surplus may remain safely impossible; fail closed instead of inferring it.
4. Cross-provider rollback is not assumed; compensation/escrow may be required.
5. Large multiblocks need hard structure/search budgets.
6. Visual fluid duplication is a duplication risk; controller storage stays sole authority.
7. Stage sequencing remains 07.07 before 07.08.

## Definition of done

Black Arcana remains authoritative for reserve/reservoir/binding/transfer; providers retain their own authority; exact thirst-first accounting cannot duplicate/mint blood; the reservoir is bounded/persistent/chunk-safe; binding is explicit and non-siphoning; reserve costs use the canonical cost transaction; bite surplus exists only with causal provider proof; optional integrations fail safely; final CI is green on latest-main ancestry; and real-modpack rows remain evidence-based rather than inferred.