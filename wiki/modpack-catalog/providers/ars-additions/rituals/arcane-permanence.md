# Ars Additions — Arcane Permanence

Status: `SOURCE-PINNED 21.3.0 / FORCE-LOADING PROVIDER RITUAL / RUNTIME QA REQUIRED`

- Registry id: `ars_additions:ritual_chunk_loading`
- Display name: Arcane Permanence
- Source class: `RitualChunkLoading`

## Provider-native behavior

This ritual is explicitly a chunk force-loader. It captures the activating player UUID, derives a square chunk set from a configurable chunk-radius, and delegates load/unload state to provider `ChunkLoadingData`.

The source periodically reasserts loading every 20 ticks and releases chunks when Source is needed, the ritual status changes, it ends or is destroyed. Activating player identity and elapsed ticks are persisted in ritual NBT.

## Source-default configuration

- Source cost enabled: yes.
- Repeating cost: yes.
- Cost: 10,000 Source.
- Cost interval: 24,000 ticks (one Minecraft day).
- Initial radius: 0 chunks, i.e. a 1×1 chunk footprint.
- Incremental radius: disabled by default.
- Increment item: `ars_nouveau:source_gem_block`.
- Maximum incremental increases: 1.
- Activating player required online: yes in config; effective enforcement is a provider runtime QA item beyond this class.
- Per-player ritual limit: effectively unbounded by default (`Integer.MAX_VALUE`).
- Chunk-loading logging: disabled.

The ritual's `canStart` also checks provider `ChunkLoadingData.countChunks(...)` against the configured player limit.

## Black Arcana safety boundary

Black Arcana's architecture remains no-force-load by default. This provider ritual does not create an entitlement for Black Arcana casts/domains to load chunks. Any future observation/compatibility bridge must respect provider ownership and must not widen Black Arcana's Stage 04/07.06 loaded-chunk contracts.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`RitualChunkLoading`, `ServerConfig`).
