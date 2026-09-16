# Not Enough Glyphs 4.6.1 — Runtime Boundaries and Safety Audit

## Server/casting boundary

NEG registers Ars spell parts through `APIRegistry.registerSpell` and uses Ars `SpellCasterRegistry`, `AbstractCaster`, `SpellResolver`, mana/cast context and turret behavior maps. It extends this runtime; it does not define a second independent mana/casting engine.

Black Arcana integration rule: observe/adapt only through a real causal hook. Never replay the provider primitive or debit Ars resources again.

## Contingency boundary

Seven NEG contingency glyphs extend Sauce `AbstractContingency` through `NEGAbstractContingency`:

- Fall;
- Heal;
- Health;
- Death;
- Fire;
- Blink;
- Expire.

NEG event handlers trigger Sauce `ContingencyEffectInstance` for heal, death/totem and teleport paths. Other contingency behavior belongs to Sauce/base contracts. Black Arcana must not register a second trigger for the same stored contingency.

Source-specific thresholds observed:

- Fall: base 5 blocks; Amplify +1 block, Dampen -1 block.
- Health: base 20%; Amplify +10 percentage points, explicit Amplify limit 3.
- Expire: provider config is built through inherited potion-duration helpers with source arguments 60 / 30 / 200; unit interpretation is delegated to the Sauce/Ars base and is not rewritten here.

## Trail projectile

`TrailingProjectile` is a provider entity owned by NEG. Audited source imposes a maximum proc count of 20 and uses local entity/block resolution around the projectile. It is not a Black Arcana hazard/projectile and must not be duplicated by a BA scheduler.

## Missile projectile

`MissileProjectile` resolves its stored Ars spell on server-side hit/expiration and uses a local AABB derived from AOE. No global entity scan was observed. The audited class does not expose a separate explicit entity-count cap for that local AABB; keep this as a performance/QA consideration rather than inventing one.

## Plane geometry

`PropagatePlane`:

- Tier II; default mana 200;
- per-spell limit exactly 1;
- width derives from `1 + AOE`;
- depth derives from Pierce count;
- Sensitive switches to circular/cylindrical selection;
- Dampen makes the plane hollow;
- Randomize probabilistically drops positions;
- uses `SpellUtil.calcAOEBlocks` and then resolves the remainder through the provider resolver.

This is material external coverage for generic plane/circle/hollow geometry.

## Provider world mutation / protection

`EffectPlow` explicitly calls Ars `BlockUtil.destroyRespectsClaim` before applying its hoe-style action.

`EffectFlatten` does not expose an equivalent explicit claim check in the audited class. That observation does **not** prove a protection bypass: downstream APIs/events may still enforce policy. Exact compatibility with the user's claim/protection stack remains runtime QA.

Black Arcana's `WorldEffectPolicy` remains mandatory for BA-owned destructive effects. It must not be used to duplicate/replay an already-settled provider mutation.

## Feed / Stuffed event path

`Feed` consumes one valid food from the caster inventory and applies NEG `stuffed` for 400 ticks, with amplifier capped at 9 by the class. Source defaults:

- Feed Tier II, default mana 30;
- `foodxplosion_chance` default 0.1, range 0..1;
- `stuffed_crush_multiplier` default 0.25, lower bound 0.

On Ars crush damage, Stuffed increases crush damage. Under 25% health, explosion chance is multiplied by Stuffed level; the explosion path kills the target and applies crush-derived damage in a local ±4 AABB. This is provider event/effect authority, not a Black Arcana Backlash proc.

## Ride

Ride default mana is 20 and belongs to Manipulation. It refuses self, fake-player use, `Enemy` targets and entity types in NEG `ride_blacklist`; it mounts without granting steering.

## Resize

NEG unconditionally registers its fallback under `ars_scalaes:resize`. The class is Tier II, default mana 100 and manipulates vanilla `Attributes.SCALE` via provider grow/shrink effects. Exact duration helper units/values should remain provider-owned because source uses inherited config helpers and differing fallback literals.

## Mixins

- `ScribesBlockMixin`: on server main-hand interaction, a non-sneaking Spell Binder can open the normal Ars glyph-crafting packet/UI path.
- `SummoningFocusMixin`: a Binder Summoning Focus perk can satisfy Ars Summoning Focus containment semantics.

These are compatibility extensions into Ars, not Black Arcana authority.

## Registered NEG runtime objects

- 1 item: Spell Binder;
- 1 menu: `spell_holder`;
- 1 Binder caster data component;
- 2 entity types: `trail`, `missile`;
- 3 MobEffects: `grow`, `shrink`, `stuffed`;
- 2 C2S payloads;
- particle/timeline registrations and turret behaviors for provider cast methods.
