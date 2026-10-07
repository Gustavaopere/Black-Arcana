# Everlasting Allegiance

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:everlasting_allegiance`
- Owner/reachability: `minecraft:trident` with vanilla **Loyalty**
- Semantic type: deliberate supernatural damaging trident recall
- State: `COUNTED_EXACT`

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Everlasting Allegiance when Loyalty is present and neither the earlier Riptide nor Channeling selector branch is selected.

This closes owner/reachability through the exact vanilla-trident + enchantment surface.

## Exact provider settlement

The exact skill obtains the provider patch for the tracked thrown trident and invokes `recalledBySkill()`.

Exact thrown-trident behavior then performs Epic Fight's provider-owned return path and entity-hit settlement.

This differs semantically from vanilla Loyalty's automatic passive return because Epic Fight exposes an explicit player skill action and its own damaging recall lifecycle.

## Deduplication boundary

Repeated hits or movement during the returning trident lifecycle are settlement of the same recall root, not separate spell identities.

## Authority boundary

Epic Fight owns thrown-trident tracking, skill activation, return path, hit processing and resource settlement. Black Arcana must not trigger a second recall or duplicate damage.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
