# YUNG's Better End Island — 1.21.1-NeoForge-3.1.2

Status: `✅ CATALOGED / CURRENT PHYSICAL 3.1.2 / ZERO_SEMANTIC_END_WORLDGEN_DRAGON_FIGHT_OVERLAY / +0 STRICT / DRAGON-FIGHT QA SEPARATE`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`.

- JAR: `YungsBetterEndIsland-1.21.1-NeoForge-3.1.2.jar`;
- mod id: `betterendisland`;
- runtime: `1.21.1-NeoForge-3.1.2`;
- physical SHA-1: `832f2c17425debe74a9f267f4136f1a0f0221d19`;
- Minecraft / loader: 1.21.1 / NeoForge;
- host dependency: YUNG's API.

## Semantic disposition

This provider redesigns the End central island and dragon-fight flow:

- pillars/gateways/spawn platform/tower;
- proximity-triggered initial dragon fight;
- central-island state;
- resummon crystal positions/compatibility;
- reset/configuration surfaces.

It does **not** establish an independent provider-owned player spell/glyph/rite/ritual identity.

The initial dragon appearance is world/fight-state progression triggered by proximity, not a discrete player-owned cast. Dragon resummoning remains the underlying Minecraft End Crystal resummon lifecycle; changing arena positions/compatibility does not create a second semantic ritual identity owned by this addon.

Canonical disposition:

`ZERO_SEMANTIC_END_WORLDGEN_DRAGON_FIGHT_OVERLAY`

Strict semantic contribution: **+0**.

## Ownership boundary

- Minecraft retains Ender Dragon entity/fight authority.
- YUNG's Better End Island owns its central-island/worldgen/fight-flow overlay.
- BetterEnd owns its separate dimensional biome/content surfaces.
- Administrative `/end_island reset` is maintenance tooling, not a magic action.

## Catalog consequence

- provider directory: ✅ cataloged;
- independent semantic magic identities: **0**;
- strict delta: **+0**;
- first-entry/resummon/reset/BetterEnd coexistence: runtime/world QA separate;
- no duplicate dragon-summoning ritual is added to the semantic ledger.
