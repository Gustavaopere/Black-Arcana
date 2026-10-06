# Charged Ender Pearl Teleport

- Provider: **Bosses of Mass Destruction** (`bosses_of_mass_destruction`)
- Version: `1.3.3`
- Exact physical/publisher SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`
- Owner item: **Charged Ender Pearl**
- Semantic type: deliberate supernatural projectile teleport action
- State: `CONDITIONAL`

## Identity and trigger

Deliberate use of Charged Ender Pearl launches the provider's Charged Ender Pearl entity. The semantic root is the player-invoked teleport action; projectile flight and impact handling are its settlement path.

## Exact impact settlement

On collision, exact-artifact inspection closes provider behavior that:

- teleports the owner to the impact point;
- resets fall distance;
- applies Resistance;
- applies Slow Falling;
- applies nearby knockback;
- synchronizes impact effects;
- discards the projectile.

Those effects remain one causal action identity.

## Exact recipe

The exact shapeless recipe requires:

- Void Thorn;
- vanilla Ender Pearl;
- Ancient Anima.

Exact provider data supplies Ancient Anima through Night Lich entity loot.

## Reachability gate

Normal Ancient Anima acquisition depends on the Night Lich path. That path's normal Soul Star production is gated by deployed `lichConfig.summonMechanic.isEnabled`, whose effective value is not captured.

Therefore the Charged Ender Pearl action inherits that unresolved normal-acquisition gate.

## Disposition

- exact action identity: closed;
- exact impact settlement: closed;
- exact recipe: closed;
- current normal reachability: conditional through the Lich/Ancient Anima chain;
- strict state: `CONDITIONAL`.

## Evidence boundary

No additional root is created by Resistance, Slow Falling, knockback, impact VFX or projectile lifecycle.

Source: `../EXACT-1.3.3-ARTIFACT-AUDIT.md`.
