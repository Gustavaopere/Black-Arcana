# Capability Matrix Delta — Soul Fire'd 6.1.0

Scope: exact physical `soul_fire_d` 6.1.0 + exact publisher NeoForge File ID `7364962` + exact official `1.21` source revision `0cc7a03b950e74742eb75f51642cc7a0190c7127`.

| Capability / surface | Exact result | Authority | Black Arcana disposition |
|---|---|---|---|
| Standalone spells | 0 | none | no spell-catalog inflation |
| Glyphs / rituals | 0 / 0 | none | no BA duplication |
| Generic custom-fire API | moved out in 6.x | Prometheus 1.2.5 | provider-native boundary only; do not rebuild framework |
| Soul Fire type | `minecraft:soul` | Soul Fire'd definition via Prometheus runtime | preserve provider identity |
| Soul Fire light | 10 | Soul Fire'd definition | no BA override by default |
| Soul Fire damage value | 2 | Soul Fire'd definition / Prometheus execution | no duplicate damage settlement |
| Soul Fire flame particle | vanilla Soul Fire flame particle | Minecraft asset + provider definition | presentation is not cast authority |
| Associated fire charge | `minecraft:soul_fire_charge` | Soul Fire'd content registered through Prometheus | do not duplicate item/recipe |
| Soul Fire Charge recipe | shapeless; 16 output | Soul Fire'd data | no duplicate acquisition |
| Soul Fire Aspect | `minecraft:soul_fire_aspect`, max 2 | Soul Fire'd static datapack + Prometheus ignite | enchantment, not spell |
| Soul Flame | `minecraft:soul_flame`, max 1 | Soul Fire'd static datapack + Prometheus ignite | enchantment, not spell |
| Enchantment exclusivity | Prometheus Fire Aspect/Flame exclusive sets | Prometheus tags + Soul Fire'd data | preserve provider exclusivity |
| Static enchantment datapack | `soul_fire_d:enchantments`, top position | Soul Fire'd/Cobweb | no duplicate data override |
| GLM serializers | 1: `soul_fire_d:chest_loot_modifier` | Soul Fire'd/NeoForge | no second loot settlement |
| Bastion book acquisition | two independent 5% level-1 additions | Soul Fire'd loot data | no duplicate reward path |
| Common mixins | 0 | none | do not infer hooks from config filename |
| NeoForge mixins | 0 | none | do not infer hooks from config filename |
| Mana / cast resource | 0 | none | BA retains own resource/cast authority |
| Corruption / Strain / Arcane Danger | none | Black Arcana | no coupling |
| BA destructive hazards | no provider authority | Black Arcana `WorldEffectPolicy` | provider fire type never bypasses policy |

## Deduplication result

Soul Fire'd closes a fire/content overlap, not a missing Black Arcana spell runtime. The physical pack already owns Soul Fire behavior, two Soul Fire enchantments, their acquisition and a provider-native fire framework through Prometheus.

Black Arcana may still have original fire-domain magic, but it must distinguish **spell/hazard causality** from the provider's generic entity-fire and enchantment mechanics.

## Authority result

Prometheus is the 6.x framework owner. Soul Fire'd owns the Soul-specific definitions/content. Black Arcana owns BA magic runtime and world safety. RPG Skill Tree remains progression-only through real contracts.
