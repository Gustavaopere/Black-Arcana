# Create: Enchantable Machinery 3.6.0 — semantic surface disposition

Status: `ZERO_SEMANTIC_MACHINE_ENCHANTMENT_APPLICATION`

| Surface | Exact behavior | Semantic state |
|---|---|---|
| 11 enchantable Create machine variants | mapped block/state containers for enchantment data | `EXCLUDED_MACHINE_STATE` |
| Enchanting Table / anvil compatibility | applies existing vanilla/modded enchantments to supported machine items | `EXCLUDED_ENCHANTMENT_ECONOMY` |
| Drill/Roller/Saw use mixins | convert/delegate matching already-enchanted machine item to enchantable variant | `EXCLUDED_STATE_APPLICATION` |
| Efficiency handling | changes machine speed/processing behavior by reading existing enchantment level | `EXCLUDED_EXTERNAL_ENCHANT_EFFECT` |
| Silk Touch / Fortune handling | modifies machine harvest/drop settlement using existing enchantments | `EXCLUDED_EXTERNAL_ENCHANT_EFFECT` |
| Goggles/Jade/glint | presentation of persisted enchantment state | `EXCLUDED_PRESENTATION` |
| Break/place/loot copy | persists `minecraft:enchantments` component | `EXCLUDED_PERSISTENCE` |
| Provider-owned enchantment definitions | none in exact artifact | `ZERO_ENCHANTMENT_ROSTER` |
| Spell/ritual/glyph/ability roster | none in exact artifact | `ZERO_MAGIC_ACTION_ROSTER` |

## Accounting

- provider-owned enchantment identities: **0**;
- provider-owned semantic magic actions: **0**;
- strict delta: **+0**;
- folder state: **✅ cataloged**.

Machine/enchantment combinations are parameters of existing enchantments and are never multiplied into separate Black Arcana semantic objects.
