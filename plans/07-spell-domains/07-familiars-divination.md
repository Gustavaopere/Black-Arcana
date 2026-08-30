# 07.07 — Familiars & Divination

## Candidate mechanics
Bound familiars, remote/astral scouting, scrying and occult perception.

## Constraints
Do not bypass server visibility/protection rules unintentionally. Remote views must not force-load unlimited chunks. Familiars have ownership, dimension, death and logout cleanup semantics.

## Integration
Eidolon/Ars may supply ritual/utility flavor; Black Arcana owns only missing behavior needed for the approved fantasy.

## Implemented checkpoint — Nullifying Gaze

`black_arcana:nullifying_gaze` now has a server-authoritative NeoForge runtime for the approved T3 Noetic contract.

- The caster and target are resolved from loaded server entities; the target must remain alive, in the caster dimension, inside the configured bounded range and in direct line of sight.
- Generic entity interaction/protection admission is evaluated before any effect inspection or mutation.
- Boss targets fail closed through `NullifyingGazeTargetPolicy`; provider-specific boss nullification requires a future explicit contract rather than inheriting generic CONTROL allowance.
- Only effects explicitly tagged/adapted as nullifiable are candidates. Unknown effects remain untouched.
- `black_arcana:nullification_protected` and protected adapter registrations override nullifiable registrations.
- At most one eligible effect is removed per settlement. Candidate selection is deterministic by effect resource ID.
- Target/range/LOS state is revalidated immediately before mutation.
- Removal uses the public `LivingEntity.removeEffect(Holder)` path; no reflection or private-state mutation is used.
- Runtime adapter registrations are monotonic for one server lifetime and are discarded on server stop; no vanilla effect is implicitly allowlisted by Black Arcana.

Verification checkpoint: commit `5b0ccd31f16ae31597989ab8227dbd159c01e221`, CI run `33341746849` — unit tests, diff sanity, NeoForge build, built-JAR verification, GameTest server and dedicated-server smoke all passed. The GameTest suite includes approved-effect removal, unknown/protected preservation, exactly-one removal and range/LOS fail-closed coverage; the unit suite separately proves default boss resistance.

## Acceptance
No chunk-loading exploit, duplication, cross-player information leak beyond designed range/permissions or orphan familiar entities.
