# Elastic Tether

- ID: `ironsable:elastic_tether` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School: **NÃO VERIFICADO**.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast sequence: provider describes a three-cast setup; exact recast implementation/timing **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Range / tether force / duration / caps: **NÃO VERIFICADO**.

## Contract

Official behavior is an arcane tether established through three casts: mark one point, mark another, then the two anchors are hauled together until they touch. Terrain is immovable, so tethering a ship to terrain can lock it in place. Casting again snaps/breaks the tether.

The provider description makes anchor type matter: terrain is an immovable authority, not another movable physics body.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; every level in IronSable creative tab. Exact values: **NÃO VERIFICADO**.

## Dedup / authority

Anchor recording, tether lifecycle, attraction and snap cleanup are IronSable-owned. Do not add a parallel pull constraint.

## Fail-closed

If either anchor cannot be resolved to the provider's exact world/sublevel frame, do not invent a global-coordinate tether.

## Evidence state

Exact release + runtime ID + official semantic contract; school/stats/API/bytecode pending.