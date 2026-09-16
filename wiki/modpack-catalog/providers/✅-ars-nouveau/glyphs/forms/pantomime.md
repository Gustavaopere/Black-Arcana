# Pantomime

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_pantomime`
- Source class: `MethodPantomime`

## Source-pinned behavior

Pantomime resolves the following spell effects at a provider-computed block position in the caster's line of sight rather than requiring a normal clicked target. Its base distance is derived from the caster's view pitch and then modified by Amplify/Dampen.

The exact source uses a default mana cost of **5**. Dampen is explicitly limited to one instance by this Form's default augment-limit table. Provider configuration remains authoritative for effective casting cost and other configurable spell-part data.

## Compatible augments

The exact source permits:

- `ars_nouveau:glyph_amplify` — increases target distance;
- `ars_nouveau:glyph_dampen` — reduces target distance, default limit 1 on this Form;
- `ars_nouveau:glyph_sensitive` — highlights the selected block through provider presentation behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `#c:glass_blocks` ×8.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned: using the crafted Glyph server-side records it in Ars player data and consumes the Glyph in survival. Runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Pantomime is an Ars-owned line-of-sight targeting form. Its existence is a strong deduplication signal against generic "cast at a nearby looked-at block" content. Black Arcana targeting remains server-owned under D006/D019 and must not trust an Ars/client-computed position as authoritative for Black Arcana world effects.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`