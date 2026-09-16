# Ars Creo 5.4.0 — technical audit

Status: `SOURCE-PINNED STATIC/RUNTIME-PATH AUDIT / INSTALLED-JAR QA PENDING`

Source pin: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`.

## Registration

`ArsCreo` registers one block/item/BE family, one creative tab and two Create Display Sources. During common setup it installs Create movement/interaction behavior on existing Ars Nouveau turrets, Source Jars, Portal Block and Ritual Block; registers SourceInfo for normal/creative Source Jars; and exposes NeoForge `FluidHandler.BLOCK` on the Ars Potion Jar BE through `PotionTank`.

## Moving spell casts

`ITurretBehavior.castSpell`:

- decodes the Ars `SpellCaster` from contraption block-entity NBT;
- rejects invalid spells;
- creates an Ars `SpellContext` with `ANFakePlayer` and Ars Creo `ContraptionCaster`;
- marks wrapped caster type `OTHER`;
- charges Source from jars on the contraption first;
- if insufficient, falls back to Ars `SourceUtil` within range 6;
- resolves Projectile or Touch through Ars resolver paths.

`ContraptionCaster.expendMana` is intentionally empty because cost is settled manually as Source. This does not authorize a second mana/Source charge outside the provider path.

Basic turret casts from server-side player interaction with the moving actor. Timer turret casts when `gameTime % time == 0` for positive stored `time`. Enhanced turret casts when its moving actor visits a new block position. Rotating Turret is registered for display output but no movement/cast behavior for it is registered in exact `CreateCompat.setup()`.

## Source on contraptions

`ContraptionSource` implements Ars `ISourceTile` by aggregating registered `SourceInfo` blocks inside `contraption.getBlocks()`.

Normal Source Jar info uses source NBT, max Source 10,000 and transfer rate 10,000. Add/remove updates the contraption block info when the rendered fill state changes. Creative Source Jar makes `hasInfiniteSource()` true.

`SourceJarBehavior` adds one `ContraptionSourceProvider` to Ars `SourceManager` per moving contraption and removes it on stop. `SourceUtilMixin` special-cases infinite contraption Source and refunds already-taken providers before returning the creative provider.

## Portal bridge

`PortalBehavior` reconstructs portal destination data from the moving block's stored NBT and delegates teleport to Ars `PortalTile.teleportEntityTo`. It ignores the contraption entity itself, handles entities in the moving portal cell on tick/new-position/collision paths and clears fall distance after handling.

No Black Arcana teleport authorization follows from this provider behavior.

## Ritual bridge

`RitualBehavior` reconstructs an Ars ritual from `ritualID` + serialized ritual state, assigns a stand-in `RitualBrazierTile` at the moving position, consumes eligible item entities, obtains Source through Ars `SourceUtil`, runs `ritual.tryTick` and serializes state back into `MovementContext.blockEntityData`.

The source itself warns that some rituals may not work because the real tile is mocked. `RitualInteraction`'s custom interaction body is commented out in exact 5.4.0, so runtime interaction support beyond movement ticking must not be inferred.

## Potion Jar fluid bridge

`PotionTank` exposes Ars Potion Jar content as Create potion fluid through a NeoForge block-fluid capability. Capacity conversion is `maxFill * 2.5 mB`; potion-unit conversion uses `0.4` in the opposite direction with ceiling during fill/drain. It only accepts Create Potion source fluid carrying `POTION_CONTENTS` that the Ars jar accepts.

The jar remains authority for potion identity/count. Conversion rounding and third-party fluid automation require runtime QA.

## Networking

Two payload types are registered as play-to-client:

- `ars_creo:update_jar`;
- `ars_creo:update_contraption`.

Both mutate client-side contraption representation only. In the exact 5.4.0 source search, no active production send call for either packet was located; the `PacketUpdateContraption` send appears in a commented Ritual block and `PacketUpdateJarContraption` only appears in registration/class definitions. Therefore the catalog classifies them as `REGISTERED S2C SURFACE / ACTIVE SEND PATH NOT PROVEN`.

## Mixins

Common mixin: `SourceUtilMixin` for creative/infinite contraption Source behavior.

Client mixin: `GeoEntityRendererMixin`; presentation only unless later runtime evidence proves otherwise.

## Bounds and performance

Source aggregation scans blocks in the current Create contraption when queried. This is bounded by contraption size, not a global world scan. Ritual/portal/turret behaviors operate through Create actor callbacks/local cell queries. Black Arcana must not copy these loops into a parallel per-tick integration path.