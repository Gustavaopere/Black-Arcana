# 03.03 — Eidolon: Repraised

## Intent
Make Eidolon the primary occult/ritual presentation layer where its public API/data model permits it.

## Verified 1.21.1 surface
- `alexthw.eidolon_repraised.api.ritual.Ritual` is public and subclassable.
- `RitualRegistry.register(ResourceLocation, Ritual)` and `find(ResourceLocation)` are public.
- `GenericRitualRecipe` resolves the ritual implementation by registered id.
- Generated ritual JSON uses recipe type `eidolon_repraised:ritual_brazier`.

## Preparatory implementation
- non-destructive `black_arcana:eidolon_integration_probe` ritual registered through the public API;
- conditional recipe guarded by `neoforge:mod_loaded`;
- optional mod-bus bootstrap performs registration only when Eidolon is loaded;
- server descriptor advertises only `RITUAL_HOST` after the registered ritual is confirmed;
- descriptor itself has no Eidolon binary references;
- failed registration/linkage becomes `API_INCOMPATIBLE`, never a silent capability.

## Rule
If Eidolon lacks a stable public hook for a future grand ritual, implement a Black Arcana ritual engine that consumes/recognizes Eidolon content instead of mixin-patching internals by default.

## Acceptance state
Source implementation and source-level contracts are prepared. The positive installed-Eidolon runtime profile still requires a real executing runner before this task can receive a completion check.
