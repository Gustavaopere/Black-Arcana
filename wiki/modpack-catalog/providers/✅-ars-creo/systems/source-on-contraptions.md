# Source on Create contraptions

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Ars Creo registers Ars Source Jar and Creative Source Jar as `SourceInfo` types and exposes the moving contraption through an Ars `ISpecialSourceProvider`.

Normal Source is read from the jar NBT, maxes at 10,000 per registered normal jar in this source implementation and is added/removed directly from the contraption's serialized block info. The aggregate `ContraptionSource` sums the registered Source blocks and uses the maximum transfer rate among them.

A Creative Source Jar causes `hasInfiniteSource()` to return true. `SourceUtilMixin` then special-cases Ars source search/take logic for this provider.

`SourceJarBehavior` adds one provider per moving contraption to Ars `SourceManager` and removes it when movement stops.

Authority remains Ars Source. Black Arcana must not create a parallel moving-resource cache or second deduction.