# Create: Chromatic Return 1.0.4 — semantic surface disposition

Status: `EXACT-CURRENT / ZERO_SEMANTIC_ENCHANT_GEAR_INFRA`

| Surface | Exact role | State | Reason |
|---|---|---|---|
| Durasteel Infused Book | crouch + off-hand book applies `durable` to eligible main-hand tool | `EXCLUDED` | enchantment application/economy utility, not standalone magic action |
| Industrium Infused Book | crouch + off-hand book applies `wrenching` | `EXCLUDED` | enchantment application/economy utility |
| Silkstrum Infused Book | crouch + off-hand book applies `super_silk_touch` | `EXCLUDED` | enchantment application/economy utility |
| `durable` enchantment | prevents/repairs durability loss through provider enchant behavior | `EXCLUDED` | downstream enchantment effect |
| `wrenching` enchantment | custom right-click/block interaction behavior | `EXCLUDED` | downstream enchantment effect |
| `super_silk_touch` enchantment | custom block-break/silk behavior | `EXCLUDED` | downstream enchantment effect |
| Multiplite/Antiplite charm flight | equipment/Curios-driven Creative Flight state | `EXCLUDED` | passive gear mobility, no cast root |
| Refined/Shadow/Industrium/Silkstrum charms | passive speed/haste/strength/jump/equipment effects | `EXCLUDED` | passive gear state |
| Antiplite charm-slot modification | adds/removes Curios charm slots while equipped | `EXCLUDED` | equipment/inventory infrastructure |
| Glow Saber / Glow Claws | weapon/tool attacks/mining | `EXCLUDED` | ordinary weapon/tool operation despite extreme power |

## Result

- exact independent semantic magic identities: **0**;
- strict delta: **+0**;
- disposition: **`ZERO_SEMANTIC_ENCHANT_GEAR_INFRA`**.
