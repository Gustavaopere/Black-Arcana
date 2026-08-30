# 07.05 — Black Flame

## Fantasy
A soul-corrupting flame family with visually aggressive behavior but server-controlled terrain impact.

## Model
Separate entity damage/status, visual flame propagation and block mutation. Spread uses the bounded `BlackPyreFrontierScheduler`; terrain work must consume the frozen Stage 04 world-safety contracts instead of delegating to vanilla fire tick.

## Existing preparatory infrastructure
- `BlackPyreDomainSpecifications` defines the canonical `black_arcana:black_pyre` T3 Cinder contract.
- `BlackPyreSafetyCeilings` bounds radius, cells, spread work, concurrent frontiers and lifetime.
- `BlackPyreFrontierScheduler` provides bounded, deduplicated propagation and accepts only caller-approved/loaded cells.
- unit tests cover scheduler capacity, deduplication and hard ceilings.

## Validated entity-damage boundary
`MinecraftBlackPyreRuntime` now provides a server-authoritative safe-mode damage path:
- caster and targets are resolved from live server state;
- target UUIDs are deduplicated and absolutely bounded;
- every target consumes canonical `EntityInteractionType.DAMAGE` admission;
- PvP, alliance, boss and invulnerability semantics come from the frozen Stage 04 resolver/policy;
- target identity and authorization are revalidated immediately before `hurt`;
- actual health loss, rather than requested damage, is reported;
- entity damage remains functional when terrain presentation is disabled or unavailable.

The TDD RED checkpoint `a3517134745eecab005dd3947ec56ea145e98f53` produced workflow run `33318159587` (#637): all pre-existing tests/build gates passed and exactly the three new Black Pyre GameTests failed because `MinecraftBlackPyreRuntime` did not exist. Implementation checkpoint `5811b030ccd44e25bd6cb6e4c6270ddad8264439` then passed workflow run `33318334221` (#638) in full: JUnit, diff sanity, NeoForge build, JAR inspection, all 74 GameTests and dedicated-server smoke.

## World modes
`COSMETIC`: visual only. `TEMPORARY`: reversible scorched/fire-like blocks. `LIMITED`: bounded permanent mutation. `FULL`: explicit server opt-in.

## Frozen Stage 04 contract gap
The current Stage 04 temporary block gateway correctly enforces world-effect policy, loaded chunks, bounded work and rollback, but its block-mutation route has no semantically explicit claim/protected-block authorization query. `ProtectedDestinationGuard` is explicitly a displacement/control destination contract, and `EntityInteractionType` has no world/block-mutation member.

Therefore Black Pyre terrain mutation is currently **fail-closed**. When terrain is requested, the validated runtime returns `black_pyre_terrain_protection_contract_missing`, applies no terrain mutation, and preserves independently authorized entity damage. It does not misuse `CONTROL`/`DISPLACEMENT`, call raw `setBlock`, or substitute uncontrolled vanilla fire spread.

Because Stage 04 is frozen, enabling temporary/permanent Pyre terrain requires an explicit reviewed Stage 04 follow-up that introduces a provider-neutral block/world-mutation protection contract. This is a recorded dependency, not a silent Stage 07 redesign.

## Balance
Boss damage modifier/cap, spread radius/count, duration, concurrent frontier cap and friendly-fire policy remain Stage 08/final-config concerns below the technical ceilings.

## Acceptance status
Partially satisfied in preparatory Stage 07: server-authoritative entity damage and bounded propagation primitives are tested; uncontrolled vanilla fire cascade is absent. Terrain lifecycle/restart/rollback/stress acceptance remains blocked until the Stage 04 protected-block contract gap is explicitly resolved.
