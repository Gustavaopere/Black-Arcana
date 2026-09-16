# Ars Elemental 0.7.10.1 — glyph acquisition

Status: `39/39 PRODUCTION GLYPH RECIPES SOURCE-PINNED`

Source: exact `AEGlyphProvider` at `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`.

These are datagen recipes for Ars Nouveau glyph learning. The provider source pin confirms recipe generation; installed datapack/runtime QA remains pending.

| Glyph | Ingredients / learning inputs |
|---|---|
| Conjure Terrain | Earth Essence; Dirt |
| Watery Grave | Kelp; Prismarine Shard; Water Essence |
| Bubble Shield | Heart of the Sea; Prismarine Shard; Bastion Pod; Water Essence |
| Poison Spores | Spore Blossom; Red Mushroom; Earth Essence |
| Discharge | Lightning Rod; Flashing Pod; Air Essence |
| Spark | Air Essence; item tag `minecraft:wool`; Iron Bars |
| Charm | Anima Essence; Golden Carrot; Source Berry Pie; Cake |
| Life Link | Lead; Anima Essence; Sculk Sensor |
| Phantom Grasp | 2× Phantom Membrane; Anima Essence |
| Conflagrate | Gunpowder; Fire Essence; Bombegrante Pod; Netherite Scrap |
| Cauterize | Fire Essence; Abjuration Essence; Blaze Powder; Ghast Tear |
| Rage | Fire Essence; Anima Essence; Wilden Horn; Red Carpet; Fermented Spider Eye |
| Sliding | Water Essence; Abjuration Essence; Slime Ball; Ice |
| Geyser | Fire Essence; Water Essence; Magma Block; Wind Charge |
| Mist | Water Essence; Air Essence; Phantom Membrane; Blue Ice |
| Water Jet | Water Essence; Manipulation Essence; Prismarine Shard; Wilden Spike; Breeze Rod |
| Oxidize | Water Essence; Air Essence; Oxidized Copper; Abjuration Essence |
| Cavitate | Water Essence; Heart of the Sea; Pufferfish; Sponge |
| Spike | Pointed Dripstone; Netherite Ingot; Earth Essence |
| Envenom | Poisonous Potato; Fermented Spider Eye; Suspicious Stew |
| Arc Projectile | Arrow; Snowball; Slime Ball; Ender Pearl |
| Homing Projectile | Nether Star; Manipulation Essence; Dowsing Rod; Ender Eye |
| Propagate Arc | Manipulation Essence; Arc Projectile glyph item |
| Propagate Homing | Manipulation Essence; Homing Projectile glyph item |
| Filter: Aquatic | Allow Item Scroll; item tag `minecraft:fishes` |
| Filter: Not Aquatic | Deny Item Scroll; item tag `minecraft:fishes` |
| Filter: Aerial | Allow Item Scroll; Phantom Membrane |
| Filter: Not Aerial | Deny Item Scroll; Phantom Membrane |
| Filter: Fiery | Allow Item Scroll; Blaze Powder |
| Filter: Not Fiery | Deny Item Scroll; Blaze Powder |
| Filter: Undead | Allow Item Scroll; Rotten Flesh |
| Filter: Not Undead | Deny Item Scroll; Rotten Flesh |
| Filter: Summon | Allow Item Scroll; Bone |
| Filter: Not Summon | Deny Item Scroll; Bone |
| Filter: Insect | Allow Item Scroll; Spider Eye |
| Filter: Not Insect | Deny Item Scroll; Spider Eye |
| Summon Slime | Water Essence; Conjuration Essence; 2× Slime Ball |
| Summon Bee | Earth Essence; Conjuration Essence; Mage Bloom; Honeycomb |
| Nullify Defense | Nether Star; Mark of Mastery; Netherite Block; Mark of Mastery |

## Nullify acquisition gate

Nullify Defense is registered unconditionally as a production spell part, but its generated recipe is wrapped in the NeoForge condition:

- condition type: `sauce:ae_config`
- config key: `frame_skip_recipe`
- Ars Elemental common default: `false`

Therefore the glyph can exist in the runtime registry while its normal generated learning recipe is disabled by default.

## Recipe XP

Phase 2U does not copy Ars Nouveau core tier XP assumptions onto Ars Elemental. Exact recipe experience values require verification against the exact inherited builder/API behavior before they are documented.