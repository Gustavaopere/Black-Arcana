# Ars Elemancy 1.18.3 — equipment catalog

Status: `SOURCE-PINNED FAMILY-COMPLETE`

Seven identities each expose one essence, one focus, one bangle and three four-piece armor sets.

| Identity | Focus | Essence | Bangle | School |
|---|---|---|---|---|
| Tempest | `tempest_focus` | `tempest_essence` | `tempest_bangle` | Air + Water |
| Cinder | `cinder_focus` | `cinder_essence` | `cinder_bangle` | Air + Fire |
| Silt | `silt_focus` | `silt_essence` | `silt_bangle` | Air + Earth |
| Mire | `mire_focus` | `mire_essence` | `mire_bangle` | Earth + Water |
| Vapor | `vapor_focus` | `vapor_essence` | `vapor_bangle` | Fire + Water |
| Lava | `lava_focus` | `lava_essence` | `lava_bangle` | Fire + Earth |
| Elemancer | `elemancer_focus` | `elemancer_essence` | `elemancer_bangle` | Ars `ELEMENTAL` |

All IDs use namespace `ars_elemancy`.

## Armor naming

For every identity `x`:

### Light

- `x_hood`
- `x_tunic`
- `x_pants`
- `x_shoes`

### Medium

- `x_hat`
- `x_robes`
- `x_leggings`
- `x_boots`

### Heavy

- `x_helmet`
- `x_chestplate`
- `x_leggings_heavy`
- `x_boots_heavy`

Thus 7 identities × 3 weights × 4 pieces = **84 armor items**.

## Composite school definitions

The six dual schools are local `SpellSchool` objects:

- Tempest = Air + Water;
- Cinder = Air + Fire;
- Silt = Air + Earth;
- Mire = Earth + Water;
- Vapor = Fire + Water;
- Lava = Fire + Earth.

Elemancer equipment uses Ars Nouveau `SpellSchools.ELEMENTAL` instead of a seventh locally constructed SpellSchool.

These school objects categorize equipment and compatibility. Their existence is **not** evidence of six new glyph schools with local spell registries.