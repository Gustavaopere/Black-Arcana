# Stage 04 — World Safety preparatory architecture

Status: implementation-advanced, verification pending.

Code checkpoint before this document: `ff8ccc423c29c18f287142fd8e4198f8b7aef9b3` on `prep/04-world-safety`.

## Purpose

Stage 04 establishes mandatory safety boundaries before destructive or displacement-oriented Black Arcana spell domains are implemented. The core does not grant content code an implicit right to mutate terrain, control protected entities, force-load destinations, or leave temporary state behind after restart.

## World-effect policy

`ConfigurableWorldEffectPolicy` is the canonical cast preflight policy exposed by `ArcanaServerRuntime`.

Modes are ordered ceilings:

- `OFF`
- `COSMETIC`
- `TEMPORARY`
- `LIMITED`
- `FULL`

Every `ArcanaSpellDefinition` with `requestsWorldMutation=true` must have a `WorldEffectProfile`. Missing profiles fail closed. Profiles declare mutation type, persistence/destructiveness class, worst-case affected units and whether entity damage is included.

`WorldEffectPolicyConfig.safeDefaults()` uses `TEMPORARY`, a 4096-unit global ceiling and independent entity-damage permission. Per-spell overrides may only make the global policy stricter; they cannot elevate it.

Iron's, Ars and Malum synthetic engines use the runtime-owned policy instead of local allow-all lambdas.

## Admission and budgets

`WorldEffectAdmissionService` applies the policy before consuming world-work budget. `WorldEffectBudgetLedger` bounds total work per cast and active cast tracking; idle entries are pruned by the server runtime.

`LoadedChunkGuard` accepts only an injected boolean probe for already-loaded chunks. It has no API capable of creating tickets, loading or generating chunks. The default runtime caps one effect at 64 referenced chunks.

The existing `BoundedWorkScheduler` remains the global per-tick work queue. Default runtime limits are 2048 queued effects and 128 work units per tick. Overflow rejects/degrades instead of expanding the queue.

Stress tests cover the 64-chunk ceiling, 4096 total units per cast and 128-unit tick budget at a full 2048-entry queue.

## Temporary block lifecycle

The only supported Stage 04 route for temporary block replacement is:

`TemporaryBlockMutationGateway -> TemporaryMutationTracker -> TemporaryBlockBackend`

The gateway:

1. validates expiry bounds;
2. runs world policy, loaded-chunk and budget admission;
3. reads the current loaded state;
4. records rollback ownership before writing;
5. performs compare-and-set replacement;
6. rolls back the tracking record when a definite CAS failure proves no write occurred.

If a backend throws during the write, the rollback record remains intentionally pending because a partial/ambiguous write must be recoverable.

`TemporaryMutationTracker` stores dimension/position, owner, cast id, original state, Black Arcana replacement and expiry. Overlapping Black Arcana mutations preserve the first original state while extending/replacing the owned temporary state. Later player/mod edits are detected and are never overwritten by expiry cleanup.

Pending records are bounded to 16,384 by the default runtime and persisted in `BlackArcanaSavedData`. The persisted field is optional under schema 1 so older saves without it continue loading.

## Minecraft backend

`MinecraftTemporaryBlockBackend` is the NeoForge/Minecraft adapter.

It:

- resolves dimensions from authoritative server registries;
- uses `ServerChunkCache#getChunkNow` and therefore does not force chunk loading;
- serializes full `BlockState` through `NbtUtils` SNBT;
- compare-and-sets the expected state before replacement;
- refuses current or replacement states with block entities, preventing accidental inventory/arbitrary block-entity NBT loss;
- writes with `Block.UPDATE_ALL | Block.UPDATE_SUPPRESS_DROPS` to prevent duplicate drops during temporary swaps and rollback.

`ArcanaServerRuntimeManager` installs this backend once per server before optional integrations bootstrap.

## Restoration

`TemporaryRestorationService` checks at most 128 pending expirations per default runtime tick.

Outcomes:

- expected Black Arcana replacement still present -> CAS restore original and then retire record;
- another actor changed the block -> preserve external state and retire record;
- chunk/dimension unavailable -> keep record pending without force-loading;
- backend read/write failure -> keep record pending and record failure telemetry.

The runtime exposes the last bounded restoration counters for diagnostics.

## Entity interaction policy

`MinecraftEntityProtectionResolver` derives facts only from server/entity state:

- player identity;
- scoreboard/team alliance through `Entity#isAlliedTo`;
- boss membership through the conventional `c:bosses` entity-type tag;
- entity invulnerability plus creative/spectator privilege;
- live `MinecraftServer#isPvpAllowed()`.

`EntityInteractionAdmissionService` evaluates `DefaultEntityInteractionPolicy` before external protection adapters.

Safe defaults:

- server PvP disabled -> hostile player effects denied;
- allied target -> hostile effects denied;
- invulnerable/creative/spectator target -> denied;
- bosses may still receive bounded damage/control/displacement;
- boss execution, resurrection denial and permanent domain capture are denied;
- boss control/displacement/damage use stricter limits.

## Claims and protected destinations

`ProtectionAdapterRegistry` is provider-neutral and fail-closed if an adapter throws or links incorrectly. No specific claim mod is embedded in core.

`ProtectedDestinationGuard` requires the destination chunk to already be loaded before consulting claim/protection adapters. Dimension mismatch is denied before either operation. The guard contains no teleport or chunk-loading API; Stage 07 displacement spells must consume this contract rather than invent a new path.

## Tests present in source

Pure JUnit coverage includes:

- mode hierarchy and policy overrides;
- missing-profile fail-closed semantics;
- total cast budgets and loaded-chunk limits;
- scheduler stress/overflow bounds;
- temporary overlap, player edits, unloaded chunks and confirmation-before-retire;
- gateway atomic registration/CAS semantics;
- restoration backend read-failure containment;
- PvP/team/boss/invulnerable policy;
- combined entity policy + protection adapters;
- protected/unloaded destination gates;
- persistence of temporary mutation records.

GameTests include:

- Minecraft block-state CAS and stale-state protection;
- block-entity mutation refusal;
- temporary mutation -> expiry -> runtime restoration;
- preservation of external edits;
- temporary rollback SavedData round-trip;
- server PvP, scoreboard allies, `c:bosses` and invulnerable entities;
- synthetic claim-protected and unloaded displacement destinations;
- `OFF` through `FULL` policy semantics on a GameTest server.

## Verification state

No Stage 04 task is marked complete yet because GitHub-hosted workflow jobs are currently failing before runner setup. Verification branch `feat/verify-world-safety-v2` at `0a65646a35f8c1f558ccbbf3a7e2988277653075` produced run `33142961930`, job `98757665414`, with `steps=null`; no checkout, Gradle, NeoForge, GameTest or dedicated-server command executed.

A source checkpoint must therefore remain preparatory until a runner executes the repository gates.
