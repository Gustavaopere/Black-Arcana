# Dark Ritual Dagger — Sacrifice

- Provider: **Born in Chaos** (`born_in_chaos_v1`)
- Version: `1.7.6`
- Exact physical/publisher SHA-1: `73704f38ac368c03716f9cc8f537470d3b352fa2`
- Owner: `born_in_chaos_v1:dark_ritual_dagger`
- Trigger: provider player `EntityInteract` on an eligible animal/minion
- State: `COUNTED_EXACT`

## Semantic identity

The provider resolves one Sacrifice action, applies the provider `SACRIFICE`/benefit state and settles dagger cooldown/durability. Those consequences remain part of the same causal root.

## Exact acquisition

Exact provider recipe `dark_ritual_dagger_k`.

## Boundary

Eligibility, benefit state, cooldown, durability and target settlement remain Born in Chaos authority. Black Arcana catalogs the identity and must not replay provider settlement or charge a second resource/cost.

Sources: [`../EXACT-1.7.6-ARTIFACT-ACTION-AUDIT.md`](../EXACT-1.7.6-ARTIFACT-ACTION-AUDIT.md), [`SUPERNATURAL-ACTION-CARDS.md`](SUPERNATURAL-ACTION-CARDS.md).
