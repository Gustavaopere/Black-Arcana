# Foundation domain contracts

The package `dev.gustavopere.blackarcana.api` is deliberately free of Minecraft client classes and external magic-mod types.

The canonical execution order is:

1. progression gate;
2. cooldown validation;
3. target resolution;
4. resource-cost affordability validation;
5. world-effect policy authorization;
6. atomic cost reservation/revalidation;
7. effect execution;
8. cost commit after successful effect, or refund on failed/exceptional effect execution;
9. cooldown start after successful effect and committed cost.

`CostProvider.check` is an early deterministic affordability gate. `CostProvider.reserve` is the race-safe transaction boundary immediately before execution and returns a provider-owned `CostReservation`. A successful reservation must be atomically committable/refundable by the provider. The cast engine calls exactly one terminal path: `commit` after a successful effect, or `refund` if effect execution fails or throws before commit. Composite providers introduced in Stage 02 must reserve all component costs atomically or deny the reservation without partial consumption.

Expected denial states are values (`ArcanaCastResult.Status` + code/detail), not exceptions. Exceptions remain reserved for programmer errors and broken invariants; an exceptional effect path still refunds an uncommitted reservation before propagating the exception.

`ArcanaIntegration` exposes only Black Arcana-owned availability/version metadata. Iron's, Ars Nouveau, Eidolon, Malum and RPG-specific types must stay behind adapters introduced in Stage 03.

The foundation intentionally does not define a universal mana capability. `CostProvider` is the extension seam for mana, source, spirits, health, items, durability, composite costs, or zero-cost effects.
