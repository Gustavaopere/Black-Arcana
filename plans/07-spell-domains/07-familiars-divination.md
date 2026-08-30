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

## Implemented checkpoint — Occult Appraisal

`black_arcana:occult_appraisal` now exposes only a bounded, server-owned metadata projection for loaded non-player targets.

- The caster must be a loaded living entity; the target is resolved only from the caster's already-loaded server level, so appraisal does not scan or force-load remote chunks or dimensions.
- Range is bounded by `FamiliarSafetyCeilings.MAX_SCRY_RANGE` and direct server-validated line of sight is required.
- Player targets fail closed with `occult_appraisal_player_privacy` until an explicit server privacy/consent policy is wired; no player metadata is returned before that contract exists.
- Requested fields are filtered through `DivinationVisibilityPolicy`. The current approved metadata vocabulary is `health`, `status_effects`, `held_item`, `armor_summary` and `occult_trace`.
- A request that contains no approved field fails closed with `occult_appraisal_no_approved_metadata` rather than returning a successful empty projection.
- `full_nbt`, `container_inventory`, `capabilities` and other arbitrary target state are never projected.
- Held-item appraisal exposes only the item registry ID; health/status/armor projections use bounded primitive/string summaries and do not copy live `ItemStack`, component, NBT or capability state.
- Denied appraisal results are structurally unable to carry metadata.

Verification checkpoint: commit `5c4586a33d9fd042b82e43aaeff1d7c0d67786ce`, CI run `33342357187` — unit tests, diff sanity, NeoForge build, built-JAR verification, all 100 GameTests and dedicated-server smoke passed. The preceding RED checkpoint `205b2c6bc720bba522cca871b8a0a940c95cf8f0` failed exactly the player-privacy and unknown-only whitelist tests while the remaining GameTests stayed green.

## Acceptance
No chunk-loading exploit, duplication, cross-player information leak beyond designed range/permissions or orphan familiar entities.
