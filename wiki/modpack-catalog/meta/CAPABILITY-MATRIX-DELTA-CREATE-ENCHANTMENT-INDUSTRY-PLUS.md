# Capability Matrix Delta — Create Enchantment Industry Plus 1.1.1

Scope: exact physical `create_enchantment_industry_plus` 1.1.1 + exact official source revision `TiesToetToet/create_enchantment_industry_plus@fb97ed35288f7ff2c80d43ef33f051db93d281d5`.

| Capability / surface | Exact result | Authority | Black Arcana disposition |
|---|---|---|---|
| Standalone spells | 0 | none | no spell-catalog inflation |
| Glyphs / rituals | 0 / 0 | none | no BA duplication |
| Provider mana / cast resource | 0 | none | BA retains cast/resource authority |
| Registered addon items | 1: `create_enchantment_industry_plus:sac` | CEI Plus | preserve provider identity |
| Addon-owned recipe JSONs | 6 | CEI Plus data + executing recipe provider | no duplicate settlement |
| Host-recipe disable overlays | 1: CEI `mixing/ink` with `neoforge:never` | CEI Plus datapack overlay | do not re-enable through BA |
| Pressing route | leather → `sac` | Create process + CEI Plus recipe | Create executes; addon defines recipe |
| Glow Ink route | ink sac + 250 CEI experience → glow ink sac | Create + CEI + CEI Plus | no second experience debit |
| Black-dye fill route | `sac` + 250 CDP black dye → ink sac | Create + CDP + CEI Plus | preserve provider resource identity |
| Grinding route | ink sac → 250 CDP black dye | CDP `grinding` + CEI Plus recipe | no fallback grinder invented |
| Mixing route A | ink sac + water → CDP black dye + `sac` | Create + CDP + CEI Plus | no duplicate conservation settlement |
| Mixing route B | wither rose + water → CDP black dye | Create + CDP + CEI Plus | no duplicate recipe |
| Public drain flow | described publicly; absent from exact 1.1.1 source tree | owner not proven | fail-closed / do not invent |
| Create metadata range | `[6.0.4,6.1.0)` under mis-keyed `dependencies.create_enchantment_industry` table | source metadata anomaly | physical Create 6.0.10 present; addon-owned declaration/loader treatment not asserted |
| Declared CEI dependency | `[2.0.0,)` under addon dependency table | provider metadata | physical CEI 2.5.3b satisfies |
| Create Dragons Plus dependency | used by recipe data, not declared in metadata | CDP content/type authority | record implicit data dependency; no synthetic fallback |
| Java source files | 2 | CEI Plus | tiny closed source surface |
| Mixins | 0 | none | no inferred hidden hook |
| Network / persistence | none observed | none | no BA pipeline relation |
| Corruption / Strain / Arcane Danger | none | Black Arcana | no coupling |

## Deduplication result

Create Enchantment Industry Plus closes a processing/recipe overlap, not a missing spell family. Its current semantic contribution is one intermediate item plus six explicit recipes and one host-recipe disable overlay.

The current pack already has Create, Create: Enchantment Industry and Create: Dragons Plus as the execution/resource providers required by these data routes. Black Arcana must not reproduce their processing, fluids, recipe types or resource settlement.

## Authority result

Create owns Create processing execution. Create: Enchantment Industry owns its experience/enchantment-processing domain. Create: Dragons Plus owns the `black_dye` fluid and `grinding` type referenced by the data. CEI Plus owns only its item and recipe/data overlays. Black Arcana owns BA magic runtime and world safety. RPG Skill Tree remains progression-only through real contracts.