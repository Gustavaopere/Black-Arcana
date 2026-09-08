# Ars Additions 21.3.0 — Stateful systems

Status: `SOURCE-PINNED / SYSTEM AUTHORITY AUDIT IN PROGRESS / RUNTIME+PACK QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

This directory tracks provider-owned systems whose behavior cannot be represented accurately as a single spell page.

## Audited surfaces

- [Warp Index and Warp Nexus](warp-and-nexus.md)
- [Ender Source](ender-source.md)
- [Source Spawner](source-spawner.md)
- [Handy Haversack](handy-haversack.md)
- [Memory Crystal](memory-crystal.md)
- [Advanced Dominion Wand](advanced-dominion-wand.md)
- [XP Jar](xp-jar.md)

## Cross-provider boundary

Ars Additions is not a second Black Arcana runtime. These systems retain provider-native state, Source accounting, inventories, network validation, world references and persistence. Black Arcana may only observe/integrate through a verified exact-version seam and must not duplicate provider settlement or infer authority from item names, particles or client presentation.

Runtime/config/client/full-pack acceptance remains separate from source catalog completion.
