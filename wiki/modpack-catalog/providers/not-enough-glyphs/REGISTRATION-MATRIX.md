# Not Enough Glyphs 4.6.1 — Current-Pack Registration Matrix

Authority for conditional registration: `ArsNouveauRegistry.registerGlyphs()` at source pin `2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b`, reconciled with the physical modlist.

## Totals

- NEG calls `APIRegistry.registerSpell` for **40** primitives under the current pack's loaded-mod conditions.
- **39** are source-enabled before external/user config.
- `not_enough_glyphs:momentum` is registered but source-disabled.
- Four Ars Elemental primitives are appended to NEG's internal `registeredSpells` list because Ars Elemental is installed; they are **not** registered by NEG and are excluded from the 40.
- Ars Controle Random is not registered by NEG because Ars Controle is installed.

| Namespace/role | Count | Current-pack condition |
|---|---:|---|
| NEG-native | 15 | always registered; Momentum disabled by source |
| Too Many Glyphs fallback | 14 | `toomanyglyphs` absent |
| Ars Trinkets fallback | 2 | `ars_trinkets` absent |
| Ars Omega fallback | 8 | `arsomega` absent |
| Ars Scalaes fallback | 1 | unconditionally registered by NEG |
| Ars Elemental delegated references | 4 | `ars_elemental` present; no NEG re-registration |
| Ars Controle Random fallback | 0 | `ars_controle` present; fallback suppressed |

## Effective registrations

| Registry identity | Implementation class | Status | Acquisition summary |
|---|---|---|---|
| `not_enough_glyphs:plow` | `EffectPlow` | enabled | Earth Essence + Stone Hoe |
| `not_enough_glyphs:trail` | `MethodTrail` | enabled | Dragon's Breath + 2 Echo Shards + Air Essence |
| `not_enough_glyphs:momentum` | `EffectMomentum` | **source-disabled** | no generated glyph recipe |
| `not_enough_glyphs:ride` | `EffectRide` | enabled | Saddle + Manipulation Essence |
| `not_enough_glyphs:feed` | `EffectFeed` | enabled | 6 food-tag items + Conjuration Essence |
| `not_enough_glyphs:filter_light` | `FilterLight` | enabled | Torch |
| `not_enough_glyphs:filter_dark` | `FilterDark` | enabled | Torch + black dye tag |
| `not_enough_glyphs:contingency_fall` | `FallContingency` | enabled | Abjuration Essence + Repeater + Feather |
| `not_enough_glyphs:contingency_heal` | `HealContingency` | enabled | Abjuration Essence + Repeater + Honey Bottle |
| `not_enough_glyphs:contingency_health` | `HeroicsContingency` | enabled | Abjuration Essence + Repeater + Leather Chestplate |
| `not_enough_glyphs:contingency_death` | `DeathContingency` | enabled | Abjuration Essence + Repeater + skull tag |
| `not_enough_glyphs:contingency_fire` | `FireContingency` | enabled | Abjuration Essence + Repeater + Magma Cream |
| `not_enough_glyphs:contingency_blink` | `BlinkContingency` | enabled | Abjuration Essence + Repeater + Ender Pearl |
| `not_enough_glyphs:contingency_time` | `ExpireContingency` | enabled | Abjuration Essence + Repeater + Clock |
| `not_enough_glyphs:propagate_plane` | `PropagatePlane` | enabled | Manipulation Essence + Diamond Block + Firework Star + Wilden Spike |
| `toomanyglyphs:ray` | `MethodRay` | enabled fallback | Target + Source Gem |
| `toomanyglyphs:reverse_direction` | `EffectReverseDirection` | enabled fallback | Manipulation Essence + Glass Pane |
| `toomanyglyphs:chaining` | `EffectChaining` | enabled fallback | Manipulation Essence + 3 Chains + Lapis Block + Redstone Block + Source Gem Block |
| `toomanyglyphs:filter_block` | `FilterBlock` | enabled fallback | cobblestone tag |
| `toomanyglyphs:filter_entity` | `FilterEntity` | enabled fallback | iron nugget tag |
| `toomanyglyphs:filter_living` | `FilterLiving` | enabled fallback | Dandelion |
| `toomanyglyphs:filter_living_not_monster` | `FilterLivingNotMonster` | enabled fallback | Oxeye Daisy |
| `toomanyglyphs:filter_living_not_player` | `FilterLivingNotPlayer` | enabled fallback | Blue Orchid |
| `toomanyglyphs:filter_monster` | `FilterMonster` | enabled fallback | Lily of the Valley |
| `toomanyglyphs:filter_player` | `FilterPlayer` | enabled fallback | Poppy |
| `toomanyglyphs:filter_item` | `FilterItem` | enabled fallback | Emerald |
| `toomanyglyphs:filter_animal` | `FilterAnimal` | enabled fallback | Beef |
| `toomanyglyphs:filter_is_baby` | `FilterBaby` | enabled fallback | egg tag |
| `toomanyglyphs:filter_is_mature` | `FilterMature` | enabled fallback | Chicken |
| `ars_trinkets:filter_self` | `FilterSelf.SELF` | enabled fallback | Cornflower |
| `ars_trinkets:filter_not_self` | `FilterSelf.NOT_SELF` | enabled fallback | Allium |
| `arsomega:flatten` | `EffectFlatten` | enabled fallback | Earth Essence + Iron Shovel + Anvil |
| `arsomega:propagate_underfoot` | `PropagateUnderfoot` | enabled fallback | Manipulation Essence + Ars Underfoot glyph |
| `arsomega:propagate_projectile` | `PropagateProjectile` | enabled fallback | Manipulation Essence + Ars Projectile glyph |
| `arsomega:propagate_self` | `PropagateSelf` | enabled fallback | Manipulation Essence + Ars Self glyph |
| `arsomega:missile` | `MethodMissile` | enabled fallback | 2 Firework Rockets + Air Essence + Fire Essence |
| `arsomega:overhead` | `MethodOverhead` | enabled fallback | Iron Helmet + Air Essence |
| `arsomega:propagate_missile` | `PropagateMissile` | enabled fallback | Manipulation Essence + Missile glyph |
| `arsomega:propagate_overhead` | `PropagateOverhead` | enabled fallback | Manipulation Essence + Overhead glyph |
| `ars_scalaes:resize` | `EffectResize` | enabled fallback | Manipulation Essence + Abjuration Essence + Brown Mushroom |

## Delegated but not re-registered

Because `ars_elemental` is installed, NEG adds these provider objects only to its internal documentation/listing surface: Arc Projectile, Homing Projectile, Propagate Arc and Propagate Homing. Their runtime registration authority remains Ars Elemental.

Because `ars_controle` is installed, `FilterRandom` is not registered by NEG. Runtime authority remains Ars Controle.

## Phase 2BI config gate

The matrix's 39 `source-enabled` rows are **not yet active-pack counted rows**. Exact Ars Nouveau 5.13.1 source proves the controlling config contract:

- `GlyphRegistry.registerSpell(part)` calls `part.buildConfig(...)`;
- the resulting spec is registered as `ModConfig.Type.SERVER`;
- the explicit filename is `<namespace>/<path>.toml`, yielding `not_enough_glyphs/<glyph>.toml` for NEG IDs;
- base `AbstractSpellPart` defines `[general].enabled = true` as a source default and `isEnabled()` reads that value;
- NEG `momentum` remains explicitly disabled by its own override.

Because NeoForge SERVER configs can be overridden per world and the deployed server/world config set is not available in authoritative project material, the 39 rows stay `CONDITIONAL`. Source defaults are not substituted for deployed state. Semantic delta: **+0**; strict total: **1249**.
