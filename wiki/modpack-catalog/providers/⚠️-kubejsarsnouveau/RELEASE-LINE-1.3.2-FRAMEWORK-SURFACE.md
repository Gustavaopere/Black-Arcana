# kubejsarsnouveau 1.3.2 — publisher release-line framework surface

Status: `RELEASE-LINE SOURCE AUDITED / PHYSICAL 1.3.2 HASH KNOWN / BYTE-EQUIVALENT SOURCE PIN NOT PROVEN / RECIPE CAPABILITIES ONLY`

## Provenance

Physical artifact:

- `kubejsarsnouveau-1.3.2.jar`;
- SHA-1 `f39f4f409e628731be551fd961fac2964768d358`;
- CurseForge project 833926, file 7181937.

Publisher release-line source checkpoint:

`BobVarioa/kjsarsnouveau@18278a05d27def7200158a6d08516d5f22318e44`

The publisher file page links 1.3.2 to PR #9. The public commit chain reaches `18278a05...`, but its Gradle metadata says `mod_version=1.3.1`; do not call this a byte-equivalent 1.3.2 source pin.

## 1. KubeJS recipe component types

`KubeJSArsNouveauPlugin.registerRecipeComponents` registers exactly three custom component types from `ArsComponents`:

1. `ars_nouveau:crush_item`;
2. `ars_nouveau:color`;
3. `ars_nouveau:sound`.

### Crush item

`CrushItem` contains item stack, chance and max range. Its component implements KubeJS replacement matching against an ingredient and can replace a matched crush output with a new item stack.

### Color

`Color` contains id, red, green and blue.

### Sound

`Sound` contains optional sound/family id, volume and pitch.

These are recipe serialization components, not magical semantic objects.

## 2. Recipe schemas

`registerRecipeSchemas` registers exactly six schemas under the Ars Nouveau namespace.

### `ars_nouveau:enchanting_apparatus`

Fields: `pedestalItems` (zero-or-more ingredients), `reagent`, `result`, `sourceCost`/`source` optional default 0, and `keepNbtOfReagent`/`keepNbt` optional default false.

### `ars_nouveau:enchantment`

Fields: `pedestalItems`, `enchantment`, `level`, `sourceCost`/`source`.

### `ars_nouveau:crush`

Fields: `input`, list of custom `crush_item` outputs, and `skip_block_place` optional default true.

### `ars_nouveau:imbuement`

Fields: `input`, `output`, `source`, zero-or-more `pedestalItems`.

### `ars_nouveau:glyph`

Fields: list `inputs`, item-stack `output`, and `exp` with aliases `experience`/`xp`, optional default 0.

This schema describes a glyph **recipe**. No release-line source registration of a new `AbstractSpellPart`/glyph implementation builder was found.

### `ars_nouveau:caster_tome`

Fields: `tome_type`/`tomeType` default `ars_nouveau:caster_tome`, `name`, `flavour_text` and aliases, custom `color`, string-list `spell`, and optional custom `sound`.

The schema supports alternate constructors down to a name-only form. It serializes tome recipe/preset data; it does not define glyph implementation logic.

## 3. Bindings

The release-line plugin source contains a `registerBindings` block for `CrushItem`, `Color` and `Sound`, but the entire override is commented out by commit `b3589e5a...` ("Remove bindings").

Active named KubeJS bindings established: **0**.

Do not count commented source as runtime surface.

## 4. Registry and event surfaces

Repository-wide searches at the release-line checkpoint found no:

- `registerBuilderTypes`;
- `registerEvents`;
- `AbstractSpellPart`;
- `SpellPart`;
- glyph registry builder;
- `RegistryInfo` builder registration;
- `StartupEvents` registration path.

Therefore this bridge is not established as a glyph-implementation construction framework.

## 5. Capability counts

- custom recipe component types: **3**;
- recipe schemas: **6**;
- active bindings: **0**;
- registry builder types: **0**;
- provider KubeJS event handlers: **0**;
- fixed glyph implementations: **0 established**;
- fixed spell programs: **0 established**.

These are framework capability counts and must not be added to the global magic semantic denominator.

## 6. Semantic implications

Scripts using these schemas can materially alter recipe inputs/outputs, Source cost, glyph acquisition recipes, caster tome spell/glyph sequences, and enchanting/imbuement/crush processing.

That may affect **reachability/acquisition/progression**, so the current script tree still matters operationally.

However, absent another registration mechanism outside this bridge, a recipe created through these six schemas does not become a new Ars glyph implementation merely because its recipe type is `ars_nouveau:glyph`.

Strict provider-owned semantic delta: **+0**.
