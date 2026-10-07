# Helvar's Sword — Sword Wave

- Provider: **Bosses'Rise** (`block_factorys_bosses`)
- Version: `2.1.2`
- Exact physical/publisher SHA-1: `249a5f2ba43fd341d4a2831691c154d92aa5a12d`
- Owner: `block_factorys_bosses:knight_sword`
- Trigger: right-click charge/release
- State: `COUNTED_EXACT`

## Semantic identity

The provider creates one Sword Wave action through its dedicated item-use/cooldown path.

## Exact acquisition

Exact current acquisition is closed through Underworld Knight/Helvar entity loot.

## Boundary

Normal melee attacks remain excluded; downstream SwordWaveEntity lifecycle is settlement of this root.

Bosses'Rise remains authority for input handling, targeting, cooldown/resource state, animation and settlement. Black Arcana catalogs the identity and must not replay it.

Source: `../EXACT-2.1.2-ARTIFACT-ACTION-AUDIT.md`.
