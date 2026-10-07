# Wrathful Lightning

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:wrathful_lighting`
- Owner/reachability: `minecraft:trident` with vanilla **Channeling**
- Semantic type: deliberate supernatural lightning invocation
- State: `COUNTED_EXACT`

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Wrathful Lightning when the trident has Channeling, after the Riptide branch and before Loyalty.

This selector closes current catalog reachability without inventing an Epic Fight-owned item: the owner surface remains the vanilla trident, while the enchantment selects the provider-owned innate.

The registry id intentionally uses `lighting`; the player-facing identity is **Wrathful Lightning**.

## Exact provider settlement

The exact skill/animation seam attaches Epic Fight's server-side `SUMMON_THUNDER` event to this skill action.

That establishes one provider-owned supernatural lightning root. The spawned lightning/event processing, particles, animation, damage and downstream hit consequences are settlement details of the same action rather than additional magic identities.

## Fallback boundary

If Riptide is present, the exact trident selector resolves Tsunami instead. Wrathful Lightning is therefore not simultaneously selected by the same innate-selector pass.

## Authority boundary

Epic Fight remains authority for battle mode, skill activation, animation, innate gauge/resource state, event execution and damage settlement. Black Arcana must not replay thunder or charge a second resource/cooldown cost.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
