# KubeJS Ars Nouveau 1.3.2 — publisher release-line framework surface

Status: `RELEASE-LINE SOURCE AUDITED / PHYSICAL 1.3.2 HASH KNOWN / BYTE-EQUIVALENT SOURCE PIN NOT PROVEN / RECIPE CAPABILITIES ONLY`

## Provenance

Physical artifact:

- `kubejsarsnouveau-1.3.2.jar`;
- SHA-1 `f39f4f409e628731be551fd961fac2964768d358`;
- CurseForge project/file `833926 / 7181937`.

Publisher release-line source checkpoint:

`BobVarioa/kjsarsnouveau@18278a05d27def7200158a6d08516d5f22318e44`

The 1.3.2 publisher file points to the update-to-latest-KubeJS release line, but the public repository at this checkpoint still declares `mod_version=1.3.1`. Treat the source as release-line framework evidence, not a physical-JAR↔source byte-equivalence claim.

## Recipe component types

`KubeJSArsNouveauPlugin.registerRecipeComponents` registers exactly three custom components:

1. `ars_nouveau:crush_item`;
2. `ars_nouveau:color`;
3. `ars_nouveau:sound`.

`crush_item` serializes stack/chance/max-range data; `color` serializes id/R/G/B; `sound` serializes optional sound family, volume and pitch. These are recipe serialization components, not magical semantic objects.

## Recipe schemas

`registerRecipeSchemas` registers exactly six Ars Nouveau recipe schemas:

1. `ars_nouveau:enchanting_apparatus`;
2. `ars_nouveau:enchantment`;
3. `ars_nouveau:crush`;
4. `ars_nouveau:imbuement`;
5. `ars_nouveau:glyph`;
6. `ars_nouveau:caster_tome`.

The glyph schema describes acquisition/recipe data for an existing valid glyph; it does not register a new glyph implementation. The caster-tome schema stores a sequence of existing spell-part IDs plus presentation metadata; it does not mint new spell-part identities.

## Active scripting surface

The inspected release-line plugin contains a `registerBindings` block for `CrushItem`, `Color` and `Sound`, but that override is commented out by commit `b3589e5a...`.

Established active counts at the checkpoint:

- custom recipe component types: **3**;
- recipe schemas: **6**;
- active named KubeJS bindings: **0**;
- KubeJS registry-builder registrations: **0**;
- provider KubeJS event groups/handlers: **0**;
- fixed provider-owned glyph implementations: **0**;
- fixed provider-owned spell programs: **0**.

Repository-wide inspection at the checkpoint found no `registerBuilderTypes`, `registerEvents`, `AbstractSpellPart`/`SpellPart` construction surface, glyph registry builder or StartupEvents registration path owned by this bridge.

## Semantic implication

Scripts can materially alter recipe inputs/outputs, Source or XP cost, glyph acquisition, enchanting/imbuement/crush processing and caster-tome presets. Those changes can affect reachability/economy of existing Ars content.

They do not, through the established bridge surface, create a provider-owned glyph implementation.

Strict provider-owned semantic delta: **+0**.
