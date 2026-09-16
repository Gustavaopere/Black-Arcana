# Ars Elemancy 1.18.3 — bangles

Status: `7/7 SOURCE-PINNED / RUNTIME ATTRIBUTE QA PENDING`

All seven bangles extend Ars Elemental `ElementalCurio`, implement Sauce `ISchoolBangle`, and are included in generated `curios:bracelet` tag data.

For each subschool present on a bangle's school, source adds:

| Subschool | Attribute behavior |
|---|---|
| Air | `+0.06` Movement Speed ADD_VALUE; `+1.2` Attack Knockback ADD_VALUE |
| Earth | `+0.3` Knockback Resistance ADD_VALUE |
| Fire | if biome base temperature > 1.8: `+0.035` Movement Speed ADD_VALUE |
| Water | `+0.5` NeoForge Swim Speed ADD_VALUE; if in water/rain: `+0.035` Movement Speed ADD_VALUE |
| Anima | `+4` Max Health ADD_VALUE |
| Summon | `+2` Sauce Summon Power ADD_VALUE |

The locally constructed six dual schools only contain elemental Air/Water/Earth/Fire pairs. The Anima/Summon branches are generic implementation surface and are not attributed to those six registered bangles.

Elemancer Bangle uses Ars `SpellSchools.ELEMENTAL`. Exact expansion of that host school's subschools must be verified against the physical Ars Nouveau version before claiming a specific combination of all branch attributes.

Attribute application remains Curios/provider-owned. Black Arcana does not reapply these modifiers based on item presence.