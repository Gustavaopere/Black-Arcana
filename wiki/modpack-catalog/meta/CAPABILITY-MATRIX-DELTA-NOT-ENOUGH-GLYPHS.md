# Capability Matrix Delta — Not Enough Glyphs 4.6.1

Phase 2AF closes the current-pack source-level capability inventory for NEG. It improves deduplication evidence only; Phase 3 remains blocked.

| Capability family | Current NEG/provider evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| Event-triggered stored spells | 7 Sauce-backed contingencies | Sauce + NEG + Ars caster/mana | externally covered; no second generic contingency engine |
| Trail repeated delivery | NEG Trail + TrailingProjectile | NEG/Ars resolver | external coverage; no duplicate tick/projectile loop |
| Missile delivery | Omega fallback Missile + MissileProjectile | NEG fallback under `arsomega` + Ars | external coverage; preserve historical namespace/provider semantics |
| Ray delivery | TMG fallback Ray | NEG fallback under `toomanyglyphs` + Ars | external coverage |
| Chained resolution | TMG fallback Chaining | NEG fallback + Ars | external coverage; bounded config/provider runtime remains authority |
| Plane/circle/hollow geometry | Propagate Plane | NEG/Ars | external geometry coverage; generic plane geometry is not a BA gap |
| Target predicates | light/dark + 13 fallback target filters | Ars/NEG fallback | external filter coverage |
| Farming/terrain utility | Plow; Omega fallback Flatten | provider | overlap; do not replay mutations; protection QA preserved |
| Mounting | Ride | NEG/Ars | external entity-control coverage |
| Food/Stuffed/crush interaction | Feed + Stuffed + event handler | NEG/Ars/Sauce attributes | external gameplay effect; not BA Backlash |
| Resize | `ars_scalaes:resize` fallback | NEG fallback + vanilla SCALE/Ars | external resize coverage |
| Multi-spell cast device | Spell Binder 25 storage / 10 caster | NEG + Ars caster | no second spellbook/container runtime |
| Spell focus through item perks | six current focus perks | NEG + Ars/Ars Elemental | provider-native; do not transfer spell-school authority |
| Random spell-stat mutation | Wild Magic thread | NEG/Sauce/Ars stats | generic randomness is not a Chaos gap |
| Mana discount/damage tradeoff | Cheap Damage thread | Sauce mana-discount + Ars damage attr | provider stats, not BA resource |
| Slow/projectile-power tradeoff | Slow Power thread | NEG/Ars stats | provider stats |
| Physical Binder combat modifiers | Sharp/Knockback threads | vanilla attributes + NEG | gear behavior, not BA spell authority |
| Spell crit | crit chance/damage threads | Sauce crit attributes | provider-owned crit semantics |
| Provider migration aliases | old Ars namespace aliases for perks | NEG/Ars registry | migration only; do not count duplicate capabilities |

## Gap impact

The following generic ideas cannot be asserted as Black Arcana gaps solely from fantasy similarity:

- trigger a stored spell on fall/heal/health/death/fire/teleport/time;
- generic ray/missile/trail delivery;
- generic chain-to-nearby-targets;
- plane/circle/hollow propagation;
- generic block/entity/player/monster/animal/self filters;
- generic resize;
- multi-spell Binder/container;
- generic random spell-stat mutation or crit thread.

A Black Arcana design remains legitimate only if it proves a materially different semantic contract while preserving Black Arcana authority and provider boundaries.
