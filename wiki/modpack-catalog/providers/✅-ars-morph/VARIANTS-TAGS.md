# Ars Morph 2.0.0 — Identity2 variants and form-capability tags

Status: `8 VARIANT ADAPTERS + 6 ENTITY TAGS CATALOGED / RUNTIME QA OPEN`

## Variant authority

Ars Morph registers `IdentityVariantAdapter` implementations with Identity2. These adapters define which Ars entity state is extracted, reapplied and exposed as discoverable Identity variants. Identity2 remains owner of the actual variant lifecycle/storage.

## Ars Nouveau variant adapters — 5

### Starbuncle

Fields:

- `color` string;
- `tamed` boolean.

Discovery iterates host `Starbuncle.carbyColors` and emits both untamed and tamed variants for each host-defined color. Phase 2X does not hard-code the host color count because it is host-version data.

### Whirlisprig

Field: `color` string.

Discovery is explicitly four seasons:

- summer;
- winter;
- autumn;
- spring.

### Wixie

Field: `color` string.

Discovery iterates host `EntityWixie.COLORS`; host-defined count is not duplicated into the bridge catalog.

### Drygmy

Field: `color` string.

Discovery iterates host `EntityDrygmy.COLORS`.

### Bookwyrm

Field: `color` string.

Discovery iterates host `EntityBookwyrm.COLORS`.

## Optional Ars Elemental variant adapters — 3

Registered from `ElementalModule` only through the Ars Elemental loaded gate in `IdentityReg`.

### Firenando

Field: `Variant` string.

Discovery iterates `FirenandoEntity.Variants`. Applying any variant also sets Ars Elemental Firenando `ACTIVE=true` before applying color/variant.

### Mermaid / Siren

The adapter class is `MermaidVariantAdapter`, while registration targets Ars Elemental `SIREN_ENTITY`. Field: `Variant` string. Discovery iterates host `MermaidEntity.Variants`.

This naming difference is preserved rather than normalized into an invented class/entity name.

### Flashjack

Field: `Variant` string.

The bridge defines exactly three local discoverable values:

1. `flashjack`;
2. `bluejay`;
3. `flapjack`.

## Identity2 entity-type tags — 6

All six tag files use `replace:false`, so Ars Morph adds to Identity2 capability sets rather than replacing provider-native membership.

| Tag | Required entries | Optional entries (`required:false`) |
|---|---|---|
| `identity2:can_fly` | `ars_nouveau:bookwyrm`, `ars_nouveau:wixie` | `ars_elemental:flashjack_entity` |
| `identity2:can_breathe_underwater` | `ars_nouveau:amethyst_golem`, `ars_nouveau:alakarkinos` | `ars_elemental:siren_entity` |
| `identity2:cant_swim` | `ars_nouveau:amethyst_golem` | — |
| `identity2:fire_immune` | — | `ars_elemental:firenando_entity` |
| `identity2:lava_walking` | — | `ars_elemental:firenando_entity` |
| `identity2:slow_falling` | `ars_nouveau:whirlisprig` | `ars_elemental:firenando_entity` |

Optional Ars Elemental values are data-safe when the provider is absent because they are marked non-required.

## Deduplication consequences

- Do not store a second BA/RPG copy of color/tamed/variant data for these forms.
- Do not replace the Identity2 capability tags with equivalent local boolean attributes.
- Do not add a second flight/fire-immunity/lava-walking/slow-falling effect merely because the same thematic benefit exists in BA progression.
- If BA needs to observe a player's current form, use a real Identity2 boundary and treat the provider's resulting state as authoritative.
- Ars Morph adapters are compatibility evidence, not permission to copy their implementation or assets.

## Runtime QA

Validate variant discovery, extract/apply round trips, save/reload, death/respawn, logout/reconnect and dimension change against physical Identity2 2.2.4 and the current Ars hosts. Test optional Ars Elemental entries with provider present and in an isolated absence matrix.
