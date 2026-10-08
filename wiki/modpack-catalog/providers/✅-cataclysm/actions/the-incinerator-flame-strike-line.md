# The Incinerator — Flame Strike Line

- Provider: **L_Ender's Cataclysm** (`cataclysm`)
- Exact installed version: `3.33`
- Physical/publisher SHA-1: `5ff39c0eddfa08ea0e921bdcb17da7f32f0b00ce`
- Semantic root: **15/27**
- Owner: `cataclysm:the_incinerator`
- Trigger: fully charged release
- State: `COUNTED_EXACT`

## Semantic action

creates the provider forward sequence of Flame Strikes and settles cooldown.

## Exact acquisition

exact provider recipe.

## Semantic exclusion/deduplication

Individual spawned strikes are downstream substeps.

## Provider boundary

Cataclysm retains ownership of activation, costs, cooldowns, attachments, spawned effects/entities, world state and settlement. Black Arcana inventories the identity without duplicating its runtime or charging an additional resource.

Source: [exact 3.33 aggregate](README.md), grounded in [exact-artifact audit](../EXACT-3.33-ARTIFACT-AUDIT.md).
