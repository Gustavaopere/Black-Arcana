# Foundation domain contracts

The package `dev.gustavopere.blackarcana.api` is deliberately free of Minecraft client classes and external magic-mod types.

The canonical execution order is:

1. progression gate;
2. cooldown validation;
3. target resolution;
4. resource-cost validation;
5. world-effect policy authorization;
6. cost consumption;
7. effect execution;
8. cooldown start after successful effect.

Expected denial states are values (`ArcanaCastResult.Status` + code/detail), not exceptions. Exceptions remain reserved for programmer errors and broken invariants.

`ArcanaIntegration` exposes only Black Arcana-owned availability/version metadata. Iron's, Ars Nouveau, Eidolon, Malum and RPG-specific types must stay behind adapters introduced in Stage 03.

The foundation intentionally does not define a universal mana capability. `CostProvider` is the extension seam for mana, source, spirits, health, items, durability, composite costs, or zero-cost effects.
