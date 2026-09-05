# 07.05 — Black Flame

## State

**DESIGN APPROVED / IMPLEMENTATION NOT STARTED.**

This domain must be implemented sequentially from canonical `main@0e508b646b602beefd136bf9602945e247b2a524`. Historical stacked PR #22 is review material only and must not become ancestry. Stage 07.06–07.07 remain out of scope.

The approved architecture includes one additive Stage 04 world-mutation protection extension because the frozen Stage 04 API can authorize entity interactions and protected displacement destinations but does not currently express claim/protection semantics for block mutation. Black Pyre must not encode block coordinates into entity-oriented `ProtectionQuery` or silently bypass claim adapters.

## Fantasy and identity

Black Flame is a forbidden soul-fire family with aggressive visual propagation, policy-controlled entity damage/status and server-authoritative terrain effects. It is not vanilla fire with a cosmetic skin. Black Arcana owns the propagation graph, world-safety admission, settlement and cleanup.

The first canonical spell is `black_arcana:black_pyre`.

## Host/provider boundary

- **Iron's Spells 'n Spellbooks** may host the active-cast presentation/cost surface when an exact supported hook is available.
- **Malum** may provide spirit flavor or bounded amplification only through a verified causal/value-bearing hook. If such a hook is unavailable or ambiguous, amplification fails closed rather than being approximated from generic spirit state.
- **Black Arcana** owns entity admission, propagation scheduling, world-mode policy, block protection, mutation settlement, restoration and lifecycle cleanup.
- No provider may invoke vanilla fire spread as a substitute for the Black Pyre frontier.

Real-modpack/provider/manual host validation remains deferred under D031 unless executed with the actual pack. Automated CI cannot promote those lines to PASS.

## Mechanics

### Black Pyre

A server-authoritative ignition launches or places forbidden soul-fire. It has three independent effect planes:

1. **Entity plane** — direct/ongoing Black Pyre damage or status on eligible entities. Entity effects use canonical `EntityInteractionAdmissionService` and are re-authorized immediately before settlement.
2. **Visual plane** — Black Flame presentation propagated through the bounded frontier without requiring block mutation.
3. **Terrain plane** — optional policy-governed block mutation, admitted per cell through the Stage 04 world-effect and world-mutation protection authorities.

Failure of the terrain plane must not retroactively roll back already-authorized entity damage when the contract defines those outcomes as independent. Terrain failure must return an explicit machine-readable denial/degradation code.

## Bounded frontier scheduler

Black Pyre must never delegate propagation to vanilla fire/random ticks. A Black Arcana scheduler owns every frontier.

Hard technical ceilings:

- radius: `<= 12` blocks from the frontier origin;
- cells per frontier: `<= 256`;
- processed/admitted spread candidates per tick per frontier: `<= 16`;
- concurrent frontiers per server runtime: `<= 8`;
- lifetime: `<= 1_200` ticks;
- unloaded candidate cells are dropped, never retained as chunk-load work;
- duplicate cells are idempotently ignored;
- finishing/expiry/server-stop removes frontier runtime state.

These are safety ceilings. Stage 08 may tune normal values downward but must not silently raise them.

## World modes

Black Pyre uses the existing `WorldEffectMode` ordering and must not create a second configuration hierarchy.

### `COSMETIC`

- visual frontier only;
- zero block mutation;
- entity effects remain governed independently by entity-damage policy;
- no temporary restoration record is created because nothing changed in the world.

### `TEMPORARY` — default terrain behavior

- reversible scorched/fire-like replacement only;
- each cell must pass loaded-chunk, per-cast world budget and world-mutation protection admission;
- settlement routes through `TemporaryBlockMutationGateway`/`TemporaryMutationTracker` using compare-and-set semantics;
- expiry, restart recovery and cleanup must restore only mutations still owned by the recorded Black Arcana mutation, never overwrite later player/world changes;
- lifetime never exceeds the Black Pyre lifetime ceiling.

### `LIMITED`

- bounded permanent mutation is allowed only when the effective server mode permits `LIMITED`;
- each mutation must pass the same loaded-chunk, budget and world-mutation protection authority as temporary cells;
- settlement must use a dedicated bounded compare-and-set gateway rather than direct arbitrary `ServerLevel#setBlock` calls from spell code;
- no restoration record is expected for a successfully committed permanent mutation;
- permanent work remains bounded by frontier and world-effect budgets.

### `FULL`

- explicit server opt-in only;
- uses the same protected, bounded settlement route as `LIMITED`;
- `FULL` does **not** mean unlimited radius, unlimited cells, vanilla fire cascade, chunk loading or protection bypass;
- it only permits the most destructive mutation class allowed by the registered spell profile/configuration while all technical ceilings remain enforced.

`OFF` remains a stronger global denial mode where world-effect policy rejects terrain work entirely.

## Stage 04 additive authority extension

### Problem being solved

Current Stage 04 `ProtectionQuery` is entity/destination oriented: it carries caster, dimension, string target identity and `EntityInteractionType`. Existing interaction types are `DAMAGE`, `CONTROL`, `DISPLACEMENT`, `EXECUTION`, `RESURRECTION_DENIAL` and `DOMAIN_CAPTURE`. Reusing this contract for block mutation would create ambiguous adapter semantics.

A second Stage 04 issue is that `WorldEffectProfile` is explicitly a static worst-case declaration, while the current `ConfigurableWorldEffectPolicy#authorize(request, target)` treats `profile.mutationClass()` as the exact class required for every mutation attempt. A single Black Pyre profile declared at worst-case `PERMANENT` would therefore be rejected in `TEMPORARY` and `LIMITED`, even when the actual requested cell operation is less destructive. Creating multiple spell IDs or parallel configuration trees to work around that would violate the domain contract.

### Requested mutation-class admission

Preserve the existing policy API and semantics for current callers, and add a narrow requested-class admission path for Stage 07.05.

The registered `WorldEffectProfile` remains the spell's **maximum/worst-case declaration**. For Black Pyre it may declare the maximum mutation class the spell can ever request under explicit server configuration. A new overload/service path accepts a `requestedMutationClass` for the actual operation and must enforce all of the following:

- `requestedMutationClass` is not more destructive than `profile.mutationClass()`;
- the effective `WorldEffectMode` allows the requested class;
- the existing global/per-spell affected-unit limits still apply;
- entity-damage configuration remains independently enforced where applicable;
- the canonical `WorldEffectBudgetLedger` is still the only cumulative per-cast budget;
- the existing `authorize(request, target)` path remains source- and behavior-compatible for all predecessor callers.

Black Pyre uses:

- no block admission for `COSMETIC` because no mutation occurs;
- requested class `TEMPORARY` for reversible cells;
- requested class `LIMITED` for bounded permanent cells under `LIMITED` mode;
- requested class `PERMANENT` for the maximum explicit `FULL` path.

`TemporaryBlockMutationGateway` must route its Black Pyre operation through requested class `TEMPORARY` rather than forcing the spell's worst-case profile class. Existing temporary callers with a `TEMPORARY` profile must remain behaviorally unchanged. The permanent gateway accepts only `LIMITED` or `PERMANENT` requested classes and rejects weaker/invalid classes rather than guessing.

### New provider-neutral mutation-protection contract

Add an explicit block/world-mutation protection route without changing existing entity-interaction semantics.

The new query must identify at minimum:

- caster UUID;
- dimension ID;
- exact block position/cell identity;
- `WorldMutationType` (for Black Pyre terrain: the registered Black Pyre mutation type, expected to be `FIRE_SPREAD` for frontier-owned terrain work);
- requested `WorldMutationClass`/persistence class;
- Black Arcana spell ID and cast provenance for diagnostics/deduplication.

The registry/guard must:

- be bounded by an adapter-count ceiling;
- fail closed when an installed adapter throws, links incorrectly or returns invalid data;
- require all installed adapters to allow a mutation;
- not force-load chunks;
- keep existing entity `ProtectionAdapterRegistry` behavior source-compatible;
- expose no generic bypass flag to spell code.

An empty mutation-protection registry is a neutral allow after all core world policy/loaded-chunk checks, matching the existing provider-neutral registry model: absence of an optional claim adapter does not imply that every block in an otherwise unclaimed world is protected. If an adapter is installed, its denial/failure is authoritative and fail-closed.

Optional claim/provider integrations consume this provider-neutral query. Black Pyre itself must not know claim-mod internals.

### Settlement gateways

Temporary block work continues through the existing `TemporaryBlockMutationGateway` after mutation-protection admission and requested-class world admission.

Add a narrow permanent mutation gateway for `LIMITED`/`FULL` that:

- accepts only already-loaded target state;
- validates requested mutation class against the registered worst-case profile and effective mode;
- performs mutation-protection admission before consuming mutation budget;
- rechecks mutation-protection admission immediately before side effect when mutable provider state can change;
- uses compare-and-set semantics against the observed block state;
- consumes the canonical per-cast world-effect budget exactly once per admitted mutation attempt;
- rejects stale state rather than overwriting concurrent player/world edits;
- exposes no chunk-loading API;
- reports explicit denial codes.

The temporary route must similarly perform mutation-protection admission before invoking the existing gateway that consumes canonical world-effect budget, so a claim denial does not burn budget for work that was never eligible to settle.

Spell/runtime code must not mutate terrain directly around these gateways.

## Entity damage/status policy

Black Pyre entity settlement must:

- require a loaded, alive server-side caster;
- deduplicate target UUIDs and honor the canonical absolute target cap;
- require same permitted server level unless a future contract explicitly says otherwise;
- use `EntityInteractionType.DAMAGE` admission and reauthorization immediately before damage;
- preserve allied/friendly-fire/PvP/boss limits from canonical policy;
- clamp requested raw damage to a technical ceiling and never treat a policy cap greater than `1.0` as an implicit damage amplifier;
- report actual confirmed health loss rather than nominal pre-mitigation damage when returning settlement metrics;
- not create mastery/lifesteal/proc credit outside existing canonical damage provenance rules.

Final ordinary damage, boss multiplier, PvP multiplier and cooldown tuning remain Stage 08 responsibility below hard safety ceilings.

## Causality, deduplication and anti-abuse

- one frontier ID maps to one bounded frontier lifecycle;
- duplicate seed/frontier creation with the same identity is rejected;
- cell identity is stable and deduplicated before work is admitted;
- world budget is charged once per admitted mutation attempt under the canonical budget ledger;
- protection denials occur before world-budget consumption;
- failed compare-and-set does not become a successful mutation;
- a later player/world block edit must never be reverted by stale temporary cleanup;
- entity targets are settled at most once per effect pass unless the spell explicitly schedules a separate bounded tick/effect instance;
- optional Malum amplification must have causal ownership for this cast and a bounded numeric value; generic inventory/spirit presence is insufficient evidence.

## Failure semantics

Fail closed for:

- missing/unavailable Black Arcana runtime;
- unloaded target chunk/cell;
- requested mutation class above the spell's worst-case declared class;
- world mode below requested mutation class;
- missing spell world-effect profile;
- world-effect budget exhaustion;
- installed protection adapter denial/failure;
- mutation-protection authority unavailable from the runtime when terrain settlement is requested;
- stale block state at settlement;
- invalid/expired frontier;
- out-of-radius or over-cell-budget candidate;
- invalid/non-finite entity damage request;
- ambiguous provider amplification.

Visual degradation may continue where the approved mode permits cosmetic presentation, but it must not be represented as successful terrain mutation.

## Lifecycle and persistence

- frontier runtime state is bounded and ephemeral;
- temporary mutation restoration data uses the canonical Stage 04 tracker/persistence path;
- server restart must not resurrect expired frontiers as active spread jobs;
- pending unloaded candidates are not persisted for later activation;
- restoration after restart processes bounded work and only restores still-owned temporary replacements;
- server stop clears in-memory frontier state after durable temporary restoration state has been handled by the existing persistence path.

## Required TDD / validation matrix

Implementation starts RED and must cover at least:

### Pure/core tests

- scheduler rejects configuration above every hard ceiling;
- frontier count cap;
- cell deduplication and cell cap;
- per-tick processing cap;
- radius rejection;
- unloaded candidates are dropped/no deferred chunk-load queue;
- expiry/finish cleanup;
- mutation-protection registry empty-registry neutral allow, all-allow, denial and adapter-exception fail-closed;
- mutation query preserves position/type/class/caster/spell/cast provenance;
- requested-class admission rejects class above profile maximum;
- requested-class admission permits TEMPORARY under a PERMANENT worst-case profile when effective mode is TEMPORARY;
- legacy world-effect admission behavior remains unchanged for predecessor callers;
- protection denial occurs before world-budget consumption;
- permanent gateway stale-state compare-and-set denial;
- world-mode ordering: OFF < COSMETIC < TEMPORARY < LIMITED < FULL;
- LIMITED/FULL cannot bypass technical frontier budgets.

### GameTests

- COSMETIC produces no terrain mutation;
- safe-mode/entity-only Black Pyre damages one eligible target without terrain mutation;
- allied/protected target is not damaged;
- boss/player limits are honored;
- TEMPORARY mutation applies only in loaded authorized cells even when Black Pyre's profile declares a PERMANENT worst case;
- temporary mutation expires and restores;
- player/world edit after temporary mutation is not overwritten by cleanup;
- restart/reload path restores temporary state cleanly without reviving spread;
- chunk-edge candidate never force-loads an unloaded chunk;
- protected block/claim cell fails closed and does not consume mutation budget;
- LIMITED bounded permanent mutation commits only under an allowed mode and protection decision;
- FULL/PERMANENT mutation is denied unless server mode explicitly allows FULL;
- FULL does not exceed radius/cell/per-tick/concurrent-frontier ceilings;
- stale cell revalidation prevents overwrite;
- no vanilla fire cascade/random-tick propagation occurs;
- stress case proves bounded work under max legal frontier count/cell count.

### Pipeline

Before merge the exact PR head must pass:

- JUnit/pure tests;
- diff sanity;
- NeoForge 1.21.1 build on Java 21;
- built-JAR verification;
- complete required GameTest server suite;
- dedicated-server smoke.

After merge, the exact `main` SHA must pass the same pipeline and publish the canonical QA JAR before 07.05 is marked canonical.

## Documentation/promotion rules

During implementation this file remains `05-black-flame.md` and must state the real status. Only after runtime merge plus exact-SHA post-merge GREEN may a documentation follow-up rename it to `✅-05-black-flame.md` and update `README.md`, `plans/STATUS.md` and the Black Arcana Notion dossiê.

Do not start 07.06 automatically.
